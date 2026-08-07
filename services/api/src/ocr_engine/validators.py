from services.api.src.ocr_engine.enums import OCRLanguage
from services.api.src.ocr_engine.exceptions import (
    PreprocessingException,
    UnsupportedLanguageException,
)


def validate_ocr_languages(languages: list[str]) -> None:
    """Ensure that all target languages are supported."""
    for lang in languages:
        try:
            OCRLanguage(lang)
        except ValueError:
            raise UnsupportedLanguageException(lang) from None


def validate_image_file(file_path: str) -> None:
    """Validate that the file path suffix matches supported OCR formats."""
    valid_suffixes = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".pdf",
        ".bmp",
        ".tiff",
        ".tif",
    }
    lower_path = file_path.lower()
    if not any(lower_path.endswith(suffix) for suffix in valid_suffixes):
        raise PreprocessingException(
            f"Unsupported file format for OCR extraction: '{file_path}'"
        )
