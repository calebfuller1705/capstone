from pathlib import Path
import pytest
from src.api.main import validate_startup_config


def test_placeholder_key_rejected_outside_pytest(monkeypatch: pytest.MonkeyPatch) -> None:
    """Row 1 guard: placeholder keys must fail fast at startup outside pytest and CI."""
    monkeypatch.setenv("VIRUSTOTAL_API_KEY", "YourVirusTotalAPIKeyHere")
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    monkeypatch.delenv("CI", raising=False)
    with pytest.raises(RuntimeError, match="placeholder/mock value"):
        validate_startup_config()


def test_stateless_migration_sentinel_exists_and_has_no_ddl() -> None:
    """Row 2 guard: migrations/0001-stateless.sql must remain an empty DDL-free sentinel (ADR-0005)."""
    sentinel = Path(__file__).resolve().parents[2] / "migrations" / "0001-stateless.sql"
    assert sentinel.is_file(), "migrations/0001-stateless.sql sentinel file is missing"
    content = sentinel.read_text(encoding="utf-8").upper()
    assert "CREATE TABLE" not in content, "Stateless sentinel must not define database tables (CON-04)"
