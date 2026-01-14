# this code work for face anaysis with gpu
# # backend/app/core/face_detector.py
# import cv2
# import numpy as np
# import base64


# def base64_to_image(base64_str: str):
#     """
#     Convert base64 image to OpenCV format
#     """
#     img_bytes = base64.b64decode(base64_str.split(",")[-1])
#     np_arr = np.frombuffer(img_bytes, np.uint8)
#     return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


# below code is work for face analysis without gpu and face recognition model
import cv2
import numpy as np
import base64

def base64_to_image(base64_str: str):
    """
    Convert base64 image to RGB NumPy array for face_recognition
    """
    img_bytes = base64.b64decode(base64_str.split(",")[-1])
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # OpenCV loads BGR
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)  # Convert to RGB
    return img_rgb

