import click


class OrderedGroup(click.Group):
    """Click group that lists commands in order."""

    def list_commands(self, ctx: click.Context):
        """List commands in order."""
        return list(self.commands)

    def get_command(self, ctx: click.Context, cmd_name: str):
        """Get a command by name."""
        return self.commands.get(cmd_name)
