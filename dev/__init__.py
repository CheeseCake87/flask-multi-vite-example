from pathlib import Path

import toml
from dotenv import load_dotenv

load_dotenv()


class PathNotValidException(Exception):
    pass


class Config:
    cwd: Path
    pyproject: Path
    config: dict

    npm_binary: str
    flask_app: str
    vite: dict

    flask_static_root: Path

    def __init__(self):
        self.cwd = Path.cwd()
        pyproject = self.cwd / "pyproject.toml"

        if not pyproject.exists():
            raise FileNotFoundError("pyproject.toml not found.")

        self.pyproject = pyproject
        self.config = self._load_config()

    def _convert_to_path(self, path: str) -> Path:
        if Path(path).exists() and Path(path).is_dir():
            return Path(path)
        else:
            if Path(self.cwd / path).exists() and Path(self.cwd / path).is_dir():
                return Path(self.cwd / path)

        raise PathNotValidException(f"{path} is not a valid path.")

    def _load_config(self):
        config_raw = toml.load(self.pyproject)
        dev = config_raw.get("dev", {})
        vite = dev.get("vite", {})

        self.npm_binary = dev.get("npm_binary", "npm")
        self.flask_app = dev.get("flask_app", "app")
        self.flask_static_root = self._convert_to_path(dev.get("flask_static_root", "app/static"))

        for key, value in vite.items():
            for k, v in value.items():
                vite[key][k] = self._convert_to_path(v)

        dev["vite"] = vite
        self.vite = vite

        return dev
