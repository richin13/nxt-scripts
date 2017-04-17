from nxt.motor import PORT_A, PORT_B, PORT_C
from .helpers.robot import Robot, SERVO_NICE


def main():
    robot = Robot(debug=True, verbose=True)

    # Motors
    robot.init_synchronized_motors(PORT_A, PORT_C)
    robot.init_servo(PORT_B)

    robot.set_servo(SERVO_NICE)
    sides = 4  # Spoiler alert! It's a square.
    side_length = 10  # In centimeters
    angle = 90

    for _ in range(sides):
        robot.move_forward(dist=side_length)
        robot.spin(degrees=(180 - angle), power=50)

    print('[DONE] Won\'t do anything else.')


if __name__ == '__main__':
    main()
