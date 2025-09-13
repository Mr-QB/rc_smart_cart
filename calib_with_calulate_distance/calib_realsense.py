# #!/usr/bin/env python3
# import rospy
# import cv2
# import numpy as np
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
# import message_filters

# # ===== Camera parameters from calibration =====
# DIM = (848, 800)
# K = np.array([
#     [286.209808349609, 0.0, 429.882110595703],
#     [0.0, 286.291900634766, 413.309387207031],
#     [0.0, 0.0, 1.0]
# ])
# D = np.array([
#     [-0.00804748],
#     [ 0.04675084],
#     [-0.04368873],
#     [ 0.00814379]
# ])

# class DualFisheyeUndistortNode:
#     def __init__(self):
#         self.bridge = CvBridge()

#         # Precompute undistortion maps once
#         self.map1, self.map2 = cv2.fisheye.initUndistortRectifyMap(
#             K, D, np.eye(3), K, DIM, cv2.CV_16SC2
#         )

#         # Subscribe to both fisheye topics with approximate time sync
#         sub1 = message_filters.Subscriber("/camera/fisheye1/image_raw", Image)
#         sub2 = message_filters.Subscriber("/camera/fisheye2/image_raw", Image)

#         ats = message_filters.ApproximateTimeSynchronizer(
#             [sub1, sub2],
#             queue_size=5,
#             slop=0.05
#         )
#         ats.registerCallback(self.callback)

#     def undistort(self, frame):
#         return cv2.remap(
#             frame, self.map1, self.map2,
#             interpolation=cv2.INTER_LINEAR,
#             borderMode=cv2.BORDER_CONSTANT
#         )

#     def callback(self, img1_msg, img2_msg):
#         try:
#             frame1 = self.bridge.imgmsg_to_cv2(img1_msg, desired_encoding="bgr8")
#             frame2 = self.bridge.imgmsg_to_cv2(img2_msg, desired_encoding="bgr8")
#         except Exception as e:
#             rospy.logerr("CV Bridge error: %s" % e)
#             return

#         und1 = self.undistort(frame1)
#         und2 = self.undistort(frame2)

#         # Combine side by side
#         combined = np.hstack((und1, und2))

#         cv2.imshow("T265 Fisheye 1 & 2 Undistorted", combined)
#         cv2.waitKey(1)

# if __name__ == "__main__":
#     rospy.init_node("t265_dual_fisheye_undistort")
#     DualFisheyeUndistortNode()
#     rospy.loginfo("Dual fisheye undistort node started.")
#     rospy.spin()
#     cv2.destroyAllWindows()


#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import message_filters

# ===== Camera parameters from rs-enumerate-devices -c =====
DIM = (848, 800)

# Fisheye 1 intrinsics
K1 = np.array([
    [286.209808349609, 0.0, 429.882110595703],
    [0.0, 286.291900634766, 413.309387207031],
    [0.0, 0.0, 1.0]
])
D1 = np.array([[-0.00804748], [0.04675084], [-0.04368873], [0.00814379]])

# Fisheye 2 intrinsics
K2 = np.array([
    [286.449005126953, 0.0, 422.782196044922],
    [0.0, 286.439605712891, 400.777099609375],
    [0.0, 0.0, 1.0]
])
D2 = np.array([[-0.00792319], [0.04615819], [-0.04278706], [0.00779190]])

class DualFisheyeUndistortNode:
    def __init__(self):
        self.bridge = CvBridge()

        # Precompute undistortion maps for each eye
        self.map1_left, self.map2_left = cv2.fisheye.initUndistortRectifyMap(
            K1, D1, np.eye(3), K1, DIM, cv2.CV_16SC2
        )
        self.map1_right, self.map2_right = cv2.fisheye.initUndistortRectifyMap(
            K2, D2, np.eye(3), K2, DIM, cv2.CV_16SC2
        )

        # Subscribers with approximate time sync
        sub1 = message_filters.Subscriber("/camera/fisheye1/image_raw", Image)
        sub2 = message_filters.Subscriber("/camera/fisheye2/image_raw", Image)

        ats = message_filters.ApproximateTimeSynchronizer(
            [sub1, sub2],
            queue_size=5,
            slop=0.05
        )
        ats.registerCallback(self.callback)

    def callback(self, img1_msg, img2_msg):
        try:
            frame1 = self.bridge.imgmsg_to_cv2(img1_msg, desired_encoding="bgr8")
            frame2 = self.bridge.imgmsg_to_cv2(img2_msg, desired_encoding="bgr8")
        except Exception as e:
            rospy.logerr("CV Bridge error: %s" % e)
            return

        # Undistort each image with its own calibration
        und1 = cv2.remap(frame1, self.map1_left, self.map2_left, interpolation=cv2.INTER_LINEAR)
        und2 = cv2.remap(frame2, self.map1_right, self.map2_right, interpolation=cv2.INTER_LINEAR)

        # Combine and display
        combined = np.hstack((und1, und2))
        cv2.imshow("T265 Fisheye 1 & 2 Undistorted", combined)
        cv2.waitKey(1)

if __name__ == "__main__":
    rospy.init_node("t265_dual_fisheye_undistort")
    DualFisheyeUndistortNode()
    rospy.loginfo("Dual fisheye undistort node with separate calibration started.")
    rospy.spin()
    cv2.destroyAllWindows()
