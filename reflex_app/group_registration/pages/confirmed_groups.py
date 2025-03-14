import reflex as rx

from ..components.groups_viewer import groups_viewer

from ..db.group import get_confirmed_groups

from ..layouts.common import common_layout


class ConfirmedGroupsState(rx.State):
    groups: list[dict] = []

    def fetch_groups(self):
        self.groups = get_confirmed_groups()


@rx.page(route="/groups", on_load=ConfirmedGroupsState.fetch_groups)
def confirmed_groups() -> rx.Component:
    return common_layout(
        rx.center(
            rx.cond(
                ConfirmedGroupsState.groups,
                rx.vstack(
                    rx.heading("Confirmed Groups", size="4"),
                    groups_viewer(ConfirmedGroupsState.groups),
                    width="60%",
                ),
                rx.heading("There are no confirmed groups yet!"),
            ),
        ),
    )
