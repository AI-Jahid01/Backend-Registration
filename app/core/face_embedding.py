
# # this below code is for face embedding extraction with gpu
# # backend/app/core/face_embedding.py
# import numpy as np
# from insightface.app import FaceAnalysis
# from app.core.face_detector import base64_to_image

# # Initialize InsightFace model once
# face_app = FaceAnalysis(name="buffalo_l")
# face_app.prepare(ctx_id=0, det_size=(640, 640))


# def generate_face_embedding(base64_image: str):
#     """
#     Extract 512-D ArcFace embedding from image
#     """
#     image = base64_to_image(base64_image)

#     faces = face_app.get(image)

#     if not faces:
#         return None

#     # Take largest face (closest)
#     face = max(faces, key=lambda f: f.bbox[2] * f.bbox[3])

#     return face.embedding


# below code is for face embedding extraction without gpu and face recognition model
# backend/app/core/face_embedding.py
import base64
import numpy as np
from io import BytesIO
from PIL import Image
import face_recognition

# def base64_to_image(base64_str: str) -> np.ndarray:
#     """
#     Convert base64 string to a numpy image array.
#     """
#     # Remove header if present
#     if "," in base64_str:
#         base64_str = base64_str.split(",")[1]

#     image_data = base64.b64decode(base64_str)
#     image = Image.open(BytesIO(image_data)).convert("RGB")
#     return np.array(image)

def base64_to_image(base64_str: str) -> np.ndarray:
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]

    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data)).convert("RGB")

    # 🔽 Resize if too large
    max_size = 800
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size))

    return np.array(image)



# def generate_face_embedding(base64_image: str):
#     """
#     Extract 128-D face embedding using face_recognition (CPU-friendly).

#     Args:
#         base64_image (str): Base64-encoded image string.

#     Returns:
#         np.ndarray | None: 128-D embedding vector, or None if no face detected.
#     """
#     image = base64_to_image(base64_image)

#     # Detect faces and get embeddings
#     encodings = face_recognition.face_encodings(image)

#     if not encodings:
#         return None

#     # Take the largest face (closest to camera)
#     face_locations = face_recognition.face_locations(image)
#     largest_face_index = np.argmax([
#         (bottom - top) * (right - left) for top, right, bottom, left in face_locations
#     ])

#     return encodings[largest_face_index]


# this one is optimized version
def generate_face_embedding(base64_image: str):
    image = base64_to_image(base64_image)

    # Step 1: detect all faces
    face_locations = face_recognition.face_locations(image, model="hog")

    if not face_locations:
        return None

    # Step 2: pick largest face
    largest_face = max(
        face_locations,
        key=lambda box: (box[2] - box[0]) * (box[1] - box[3])
    )

    # Step 3: get encoding ONLY for that face
    encoding = face_recognition.face_encodings(
        image,
        known_face_locations=[largest_face]
    )

    if not encoding:
        return None

    return encoding[0]


