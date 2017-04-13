from nxt import locator
from nxt.sensor.common import PORT_2, PORT_3
from nxt.motor import PORT_A, PORT_B, PORT_C
from .helpers import Robot, SERVO_NICE, ON, OFF
from .helpers import normalize


def main():
    brick = locator.find_one_brick()  # USB connection
    robot = Robot(brick)

    # Sensors
    light = robot.init_light_sensor(PORT_2)
    touch = robot.init_touch_sensor(PORT_3)

    # Motors
    robot.init_servo(PORT_B)
    robot.init_synchronized_motors(PORT_A, PORT_C)

    # Initial setup
    robot.set_servo(SERVO_NICE)  # It's called nice because the servo movement looks freaking awesome
    robot.turn_light_sensor(ON)

    # Light sensor calibration
    black, white = robot.calibrate_light()

    # Thresholds
    lower = 4 * (10 ** -1)
    upper = 9 * (10 ** -1)

    def until(light_sensor, touch_sensor, **kwargs):
        return normalize(light_sensor.get_lightness(), black, white) < upper or touch_sensor.is_pressed()

    robot.move_forward(until=until, until_args=(light, touch))
    while robot.running:
        light_level = normalize(light.get_lightness(), black, white)
        if light_level > lower:
            robot.debug('Current light level: ', light_level)
            robot.turn_right(8, 15)  # Turn right 15° to see if we correct the course
            light_level_tmp = normalize(light.get_lightness(), black, white)
            if light_level_tmp > light_level:
                robot.debug('Right turn didn\'t improve course. Turning left...')
                robot.turn_left(8, 30)

        robot.move_forward(until=until, until_args=(light, touch))

    # WARNING: From here, the code is even more experimental.
    # I encourage you to consider this some sort of fancy pseudo-code.
    if touch.is_pressed():
        robot.debug('Found an obstacle.')
        robot.turn_right(50, 45)
        robot.move_forward(dist=10, power=100)  # Dist is given in cm

    robot.turn_light_sensor(OFF)


if __name__ == '__main__':
    main()
