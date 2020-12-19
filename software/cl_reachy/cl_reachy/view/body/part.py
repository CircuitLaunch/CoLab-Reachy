from . import config

class Part(object):
    def __init__(self, motors):
        self.motors = motors
        
    def set_compliance(self, compliance):
        for m in self.motors:
            m.compliant = compliance
            print("###m: ", m)

    def is_angle_within_limits(self, angle, limits):
        return (angle >= limits[0] and angle <= limits[1])
            
    def move_motor(self, motor, goal_position, limits):
        print("###move_motor - goal_position: ", goal_position)
        print("###limits: ", limits)
        """
        if not self.is_angle_within_limits(goal_position, limits):
            print("###False")
            return False
        """

        self.goal_position = goal_position
        print("###True")
        return True

        

    
