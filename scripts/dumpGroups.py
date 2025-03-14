#!/usr/bin/env python3

import psycopg2
import os

conn = psycopg2.connect(
    database="groups",
    host="localhost",
    user="groups_user",
    password=os.getenv("DB_PASSWORD", "dev_password"),
    port="5432",
)
cursor = conn.cursor()


def terminate_and_exit():
    cursor.close()
    conn.close()
    exit(0)


def get_confirmed_groups():
    cursor.execute(
        """select group_id, email, github
        from group_element
        where group_id in (select group_id
                          from group_element
                          group by group_id
                          having bool_and(invite_status))
        order by group_id;"""
    )
    return cursor.fetchall()


def print_groups(groups):
    print("Group,Email,GitHub")
    for element in groups:
        print(f"{element[0]},{element[1]},{element[2]}")


if __name__ == "__main__":
    confirmed_groups = get_confirmed_groups()
    print_groups(confirmed_groups)
    terminate_and_exit()
