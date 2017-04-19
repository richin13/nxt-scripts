from nxt import *
from scripts.helpers import *

# Constants
MOTOR_PWR = 80

STEP = 5
AVOIDANCE_STEP = 10
STEP_AFTER_OBSTACLE = 10

# Record movements for going back to start point
movements = []

def main():
    brick = locator.find_one_brick()  # USB connection
    robot = Robot(brick, verbose=True, debug=True)

    # Sensors
    touch = robot.init_touch_sensor(PORT_3)
    sound = robot.init_sound_sensor(PORT_4)

    # Motors
    robot.init_servo(PORT_B)
    robot.init_synchronized_motors(PORT_A, PORT_C)

    # TODO
    # Calibrate sound sensor and wait for loud sound to start
    #robot.calibrate_sound(interactive=True)


    # Move every 5 cm and check for obstacle
    start_moving_until_obstacle(robot)

    # Try to go around obstacle, loop until obstacle 
    # is cleared
    while True:
        robot.debug("Trying to go around obstacle...")
        attemp_detour(robot)

        if not touch.pressed():
            robot.debug("Obstacle cleared!!")
            break
        else
            robot.debug("Trying again...")
    

    # Obstacle cleared, move 10 cm
    move_fw_and_save(dist=STEP_AFTER_OBSTACLE, robot)

    # Go back to start
    undo_all_movements(robot)


def start_moving_until_obstacle(robot):
    while not touch.pressed():
        move_fw_and_save(dist=STEP, robot)


def attemp_detour(robot):
    robot.move_backwards(dist=4)
    turn_right_and_save(degrees=90, robot)

    move_fw_and_save(dist=AVOIDANCE_STEP, robot)
    
    turn_left_and_save(degrees=90, robot)
    robot.move_forward(dist=4)


def undo_all_movements(robot):
    for move in reversed(movements):
        amount = move[0]
        move_type = move[1]

        if move_type == 'step':
            robot.move_backwards(dist=amount)
        elif move_type == 'right-t':
            robot.turn_left(MOTOR_PWR, amount)
        elif move_type == 'left-t':
            robot.turn_right(MOTOR_PWR, amount)

        movements.pop()


def move_fw_and_save(dist=STEP, robot):
    robot.move_forward(dist=dist)
    movements.append((distance, 'step'))


def turn_right_and_save(degrees=None, robot):
    robot.turn_right(MOTOR_PWR, degrees)
    movements.append((degrees, 'right-t'))


def turn_left_and_save(degrees=None, robot):
    robot.turn_left(MOTOR_PWR, degrees)
    movements.append((degrees, 'left-t'))


if __name__ == '__main__':
    main()