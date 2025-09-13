# # #!/usr/bin/env python3
# # import rospy
# # import cv2
# # import numpy as np
# # from sensor_msgs.msg import Image
# # from cv_bridge import CvBridge
# # import message_filters
# # from ultralytics import YOLO

# # # ========== Camera parameters (của T265) ==========
# # DIM = (848, 800)

# # K1 = np.array([
# #     [286.2098, 0.0, 429.8821],
# #     [0.0, 286.2919, 413.3094],
# #     [0.0, 0.0, 1.0]
# # ])
# # D1 = np.array([[-0.00804748], [0.04675084], [-0.04368873], [0.00814379]])

# # K2 = np.array([
# #     [286.4490, 0.0, 422.7822],
# #     [0.0, 286.4396, 400.7771],
# #     [0.0, 0.0, 1.0]
# # ])
# # D2 = np.array([[-0.00792319], [0.04615819], [-0.04278706], [0.00779190]])

# # # baseline (m) giữa 2 camera của T265
# # BASELINE = 0.063  # 63 mm

# # class PersonDistanceNode:
# #     def __init__(self):
# #         rospy.loginfo("Init YOLOv8 + Stereo triangulation node...")
# #         self.bridge = CvBridge()
# #         self.model = YOLO("yolov8n.pt")   # load model YOLOv8 nhỏ

# #         # undistort maps
# #         self.map1_left, self.map2_left = cv2.fisheye.initUndistortRectifyMap(
# #             K1, D1, np.eye(3), K1, DIM, cv2.CV_16SC2
# #         )
# #         self.map1_right, self.map2_right = cv2.fisheye.initUndistortRectifyMap(
# #             K2, D2, np.eye(3), K2, DIM, cv2.CV_16SC2
# #         )

# #         # ROS subscribers
# #         sub1 = message_filters.Subscriber("/camera/fisheye1/image_raw", Image)
# #         sub2 = message_filters.Subscriber("/camera/fisheye2/image_raw", Image)

# #         ats = message_filters.ApproximateTimeSynchronizer([sub1, sub2], queue_size=5, slop=0.05)
# #         ats.registerCallback(self.callback)

# #     def detect_person_center(self, frame):
# #         """Trả về tâm bbox người (x, y) hoặc None"""
# #         results = self.model(frame, verbose=False)
# #         for r in results:
# #             for box in r.boxes:
# #                 if int(box.cls[0]) == 0:  # class 0 = person
# #                     x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
# #                     cx = (x1 + x2) // 2
# #                     cy = (y1 + y2) // 2
# #                     return (cx, cy), (x1, y1, x2, y2)
# #         return None, None

# #     def callback(self, img1_msg, img2_msg):
# #         # convert ROS → OpenCV
# #         frame1 = self.bridge.imgmsg_to_cv2(img1_msg, "bgr8")
# #         frame2 = self.bridge.imgmsg_to_cv2(img2_msg, "bgr8")

# #         # undistort
# #         und1 = cv2.remap(frame1, self.map1_left, self.map2_left, interpolation=cv2.INTER_LINEAR)
# #         und2 = cv2.remap(frame2, self.map1_right, self.map2_right, interpolation=cv2.INTER_LINEAR)

# #         # detect person
# #         c1, bbox1 = self.detect_person_center(und1)
# #         c2, bbox2 = self.detect_person_center(und2)

# #         if c1 and c2:
# #             disparity = abs(c1[0] - c2[0])
# #             if disparity > 0:
# #                 focal = K1[0, 0]  # fx
# #                 Z = (focal * BASELINE) / disparity
# #                 distance_cm = Z * 100

# #                 # vẽ bbox + khoảng cách
# #                 cv2.rectangle(und1, (bbox1[0], bbox1[1]), (bbox1[2], bbox1[3]), (0, 255, 0), 2)
# #                 cv2.putText(und1, f"{distance_cm:.1f} cm", (bbox1[0], bbox1[1]-10),
# #                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

# #         # hiển thị
# #         cv2.imshow("Cam1", und1)
# #         cv2.imshow("Cam2", und2)
# #         cv2.waitKey(1)

# # if __name__ == "__main__":
# #     rospy.init_node("person_distance_node")
# #     node = PersonDistanceNode()
# #     rospy.loginfo("Person distance estimation node started.")
# #     rospy.spin()
# #     cv2.destroyAllWindows()


# #!/usr/bin/env python3
# import rospy
# import cv2
# import numpy as np
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
# import message_filters
# from ultralytics import YOLO

# # ========== Camera parameters (của T265) ==========
# DIM = (848, 800)

# K1 = np.array([
#     [286.2098, 0.0, 429.8821],
#     [0.0, 286.2919, 413.3094],
#     [0.0, 0.0, 1.0]
# ])
# D1 = np.array([[-0.00804748], [0.04675084], [-0.04368873], [0.00814379]])

