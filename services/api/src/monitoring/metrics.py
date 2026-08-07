class AppMetrics:
    """Registry managing in-memory application metrics."""

    _api_requests: int = 0
    _total_duration_ms: float = 0.0
    _db_latency_ms: float = 0.0
    _redis_latency_ms: float = 0.0

    _ocr_success: int = 0
    _ocr_fail: int = 0
    _ai_success: int = 0
    _ai_fail: int = 0

    @classmethod
    def record_request(cls, duration_ms: float) -> None:
        """Increment api requests count and add duration millisecond pings."""
        cls._api_requests += 1
        cls._total_duration_ms += duration_ms

    @classmethod
    def update_db_latency(cls, latency_ms: float) -> None:
        """Assign current latency metrics for database."""
        cls._db_latency_ms = latency_ms

    @classmethod
    def update_redis_latency(cls, latency_ms: float) -> None:
        """Assign current latency metrics for redis."""
        cls._redis_latency_ms = latency_ms

    @classmethod
    def record_ocr(cls, success: bool) -> None:
        """Increment OCR success or failure counters."""
        if success:
            cls._ocr_success += 1
        else:
            cls._ocr_fail += 1

    @classmethod
    def record_ai(cls, success: bool) -> None:
        """Increment AI success or failure counters."""
        if success:
            cls._ai_success += 1
        else:
            cls._ai_fail += 1

    @classmethod
    def to_prometheus_format(cls) -> str:
        """Format in-memory metrics into a Prometheus text scraping payload."""
        lines = [
            "# HELP leadscan_api_requests_total Total API requests received.",
            "# TYPE leadscan_api_requests_total counter",
            f"leadscan_api_requests_total {cls._api_requests}",
            "",
            "# HELP leadscan_request_duration_ms_total Total request duration.",
            "# TYPE leadscan_request_duration_ms_total counter",
            f"leadscan_request_duration_ms_total {cls._total_duration_ms}",
            "",
            "# HELP leadscan_db_latency_ms Latency of DB pings in ms.",
            "# TYPE leadscan_db_latency_ms gauge",
            f"leadscan_db_latency_ms {cls._db_latency_ms}",
            "",
            "# HELP leadscan_redis_latency_ms Latency of Redis pings in ms.",
            "# TYPE leadscan_redis_latency_ms gauge",
            f"leadscan_redis_latency_ms {cls._redis_latency_ms}",
            "",
            "# HELP leadscan_ocr_jobs_total Total OCR jobs by outcome.",
            "# TYPE leadscan_ocr_jobs_total counter",
            f'leadscan_ocr_jobs_total{{status="success"}} {cls._ocr_success}',
            f'leadscan_ocr_jobs_total{{status="failed"}} {cls._ocr_fail}',
            "",
            "# HELP leadscan_ai_jobs_total Total AI jobs by outcome.",
            "# TYPE leadscan_ai_jobs_total counter",
            f'leadscan_ai_jobs_total{{status="success"}} {cls._ai_success}',
            f'leadscan_ai_jobs_total{{status="failed"}} {cls._ai_fail}',
        ]
        return "\n".join(lines)
