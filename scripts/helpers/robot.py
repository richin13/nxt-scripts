from __future__ import print_function
from __future__ import division

from nxt.sensor import *
from nxt.motor import *

import time
from math import pi
from time import sleep
from morse import string_to_morse

from .utils import countdown

try:
    import threading
except ImportError:
    import dummy_threading as threading

# GLOBALS
AVAILABLE_SENSORS = [Light, Sound, Touch, Ultrasonic]
WHEEL_DIAMETER = 15
WHEEL_WIDTH = 7
WHEELS_DISTANCE = 45
DISTANCE_PER_ROTATION = pi * WHEEL_DIAMETER
SERVO_UP = 0x0F
SERVO_DOWN = 0xF0
SERVO_NICE = 0xFF
ON = True
OFF = False


class _Meta(type):
    def __new__(mcs, name, bases, namespace):
        for sensor in AVAILABLE_SENSORS:
            namespace[sensor.__name__.lower()] = None
        return type.__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        super(_Meta, cls).__init__(name, bases, namespace)

        for _sensor in AVAILABLE_SENSORS:
            def func(self, port, sensor=_sensor):
                setattr(self, sensor.__name__.lower(), namespace['_init_sensor'](port, sensor))
                return getattr(self, sensor.__name__.lower())

            setattr(cls, 'init_%s_sensor' % _sensor.__name__.lower(), func)


