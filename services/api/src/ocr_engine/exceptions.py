from fastapi import HTTPException, status


class OCREngineException(HTTPException):
    """Base exception for all OCR engine processing errors."""
    pass


class OCRJobNotFoundException(OCREngineException):
    """Exception raised when an OCR job record is missing from the database."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OCR job not found",
        )


class OCRPageNotFoundException(OCREngineException):
    """Exception raised when a specific page log within an OCR job is missing."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OCR page not found",
        )


class PreprocessingException(OCREngineException):
    """Exception raised when image adjustments fail (e.g. invalid operations)."""

    def __init__(
        self, detail: str = "Image preprocessing execution failed"
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class UnsupportedLanguageException(OCREngineException):
    """Exception raised when an unsupported language code is requested."""

    def __init__(self, lang_code: str = "target language") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OCR language code '{lang_code}' is currently unsupported",
        )


class OCRProviderException(OCREngineException):
    """Exception raised when a third-party OCR provider encounters an error."""

    def __init__(
        self, provider: str = "OCR Provider", detail: str = "Unknown error"
    ) -> None:
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"OCR execution via {provider} failed: {detail}",
        )
