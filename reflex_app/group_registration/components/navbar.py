import os
import reflex as rx

from .dark_mode_toggle import dark_mode_toggle

SITE_NAME = os.getenv("SITE_NAME", "SITE NAME")


def site_name() -> rx.Component:
    return rx.heading(
        SITE_NAME,
        size="9",
        weight="bold",
    )


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.button(
        rx.color_mode_cond(
            rx.text(text, color="black", size="4"),
            rx.text(text, color="white", size="4"),
        ),
        on_click=rx.redirect(url),
        variant="ghost",
        color_scheme="gray",
    )


def github_link() -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.color_mode_cond(
                rx.text("@ruicunham", color="black", size="3"),
                rx.text("@ruicunham", color="white", size="3"),
            ),
            rx.color_mode_cond(
                rx.icon("github", color="black", size=30),
                rx.icon("github", color="white", size=30),
            ),
            align="center",
            justify="center",
        ),
        on_click=rx.redirect("https://www.github.com/ruicunham"),
        variant="ghost",
        color_scheme="gray",
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                site_name(),
                rx.hstack(
                    navbar_link(
                        "Main Page",
                        "/",
                    ),
                    navbar_link(
                        "Groups",
                        "/groups",
                    ),
                    navbar_link(
                        "Pending Groups",
                        "/pending-groups",
                    ),
                    navbar_link(
                        "Register New Group",
                        "/registration",
                    ),
                    align_items="center",
                    justify="between",
                    spacing="5",
                ),
                rx.spacer(),
                rx.hstack(
                    github_link(),
                    dark_mode_toggle(),
                    align_items="center",
                    justify="between",
                ),
                align_items="center",
                justify="between",
                spacing="5",
            )
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                site_name(),
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", size=30)),
                    rx.menu.content(
                        rx.menu.item(
                            "Main Page",
                            on_select=rx.redirect("/"),
                        ),
                        rx.menu.item(
                            "Groups",
                            on_select=rx.redirect("/groups"),
                        ),
                        rx.menu.item(
                            "Pending Groups",
                            on_select=rx.redirect("/pending-groups"),
                        ),
                        rx.menu.item(
                            "Register New Group",
                            on_select=rx.redirect("/registration"),
                        ),
                        github_link(),
                        dark_mode_toggle(),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        padding="2em",
        width="100%",
    )
