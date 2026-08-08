def import_models() -> None:
    """Import all database models to register them on SQLAlchemy metadata."""
    # Core Authentication and User management
    import services.api.src.ai.models  # noqa: F401
    import services.api.src.audit.models  # noqa: F401
    import services.api.src.auth.models  # noqa: F401

    # Document management and processing pipelines
    import services.api.src.documents.models  # noqa: F401
    import services.api.src.monitoring.models  # noqa: F401

    # Core foundation modules
    import services.api.src.notifications.models  # noqa: F401
    import services.api.src.ocr.models  # noqa: F401
    import services.api.src.ocr_engine.models  # noqa: F401

    # Organization management
    import services.api.src.organization.models  # noqa: F401
    import services.api.src.reports.models  # noqa: F401

    # Extra features: Search & Reports
    import services.api.src.search.models  # noqa: F401
    import services.api.src.storage.models  # noqa: F401
    import services.api.src.users.models  # noqa: F401
    # Workspace management
    import services.api.src.workspaces.models  # noqa: F401
    import services.api.src.workflow.models  # noqa: F401

    # Processing & Sync Subsystems
    import services.api.src.document_model.models  # noqa: F401
    import services.api.src.ai_understanding.models  # noqa: F401
    import services.api.src.connectors.models  # noqa: F401
    import services.api.src.sync_engine.models  # noqa: F401
    import services.api.src.scanner.models  # noqa: F401
