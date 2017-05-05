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
    robot.move_forward(seconds=3, wait=True)
    robot.move_backwards(seconds=3, wait=True)

if __name__ == '__main__':
    main()
