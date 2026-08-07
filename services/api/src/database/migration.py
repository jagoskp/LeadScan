import alembic.command as alembic_command
from alembic.config import Config


def get_alembic_config(ini_path: str = "alembic.ini") -> Config:
    """Retrieve an Alembic Config object initialized from the ini file."""
    return Config(ini_path)


def upgrade_database(ini_path: str = "alembic.ini") -> None:
    """Run all migrations to the latest revision (head)."""
    cfg = get_alembic_config(ini_path)
    alembic_command.upgrade(cfg, "head")


def downgrade_database(revision: str, ini_path: str = "alembic.ini") -> None:
    """Downgrade migrations to a specified target revision."""
    cfg = get_alembic_config(ini_path)
    alembic_command.downgrade(cfg, revision)


def create_revision(
    message: str, autogenerate: bool = True, ini_path: str = "alembic.ini"
) -> None:
    """Generate a new database migration revision script."""
    cfg = get_alembic_config(ini_path)
    alembic_command.revision(cfg, message=message, autogenerate=autogenerate)
