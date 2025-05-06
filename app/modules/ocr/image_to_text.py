from PIL import Image, ImageEnhance
from pathlib import Path
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='vi', show_log=False)

def preprocess_image(path: str, contrast_factor: float = 1.5) -> str:
    """
    Preprocess the image by increasing its contrast.

    Args:
        path (str): Path to the image file.
        contrast_factor (float): Factor to increase contrast (default is 1.5).

    Returns:
        str: Path to the preprocessed image.
    """
    # Open the image
    image = Image.open(path)
    
    # Convert to grayscale
    image = image.convert("L")

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    enhanced_image = enhancer.enhance(contrast_factor)

    # Save the enhanced image to a temporary file
    temp_path = Path(path).with_name("contrast_enhanced_" + Path(path).name)
    enhanced_image.save(temp_path)

    return str(temp_path)

def convert_image_to_text(path: str):

    # Convert Path object to string if necessary
    if isinstance(path, Path):
        path = str(path)

    # Preprocess the image to increase brightness
    brightened_path = preprocess_image(path, 2.0)

    result = ocr.ocr(brightened_path, cls=True)
    lines = []
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            line_text = line[1][0]
            line_conf = line[1][1]
            if line_conf < 0.7:
                continue
            if line_text.strip():
                lines.append(line_text.strip())

    return '\n'.join([line for line in lines])
