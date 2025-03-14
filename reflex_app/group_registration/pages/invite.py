import reflex as rx

from ..components.single_group import single_group

from ..db.group import get_group_by_invite_id, accept_invite, reject_invite

from ..layouts.common import common_layout


class InviteState(rx.State):
    invite_id: str = ""
    tmp_group_id: str = ""
    group: list[dict] = []

    def fetch_invite(self):
        self.invite_id = self.router.page.params.get("invite_id", "")

        if not self.invite_id:
            return rx.redirect("/groups")

        self.group = get_group_by_invite_id(self.invite_id)
        self.tmp_group_id = self.group[0]["group_id"]

    @rx.event
    def reject_invite(self):
        reject_invite(self.invite_id)
        return rx.redirect("/groups")

    @rx.event
    def accept_invite(self):
        group_id = accept_invite(self.invite_id)
        return rx.redirect(f"/group/{group_id}")


def reject_button() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.button(
                "Reject",
                color_scheme="red",
            ),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Reject Invite"),
            rx.alert_dialog.description(
                "Are you sure you want to reject this invite?",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button(
                        "Cancel",
                        color_scheme="gray",
                    ),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Reject",
                        color_scheme="red",
                        on_click=InviteState.reject_invite,
                    ),
                ),
                spacing="3",
            ),
        ),
    )


def options() -> rx.Component:
    return rx.hstack(
        reject_button(),
        rx.button(
            "Accept",
            color_scheme="grass",
            on_click=InviteState.accept_invite,
        ),
        justify="end",
        width="100%",
    )


@rx.page(route="/invite", on_load=InviteState.fetch_invite)
def invite() -> rx.Component:
    return common_layout(
        rx.center(
            rx.vstack(
                rx.heading(f"Invite - {InviteState.tmp_group_id}", size="4"),
                single_group(InviteState.group),
                options(),
                width="60%",
            ),
        ),
    )
