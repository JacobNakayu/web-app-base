# Web App Base

>[!WARNING]
>This is a pretty early iteration that I made while I was still teaching myself how to code. The project that I based this off of has developed a lot, and I haven't yet gone back and fixed some of the wonky configurations yet, so it might need some tweaking.

## Summary
Basic setup for a web application. The goal is to have a ready-to-go base of file structures and config files that can be customized into a full app.

This runs in a docker container, so all development can happen locally and in a perfect simulation of the real environment.

Made up of two sections:
- A front-end built using Vite and Vue
  - Handles user experience and navigation
- A back-end built using Django and Postgresql
  - Handles database storage and queries, Nessus scan processing, and ServiceNow ticket creation

## Documentation
All documentation for this project is written as markdown files in the [documentation](./documentation/) directory, including instructions for [setting up a local instance](./documentation/01-first-setup.md).

## Other Notes
- Once you have built it, you can access the frontend docker container itself by running this command in your terminal:
    ```
    docker exec -it <WHATEVER-YOU-NAMED-THE-CONTAINER>-1 bash
    ```
    - This will give you access to the actual file structure in the docker for debug purposes.
    - Replace "web" with "db" if you need to access the database container.

- You'll have to run `npm install` in the local project directory after building for the first time before the Dev instance will work

- Also if you rename any directories, be sure to search and replace for all those terms in the code
