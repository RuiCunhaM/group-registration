#!/usr/bin/env python3

import argparse
import psycopg2
import csv
import os

conn = psycopg2.connect(
    database="groups",
    host="localhost",
    user="groups_user",
    password=os.getenv("DB_PASSWORD", "dev_password"),
    port="5432",
)
cursor = conn.cursor()


def terminate():
    conn.commit()
    cursor.close()
    conn.close()


def insert_email(email):
    try:
        cursor.execute(
            "insert into valid_email (email) values (%s) on conflict (email) do nothing;",
            (email,),
        )
    except:
        print(f'Failed to insert email: "{email}"')


def load_file(file):
    with open(file) as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            insert_email(line[0])
        print("Finished loading emails")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file")
    parser.add_argument("-e", "--email")
    args = parser.parse_args()

    if args.file:
        load_file(args.file)
        terminate()
    elif args.email:
        insert_email(args.email)
        terminate()
    else:
        terminate()
        exit(1)
