class CertificationException(Exception):
    """Base exception for Enterprise Release Certification errors."""

    def __init__(self, message: str, code: str = "CERTIFICATION_ERROR", status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class ProductionBlockerException(CertificationException):
    """Raised when a production blocker is detected during certification audit."""

    def __init__(self, detail: str):
        super().__init__(f"Production Blocker Detected: {detail}", code="PRODUCTION_BLOCKER", status_code=422)
