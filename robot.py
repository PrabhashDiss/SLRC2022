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

    def line_follow(self, speed=80, go_color='White', stop_color='Red', reverse_color='Green'):
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
                if color == go_color:
                    self.move_forward(speed)
                elif color == stop_color:
                    self.stop()
                    break
                elif color == reverse_color:
                    self.reverse()

    def run_line_maze_arena(self):
        pass

    def run_cave_arena(self):
        # read sensor values
        color = self.colour_sensor.detects_colour()

        # Move forward 13 cm
        robot.move_forward(80)
        time.sleep(0.5)
        robot.stop()

        # Turn left
        robot.turn_left()

        # Check for barriers
        while True:
            # Move forward
            robot.move_forward(80)

            front_dist = robot.front_dist_sensor.get_distance()
            if front_dist < 15:
                robot.stop()
                # Avoid barrier by turning right
                robot.turn_right()
                robot.move_forward(80)
                time.sleep(0.5)
                robot.turn_left()
                # Check for barriers again
                while True:
                    # Move forward
                    robot.move_forward(80)

                    front_dist = robot.front_dist_sensor.get_distance()
                    if front_dist < 15:
                        robot.stop()
                        # Avoid barrier by turning left
                        robot.turn_left()
                        robot.move_forward(80)
                        time.sleep(0.5)
                        robot.turn_right()

                    # Check for finish line
                    color = robot.colour_sensor.detects_colour()
                    if color == 'White':
                        robot.stop()
                        break

            # Check for finish line
            color = robot.colour_sensor.detects_colour()
            if color == 'White':
                robot.stop()
                break

    def run_7_segment_number_constructing_arena(self):
        def identify_number():
            # Move 35cm forward
            robot.move_forward(80)
            time.sleep(0.5)
            robot.stop()
            # Check for barrier
            front_dist = robot.front_dist_sensor.get_distance()
            if front_dist < 20:
                # Turn left
                robot.turn_left()
                # Check for barrier
                front_dist = robot.front_dist_sensor.get_distance()
                if front_dist < 20:
                    # Reverse
                    robot.reverse()
                    # Check for barrier
                    front_dist = robot.front_dist_sensor.get_distance()
                    if front_dist < 20:
                        # Turn right
                        robot.turn_right()
                        # Move 35cm forward
                        robot.move_forward(80)
                        time.sleep(0.5)
                        robot.stop()
                        # Turn left
                        robot.turn_left()
                        # Move 70cm forward
                        robot.move_forward(80)
                        time.sleep(0.5)
                        robot.stop()
                        # Turn left
                        robot.turn_left()
                        # Move 70cm forward
                        robot.move_forward(80)
                        time.sleep(0.5)
                        robot.stop()
                        # Turn left
                        robot.turn_left()
                        # Move 35cm forward
                        robot.move_forward(80)
                        time.sleep(0.5)
                        robot.stop()
                        # Check for barrier
                        front_dist = robot.front_dist_sensor.get_distance()
                        if front_dist < 20:
                            # Turn left
                            robot.turn_left()
                            # Check for barrier
                            front_dist = robot.front_dist_sensor.get_distance()
                            if front_dist < 20:
                                # Reverse
                                robot.reverse()
                                # Move 35cm forward
                                robot.move_forward(80)
                                time.sleep(0.5)
                                robot.stop()
                                # Turn left
                                robot.turn_left()
                                # Move 70cm forward
                                robot.move_forward(80)
                                time.sleep(0.5)
                                robot.stop()
                                # Turn left
                                robot.turn_left()
                                # Move 35cm forward
                                robot.move_forward(80)
                                time.sleep(0.5)
                                robot.stop()
                                # Turn left
                                robot.turn_left()
                                # Check for barrier
                                front_dist = robot.front_dist_sensor.get_distance()
                                if front_dist < 20:
                                    return 8
                                else:
                                    return 9
                            else:
                                return 4
                        else:
                            return 3
                    else:
                        # Move 70cm forward
                        robot.move_forward(80)
                        time.sleep(0.5)
                        robot.stop()
                        # Turn left
                        robot.turn_left()
                        # Move 70cm forward
                        robot.move_forward(80)
                        time.sleep(0.5)
                        robot.stop()
                        # Turn left
                        robot.turn_left()
                        # Move 70cm forward
                        robot.move_forward(80)
                        time.sleep(0.5)
                        robot.stop()
                        # Turn left
                        robot.turn_left()
                        # Move 35cm forward
                        robot.move_forward(80)
                        time.sleep(0.5)
                        robot.stop()
                        # Turn right
                        robot.turn_right()
                        # Check for barrier
                        front_dist = robot.front_dist_sensor.get_distance()
                        if front_dist < 20:
                            return 6
                        else:
                            return 5
                else:
                    return 2
            else:
                # Move 35cm forward
                robot.move_forward(80)
                time.sleep(0.5)
                robot.stop()
                # Turn right
                robot.turn_right()
                # Check for barrier
                front_dist = robot.front_dist_sensor.get_distance()
                if front_dist < 20:
                    return 0
                else:
                    # Move 35cm forward
                    robot.move_forward(80)
                    time.sleep(0.5)
                    robot.stop()
                    # Turn right
                    robot.turn_right()
                    # Check for barrier
                    front_dist = robot.front_dist_sensor.get_distance()
                    if front_dist < 20:
                        return 7
                    else:
                        return 1

    def run_elevated_arena(self):
        line_follow(stop_color='Blue')
