# web-app-base

## Summary
Tool to bridge Nessus vulnerability scans and ServiceNow tickets (Replacement for Lecxe)

app_name runs in a docker container, so all development can happen locally and in a perfect simulation of the real environment.

app_name is made up of two sections:
- A front-end built using Vite and Vue
  - Handles user experience and navigation
- A back-end built using Django and Postgresql
  - Handles database storage and queries, Nessus scan processing, and ServiceNow ticket creation

## Documentation
All documentation for this project is written as markdown files in the [documentation](./documentation/) directory, including instructions for [setting up a local instance](./documentation/01-first-setup.md).

## Other Notes
- Once you have built it, you can access the frontend docker container itself by running this command in your terminal:
    ```
    docker exec -it web-app-base-web-1 bash
    ```
    - This will give you access to the actual file structure in the docker for debug purposes.
    - Replace "web" with "db" if you need to access the database container.
