from . import config
from .part import Part

class RightArm(Part):
    def __init__(self, motors, fans, goto):
        super().__init__(motors)

        self.fans = fans

        (self.shoulder_fan, self.elbow_fan, self.wrist_fan) = self.fans

        self.goto = goto
        
    def turn_on_fans(self):
        self.shoulder_fan.on()
        self.elbow_fan.on()
        self.wrist_fan.on()

    def turn_off_fans(self):
        self.shoulder_fan.off()
        self.elbow_fan.off()
        self.wrist_fan.off()

    def move_to_zero(self):
        self.goto({
            'right_arm.shoulder_pitch': 0,
            'right_arm.shoulder_roll': 0,
            'right_arm.arm_yaw': 0,
            'right_arm.elbow_pitch': 0,
            'right_arm.hand.forearm_yaw': 0,
            'right_arm.hand.wrist_pitch': 0,
            'right_arm.hand.wrist_roll': 0,
            'right_arm.hand.gripper': 0,
        }, duration=3, wait=True)

    def wave(self):
        self.set_compliance(False)
        self.move_to_zero()

        #Wave Frame 1, bring arm up
        self.goto({
            'right_arm.shoulder_pitch': -20,
            'right_arm.shoulder_roll': -10,
            'right_arm.arm_yaw': -10,    
            'right_arm.elbow_pitch': -120,
            'right_arm.hand.forearm_yaw': 0,
            'right_arm.hand.wrist_pitch': 0,
            'right_arm.hand.wrist_roll': 0,
            'right_arm.hand.gripper': 0,
        }, duration=2, wait=True)

        #Wave Frame 2 (Hand Wave)
        self.goto({
            'right_arm.hand.wrist_roll': 40,
            'right_arm.hand.gripper': 0,
        }, duration=0.75, wait=True)

        self.goto({
            'right_arm.hand.wrist_roll': -40,
            'right_arm.hand.gripper': 0,
        }, duration=0.75, wait=True)

        self.goto({
            'right_arm.hand.wrist_roll': 40,
            'right_arm.hand.gripper': 0,
        }, duration=0.75, wait=True)

        self.goto({
            'right_arm.hand.wrist_roll': -40,
            'right_arm.hand.gripper': 0,
        }, duration=0.75, wait=True)

        sleep(2) #wait 2 seconds

        # always go back to zero and reset compliance
        self.move_to_zero()
        self.set_compliance(True)
        
    def open_hand_wave(self):
        self.set_compliance(False)
        self.move_to_zero()

        # open hand wave
        pos_RB = {
            'right_arm.shoulder_pitch': 0, 
            'right_arm.shoulder_roll': -10,
            'right_arm.arm_yaw': -90, # rotate arm outwards negative, -45 too far front and -90 too far back, too angled at -60
            'right_arm.elbow_pitch': -120,# too low at -45, may be too angled at -120
            'right_arm.hand.forearm_yaw': -90,
            'right_arm.hand.wrist_pitch': 0,
            'right_arm.hand.wrist_roll': 0, #angle to see open hand (positive is away?) - changed it to roll given open hand position is friendlier - changed everything else accordingly
            'right_arm.hand.gripper': 0,
        }

        # Loop Hand Wave
        pos_RC = {
            'right_arm.shoulder_pitch': 0, 
            'right_arm.shoulder_roll': -10,
            'right_arm.arm_yaw': -90,
            'right_arm.elbow_pitch': -120,
            'right_arm.hand.forearm_yaw': -90,
            'right_arm.hand.wrist_pitch': 0, #moves it back and forth (back is positive - don't want), negative back to see the wave
            'right_arm.hand.wrist_roll': -30, #want to move out before in (negative), out is positive - don't move hands move arm
            'right_arm.hand.gripper': 0,
        }

        pos_RD = {
            'right_arm.shoulder_pitch': 0, 
            'right_arm.shoulder_roll': -10,
            'right_arm.arm_yaw': -90,
            'right_arm.elbow_pitch': -120,
            'right_arm.hand.forearm_yaw': -90,
            'right_arm.hand.wrist_pitch': 0, #negative back to see the wave
            'right_arm.hand.wrist_roll': 30, #10, was okay: 45 better? want to move out before in (negative), out is positive - don't move hands - move arm
            'right_arm.hand.gripper': 0,
        }

        # Zero/Home
        self.goto(goal_positions = zero_posR, duration=2, wait=True)   
        time.sleep(2)

        # zero and rehome before and after the below loop
        self.goto(goal_positions = pos_RB, duration = 2.5, wait = True)
        for m in range(3):
            self.goto(goal_positions = pos_RC, duration = 1, wait = True)
            self.goto(goal_positions = pos_RD, duration = 1, wait = True)

        time.sleep(2)
            
        # always go back to zero and reset compliance
        self.move_to_zero()
        self.set_compliance(True)

        
