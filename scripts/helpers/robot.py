from __future__ import print_function
from __future__ import division

from nxt.sensor import *
from nxt.motor import *

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
        self.brick = brick
        self.debug = print if debug else lambda *x, **y: None
        self.verbose = print if verbose else lambda *x, **y: None
        self.lock = threading.Lock()
        self._running = False

        # Check if any sensor was given as kwarg
        if 'ligth' in kwargs:
            self.light = kwargs['light']

        if 'sound' in kwargs:
            self.sound = kwargs['sound']

        if 'touch' in kwargs:
            self.touch = kwargs['touch']

        if 'ultrasound' in kwargs:
            self.ultrasound = kwargs['ultrasound']

        # Now check if a global power was given
        if 'power' in kwargs:
            self.power = kwargs['power']
        else:
            self.power = 50

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
        if 'servo' in kwargs:
            self.servo = kwargs['servo']
        else:
            self.servo = None

    def _init_sensor(self, port, sensor):
        self.debug('Initializing sensor %s at port %s' % (sensor.__name__, str(port)))
        return sensor(self.brick, port)

    def init_synchronized_motors(self, port_left_motor, port_right_motor):
        self.left_motor = Motor(self.brick, port_left_motor)
        self.right_motor = Motor(self.brick, port_right_motor)
        self.movement_motor = SynchronizedMotors(self.left_motor, self.right_motor, True)
        return self.move

    def init_servo(self, port):
        self.servo = Motor(self.brick, port)
        return self.servo

    # utils functions
    def _move(self, *args, dist=None, until=None, power=None, seconds=None, **kwargs):
        if not self.move:
            raise RobotError(
                'Cannot move without a synchronized motor bound to self.move. Invoke "init_synchronized_motors"')
        
        self.running = True

        if power is None:
            power = self.power  # Fallback

        thread = None

        if dist is not None:
            degrees = (dist / DISTANCE_PER_ROTATION) * 360
            self.move.turn(power, degrees)
            self.running = False
        elif until is not None:
            if not callable(until):
                raise RobotError('Parameter "until" must be a callable and must return boolean')
            else:
                thread = threading.Thread(target=self._move_until, args=(until, power) + args, kwargs=kwargs)
                thread.start()
        elif seconds is not None:
            thread = threading.Thread(target=self._move_until, args=(countdown, power, time.time(), seconds), kwargs=kwargs)
            thread.start()
        else:
            self.verbose('Moving forever with power=%s' % str(power))
            self.move.run(power)
            # When this part of the code is reached we face a little problem
            # self.running is set to True and is up to the developer to reset it
            if 'wait' in kwargs:
                raise RobotError('The robot will run forever')

        while 'wait' in kwargs and self.running:
            self.verbose('Waiting for the robot to stop running...')
            thread.join()

    def move_forward(self, *args, dist=None, until=None, seconds=None, **kwargs):
        try:
            self._move(*args, dist, until, self.power, seconds, **kwargs)
        except Exception as e:
            self.running = False
            raise e

    def move_backwards(self, *args, dist=None, until=None, seconds=None, **kwargs):
        try:
            self._move(*args, dist, until, self.power * -1, seconds, **kwargs)
        except Exception as e:
            self.running = False
            raise e

    def _move_until(self, until, *args, power=None, brake=False, **kwargs):
        if power is None:
            power = self.power
        self.move.run(power)
        while not until(*args, **kwargs):
            pass
        self.stop(brake)

    def stop(self, brake=False):
        if brake:
            self.move.brake()
        else:
            self.move.idle()

        self.running = False

    def turn_right(self, power=None, degrees=0):
        self.debug('Turning right by %s degrees' % str(degrees))
        if power is None:
            power = self.power
        self.stop()
        self.left_motor.turn(power, degrees)

    def turn_left(self, power=None, degrees=0):
        self.debug('Turning left by %s degrees' % str(degrees))
        if power is None:
            power = self.power
        self.stop()
        self.right_motor.turn(power, degrees)

    def spin(self, degrees, power=None):
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
        if self.sound is None:
            raise RobotError('No sound sensor to calibrate.')

        print("Calibrating sound sensor...")
        sleep(.5)

        print('Please simulate a quiet environment for the next 5 seconds.')
        if interactive:
            input('Press [ENTER] to begin calibration for quiet environment')
        else:
            sleep(1)

        i = time()
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
        
        i = time()
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

    def set_servo(self, position):
        if position == SERVO_UP or position == SERVO_NICE:
            try:
                self.servo.turn(-20, 180)
            except BlockedException:
                pass
        if position == SERVO_DOWN or position == SERVO_NICE:
            try:
                self.servo.turn(10, 90)
            except BlockedException:
                pass

    def turn_light_sensor(self, state):
        states_nice = {True: 'On', False: 'Off'}
        if self.light is None:
            raise RobotError('No light sensor to turn %s' % states_nice[state].lower())

        self.debug('Turning light sensor %s.' % states_nice[state].lower())
        self.light.set_illuminated(state)


class RobotError(Exception):
    pass
