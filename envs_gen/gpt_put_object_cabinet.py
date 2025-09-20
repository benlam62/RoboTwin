from envs._base_task import Base_Task
from envs.put_object_cabinet import put_object_cabinet
from envs.utils import *
import sapien

class gpt_put_object_cabinet(put_object_cabinet):
    def play_once(self):
        # Capture the initial scene state
        self.save_camera_images(task_name="put_object_cabinet", step_name="step0_initial_state", generate_num_id="generate_num_3")
        
        # 1. Determine which arm is closer to the cabinet to open it, and which arm will grasp the object.
        cabinet_pos = self.cabinet.get_pose().p
        if cabinet_pos[0] < 0:
            open_arm_tag = ArmTag("left")
            grasp_arm_tag = ArmTag("right")
        else:
            open_arm_tag = ArmTag("right")
            grasp_arm_tag = ArmTag("left")

        # 2. Use the closer arm to grasp the cabinet handle.
        # To ensure a secure grip on the handle, we use a negative grasp_dis to move the gripper
        # slightly past the contact point before closing. This is a common technique for grasping handles.
        self.move(
            self.grasp_actor(
                actor=self.cabinet,
                arm_tag=open_arm_tag,
                contact_point_id=[0, 1],
                pre_grasp_dis=0.1,  # Approach from 10cm away
                grasp_dis=-0.03     # Move 3cm "into" the handle to secure the grip
            )
        )
        self.save_camera_images(task_name="put_object_cabinet", step_name="step1_grasp_cabinet_handle", generate_num_id="generate_num_3")

        # 3. Pull the drawer open by moving the arm forward (+y direction is 'front' in world coordinates).
        self.move(
            self.move_by_displacement(
                arm_tag=open_arm_tag,
                y=0.25,  # Pull forward by 25cm to open the drawer
                move_axis='world'
            )
        )
        self.save_camera_images(task_name="put_object_cabinet", step_name="step2_open_drawer", generate_num_id="generate_num_3")

        # 4. Release the handle by opening the gripper.
        self.move(
            self.open_gripper(arm_tag=open_arm_tag)
        )
        self.save_camera_images(task_name="put_object_cabinet", step_name="step3_release_handle", generate_num_id="generate_num_3")

        # 4.5. Add a retreat move to clear the handle and avoid collision.
        self.move(
            self.move_by_displacement(
                arm_tag=open_arm_tag,
                z=0.1, # Move up by 10cm
                move_axis='world'
            )
        )

        # 5. Simultaneously, move the opening arm back to its origin and use the other arm to grasp the object.
        self.move(
            self.back_to_origin(arm_tag=open_arm_tag),
            self.grasp_actor(
                actor=self.object,
                arm_tag=grasp_arm_tag
            )
        )
        self.save_camera_images(task_name="put_object_cabinet", step_name="step4_grasp_object", generate_num_id="generate_num_3")

        # 6. Lift the object up to avoid dragging it on the surface.
        self.move(
            self.move_by_displacement(
                arm_tag=grasp_arm_tag,
                z=0.15,  # Lift 15cm
                move_axis='world'
            )
        )

        # 7. Get the target pose inside the cabinet's drawer using its functional point.
        target_pose = self.cabinet.get_functional_point(0, "pose")

        # 8. Place the object inside the drawer.
        self.move(
            self.place_actor(
                actor=self.object,
                arm_tag=grasp_arm_tag,
                target_pose=target_pose,
                pre_dis=0.1,
                dis=0.02,
                pre_dis_axis='fp'  # Use the target functional point's orientation for the approach
            )
        )
        self.save_camera_images(task_name="put_object_cabinet", step_name="step5_place_object_in_drawer", generate_num_id="generate_num_3")

        # 9. Lift the arm after placing to avoid collision.
        self.move(
            self.move_by_displacement(
                arm_tag=grasp_arm_tag,
                z=0.1, # Lift 10cm
                move_axis='world'
            )
        )

        # 10. Return the grasping arm to its origin position to complete the task.
        self.move(
            self.back_to_origin(arm_tag=grasp_arm_tag)
        )
        self.save_camera_images(task_name="put_object_cabinet", step_name="step6_final_state", generate_num_id="generate_num_3")

'''
Observation Point Analysis:
1. Capture the initial state of the scene before any action is taken.
2. The robot grasps the cabinet handle with the designated arm.
3. The robot pulls the cabinet drawer open.
4. The robot opens its gripper to release the cabinet handle.
5. The robot grasps the object from the table with its other arm.
6. The robot places the object inside the open cabinet drawer.
7. The robot returns its arm to the origin position, completing the task.
'''
