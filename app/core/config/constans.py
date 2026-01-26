from pathlib import Path

ROOT_DIR = Path(__file__).parents[3]
ENV_FILE_MAP = {
    "test": ROOT_DIR / ".env.test",
    "prod": ROOT_DIR / ".env.prod",
    "dev": ROOT_DIR / ".env",
}
