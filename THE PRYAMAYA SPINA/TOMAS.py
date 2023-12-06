import math as m
import urllib.request
import cv2
import mediapipe as mp
import numpy as np

stream = urllib.request.urlopen(input("введите ip адрес камеры "))
bytes = bytes()
last_time = 0

# Calculate distance
def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


# Calculate angle.
def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree


def func_void():
    return 0

def WARING():
    return 0

"""
Function to send alert. Use this function to send alert when bad posture detected.
Feel free to get creative and customize as per your convenience.
"""


def sendWarning(x):
    pass


# =============================CONSTANTS and INITIALIZATIONS=====================================#
# Initilize frame counters.
good_frames = 0
bad_frames = 0

# Font type.
font = cv2.FONT_HERSHEY_SIMPLEX

# Colors.
blue = (255, 127, 0)
red = (50, 50, 255)
green = (127, 255, 0)
dark_blue = (127, 20, 0)
light_green = (127, 233, 100)
yellow = (0, 255, 255)
pink = (255, 0, 255)

# Initialize mediapipe pose class.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
# ===============================================================================================#


if __name__ == "__main__":
    # For webcam input replace file name with 0.
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # Width
    cap.set(4, 480)  # Lenght







    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            # Capture frames.
            #success, image = cap.read()
            # Get fps.
            fps = cap.get(cv2.CAP_PROP_FPS)
            # Get height and width.
            h, w = image.shape[:2]

            # Convert the BGR image to RGB.
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the image.
            keypoints = pose.process(image)

            # Convert the image back to BGR.
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Use lm and lmPose as representative of the following methods.
            lm = keypoints.pose_landmarks
            lmPose = mp_pose.PoseLandmark
            l_shldr_x = 0
            l_shldr_y = 0
            try:
                # Acquire the landmark coordinates.
                # Once aligned properly, left or right should not be a concern.
                # Left shoulder.
                l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
                l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)

                # Right shoulder
                r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
                r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
                # Left ear.
                l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
                l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)

                r_ear_x = int(lm.landmark[lmPose.RIGHT_EAR].x * w)
                r_ear_y = int(lm.landmark[lmPose.RIGHT_EAR].y * h)
                # Left hip.
                l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
                l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

                r_hip_x = int(lm.landmark[lmPose.RIGHT_HIP].x * w)
                r_hip_y = int(lm.landmark[lmPose.RIGHT_HIP].y * h)

                r_heel_x = int(lm.landmark[lmPose.RIGHT_HEEL].x * h)
                r_heel_y = int(lm.landmark[lmPose.RIGHT_HEEL].y * h)

                l_heel_x = int(lm.landmark[lmPose.LEFT_HEEL].x * h)
                l_heel_y = int(lm.landmark[lmPose.LEFT_HEEL].y * h)
                # Calculate distance between left shoulder and right shoulder points.

                X_arr = [l_shldr_x, r_shldr_x, l_ear_x, r_ear_x, l_hip_x, r_hip_x, r_heel_x, l_heel_x]
                Y_arr = [l_shldr_y, r_shldr_y, l_ear_y, r_ear_y, l_hip_y, r_hip_y, r_heel_y, l_heel_y]
                offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)

                # Assist to align the camera to point at the side view of the person.
                # Offset threshold 30 is based on results obtained from analysis over 100 samples.

                # Calculate angles.
                neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
                torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

                X_NACHALO_LINII = 213
                X_CONECZ_LINII = 426
                cvet = (127, 255, 0)
                flag = False
                for i in X_arr :
                    if i > X_NACHALO_LINII and i < X_CONECZ_LINII:
                        cvet = (0, 0 , 255)
                        WARING()
                        break
                    else:
                        cvet = (127, 255, 0)

                cv2.line(image, (X_NACHALO_LINII, 0), (X_NACHALO_LINII, 480), red, 8)
                cv2.line(image, (X_CONECZ_LINII, 0), (X_CONECZ_LINII, 480), red, 8)

                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), cvet, 4)
                cv2.line(image, (l_ear_x, l_ear_y), (r_ear_x, r_ear_y), cvet, 4)
                cv2.line(image, (r_shldr_x, r_shldr_y), (r_ear_x, r_ear_y), cvet, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), cvet, 4)
                cv2.line(image, (r_shldr_x, r_shldr_y), (l_shldr_x, l_shldr_y), cvet, 4)
                cv2.line(image, (r_hip_x, r_hip_y), (r_shldr_x, r_shldr_y), cvet, 4)
                cv2.line(image, (r_hip_x, r_hip_y), (l_hip_x, l_hip_y), cvet, 4)
                cv2.line(image, (r_hip_x, r_hip_y), (r_heel_x, r_heel_y), cvet, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_heel_x, l_heel_y), cvet, 4)

                cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
                cv2.circle(image, (r_shldr_x, r_shldr_y), 7, yellow, -1)

                cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)
                cv2.circle(image, (r_ear_x, r_ear_y), 7, yellow, -1)

                cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)
                cv2.circle(image, (r_hip_x, r_hip_y), 7, yellow, -1)

                cv2.circle(image, (l_heel_x, l_heel_y), 7, yellow, -1)
                cv2.circle(image, (r_heel_x, r_heel_y), 7, yellow, -1)

            except AttributeError:
                func_void()

            # Display.
            cv2.imshow('MediaPipe Pose', image)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()
