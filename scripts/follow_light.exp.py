# Warning: Experimental code.
from nxt import locator
from nxt.sensor.common import PORT_2, PORT_4
from nxt.motor import PORT_A, PORT_B, PORT_C

from .helpers import Robot, SERVO_UP, ON, OFF
from .helpers import normalize


def main():
    brick = locator.find_one_brick(debug=True)
    robot = Robot(brick, verbose=True)  # Excessive output

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
    light_off, light_on = robot.calibrate_light()  # FIXME: Output says 'Point the sensor to black line'

    # Sound sensor calibration
    quiet, loud = robot.calibrate_sound(interactive=True)

    # Thresholds
    lower = 4 * (10 ** -1)
    upper = 9 * (10 ** -1)

    # until = lambda *args, ls=light, **kwargs: normalize(ls.get_lightness(), light_off, light_on) > upper

    # TODO I should probably lock the access to light sensor.
    def until(light_sensor):
        return normalize(light_sensor.get_lightness(), light_off, light_on) > upper

    robot.move_forward(until=until, until_args=(light,))
    while robot.running:
        light_level = normalize(light.get_lightness(), light_off, light_on)
        if light_level < upper:
            robot.debug('Current light level: ', light_level)
            robot.turn_right(8, 15)  # Turn right 15° to see if we correct the course
            light_level_tmp = normalize(light.get_lightness(), light_off, light_on)
            if light_level_tmp > light_level:
                robot.debug('Right turn didn\'t improve course. Turning left...')
                robot.turn_left(8, 30)

        loudness = normalize(sound.get_sample(), quiet, loud)
        if loudness > lower:
            robot.stop()
            robot.morse('You are too loud!')
            robot.move_backwards(seconds=3, power=25, wait=True)
        robot.move_forward(until=until, until_args=(light,))

    robot.turn_light_sensor(OFF)
    print('DONE: Won\'t do anything else.')
    exit(0)


if __name__ == '__main__':
    main()
