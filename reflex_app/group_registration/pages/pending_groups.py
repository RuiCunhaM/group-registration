import reflex as rx

from ..components.groups_viewer import groups_viewer

from ..db.group import get_pending_groups

from ..layouts.common import common_layout


class PendingGroupsState(rx.State):
    groups: list[dict] = []

    def fetch_groups(self):
        self.groups = get_pending_groups()


@rx.page(route="/pending-groups", on_load=PendingGroupsState.fetch_groups)
def pending_groups() -> rx.Component:
    return common_layout(
        rx.center(
            rx.cond(
                PendingGroupsState.groups,
                rx.vstack(
                    rx.heading("Pending Groups", size="4"),
                    groups_viewer(PendingGroupsState.groups),
                    width="60%",
                ),
                rx.heading("Currently, there are no pending groups."),
            ),
        ),
    )
