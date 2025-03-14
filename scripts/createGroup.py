#!/usr/bin/env python3

import psycopg2
import base64
import os

N_BYTES = 32

conn = psycopg2.connect(
    database="groups",
    host="localhost",
    user="groups_user",
    password=os.getenv("DB_PASSWORD", "dev_password"),
    port="5432",
)
cursor = conn.cursor()

group_elements = []


def terminate_and_exit():
    conn.commit()
    cursor.close()
    conn.close()
    exit(0)


def create_group():
    cursor.execute("select nextval('group_id')")
    r = cursor.fetchone()

    if not r:
        print("ERROR: Failed to retrieve group_id")
        terminate_and_exit()

    group_id = f"G-{r[0]:02}"  # type: ignore

    for element in group_elements:
        cursor.execute(
            "insert into group_element (group_id, email, github, invite_id, invite_status) values (%s, %s, %s, %s, %s);",
            (
                group_id,
                element["email"],
                element["github"],
                base64.urlsafe_b64encode(os.urandom(N_BYTES)).decode("utf-8"),
                True,
            ),
        )

    terminate_and_exit()


if __name__ == "__main__":
    counter = 0
    while True:
        counter += 1
        email = input(f"Element nº{counter} email (leave empty to terminate): ")

        if not email:
            break

        github = input(f"Element nº{counter} GitHub username: ")

        group_elements.append(
            {
                "email": email,
                "github": github,
            }
        )

    if not group_elements:
        print("Empty group elements. Nothing to do.")
        terminate_and_exit()

    create_group()
    terminate_and_exit()
