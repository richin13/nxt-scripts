from scripts.helpers.robot import *

def main():
    robot = Robot(debug=True, verbose=True)
    robot.morse('SOS')

if __name__ == '__main__':
    main()