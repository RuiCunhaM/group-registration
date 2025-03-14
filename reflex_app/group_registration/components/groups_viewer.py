import reflex as rx


def groups_viewer(groups: list[dict]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Group"),
                rx.table.column_header_cell("Email"),
                rx.table.column_header_cell("Invite Status"),
            ),
        ),
        rx.table.body(
            rx.foreach(
                groups,
                lambda x: rx.table.row(
                    rx.table.cell(
                        rx.link(
                            x["group_id"],
                            href=f"/group/{x["group_id"]}",
                        ),
                    ),
                    rx.table.cell(x["email"]),
                    rx.table.cell(
                        rx.cond(
                            x["invite_status"],
                            rx.icon("check"),
                            rx.icon("hourglass"),
                        ),
                    ),
                ),
            )
        ),
        variant="surface",
        width="100%",
        size="1",
    )
