from nxt.motor import PORT_A, PORT_B, PORT_C
from scripts.helpers.robot import Robot, SERVO_UP
from time import sleep

def main():
    robot = Robot(debug=True, verbose=True)

    # Motors
    robot.init_synchronized_motors(PORT_A, PORT_C)
    # robot.init_servo(PORT_B)

    # robot.set_servo(SERVO_UP)
    sides = 4  # Spoiler alert! It's a square.
    side_length = 10  # In centimeters
    angle = 90

    for _ in range(sides):
        print('Doing the %d side' % _)
        robot.move_forward(dist=side_length, power=75)
        robot.spin(degrees=(360 - angle), power=75)
        sleep(2)

    print('[DONE] Won\'t do anything else.')


if __name__ == '__main__':
    main()
