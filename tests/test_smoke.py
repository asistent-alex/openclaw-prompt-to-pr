"""Smoke test — verifies the project test infrastructure is working."""


def test_smoke():
    """If this passes, pytest is correctly configured."""
    assert True


def test_skill_file_exists():
    """Verify SKILL.md is present in the project root."""
    from pathlib import Path

    skill_path = Path(__file__).resolve().parent.parent / "SKILL.md"
    assert skill_path.is_file(), f"SKILL.md not found at {skill_path}"


def test_references_directory():
    """Verify the references directory structure exists."""
    from pathlib import Path

    refs = Path(__file__).resolve().parent.parent / "references"
    assert refs.is_dir(), "references/ directory not found"
    assert (refs / "shared").is_dir(), "references/shared/ not found"
    assert (refs / "modes").is_dir(), "references/modes/ not found"