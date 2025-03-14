import reflex as rx

from ..components.single_group import single_group

from ..db.group import get_group

from ..layouts.common import common_layout


class GroupState(rx.State):
    group: list[dict] = []

    def fetch_group(self):
        self.group = get_group(self.group_id)


@rx.page(route="/group/[group_id]", on_load=GroupState.fetch_group)
def group() -> rx.Component:
    return common_layout(
        rx.center(
            rx.vstack(
                rx.heading(GroupState.group_id, size="4"),  # type: ignore
                single_group(GroupState.group),
                width="60%",
            ),
        ),
    )
