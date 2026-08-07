from enum import StrEnum


class OCRInputType(StrEnum):
    """Supported input source types for text extraction."""

    CAMERA_FRAME = "Camera Frame"
    GALLERY_IMAGE = "Gallery Image"
    PDF = "PDF"
    SCREENSHOT = "Screenshot"
    LAPTOP_SCREEN = "Laptop Screen"
    MOBILE_SCREEN = "Mobile Screen"
    VISITING_CARD = "Visiting Card"
    A4_DOCUMENTS = "A4 Documents"
    FLYERS = "Flyers"
    POSTERS = "Posters"
    SHOP_BOARDS = "Shop Boards"
    ROAD_BANNERS = "Road Banners"


class OCRProviderType(StrEnum):
    """Supported third-party or custom OCR acquisition engines."""

    TESSERACT = "Tesseract"
    PADDLEOCR = "PaddleOCR"
    GOOGLE_VISION = "Google Vision"
    AZURE_OCR = "Azure OCR"
    AWS_TEXTRACT = "AWS Textract"
    EASYOCR = "EasyOCR"
    CUSTOM_OCR = "Custom OCR"


class PreprocessingType(StrEnum):
    """Image processing routines performed prior to OCR execution."""

    RESIZE = "Resize"
    DESKEW = "Deskew"
    DENOISE = "Denoise"
    CONTRAST = "Contrast"
    BRIGHTNESS = "Brightness"
    ROTATION = "Rotation"
    PERSPECTIVE_CORRECTION = "Perspective Correction"
    CROP = "Crop"
    NOISE_REMOVAL = "Noise Removal"


class OCRLanguage(StrEnum):
    """Supported multi-language codes for translation and parsing."""

    ENGLISH = "en"
    HINDI = "hi"
    MARATHI = "mr"
    GUJARATI = "gu"
    TAMIL = "ta"
    TELUGU = "te"
    KANNADA = "kn"
    MALAYALAM = "ml"
    PUNJABI = "pa"
    BENGALI = "bn"


class OCRJobStatus(StrEnum):
    """Operational statuses of the OCR request lifecycle."""

    PENDING = "PENDING"
    PREPROCESSING = "PREPROCESSING"
    EXTRACTING = "EXTRACTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
