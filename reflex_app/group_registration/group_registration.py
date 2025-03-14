import reflex as rx

from .db.db_cursor import init_dbpool

app = rx.App()

app.register_lifespan_task(init_dbpool)
