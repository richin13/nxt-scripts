from nxt.sensor import *
from nxt.motor import *
from scripts.helpers.robot import *
from time import sleep

import unittest


class TestRobot(unittest.TestCase):
    def setUp(self):
        if self.robot is not None:
            print('Robot was other than None', type(self.robot))
        self.robot = Robot(debug=True, verbose=True)
        super().setUp()

    def test_init_light_sensor(self):
        light = self.robot.init_light_sensor(PORT_2)
        self.assertIsNotNone(light)
        self.assertEqual(type(light), Light)

    def test_init_touch_sensor(self):
        touch = self.robot.init_touch_sensor(PORT_3)
        self.assertIsNotNone(touch)
        self.assertEqual(type(touch), Touch)

    def test_init_ultrasonic_sensor(self):
        ultrasonic = self.robot.init_ultrasonic_sensor(PORT_1)
        self.assertIsNotNone(ultrasonic)
        self.assertEqual(type(ultrasonic), Ultrasonic)

    def test_init_sound_sensor(self):
        sound = self.robot.init_sound_sensor(PORT_4)
        self.assertIsNotNone(sound)
        self.assertEqual(type(sound), Sound)

    def test_init_servo(self):
        servo = self.robot.init_servo(PORT_B)
        self.assertIsNotNone(servo)
        self.assertEqual(type(servo), Motor)

    def test_init_sync_motors(self):
        sm = self.robot.init_synchronized_motors(PORT_A, PORT_C)
        self.assertIsNotNone(sm)
        self.assertIsNotNone(self.robot.move)
        self.assertEqual(type(sm), SynchronizedMotors)

    def test_move_without_motors(self):
        self.assertRaises(RobotError, self.robot.move_forward)
        self.assertRaises(RobotError, self.robot.move_backwards)

    def test_move_with_motors_forever(self):
        self.robot.init_synchronized_motors(PORT_A, PORT_C)
        self.assertFalse(self.robot.running)
        self.robot.move_forward()
        self.assertTrue(self.robot.running)
        sleep(2)
        self.robot.stop()
        self.assertFalse(self.robot.running)

    def test_spin_without_motors(self):
        self.assertRaises(RobotError, self.robot.spin, 360)

    def test_spin_with_motors(self):
        self.robot.init_synchronized_motors(PORT_A, PORT_C)
        self.robot.spin(360)
