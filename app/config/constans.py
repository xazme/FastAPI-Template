from pathlib import Path

ROOT_DIR = Path(__file__).parents[2]
print(f"{ROOT_DIR}/envs/.env.test")
ENV_FILE_MAP = {
    "test": ROOT_DIR / "envs/.env.test",
    "prod": ROOT_DIR / "envs/.env.prod",
    "dev": ROOT_DIR / "envs/.env",
}
