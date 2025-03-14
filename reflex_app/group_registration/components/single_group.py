import reflex as rx


def single_group(members: list[dict]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Email"),
                rx.table.column_header_cell("GitHub"),
                rx.table.column_header_cell("Invite Status"),
            ),
        ),
        rx.table.body(
            rx.foreach(
                members,
                lambda x: rx.table.row(
                    rx.table.cell(x["email"]),
                    rx.table.cell(x["github"]),
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
