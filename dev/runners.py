import shutil
import subprocess
from pathlib import Path

try:
    from .__init__ import Config
except ImportError:
    from __init__ import Config


def npm_run_dev(npm: str, working_dir: Path = Path.cwd()):
    subprocess.run([npm, "run", "dev"], cwd=working_dir)


def flask_run_debug(flask_app: str = "app"):
    print(flask_app)
    subprocess.run(["flask", "--app", flask_app, "run", "--debug"])


def npm_run(config: Config, working_dir: Path = Path.cwd()):
    subprocess.run([config.npm_binary, "run", "dev"], cwd=working_dir)


def npm_multi_install(config: Config):
    for key, value in config.vite.items():
        print(f"{key} running npm i...")
        subprocess.run([config.npm_binary, "i"], cwd=value.get("vite_root"))
        print(f"{key} Done.")


def npm_multi_build(config: Config):
    for key, value in config.vite.items():
        flask_assets_folder = value.get("flask_static_root") / "assets"
        if flask_assets_folder.exists():
            shutil.rmtree(flask_assets_folder)

        subprocess.run([config.npm_binary, "run", "build"], cwd=value.get("vite_root"))

        if not value.get("vite_root").exists():
            raise FileNotFoundError(f"{value.get("vite_root")} not found.")

        vite_assets_folder = value.get("vite_root") / "dist" / "assets"
        vite_static_folder = value.get("vite_root") / "static"

        if vite_static_folder.exists() and config.flask_static_root.exists():
            flask_static_root_glob = config.flask_static_root.glob("*")
            vite_static_folder_glob = vite_static_folder.glob("*")

            flask_static_root_files = [file.name for file in flask_static_root_glob]
            vite_static_folder_files = [file.name for file in vite_static_folder_glob]

            for file in vite_static_folder_files:
                if file not in flask_static_root_files:
                    shutil.copy(vite_static_folder / file, config.flask_static_root)
                    print(f"{file} copied to {config.flask_static_root}.")
                else:
                    print(f"{file} already exists in {config.flask_static_root}.")

        print(f"{key} build complete, copying files...")
        subprocess.run(["cp", "-r", vite_assets_folder, value.get("flask_static_root")])
        print(f"{key} files copied.")
