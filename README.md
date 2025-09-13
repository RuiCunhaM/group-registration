# Group Registration Platform

A monorepo containing an application for registering students' work groups. Intended to be hosted by teachers, allowing their students to register their groups and provide their individual GitHub handlers.

### Why?/Use case

At the start of each semester, we ask hundreds of students across multiple classes to form their work groups and report their individual GitHub handlers. This information is required so we can later create proper GitHub organizations and group repositories for their practical assignments.

This plataform aims to provide a tool that streamlines this process.

##### Relevant features:

- Easy and containerized deployment with automatic SSL Certificate handling (thanks to [Caddy](https://caddyserver.com/)).
- Email invites using Gmail.
- Customizable group size.
- Restrict registration to authorized emails/students.
- Validation of GitHub handlers.
- Custom main page content using Markdown.

---

## Getting Started

> [!NOTE]
> These instructions assume you have a domain pointing to the server in which you will host this platform. Furthermore, it configures its own reverse proxy (Caddy), assuming this is the only web service running on the server.

1. Clone the repository

   ```
   git clone git@github.com:RuiCunhaM/group-registration.git
   ```

2. Create a `.env` file

   ```
   cp .env.example .env
   ```

3. Edit the `.env` file with the apropriate values

   - `DOMAIN`: The host domain
   - `SITE_NAME`: The platform title. We recommend a short acronym.
   - `MIN_ELEMENTS`: The minimum number of elements each group requires.
   - `MAX_ELEMENTS`: The maximum number of elements each group can have (Can be equal to `MIN_ELEMENTS`).
   - `DB_PASSWORD`: The DB password.
   - `GMAIL_USERNAME`: A Gmail handler from where to send the automatic emails.
   - `GMAIL_APP_PASSWORD`: The Gmail APP password for `GMAIL_USERNAME`. See [here](https://support.google.com/mail/answer/185833?hl=en) how to get one.

4. Edit the `main_page.md` file to customize your main page content with Markdown syntax.

> [!TIP]
> The Markdown support in this step is not perfect. If you want more control over your main page content, directly edit the Python source code at [index.py](./reflex_app/group_registration/pages/index.py).

5. Build and start the containers.

   ```
   docker compose up -d
   ```

6. The platform should now be accessible at the domain configured in Step 3.

7. At this stage, you need to add a list of emails authorized to register in the plataform. Refer to [Utility Scripts](#utility-scripts) to see how.

---

## Utility Scripts

You'll find some utility scripts with distinct purposes in the [`scripts`](./scripts) folder. Before using any of the scripts, first export the `DB_PASSWORD` variable:

```
export $(cat .env | grep DB_PASSWORD | tr -d '"')
```

#### Add authorized emails

If you have a file with one email per line:

```
./loadEmails.py -f <file>
```

To manually add a single email:

```
./loadEmails.py -e <email>
```

#### Manually add a group

Using this script, it is possible to manually add a group of any size. The group is immediately considered valid, and students are not required to accept any invitation.

```
./createGroup.py
```

The script guides you through the process.

#### Dump group information

Dump the information about the confirmed groups. Useful to export the data collected to other tools.

```
./dumpGroups.py
```

It will print information to the `stdin`. You should redirect it to a file.

---

## Privacy Concerns

> [!WARNING]
> In the current iteration, group members are completely public, including their academic emails and GitHub handlers! In the context we use this application, we do not consider it a problem, but please be aware of such behavior.

---

## Built with:

- [Python Reflex](https://reflex.dev/)
- [Caddy](https://caddyserver.com/)
- Docker
- PostgreSQL

---

## TODO (No particular order)

- [ ] Admin page (Should remove the need for utility scripts)

  - [ ] Login
  - [ ] Add authorized emails
  - [ ] Export groups info
  - [ ] Manually add group

- [ ] Cron job to resend emails

- [ ] `Go to bottom` and `Go to top` buttons for easier navigation

- [ ] Better backend async support (We don't have any real demand operation but should improve performance nevertheless)

- [ ] README improvements
