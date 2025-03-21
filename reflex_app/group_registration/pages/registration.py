import reflex as rx
import requests
import base64
import os

from ..db.group import (
    create_pending_group,
    is_email_valid,
    is_email_registered,
    is_github_registered,
)

from ..layouts.common import common_layout

from ..services.email import send_email

N_ELEMENTS = int(os.getenv("N_ELEMENTS", 3))
SITE_NAME = os.getenv("SITE_NAME", "SITE NAME")
DOMAIN = os.getenv("DOMAIN", "DOMAIN")

# NOTE: This is mostlikely overkill
N_BYTES = 32


class RegistrationState(rx.State):
    loading = False
    error_dialog = False
    errors: list[str] = []

    def open_dialog(self):
        self.error_dialog = True

    def close_dialog(self):
        self.error_dialog = False

    def show_error(self):
        self.open_dialog()

    @rx.event(background=True)
    async def handle_submit(self, form_data: dict):
        async with self:
            self.loading = True
            self.errors.clear()

        emails = set()
        githubs = set()
        errors = []

        for i in range(N_ELEMENTS):
            emails.add(form_data[f"email_{i}"])
            githubs.add(form_data[f"github_{i}"])

        if len(emails) != N_ELEMENTS:
            errors.append("No duplicated emails allowed.")

        if len(githubs) != N_ELEMENTS:
            errors.append("No duplicated GitHub handlers allowed.")

        for email in emails:
            if not is_email_valid(email):
                errors.append(f"{email} is not an authorized email.")
                continue

            if is_email_registered(email):
                errors.append(f"{email} is already registered.")

        for github in githubs:
            response = requests.get(f"https://github.com/{github}")

            if response.status_code != 200:
                errors.append(f"{github} is invalid.")
                continue

            if is_github_registered(github):
                errors.append(f"{github} is already registered.")

        if len(errors):
            async with self:
                self.errors = errors
                self.loading = False
                self.show_error()
            return

        members = []

        for i in range(N_ELEMENTS):
            members.append(
                {
                    "email": form_data[f"email_{i}"],
                    "github": form_data[f"github_{i}"],
                    "invite_id": base64.urlsafe_b64encode(os.urandom(N_BYTES)).decode(
                        "utf-8"
                    ),
                    "invite_status": False,
                }
            )

        group_id = create_pending_group(members)

        for member in members:
            send_email(
                f"{SITE_NAME} group invitation",
                member["email"],
                f"You were invited to a group in {SITE_NAME}. Open https://{DOMAIN}/invite?invite_id={member["invite_id"]} to either accept or reject your invite.",
            )

        async with self:
            self.loading = False

        return rx.redirect(f"/group/{group_id}")


def email_and_github_form(index) -> rx.Component:
    return rx.table.row(
        rx.table.cell(
            rx.input(
                placeholder="Email",
                name=f"email_{index}",
                required=True,
                type="email",
            ),
        ),
        rx.table.cell(
            rx.input(
                placeholder="GitHub",
                name=f"github_{index}",
                required=True,
            ),
        ),
    )


def form() -> rx.Component:
    return rx.vstack(
        rx.heading("Register Group", size="4"),
        rx.form(
            rx.vstack(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Email"),
                            rx.table.column_header_cell("GitHub"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            list(range(N_ELEMENTS)),
                            lambda x: email_and_github_form(x),
                        )
                    ),
                    width="100%",
                    size="1",
                    variant="surface",
                ),
                rx.cond(
                    RegistrationState.loading,
                    rx.button(
                        rx.spinner(),
                        color_scheme="gray",
                        disabled=True,
                    ),
                    rx.button(
                        rx.text("Register"),
                        type="submit",
                        color_scheme="gray",
                    ),
                ),
                align="end",
            ),
            on_submit=RegistrationState.handle_submit,
            reset_on_submit=False,
        ),
        rx.cond(
            RegistrationState.errors,
            rx.vstack(
                rx.foreach(
                    RegistrationState.errors,
                    lambda x: rx.text(x, color_scheme="red"),
                )
            ),
        ),
        width="60%",
    )


@rx.page(route="/registration")
def registration() -> rx.Component:
    return common_layout(
        rx.dialog.root(
            rx.dialog.content(
                rx.flex(
                    rx.text("Errors Found!"),
                    rx.button(
                        "Close",
                        on_click=RegistrationState.close_dialog,
                        color_scheme="gray",
                    ),
                    direction="column",
                    spacing="3",
                ),
            ),
            open=RegistrationState.error_dialog,
        ),
        rx.center(
            form(),
        ),
    )
