import reflex as rx

from ..layouts.common import common_layout


@rx.page(route="/")
def index() -> rx.Component:
    try:
        with open("main_page.md") as file:
            return common_layout(
                rx.center(
                    rx.vstack(
                        rx.markdown(
                            file.read(),
                        )
                    )
                )
            )
    except FileNotFoundError:
        return common_layout()
