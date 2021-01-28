from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.commands.context import Context
from redbot.core.commands.help import HelpSettings

from .core.category import Category


class ThemesMeta:
    """This is the skeletal structure of any theme"""

    async def format_cog_help(self, ctx: Context, obj: commands.Cog, help_settings: HelpSettings):
        raise NotImplementedError

    async def format_category_help(self, ctx: Context, obj: Category, help_settings: HelpSettings):
        raise NotImplementedError

    async def format_bot_help(self, ctx: Context, help_settings: HelpSettings):
        raise NotImplementedError

    async def format_command_help(
        self, ctx: Context, obj: commands.Command, help_settings: HelpSettings
    ):
        raise NotImplementedError

    # https://stackoverflow.com/questions/61328355/prohibit-addition-of-new-methods-to-a-python-child-class
    # No themes can have helper methods cause "self" changes during monkey-patch, making them obselete
    def __init_subclass__(cls, *args, **kw):
        super().__init_subclass__(*args, **kw)
        # By inspecting `cls.__dict__` we pick all methods declared directly on the class
        for name, attr in cls.__dict__.items():
            attr = getattr(cls, name)
            if not callable(attr):
                continue
            for superclass in cls.__mro__[1:]:
                if name in dir(superclass):
                    break
            else:
                # method not found in superclasses:
                raise TypeError(
                    f"Method {name} defined in {cls.__name__}  does not exist in superclasses"
                )
