from .db_cursor import db_cursor

# NOTE: Perhaps in the future it is worth looking into the ORM features that Reflex provides.


def create_pending_group(members):
    with db_cursor() as cur:
        cur.execute("select nextval('tmp_group_id')")

        group_id = f"PG-{cur.fetchone()["nextval"]:02}"

        for member in members:
            cur.execute(
                """insert into group_member(group_id, email, github, invite_id, invite_status) 
                values (%s, %s, %s, %s, %s)""",
                (
                    group_id,
                    member["email"],
                    member["github"],
                    member["invite_id"],
                    member["invite_status"],
                ),
            )

        return group_id


def get_group(group_id):
    with db_cursor() as cur:
        cur.execute(
            """select group_id, email, github, invite_status 
            from group_member 
            where group_id = %s""",
            (group_id,),
        )
        return cur.fetchall()


def get_group_by_invite_id(invite_id):
    with db_cursor() as cur:
        cur.execute(
            """select group_id, email, github, invite_status 
            from group_member  
            where group_id = (select group_id from group_member where invite_id = %s)""",
            (invite_id,),
        )
        return cur.fetchall()


def get_confirmed_groups():
    with db_cursor() as cur:
        cur.execute(
            """select group_id, email, github, invite_status 
            from group_member 
            where group_id in (select group_id
                from group_member
                group by group_id
                having bool_and(invite_status))
            order by group_id"""
        )
        return cur.fetchall()


def get_pending_groups():
    with db_cursor() as cur:
        cur.execute(
            """select group_id, email, github, invite_status 
            from group_member 
            where group_id in (select group_id
                from group_member
                group by group_id
                having not bool_and(invite_status))
            order by group_id"""
        )
        return cur.fetchall()


def reject_invite(invite_id):
    with db_cursor() as cur:
        cur.execute(
            """select group_id, invite_status
            from group_member
            where invite_id = %s""",
            (invite_id,),
        )

        result = cur.fetchone()

        group_id = result["group_id"]
        invite_status = result["invite_status"]

        if group_id.startswith("G") or invite_status:
            return

        cur.execute(
            """delete         
            from group_member
            where group_id = %s""",
            (group_id,),
        )


def accept_invite(invite_id):
    with db_cursor() as cur:
        cur.execute(
            """select group_id
            from group_member
            where invite_id = %s""",
            (invite_id,),
        )

        group_id = cur.fetchone()["group_id"]

        if not group_id:
            return

        if group_id.startswith("G"):
            return group_id

        cur.execute(
            """update group_member 
            set invite_status = true 
            where invite_id = %s""",
            (invite_id,),
        )

        cur.execute(
            """select count (*) 
            from group_member 
            where group_id = %s and invite_status = false""",
            (group_id,),
        )

        if cur.fetchone()["count"] > 0:
            return group_id

        cur.execute("select nextval('group_id')")

        new_group_id = f"G-{cur.fetchone()["nextval"]:02}"

        cur.execute(
            """update group_member 
            set group_id = %s 
            where group_id = %s""",
            (
                new_group_id,
                group_id,
            ),
        )

        return new_group_id


def is_email_valid(email):
    with db_cursor() as cur:
        cur.execute(
            """select count (*) 
            from valid_email 
            where email = %s""",
            (email,),
        )
        return cur.fetchone()["count"] > 0


def is_email_registered(email):
    with db_cursor() as cur:
        cur.execute(
            """select count (*) 
            from group_member 
            where email = %s""",
            (email,),
        )
        return cur.fetchone()["count"] > 0


def is_github_registered(github):
    with db_cursor() as cur:
        cur.execute(
            """select count (*) 
            from group_member 
            where github = %s""",
            (github,),
        )
        return cur.fetchone()["count"] > 0


def get_pending_invites():
    with db_cursor() as cur:
        cur.execute(
            """select email, invite_id
            from group_member
            where invite_status = false"""
        )
        return cur.fetchall()
