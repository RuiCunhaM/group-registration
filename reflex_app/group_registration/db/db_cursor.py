import os
import psycopg2
import psycopg2.pool
import psycopg2.extras

from contextlib import contextmanager

dbpool = None


class DbPool:
    _dbpool: psycopg2.pool.ThreadedConnectionPool


async def init_dbpool():
    DbPool._dbpool = psycopg2.pool.ThreadedConnectionPool(
        5,
        5,
        host=os.getenv("DB_HOST", "localhost"),
        port="5432",
        dbname="groups",
        user="groups_user",
        password=os.getenv("DB_PASSWORD", "dev_password"),
    )


@contextmanager
def db_cursor():
    conn = DbPool._dbpool.getconn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            yield cur
            conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        DbPool._dbpool.putconn(conn)
