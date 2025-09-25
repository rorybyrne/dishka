__all__ = [
    "FromDishka",
    "_inject",
    "setup_dishka",
]

from collections.abc import Callable
from typing import TypeVar

from cyclopts import App

from dishka import Container, FromDishka, Scope
from dishka.integrations.base import wrap_injection

T = TypeVar("T")


def _inject(
    container: Container,
    scope: Scope = Scope.REQUEST,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to inject dependencies into Cyclopts commands.

    This decorator uses Dishka's wrap_injection to automatically inject
    dependencies marked with FromDishka[Service] type annotations.

    Args:
        container: Dishka Container
        scope: Scope to enter when executing the command (default: REQUEST)
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        return wrap_injection(
            func=func,
            container_getter=lambda _, __: container,
            remove_depends=True,  # Remove FromDishka parameters from signature
            manage_scope=True,  # Automatically manage scope entry/exit
            scope=scope,
        )

    return decorator


def setup_dishka(
    app: App,
    container: Container,
    *,
    scope: Scope = Scope.REQUEST,
) -> None:
    """Convenience function for apps with a single global container.

    This is a simplified version of setup_auto_injection for the common case
    where you have one container instance to use across all commands.

    Args:
        app: Cyclopts App instance
        container: The Container instance to use for all commands
        scope: Default scope for command execution

    Example:
        container = make_container(...)
        app = cyclopts.App()
        # ... define commands ...
        setup_dishka(app, container)
    """

    def container_getter(args: tuple, kwargs: dict) -> Container:
        return container

    # Apply @inject to all registered commands
    cmds = {}
    for x in app:
        if x in app.help_flags or x in app.version_flags:
            continue
        cmds[x] = app[x]

    for command_app in cmds.values():
        if command_app.default_command is not None:
            func = command_app.default_command
            # Wrap the function with @inject if not already wrapped
            if not hasattr(command_app.default_command, "__dishka_injected__"):
                command_app.default_command = _inject(
                    container=container,
                    scope=scope,
                )(func)
                # Mark as injected to avoid double-wrapping
                command_app.default_command.__dishka_injected__ = True
