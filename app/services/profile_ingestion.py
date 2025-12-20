from pathlib import Path

UPLOAD_DIR = Path("uploaded_resumes")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_resume_file(file_name: str, content: bytes) -> str:
    """Save uploaded resume to disk and return the path."""
    safe_name = file_name.replace(" ", "_")
    path = UPLOAD_DIR / safe_name
    path.write_bytes(content)
    return str(path)