# K2 = np.array([
#     [286.4490, 0.0, 422.7822],
#     [0.0, 286.4396, 400.7771],
#     [0.0, 0.0, 1.0]
# ])
# D2 = np.array([[-0.00792319], [0.04615819], [-0.04278706], [0.00779190]])

# # baseline (m) giữa 2 camera của T265
# BASELINE = 0.063  # 63 mm


# class PersonDistanceNode:
#     def __init__(self):
#         rospy.loginfo("Init YOLOv8 + Stereo triangulation node...")
#         self.bridge = CvBridge()
#         self.model = YOLO("yolov8n.pt")   # load model YOLOv8 nhỏ

#         # undistort maps
#         self.map1_left, self.map2_left = cv2.fisheye.initUndistortRectifyMap(
#             K1, D1, np.eye(3), K1, DIM, cv2.CV_16SC2
#         )
#         self.map1_right, self.map2_right = cv2.fisheye.initUndistortRectifyMap(
#             K2, D2, np.eye(3), K2, DIM, cv2.CV_16SC2
#         )

#         # ROS subscribers
#         sub1 = message_filters.Subscriber("/camera/fisheye1/image_raw", Image)
#         sub2 = message_filters.Subscriber("/camera/fisheye2/image_raw", Image)

#         ats = message_filters.ApproximateTimeSynchronizer([sub1, sub2], queue_size=5, slop=0.05)
#         ats.registerCallback(self.callback)

#     def detect_person_center(self, frame):
#         """Trả về (cx, cy), bbox của người lớn nhất hoặc None"""
#         results = self.model(frame, verbose=False)
#         best_box = None
#         max_area = 0
#         for r in results:
#             for box in r.boxes:
#                 if int(box.cls[0]) == 0:  # class 0 = person
#                     x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
#                     area = (x2 - x1) * (y2 - y1)
#                     if area > max_area:   # chọn người lớn nhất
#                         max_area = area
#                         best_box = (x1, y1, x2, y2)
#         if best_box:
#             cx = (best_box[0] + best_box[2]) // 2
#             cy = (best_box[1] + best_box[3]) // 2
#             return (cx, cy), best_box
#         return None, None

#     def callback(self, img1_msg, img2_msg):
#         # convert ROS → OpenCV
#         frame1 = self.bridge.imgmsg_to_cv2(img1_msg, "bgr8")
#         frame2 = self.bridge.imgmsg_to_cv2(img2_msg, "bgr8")

#         # undistort
#         und1 = cv2.remap(frame1, self.map1_left, self.map2_left, interpolation=cv2.INTER_LINEAR)
#         und2 = cv2.remap(frame2, self.map1_right, self.map2_right, interpolation=cv2.INTER_LINEAR)

#         # detect person
#         c1, bbox1 = self.detect_person_center(und1)
#         c2, bbox2 = self.detect_person_center(und2)

#         if c1 and c2 and bbox1 and bbox2:
#             disparity = abs(c1[0] - c2[0])
#             if disparity > 0:
#                 focal = K1[0, 0]  # fx
#                 Z = (focal * BASELINE) / disparity
#                 distance_cm = Z * 100

#                 # Vẽ bbox + khoảng cách trên cam1
#                 cv2.rectangle(und1, (bbox1[0], bbox1[1]), (bbox1[2], bbox1[3]), (0, 255, 0), 2)
#                 cv2.putText(und1, f"{distance_cm:.1f} cm",
#                             (bbox1[0], bbox1[1] - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#                 # Vẽ bbox + khoảng cách trên cam2
#                 cv2.rectangle(und2, (bbox2[0], bbox2[1]), (bbox2[2], bbox2[3]), (0, 255, 0), 2)
#                 cv2.putText(und2, f"{distance_cm:.1f} cm",
#                             (bbox2[0], bbox2[1] - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#         # hiển thị
#         # cv2.imshow("Cam1 (bbox + distance)", und1)
#         # cv2.imshow("Cam2 (bbox + distance)", und2)
#         # # ghép 2 ảnh cạnh nhau
#         combined = np.hstack((und1, und2))
#         cv2.imshow("Stereo View (Cam1 + Cam2)", combined)

#         cv2.waitKey(1)


# if __name__ == "__main__":
#     rospy.init_node("person_distance_node")
#     node = PersonDistanceNode()
#     rospy.loginfo("Person distance estimation node started.")
#     rospy.spin()
#     cv2.destroyAllWindows()



#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import message_filters
from ultralytics import YOLO

# ========== Camera parameters (của T265) ==========
DIM = (848, 800)

K1 = np.array([
    [286.2098, 0.0, 429.8821],
    [0.0, 286.2919, 413.3094],
    [0.0, 0.0, 1.0]
])
D1 = np.array([[-0.00804748], [0.04675084], [-0.04368873], [0.00814379]])

