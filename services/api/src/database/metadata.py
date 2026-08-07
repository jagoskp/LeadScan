from services.api.src.database import Base
from services.api.src.database.registry import import_models

# Ensure all models from all 12 modules are imported
import_models()

# Expose metadata for Alembic env.py autogenerate detections
target_metadata = Base.metadata
