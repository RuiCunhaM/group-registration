import reflex as rx

from reflex.style import toggle_color_mode


def dark_mode_toggle() -> rx.Component:
    return rx.button(
        rx.color_mode_cond(
            rx.icon("sun", color="black", size=30),
            rx.icon("moon", color="white", size=30),
        ),
        on_click=toggle_color_mode,
        variant="ghost",
        color_scheme="gray",
    )