K2 = np.array([
    [286.4490, 0.0, 422.7822],
    [0.0, 286.4396, 400.7771],
    [0.0, 0.0, 1.0]
])
D2 = np.array([[-0.00792319], [0.04615819], [-0.04278706], [0.00779190]])

# baseline (m) giữa 2 camera của T265
BASELINE = 0.063  # 63 mm

class PersonDistanceNode:
    def __init__(self):
        rospy.loginfo("Init YOLOv8 + Stereo solvePnP fusion node...")
        self.bridge = CvBridge()
        self.model = YOLO("yolov8n.pt")   # load model YOLOv8 nhỏ

        # undistort maps
        self.map1_left, self.map2_left = cv2.fisheye.initUndistortRectifyMap(
            K1, D1, np.eye(3), K1, DIM, cv2.CV_16SC2
        )
        self.map1_right, self.map2_right = cv2.fisheye.initUndistortRectifyMap(
            K2, D2, np.eye(3), K2, DIM, cv2.CV_16SC2
        )

        # ROS subscribers
        sub1 = message_filters.Subscriber("/camera/fisheye1/image_raw", Image)
        sub2 = message_filters.Subscriber("/camera/fisheye2/image_raw", Image)

        ats = message_filters.ApproximateTimeSynchronizer([sub1, sub2], queue_size=5, slop=0.05)
        ats.registerCallback(self.callback)

    def detect_person_bbox(self, frame):
        """Trả về bbox người hoặc None"""
        results = self.model(frame, verbose=False)
        for r in results:
            for box in r.boxes:
                if int(box.cls[0]) == 0:  # class 0 = person
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    return (x1, y1, x2, y2)
        return None

    def estimate_distance_solvepnp(self, bbox, K, D):
        """Ước lượng khoảng cách bằng solvePnP"""
        x1, y1, x2, y2 = bbox
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        image_points = np.array([
            (x1, y1),   # top-left
            (x2, y1),   # top-right
            (x2, y2),   # bottom-right
            (x1, y2),   # bottom-left
            (cx, y2)    # mid-bottom
        ], dtype=np.float32)

        # Giả định kích thước người (m)
        object_points = np.array([
            (-0.2, -1.7, 0),  # top-left
            ( 0.2, -1.7, 0),  # top-right
            ( 0.2,    0, 0),  # bottom-right
            (-0.2,    0, 0),  # bottom-left
            ( 0.0,    0, 0)   # mid-bottom
        ], dtype=np.float32)

        success, rvec, tvec = cv2.solvePnP(object_points, image_points, K, D, flags=cv2.SOLVEPNP_ITERATIVE)

        if not success:
            return None
        return float(tvec[2][0])  # Z (m)

    def callback(self, img1_msg, img2_msg):
        # convert ROS → OpenCV
        frame1 = self.bridge.imgmsg_to_cv2(img1_msg, "bgr8")
        frame2 = self.bridge.imgmsg_to_cv2(img2_msg, "bgr8")

        # undistort
        und1 = cv2.remap(frame1, self.map1_left, self.map2_left, interpolation=cv2.INTER_LINEAR)
        und2 = cv2.remap(frame2, self.map1_right, self.map2_right, interpolation=cv2.INTER_LINEAR)

        # detect
        bbox1 = self.detect_person_bbox(und1)
        bbox2 = self.detect_person_bbox(und2)

        dist1, dist2 = None, None

        if bbox1 is not None:
            dist1 = self.estimate_distance_solvepnp(bbox1, K1, D1)
            if dist1:
                cv2.rectangle(und1, (bbox1[0], bbox1[1]), (bbox1[2], bbox1[3]), (0,255,0), 2)
                cv2.putText(und1, f"{dist1*100:.1f} cm", (bbox1[0], bbox1[1]-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        if bbox2 is not None:
            dist2 = self.estimate_distance_solvepnp(bbox2, K2, D2)
            if dist2:
                cv2.rectangle(und2, (bbox2[0], bbox2[1]), (bbox2[2], bbox2[3]), (0,255,0), 2)
                cv2.putText(und2, f"{dist2*100:.1f} cm", (bbox2[0], bbox2[1]-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        # Fusion: trung bình 2 khoảng cách
        if dist1 and dist2:
            dist_avg = (dist1 + dist2) / 2.0
            rospy.loginfo(f"Stereo fused distance: {dist_avg:.2f} m")

            # hiển thị kết quả trên cam1
            cv2.putText(und1, f"Fused: {dist_avg*100:.1f} cm", (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 2)

        # Hiển thị
        cv2.imshow("Cam1 (solvePnP)", und1)
        cv2.imshow("Cam2 (solvePnP)", und2)
        cv2.waitKey(1)

if __name__ == "__main__":
    rospy.init_node("person_distance_node")
    node = PersonDistanceNode()
    rospy.loginfo("Person distance estimation node started (stereo solvePnP fusion).")
    rospy.spin()
    cv2.destroyAllWindows()
