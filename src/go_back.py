from nxt import *
from scripts.helpers import *
from time import sleep

# Constants
MOTOR_PWR = 70
LOUD_THRESHOLD = 0.8

STEP = 2
AVOIDANCE_STEP = 10
STEP_AFTER_OBSTACLE = 14

# Record movements for going back to start point
movements = []


def main():
    brick = locator.find_one_brick()  # USB connection
    robot = Robot(brick, debug=True, power=MOTOR_PWR)

    # Sensors
    touch = robot.init_touch_sensor(PORT_3)
    sound = robot.init_sound_sensor(PORT_4)
    us = robot.init_ultrasonic_sensor(PORT_1)

    # Motors
    robot.init_servo(PORT_B)
    robot.init_synchronized_motors(PORT_A, PORT_C)

    # Calibrate sound sensor and wait for loud sound
    wait_for_loud_sound(robot, sound)

    # Move until bump into obstacle
    robot.move_forward(until=touch.is_pressed, wait=True)
    movements.append((20, 'step'))

    # Gather initial distance to obstacle
    robot.move_backwards(dist=4)
    initial_dist = us.get_distance()
    print(initial_dist, 'initial_dist')

    # Try to go around obstacle, loop until obstacle
    # is cleared
    while True:
        robot.debug("Trying to go around obstacle...")
        distance_to_obstacle = attempt_detour(robot, us)

        if distance_to_obstacle > initial_dist + 80:
            robot.debug("Obstacle cleared!!")
            break
        else:
            robot.debug("Trying again...")

    # Obstacle cleared, move some distance
    move_fw_and_save(robot, dist=STEP_AFTER_OBSTACLE)

    # Go back to start
    undo_all_movements(robot)


def wait_for_loud_sound(rb, sound_sensor):
    quiet, loud = rb.calibrate_sound(interactive=True)
    while True:
        loudness = normalize(sound_sensor.get_sample(), quiet, loud)
        print(loudness)
        if loudness > LOUD_THRESHOLD:
            break
        sleep(1)


def attempt_detour(rb, us):
    sleep(1)
    spin_right_and_save(rb, 250)
    sleep(1)
    move_fw_and_save(rb, 20)
    sleep(1)
    spin_left_and_save(rb, 250)

    distance_to_obstacle = us.get_distance()
    print('dist2box', distance_to_obstacle)

    return distance_to_obstacle


def undo_all_movements(rb):
    rb.debug("Going back to start...")
    for move in reversed(movements):
        amount = move[0]
        move_type = move[1]

        if move_type == 'step':
            rb.move_backwards(dist=amount)
        elif move_type == 'r-spin':
            rb.spin(-amount)
        elif move_type == 'l-spin':
            rb.spin(amount)

        movements.pop()
        sleep(1)
    rb.debug("Done!!!")


def move_fw_and_save(rb, dist=10):
    rb.move_forward(dist=dist)
    movements.append((dist, 'step'))


def spin_right_and_save(rb, degrees=250):
    rb.spin(degrees)
    movements.append((degrees, 'r-spin'))


def spin_left_and_save(rb, degrees=250):
    rb.spin(-degrees)
    movements.append((degrees, 'l-spin'))


if __name__ == '__main__':
    main()