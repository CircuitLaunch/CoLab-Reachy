from . import config
import time
from reachy import parts
from .part import Part

class Head(Part):
    def __init__(self, motors):
        super().__init__(motors)

        if len(self.motors) != 2:
            raise Excpetion("Expcected 2 motors. {} motor(s) found".format(len(self.motors)))

        self.left_antenna, self.right_antenna = self.motors

        print("###self.left_antenna: ", self.left_antenna) 
        print("###self.right_antenna: ", self.right_antenna)
        
    def move_left_antenna(self, goal_position):
        limits = parts.head.Head.dxl_motors['left_antenna']['angle-limits']
        return self.move_motor(self.left_antenna, goal_position, limits)

    def move_right_antenna(self, goal_position):
        limits = parts.head.Head.dxl_motors['right_antenna']['angle-limits']
        return self.move_motor(self.right_antenna, goal_position, limits)
    
    def move_to_zero(self):
        # TODO: make a trajectory for this
        self.move_left_antenna(0)
        self.move_right_antenna(0)

    def wiggle(self):
        print("###wiggle - 1")
        self.set_compliance(False)

        print("###wiggle - 2")    
        self.move_to_zero()

        print("###wiggle - 3")
        angles = [45, 0, -45, 0, 45, 0, -45]
        #angles = [45, -45]

        print("###wiggle - 4")
        for angle in angles:
            print("###wiggle - 4a - angle: ", angle)
            self.move_left_antenna(angle)
            time.sleep(1.0)
            self.move_right_antenna(angle)

        print("###wiggle - 5")
            
        self.set_compliance(True)

        print("###wiggle - 6")
    
