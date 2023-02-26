from components import *

class Robot:
    def __init__(self):
        left_motor = Motor(1,1,1)
        right_motor = Motor(1,1,1)

        compass = Compass()
        encoder = Encoder()
        colour_sensor = ColourSensor()

        front_dist_sensor = DistanceSensor()
        left_dist_sensor = DistanceSensor()
        right_dist_sensor = DistanceSensor()

        left_IR1 = IRSensor(1)
        left_IR2 = IRSensor(1)
        left_IR3 = IRSensor(1)
        left_IR4 = IRSensor(1)
        right_IR1 = IRSensor(1)
        right_IR2 = IRSensor(1)
        right_IR3 = IRSensor(1)
        right_IR4 = IRSensor(1)

    def move_forward(self, speed):
        self.left_motor.move_forward(speed)
        self.right_motor.move_forward(speed)

    def move_backward(self, speed):
        self.left_motor.move_backward(speed)
        self.right_motor.move_backward(speed)

    def turn_left(self):
        self.left_motor.move_backward(70)
        self.right_motor.move_forward(70)
        time.sleep(1.5)
        self.left_motor.stop()
        self.right_motor.stop()

    def turn_right(self):
        self.left_motor.move_forward(70)
        self.right_motor.move_backward(70)
        time.sleep(1.5)
        self.left_motor.stop()
        self.right_motor.stop()

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def reverse(self):
        self.left_motor.move_backward(70)
        self.right_motor.move_backward(70)
        time.sleep(1.5)
        self.left_motor.stop()
        self.right_motor.stop()

    def line_follow(self, speed=80, go_color='White', stop_color='Red', optional_stop_color='Green'):
        while True:
            # read sensor values
            left_value = self.left_IR3.detects_black()
            right_value = self.right_IR3.detects_black()
            color = self.colour_sensor.detects_colour()

            # adjust motors based on sensor values
            elif not left_value and right_value:
                self.left_motor.move_backward(speed)
                self.right_motor.move_forward(speed)
            if left_value and not right_value:
                self.left_motor.move_forward(speed)
                self.right_motor.move_backward(speed)
            else:
                self.left_motor.move_forward(speed)
                self.right_motor.move_forward(speed)
                if color == go_color:
                    self.left_motor.move_forward(speed)
                    self.right_motor.move_forward(speed)
                elif color == stop_color:
                    self.left_motor.stop()
                    self.right_motor.stop()
                    break
                elif color == reverse_color:
                    self.reverse()
