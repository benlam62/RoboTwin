from envs._base_task import Base_Task
from envs.place_shoe import place_shoe
from envs.utils import *
import sapien

class gpt_place_shoe(place_shoe):
    def play_once(self):
        # ADD AN OBSERVATION AT THE BEGINNING OF THE TASK
        self.save_camera_images(task_name="place_shoe", step_name="step0_initial_scene", generate_num_id="generate_num_2")
        
        # 1. Determine which arm to use based on the shoe's x coordinate.
        shoe_pose = self.shoe.get_pose()
        shoe_position = shoe_pose.p
        
        # Use right arm if shoe's x > 0, otherwise use left arm.
        arm_tag = ArmTag("right" if shoe_position[0] > 0 else "left")
        
        # 2. Pick up the shoe.
        # Grasp the shoe using the selected arm, specifying contact points for a stable grasp.
        self.move(
            self.grasp_actor(
                actor=self.shoe,
                arm_tag=arm_tag,
                contact_point_id=[0, 1]
            )
        )
        self.save_camera_images(task_name="place_shoe", step_name="step1_shoe_grasped", generate_num_id="generate_num_2")
        
        # Lift the shoe up to avoid collision with the table during transport.
        self.move(
            self.move_by_displacement(
                arm_tag=arm_tag,
                z=0.1,  # Lift 10cm
                move_axis='world'
            )
        )
        
        # 3. Get the target pose for placement from the target block's functional point.
        # As per API guidelines, this pose is pre-configured for the task and should be used directly.
        target_pose = self.target_block.get_functional_point(1, "pose")
        
        # 4. Place the shoe on the target block.
        self.move(
            self.place_actor(
                actor=self.shoe,
                arm_tag=arm_tag,
                target_pose=target_pose,
                functional_point_id=0,  # Align the bottom of the shoe with the target pose.
                constrain="align",      # Enforce the specific orientation from the target_pose.
                pre_dis_axis="fp"       # Use functional point direction for pre-displacement.
            )
        )
        self.save_camera_images(task_name="place_shoe", step_name="step2_shoe_placed", generate_num_id="generate_num_2")
        
        # 5. Retract the arm to a safe position.
        # Lift the arm up after placing the shoe to avoid collision.
        self.move(
            self.move_by_displacement(
                arm_tag=arm_tag,
                z=0.1, # Lift 10cm
                move_axis='world'
            )
        )
        
        # Return the arm to its initial position.
        self.move(self.back_to_origin(arm_tag=arm_tag))
        
        # ADD AN OBSERVATION AT THE END OF THE TASK
        self.save_camera_images(task_name="place_shoe", step_name="step3_final_scene", generate_num_id="generate_num_2")

'''
Observation Point Analysis:
1. Capture the initial scene before the robot moves.
2. The robot grasps the shoe with the appropriate arm.
3. The robot places the shoe on the target block.
4. Capture the final scene after the robot arm has retracted to its home position.
'''
