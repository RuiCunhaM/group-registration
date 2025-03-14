import reflex as rx

from ..components.navbar import navbar


def common_layout(*args):
    return rx.container(
        navbar(),
        *args,
        size="4",
    )
