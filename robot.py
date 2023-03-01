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

    def move_forward_distance(robot, speed, distance):
        robot.move_forward(80)
        time.sleep(0.5)
        robot.stop()

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

    def do_action(self, action, distance=0):
        if action == 'move_forward':
            self.move_forward_distance(80, distance)
        elif action == 'turn_left':
            self.turn_left()
        elif action == 'turn_right':
            self.turn_right()
        elif action == 'reverse':
            self.reverse()

    def do_actions(self, actions):
        for action in actions:
            if action[0] == 'move_forward':
                self.do_action(action[0], action[1])
            else:
                self.do_action(action[0])

    def undo_action(self, action, distance=0):
        if action == 'move_forward':
            self.move_forward_distance(80, distance)
        elif action == 'turn_left':
            self.turn_right()
        elif action == 'turn_right':
            self.turn_left()
        elif action == 'reverse':
            self.reverse()

    def undo_actions(self, actions):
        while actions:
            action = moves.pop()
            if action[0] == 'move_forward':
                self.undo_action(action[0], action[1])
            else:
                self.undo_action(action[0])

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
        self.move_forward_distance(80, 13)

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
        '''
          b _
         a | | c
          e _
         d | | f
          g _
        '''
        NumberPaths = {
            'a': [("turn_right", None), ("move_forward", 70), ("turn_left", None), ("move_forward", 70), ("turn_left", None), ("move_forward", 35)],
            'b': [("turn_right", None), ("move_forward", 35), ("turn_left", None), ("move_forward", 35)],
            'c': [("move_forward", 35), ("turn_right", None)],
            'd': [("turn_right", None), ("move_forward", 70), ("turn_left", None), ("move_forward", 105), ("turn_left", None), ("move_forward", 70), ("turn_left", None), ("move_forward", 35), ("turn_right", None)],
            'e': [("move_forward", 35)],
            'f': [("move_forward", 35), ("turn_left", None)],
            'g': [("turn_left", None), ('move_forward', 35), ("turn_right", None), ("move_forward", 35)]
        }

        actions = []

        def identify_number():
            # Move 35cm forward
            self.move_forward_distance(80, 35)
            actions.append(('move_forward', 35))
            # Check for barrier
            front_dist = robot.front_dist_sensor.get_distance()
            if front_dist < 20:
                # Turn left
                robot.turn_left()
                moves.append(('turn_left', None))
                # Check for barrier
                front_dist = robot.front_dist_sensor.get_distance()
                if front_dist < 20:
                    # Reverse
                    robot.reverse()
                    moves.append(('reverse', None))
                    # Check for barrier
                    front_dist = robot.front_dist_sensor.get_distance()
                    if front_dist < 20:
                        # Turn right
                        robot.turn_right()
                        moves.append(('turn_right', None))
                        # Move 35cm forward
                        self.move_forward_distance(80, 35)
                        actions.append(('move_forward', 35))
                        # Turn left
                        robot.turn_left()
                        actions.append(('turn_left', None))
                        # Move 70cm forward
                        self.move_forward_distance(80, 70)
                        actions.append(('move_forward', 70))
                        # Turn left
                        robot.turn_left()
                        actions.append(('turn_left', None))
                        # Move 70cm forward
                        self.move_forward_distance(80, 70)
                        actions.append(('move_forward', 70))
                        # Turn left
                        robot.turn_left()
                        actions.append(('turn_left', None))
                        # Move 35cm forward
                        self.move_forward_distance(80, 35)
                        actions.append(('move_forward', 35))
                        # Check for barrier
                        front_dist = robot.front_dist_sensor.get_distance()
                        if front_dist < 20:
                            # Turn left
                            robot.turn_left()
                            actions.append(('turn_left', None))
                            # Check for barrier
                            front_dist = robot.front_dist_sensor.get_distance()
                            if front_dist < 20:
                                # Reverse
                                robot.reverse()
                                actions.append(('reverse', None))
                                # Move 35cm forward
                                self.move_forward_distance(80, 35)
                                actions.append(('move_forward', 35))
                                # Turn left
                                robot.turn_left()
                                actions.append(('turn_left', None))
                                # Move 70cm forward
                                self.move_forward_distance(80, 70)
                                actions.append(('move_forward', 70))
                                # Turn left
                                robot.turn_left()
                                actions.append(('turn_left', None))
                                # Move 35cm forward
                                self.move_forward_distance(80, 35)
                                actions.append(('move_forward', 35))
                                # Turn left
                                robot.turn_left()
                                actions.append(('turn_left', None))
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
                        self.move_forward_distance(80, 70)
                        actions.append(('move_forward', 70))
                        # Turn left
                        robot.turn_left()
                        actions.append(('turn_left', None))
                        # Move 70cm forward
                        self.move_forward_distance(80, 70)
                        actions.append(('move_forward', 70))
                        # Turn left
                        robot.turn_left()
                        actions.append(('turn_left', None))
                        # Move 70cm forward
                        self.move_forward_distance(80, 70)
                        actions.append(('move_forward', 70))
                        # Turn left
                        robot.turn_left()
                        actions.append(('turn_left', None))
                        # Move 35cm forward
                        self.move_forward_distance(80, 35)
                        actions.append(('move_forward', 35))
                        # Turn right
                        robot.turn_right()
                        actions.append(('turn_right', None))
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
                self.move_forward_distance(80, 35)
                actions.append(('move_forward', 35))
                # Turn right
                robot.turn_right()
                actions.append(('turn_right', None))
                # Check for barrier
                front_dist = robot.front_dist_sensor.get_distance()
                if front_dist < 20:
                    return 0
                else:
                    # Move 35cm forward
                    self.move_forward_distance(80, 35)
                    actions.append(('move_forward', 35))
                    # Turn right
                    robot.turn_right()
                    actions.append(('turn_right', None))
                    # Check for barrier
                    front_dist = robot.front_dist_sensor.get_distance()
                    if front_dist < 20:
                        return 7
                    else:
                        return 1

    def run_elevated_arena(self):
        line_follow(stop_color='Blue')
