from components import *
import time

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

    def move_forward_distance(self, speed, distance):
        self.move_forward(80)
        time.sleep(0.5)
        self.stop()

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
            action = actions.pop()
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
            if not left_value and right_value:
                self.left_motor.move_backward(speed)
                self.right_motor.move_forward(speed)
            elif left_value and not right_value:
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
        self.turn_left()

        # Check for barriers
        while True:
            # Move forward
            self.move_forward(80)

            front_dist = self.front_dist_sensor.get_distance()
            if front_dist < 15:
                self.stop()
                # Avoid barrier by turning right
                self.turn_right()
                self.move_forward(80)
                time.sleep(0.5)
                self.turn_left()
                # Check for barriers again
                while True:
                    # Move forward
                    self.move_forward(80)

                    front_dist = self.front_dist_sensor.get_distance()
                    if front_dist < 15:
                        self.stop()
                        # Avoid barrier by turning left
                        self.turn_left()
                        self.move_forward(80)
                        time.sleep(0.5)
                        self.turn_right()

                    # Check for finish line
                    color = self.colour_sensor.detects_colour()
                    if color == 'White':
                        self.stop()
                        break

            # Check for finish line
            color = self.colour_sensor.detects_colour()
            if color == 'White':
                self.stop()
                break

    def run_7_segment_number_constructing_arena(self):
        '''
          b _
         a | | c
          e _
         d | | f
          g _
        '''
        NumberEdges = {
            0: {"a": True, "b": True, "c": True, "d": True, "e": False, "f": True, "g": True},
            1: {"a": False, "b": False, "c": True, "d": False, "e": False, "f": True, "g": False},
            2: {"a": False, "b": True, "c": True, "d": True, "e": True, "f": False, "g": True},
            3: {"a": False, "b": True, "c": True, "d": False, "e": True, "f": True, "g": True},
            4: {"a": True, "b": False, "c": True, "d": False, "e": True, "f": True, "g": False},
            5: {"a": True, "b": True, "c": False, "d": False, "e": True, "f": True, "g": True},
            6: {"a": True, "b": True, "c": False, "d": True, "e": True, "f": True, "g": True},
            7: {"a": False, "b": True, "c": True, "d": False, "e": False, "f": True, "g": False},
            8: {"a": True, "b": True, "c": True, "d": True, "e": True, "f": True, "g": True},
            9: {"a": True, "b": True, "c": True, "d": False, "e": True, "f": True, "g": False}
        }
        NumberPaths = {
            'a': [("turn_right", None), ("move_forward", 70), ("turn_left", None), ("move_forward", 70), ("turn_left", None), ("move_forward", 35)],
            'b': [("turn_right", None), ("move_forward", 35), ("turn_left", None), ("move_forward", 35)],
            'c': [("move_forward", 35), ("turn_right", None)],
            'd': [("turn_right", None), ("move_forward", 70), ("turn_left", None), ("move_forward", 105), ("turn_left", None), ("move_forward", 70), ("turn_left", None), ("move_forward", 35), ("turn_right", None)],
            'e': [("move_forward", 35)],
            'f': [("move_forward", 35), ("turn_left", None)],
            'g': [("turn_left", None), ('move_forward', 35), ("turn_right", None), ("move_forward", 35)]
        }

        '''
                1
                2
        3 4 5
        '''
        BoxesPaths = {
            1: [("turn_right", None), ("move_forward", 70), ("turn_right", None)],
            2: [("turn_right", None), ("move_forward", 35), ("turn_right", None)],
            3: [("turn_left", None), ("move_forward", 70), ("turn_right", None), ("move_forward", 105), ("turn_left", None)],
            4: [("turn_left", None), ("move_forward", 70), ("turn_right", None), ("move_forward", 70), ("turn_left", None)],
            5: [("turn_left", None), ("move_forward", 70), ("turn_right", None), ("move_forward", 35), ("turn_left", None)]
        }

        actions = []

        boxes_availability = [False, False, False, False, False]
        def checkAvailability_box(box_number):
            for action in BoxesPaths[box_number]:
                self.do_action(action[0], action[1])
                actions.append(action)
            self.reverse()
            self.undo_actions(actions)
            self.reverse()
        def checkAvailability_boxes():
            for i in range(1, 6):
                checkAvailability_box(i)

        def identify_number():
            # Move 35cm forward
            self.move_forward_distance(80, 35)
            actions.append(('move_forward', 35))
            # Check for barrier
            front_dist = self.front_dist_sensor.get_distance()
            if front_dist < 20:
                # Turn left
                self.turn_left()
                actions.append(('turn_left', None))
                # Check for barrier
                front_dist = self.front_dist_sensor.get_distance()
                if front_dist < 20:
                    # Reverse
                    self.reverse()
                    actions.append(('reverse', None))
                    # Check for barrier
                    front_dist = self.front_dist_sensor.get_distance()
                    if front_dist < 20:
                        # Turn right
                        self.turn_right()
                        actions.append(('turn_right', None))
                        # Move 35cm forward
                        self.move_forward_distance(80, 35)
                        actions.append(('move_forward', 35))
                        # Turn left
                        self.turn_left()
                        actions.append(('turn_left', None))
                        # Move 70cm forward
                        self.move_forward_distance(80, 70)
                        actions.append(('move_forward', 70))
                        # Turn left
                        self.turn_left()
                        actions.append(('turn_left', None))
                        # Move 70cm forward
                        self.move_forward_distance(80, 70)
                        actions.append(('move_forward', 70))
                        # Turn left
                        self.turn_left()
                        actions.append(('turn_left', None))
                        # Move 35cm forward
                        self.move_forward_distance(80, 35)
                        actions.append(('move_forward', 35))
                        # Check for barrier
                        front_dist = self.front_dist_sensor.get_distance()
                        if front_dist < 20:
                            # Turn left
                            self.turn_left()
                            actions.append(('turn_left', None))
                            # Check for barrier
                            front_dist = self.front_dist_sensor.get_distance()
                            if front_dist < 20:
                                # Reverse
                                self.reverse()
                                actions.append(('reverse', None))
                                # Move 35cm forward
                                self.move_forward_distance(80, 35)
                                actions.append(('move_forward', 35))
                                # Turn left
                                self.turn_left()
                                actions.append(('turn_left', None))
                                # Move 70cm forward
                                self.move_forward_distance(80, 70)
                                actions.append(('move_forward', 70))
                                # Turn left
                                self.turn_left()
                                actions.append(('turn_left', None))
                                # Move 35cm forward
                                self.move_forward_distance(80, 35)
                                actions.append(('move_forward', 35))
                                # Turn left
                                self.turn_left()
                                actions.append(('turn_left', None))
                                # Check for barrier
                                front_dist = self.front_dist_sensor.get_distance()
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
                        self.turn_left()
                        actions.append(('turn_left', None))
                        # Move 70cm forward
                        self.move_forward_distance(80, 70)
                        actions.append(('move_forward', 70))
                        # Turn left
                        self.turn_left()
                        actions.append(('turn_left', None))
                        # Move 70cm forward
                        self.move_forward_distance(80, 70)
                        actions.append(('move_forward', 70))
                        # Turn left
                        self.turn_left()
                        actions.append(('turn_left', None))
                        # Move 35cm forward
                        self.move_forward_distance(80, 35)
                        actions.append(('move_forward', 35))
                        # Turn right
                        self.turn_right()
                        actions.append(('turn_right', None))
                        # Check for barrier
                        front_dist = self.front_dist_sensor.get_distance()
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
                self.turn_right()
                actions.append(('turn_right', None))
                # Check for barrier
                front_dist = self.front_dist_sensor.get_distance()
                if front_dist < 20:
                    return 0
                else:
                    # Move 35cm forward
                    self.move_forward_distance(80, 35)
                    actions.append(('move_forward', 35))
                    # Turn right
                    self.turn_right()
                    actions.append(('turn_right', None))
                    # Check for barrier
                    front_dist = self.front_dist_sensor.get_distance()
                    if front_dist < 20:
                        return 7
                    else:
                        return 1

            self.reverse()
            self.undo_actions(actions)
            self.reverse()

        def build_number():
            prev_number = identify_number()
            prev_number_edges = NumbersEdges[prev_number]
            next_number = 7
            next_number_edges = NumbersEdges[next_number]
            for i in range(ord('a'), ord('g')+1):
                if not(prev_number_edges[chr(i)]) and next_number_edges[chr(i)]:
                    for action in BoxesPaths[boxes_availability.index(True)]:
                        self.do_action(action[0], action[1])
                        actions.append(action)
                    boxes_availability[boxes_availability.index(True)] = False
                    self.reverse()
                    self.undo_actions(actions)
                    self.reverse()
                    for action in NumberPaths[chr(i)]:
                        self.do_action(action[0], action[1])
                        actions.append(action)
                    self.reverse()
                    self.undo_actions(actions)
                    self.reverse()
                if prev_number_edges[chr(i)] and not(next_number_edges[chr(i)]):
                    for action in NumberPaths[chr(i)]:
                        self.do_action(action[0], action[1])
                        actions.append(action)
                    self.reverse()
                    self.undo_actions(actions)
                    self.reverse()
                    for action in BoxesPaths[boxes_availability.index(False)]:
                        self.do_action(action[0], action[1])
                        actions.append(action)
                    self.reverse()
                    self.undo_actions(actions)
                    self.reverse()

        checkAvailability_boxes()
        identify_number()
        build_number()

    def run_elevated_arena(self):
        self.line_follow(stop_color='Blue')
