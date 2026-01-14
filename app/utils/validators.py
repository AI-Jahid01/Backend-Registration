#backend/app/utils/validators.py 
def validate_min_images(images: list, min_required: int = 5):
    if len(images) < min_required:
        raise ValueError("Minimum 5 face images required")
