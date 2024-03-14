from pathlib import Path
from pprint import pprint

import click

try:
    from .__init__ import Config
    from .runners import flask_run_debug, npm_multi_build, npm_multi_install, npm_run
except ImportError:
    from __init__ import Config
    from runners import flask_run_debug, npm_multi_build, npm_multi_install, npm_run


def command_factory(main):
    @main.command("config")
    def show_config():
        config = Config()
        print("-" * 80)
        pprint(config.config)
        print("-" * 80)

    @main.command("flask")
    def flask():
        config = Config()
        click.echo("Starting the Flask server in debug...")
        flask_run_debug(config.flask_app)

    @main.command("vite-install", help="Run npm install on all Vite apps.")
    def npm_i():
        config = Config()
        npm_multi_install(config)

    @main.command("vite-run", help="Run a single Vite app.")
    @click.argument("app", required=True)
    def npm_mb(app):
        config = Config()
        click.echo("Building npm apps...")
        app_path = Path(config.cwd / app.replace("/", ""))
        if app_path.exists():
            npm_run(config, app)
        else:
            raise FileNotFoundError(f"{app_path} not found.")

    @main.command("vite-build", help="Build a single Vite app.")
    def npm_mb():
        config = Config()
        click.echo("Building npm apps...")
        npm_multi_build(config)

    @main.command("vite-build-run")
    def npm_mbr():
        config = Config()
        click.echo("Building npm apps...")
        npm_multi_build(config)
        click.echo("Starting the Flask server in debug...")
        flask_run_debug(config.flask_app)
