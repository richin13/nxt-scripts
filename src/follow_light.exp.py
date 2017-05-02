# Warning: Experimental code.
from nxt import locator
from nxt.sensor.common import PORT_2, PORT_4
from nxt.motor import PORT_A, PORT_B, PORT_C

from scripts.helpers import Robot, SERVO_UP, ON, OFF
from scripts.helpers import normalize

from time import sleep


def main():
    brick = locator.find_one_brick(debug=True)
    robot = Robot(brick, debug=True, verbose=True, power=80)  # Excessive output

    # Motors
    robot.init_synchronized_motors(PORT_A, PORT_C)
    robot.init_servo(PORT_B)

    # Sensors
    light = robot.init_light_sensor(PORT_2)
    sound = robot.init_sound_sensor(PORT_4)

    # Intial setup
    robot.set_servo(SERVO_UP)
    robot.turn_light_sensor(ON)

    # Calibration (light)
    # light_off, light_on = robot.calibrate_light(interactive=True)  # FIXME: Output says 'Point the sensor to black line'
    light_off, light_on = 229, 900
    # Sound sensor calibration
    quiet, loud = 15, 1024 # robot.calibrate_sound(interactive=True)

    # Thresholds
    lower = 5 * (10 ** -1)
    lower_noise = 1 # 9 * (10 ** -1)
    upper = 5 * (10 ** -1)

    # until = lambda *args, ls=light, **kwargs: normalize(ls.get_lightness(), light_off, light_on) > upper
    print('starting...')
    sleep(3)
    # TODO I should probably lock the access to light sensor.
    def until(light_sensor, **kwargs):  # Must explicitly state **kwargs as his argument.
        return normalize(light_sensor.get_lightness(), light_off, light_on) < lower

    robot.move_forward(until=until, until_args=(light,))
    while robot.running:
        light_level = normalize(light.get_lightness(), light_off, light_on)
        robot.debug('Current light level: ', light_level)
        if light_level < lower:
            robot.turn_right(50, 15)  # Turn right 15° to see if we correct the course
            light_level_tmp = normalize(light.get_lightness(), light_off, light_on)
            robot.debug('temp lecture at right', light_level_tmp)
            if light_level_tmp > light_level:
                robot.debug('Right turn didn\'t improve course. Turning left...')
                robot.turn_left(50, 30)
        sleep(.4)
        s = sound.get_sample()
        loudness = normalize(s, quiet, loud)
        robot.debug('Value of loudness is ', loudness, s)
        if loudness > lower_noise:
            robot.stop()
            robot.morse('SOS')
            robot.move_backwards(seconds=3, wait=True)

        if not until(light):
            robot.move_forward(until=until, until_args=(light,))  # FIXME: Does this cause an infinite loop?

    robot.turn_light_sensor(OFF)
    print('DONE: Won\'t do anything else.')
    exit(0)


if __name__ == '__main__':
    main()
