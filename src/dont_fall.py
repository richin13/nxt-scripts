# Warning: Experimental code.
from nxt import locator
from nxt.sensor.common import PORT_2, PORT_4
from nxt.motor import PORT_A, PORT_B, PORT_C

from scripts.helpers import Robot, SERVO_DOWN, ON, OFF
from scripts.helpers import normalize

from time import sleep


def main():
    brick = locator.find_one_brick(debug=True)
    robot = Robot(brick, debug=True, verbose=True, power=80)  # Excessive output

    # Motors
    robot.init_synchronized_motors(PORT_A, PORT_C)
    robot.init_servo(PORT_B)
    light = robot.init_light_sensor(PORT_2)
    robot.turn_light_sensor(ON)

    robot.set_servo(SERVO_DOWN)

    table_value = normalize(light.get_sample(), 0, 1023)
    print(table_value)

    def until():
        print(normalize(light.get_sample(), 0, 1023))
        return normalize(light.get_sample(), 0, 1023) < 0.3

    robot.move_forward(until=until, until_args=(), until_kwargs={}, wait=True)
    robot.turn_light_sensor(OFF)

if __name__ == '__main__':
    main()
