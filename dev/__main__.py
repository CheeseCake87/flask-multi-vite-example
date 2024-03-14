import click

try:
    from .commands import command_factory
except ImportError:
    from commands import command_factory


@click.group()
def main():
    pass


command_factory(main)

if __name__ == "__main__":
    main()