class Robot(object, metaclass=_Meta):
    def __init__(self, brick, debug=True, verbose=False, **kwargs):
        """
        Initialize a new Robot object.
        :param brick: The brick. Use nxt.locator.find_one_brick
        :param debug: Whether print debug messages or not.
        :param verbose: Whether print high verbosity messages or not
        :param kwargs:
        """
        self.brick = brick
        self.debug = print if debug else lambda *x, **y: None
        self.verbose = print if verbose else lambda *x, **y: None
        self.lock = threading.Lock()
        self._running = False

        # Check if any sensor was given as kwarg
        if 'light' in kwargs:
            self.light = kwargs['light']

        if 'sound' in kwargs:
            self.sound = kwargs['sound']

        if 'touch' in kwargs:
            self.touch = kwargs['touch']

        if 'ultrasound' in kwargs:
            self.ultrasonic = kwargs['ultrasound']

        # Now check if a global power was given
        self.power = kwargs.get('power', 50)

        # Is there a SynchronizedMotors?
        if 'synchronized' in kwargs:
            self.movement_motor = kwargs['synchronized']
            self.left_motor = self.movement_motor.leader
            self.right_motor = self.movement_motor.follower
        else:
            self.movement_motor = None

            if 'right_motor' in kwargs:
                self.right_motor = kwargs['right_motor']
            else:
                self.right_motor = None

            if 'left_motor' in kwargs:
                self.left_motor = kwargs['left_motor']
            else:
                self.left_motor = None

        # Is there a Servo?
        self.servo = kwargs.get('servo', None)

    def _init_sensor(self, port, sensor):
        self.debug('Initializing sensor %s at port %s' % (sensor.__name__, str(port)))
        return sensor(self.brick, port)

    def init_synchronized_motors(self, port_left_motor, port_right_motor):
        """
        Creates a new SynchronizedMotors and binds it to self.move.
        :param port_left_motor: The port of the left motor.
        :param port_right_motor:  The port of the right motor.
        :return: The newly created SynchronizedMotors object.
        """
        self.left_motor = Motor(self.brick, port_left_motor)
        self.right_motor = Motor(self.brick, port_right_motor)
        self.movement_motor = SynchronizedMotors(self.left_motor, self.right_motor, True)
        return self.move

    def init_servo(self, port):
        """
        Initializes a servo motor. It does not change its initial position, though.
        :param port: The port where the servo motor is connected to.
        :return: The newly created Motor object
        """
        self.servo = Motor(self.brick, port)
        return self.servo

    # utils functions
    def _move(self, dist=None, until=None, seconds=None, until_args=(), until_kwargs=None, **kwargs):
        if not self.move:
            raise RobotError(
                'Cannot move without a synchronized motor bound to self.move. '
                'Invoke "init_synchronized_motors"'
            )
        if until_kwargs is None:
            until_kwargs = {}

        wait = kwargs.get('wait', False)
        power = kwargs.get('power', self.power)

        self.running = True

        self.verbose('Power is:', power)

        if dist is not None:
            degrees = (dist / DISTANCE_PER_ROTATION) * 360
            self.move.turn(power, degrees)
            self.running = False
        elif until is not None or seconds is not None:
            thread_kwargs = {
                'power': power,
                'brake': kwargs.get('brake', False),

            }
            if until is not None:
                if not callable(until):
                    raise RobotError('Parameter "until" must be a callable and must return boolean')
                else:
                    thread_kwargs['args'] = until_args
                    thread_kwargs['kwargs'] = until_kwargs
                    thread = threading.Thread(target=self._move_until, args=(until,), kwargs=thread_kwargs)
            else:
                thread_kwargs['args'] = (time.time(), seconds)
                thread_kwargs['kwargs'] = {}
                thread = threading.Thread(target=self._move_until, args=(countdown,), kwargs=thread_kwargs)

            thread.start()
            if wait and self.running:
                self.verbose('Waiting for the robot to stop running...')
                thread.join()

        else:
            self.verbose('Moving forever with power=%s' % str(power))
            self.move.run(power)
            # When this part of the code is reached we face a little problem
            # self.running is set to True and is up to the developer to reset it
            if wait:
                raise RobotError('The robot will run forever')

    def move_forward(self, dist=None, until=None, seconds=None, until_args=(), until_kwargs=None, **kwargs):
        """
        Moves the Robot forward until one condition is met. Conditions are:
         - A given distance is traveled
         - A given function returns True
         - A given amount of seconds has elapsed.
        If none of the above conditions is provided, then the robot will run until the
        method self.stop is invoked manually by the developer.
        Additionally, a wait flag can be set in the kwargs. If this flag is set
        the Thread execution will be stopped until the robot stops running.
        :param dist: The distance condition.
        :param until: The until condition. Must be a callable and must explicitly state that it
        receives *args and **kwargs as its arguments.
        :param seconds: The seconds condition.
        :param until_args: The list of arguments that will receive the until callable, if any given.
        :param until_kwargs:
        :param kwargs: The dict of keyword arguments that will be passed to the until callable.
        """
        if until_kwargs is None:
            until_kwargs = {}

        try:
            self._move(dist=dist, until=until, seconds=seconds, until_args=until_args, until_kwargs=until_kwargs,
                       **kwargs)
        except Exception as e:
            self.running = False
            raise e

    def move_backwards(self, dist=None, until=None, seconds=None, until_args=(), until_kwargs=None, **kwargs):
        """
        Moves the Robot backwards until one condition is met. Conditions are:
         - A given distance is traveled
         - A given function returns True
         - A given amount of seconds has elapsed.
        If none of the above conditions is provided, then the robot will run until the
        method self.stop is invoked manually by the developer.
        It is not necessary to pass a negative value for power.
        Additionally, a wait flag can be set in the kwargs. If this flag is set
        the Thread execution will be stopped until the robot stops running.
        :param dist: The distance condition.
        :param until: The until condition. Must be a callable and must explicitly state that it
        receives *args and **kwargs as its arguments.
        :param seconds: The seconds condition.
        :param until_args: The list of arguments that will receive the until callable, if any given.
        :param until_kwargs: The dict of keyword arguments that will be passed to the until callable.
        :param kwargs: The dict of keyword arguments that will be passed to the until callable.
        """
        if until_kwargs is None:
            until_kwargs = {}

        power = kwargs.get('power', self.power)
        assert power > 0

        try:
            self._move(dist=dist, until=until, power=power * -1, seconds=seconds, until_args=until_args,
                       until_kwargs=until_kwargs, **kwargs)
        except Exception as e:
            self.running = False
            raise e

    def _move_until(self, until, power=None, brake=False, args=(), kwargs=None):
        """
        Warning: This function is intended to be invoked by a new thread.

        :param until: Callable that will define when the robot stops. It must return a boolean.
        :param args: The until callable arguments.
        :param power: The power that will be used to move the motors.
        :param brake: Whether the motors should be braked at the end of the execution.
        :param kwargs: The until callable kwargs
        """
        if kwargs is None:
            kwargs = {}
        if power is None:
            power = self.power
        self.move.run(power)
        while not until(*args, **kwargs):
            pass
        self.stop(brake)

    def stop(self, brake=False):
        """
        If the robot is running, this method will stop it immediately.
        Otherwise, it will have no effect on the robot.
        :param brake: Whether the motors should be braked after stop them.
        """
        self.move.idle()
        if brake:
            self.move.brake()

        self.running = False

    def turn_right(self, power=None, degrees=0):
        """
        Rotates the robot a given amount of degrees to the right.
        :param power: The power to use.
        :param degrees: The amount of degrees to rotate.
        """
        self.debug('Turning right by %s degrees' % str(degrees))
        if power is None:
            power = self.power
        self.stop()
        self.left_motor.turn(power, degrees)

    def turn_left(self, power=None, degrees=0):
        """
        Rotates the robot a given amount of degrees to the left.
        :param power: The power to use.
        :param degrees: The amount of degrees to rotate.
        """
        self.debug('Turning left by %s degrees' % str(degrees))
        if power is None:
            power = self.power
        self.stop()
        self.right_motor.turn(power, degrees)

    def spin(self, degrees, power=None):
        """
        Causes the robot to rotate on its axis by turning each wheel in
        equals but opposite directions.
        :param degrees: The amount of degrees to rotate. Can be negative.
        :param power: The power to use
        """
        # TODO: check if this thing works
        self.debug('Turning robot by %s degrees' % str(degrees))
        if power is None:
            power = self.power

        left_power = power if degrees > 0 else power * -1
        right_power = left_power * -1
        degrees = abs(degrees)
        self.verbose('Left power', left_power)
        self.verbose('Right power', right_power)
        left_turn = threading.Thread(target=self.left_motor.turn, args=(left_power, degrees))
        right_turn = threading.Thread(target=self.right_motor.turn, args=(right_power, degrees))

        left_turn.start()
        right_turn.start()

        left_turn.join()
        right_turn.join()

    def morse(self, message):
        """
        Causes the brick to play a sequence of tones representing morse code.
        :param message: The message to encode as morse code.
        """
        # TODO: Adjust the wait and sleep values
        self.debug('Playing message: %s' % message)
        as_morse = string_to_morse(message)
        self.verbose('Morse repr: %s' % str(as_morse))

        for letter in as_morse:
            for m in letter:
                if m == '-':
                    self.brick.play_tone_and_wait(1200, .5)
                else:
                    sleep(.5)
            sleep(.7)

    # Props
    @property
    def move(self):
        return self.movement_motor

    @property
    def running(self):
        try:
            self.lock.acquire()
            self.verbose('Acquired lock in Robot.running')
            return self._running
        finally:
            self.lock.release()
            self.verbose('Released lock in Robot.running')

    @running.setter
    def running(self, val):
        self.lock.acquire()
        self.running = val
        self.lock.release()

    # Calibration stuff
    def calibrate_light(self, interactive=False):
        """
        Calibrates the light sensor. The first return number represents the lowest value read.
        The second one is the highest value read.
        :param interactive: Whether it should wait until the user press the enter key to continue.
        :return: A tuple with the minimum value read and the maximum value read.
        """
        if self.light is None:
            raise RobotError('No light sensor to calibrate.')

        self.debug('Calibrating light sensor...')

        end = ' ' if interactive else '\n'

        sleep(.5)
        print('Please point the sensor to the white surface', end=end)
        if interactive:
            input('and press [ENTER] to read the value')
        else:
            sleep(4)
        print('Reading white value...')
        white = self.light.get_lightness()

        sleep(.5)
        print('Please point the sensor to the black line', end=end)
        if interactive:
            input('and press [ENTER] to read the value')
        else:
            sleep(4)
        print('Reading black value...')
        black = self.light.get_lightness()

        self.debug('Calibration values: white=%d, black=%d' % (white, black))
        return black, white

    def calibrate_ultrasonic(self):
        if self.ultrasonic is None:
            raise RobotError('No ultrasound sensor to calibrate.')

    def calibrate_sound(self, interactive=False):
        """
        Calibrates the sound sensor.
        :param interactive: Whether the process should be interactive with the user or not.
        """
        if self.sound is None:
            raise RobotError('No sound sensor to calibrate.')

        print("Calibrating sound sensor...")
        sleep(.5)

        print('Please simulate a quiet environment for the next 5 seconds.')
        if interactive:
            input('Press [ENTER] to begin calibration for quiet environment')
        else:
            sleep(1)

        i = time.time()
        s = 5
        quiet_values = []
        while countdown(i, s):
            reading = self.sound.get_sample()
            self.verbose('[QUIET] Sound sample reading:', reading)
            quiet_values.append(reading)

        quiet = sum(quiet_values) / len(quiet_values)
        max_quiet = max(quiet_values)

        print('Quiet environment calibrated')
        sleep(.5)

        print('Please simulate a loud environment for the next 5 seconds')
        if interactive:
            input('Press [ENTER] to begin calibration for loud environment')
        else:
            sleep(1)

        i = time.time()
        s = 5
        loud_values = []
        while countdown(i, s):
            reading = self.sound.get_sample()
            self.verbose('[LOUD] Sound sample reading:', reading)
            if reading > max_quiet:
                loud_values.append(reading)

        loud = sum(loud_values) / len(loud_values)

        print('Loud environment calibrated')
        self.debug('Calibration values: quiet=%f, loud=%f' % (quiet, loud))

        return quiet, loud

    def set_servo(self, position, power=None, degrees=None):
        """
        Sets the servo to a given position. Use constants SERVO_DOWN, SERVO_UP and SERVO_NICE
        The power must be a positive integer and the direction of the servo's move will be
        set by the position argument (SERVO_DOWN or SERVO_UP)

        Positions are:
         - SERVO_DOWN: Sets the servo pointing towards the ground.
         - SERVO_UP: Sets the servo pointing forward.
         - SERVO_NICE: It produces an awesome movement of the servo by combining the above positions.
           First moves the servo up and then down
        :param position: Constant SERVO_DOWN, SERVO_UP or SERVO_NICE
        :param power: The power to use
        :param degrees: The degrees.
        """
        if power is None:
            power = 10
        if degrees is None:
            degrees = 90

        if position == SERVO_UP or position == SERVO_NICE:
            try:
                self.servo.turn(-2 * power, 2 * degrees)
            except BlockedException:
                pass
        if position == SERVO_DOWN or position == SERVO_NICE:
            try:
                self.servo.turn(power, degrees)
            except BlockedException:
                pass

    def turn_light_sensor(self, state):
        """
        Sets the light sensor illuminated according to the given state.
        Use constant ON and OFF
        :param state: Boolean state.
        """
        states_nice = {True: 'On', False: 'Off'}
        if self.light is None:
            raise RobotError('No light sensor to turn %s' % states_nice[state].lower())

        self.debug('Turning light sensor %s.' % states_nice[state].lower())
        self.light.set_illuminated(state)


class RobotError(Exception):
    pass
