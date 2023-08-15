import click

from kis.command.config import attach_config_group
from kis.utils.click_group import OrderedGroup


def create_entrypoint():
    """click endtrypoint"""

    @click.group(cls=OrderedGroup)
    def entrypoint():
        pass

    attach_config_group(entrypoint)

    return entrypoint


if __name__ == "__main__":
    run: click.BaseCommand = create_entrypoint()
    run()
