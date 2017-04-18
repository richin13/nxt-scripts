from time import sleep
from nxt.sensor import *
from nxt.motor import *
from nxt import locator
import _thread

RIGHT = 1
LEFT = -1
DEFAULT_POWER = 10

def set_servo_position(servo):
	try:
		servo.turn(-20, 180)
	except Exception:
		pass
	
	try:
		servo.turn(10, 90)
	except Exception:
		pass

def set_light_sensor(light, state):
	light.set_illuminated(state)

def get_sync_motor(brick):
	m1 = Motor(brick, PORT_A)
	m2 = Motor(brick, PORT_C)

	return SynchronizedMotors(m1, m2, 0)

def walk(s):
	s.run(10)

def turn(s, power, tacho, direction):
	#print('Turning...', direction)
	power *= direction
	s.idle()
	s.turn(power, tacho)


def calibrate(light):
	print('Calibrating light sensor...')
	
	sleep(.5)
	print('Please point the sensor to the white surface')
	sleep(4)
	print('Reading white value...')
	white = light.get_lightness()
	
	sleep(.5)
	print('Please point the sensor to the black line')
	sleep(4)
	print('Reading black value...')
	black = light.get_lightness()


	print('Calibration finished: white=%d, black=%d' % (white, black))
	sleep(1)
	return black, white

def _map(n, start1, stop1, start2, stop2):
	# See https://github.com/processing/p5.js
 	return ((n-start1)/(stop1-start1))*(stop2-start2)+start2

def _get_light(l, b, w):
	return _map(l.get_lightness(), b, w, 0, 1)

def main():
	b = locator.find_one_brick()
	luz = Light(b, PORT_2)
	servo = Motor(b, PORT_B)
	s = get_sync_motor(b)

	set_servo_position(servo)
	set_light_sensor(luz, True)

	black, white = calibrate(luz)
	print('Set the robot in starting position')
	sleep(5)
	print('Starting...')

	s.run(DEFAULT_POWER)
	lower_threshold = 4 * (10**-1)
	upper_threshold = 9 * (10**-1)
	l = 0.0

	while l < upper_threshold:
		l = _get_light(luz, black, white)
		if l > lower_threshold:
			print('Current light level: ', l)
			turn(s, 8, 15, RIGHT)
			lright = _get_light(luz, black, white)
			if lright > l:
				print('Right turn gave not positive outcome')
				turn(s, 8, 30, LEFT)
			s.run(DEFAULT_POWER)
	
	print('Finished because light level was:', _get_light(luz, black, white))
	s.idle()
	s.brake()
	set_light_sensor(luz, False)


if __name__ == '__main__':
	main()