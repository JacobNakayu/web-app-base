# Environment Configuration
app_name operates within Docker containers, has a postgresql database, and uses Nginx, WSGI, and Gunicorn to serve files to the production server.

I would recommend having the files open in a side tab so you can follow along with the descriptions.

--- 

<details>
<summary>Docker Containers</summary>

## Summary
These files define the modular "containers" that app_name runs in, allowing everybody with a local instance of app_name to have the same environment.

## Relevant Files

<details>
<summary>Dockerfile</summary>

[Found here](../Dockerfile)

Builds the Docker image in three stages:
- **Stage 1: Building the Application**
    1. Pulls in Node v22
        - Software that processes and runs Javascript
    2. Creates `web-app-base/` and makes it the root directory in the container
    3. Copies all files from your local `web-app-base/` to the one in the container
    4. Installs the packages Node.js needs for processing Javascript
    5. Runs the production version of the build command from [package.json](../package.json)
        - Build commands are discussed [here](./04-frontend-configuration.md)
- **Stage 2: Configuring Nginx**
    1. Pulls in Nginx
        - Serves static files and works as a middleman to pass requests from clients to Gunicorn
    2. Deletes all default configuration files that Nginx comes with
    3. Copies all files processed by the build command to a directory that Nginx can access
    4. Loads the custom configuration files like [app_name-nginx.config](../conf/app_name-nginx.conf)
- **Stage 3: Setting up Django and Gunicorn**
    1. Pulls in Django
        - A web framework that lets you use Python to make a backend for your website
    2. Sets the working directory to `web-app-base/` so Docker knows where to set things up
    3. Stops Python from writing .pyc files to save space
    4. Tells Python to log output to the terminal
    5. Copies the docker-entrypoint.sh file to the container so Docker can run the code
    6. Copies the requirements file and installs the listed packages
    7. Copies the Python application code from Stage 1 so Python can access it
    8. Copies the built files directory from Stage 1 so Django can access them
    9. Installs Gunicorn
        - HTTP server software that takes requests from Nginx, runs them through the Python code, and returns the response
    10. Opens ports to the network for Nginx and Gunicorn to use
    11. Runs the code in [docker-entrypoint.sh](../docker-entrypoint.sh)
</details>
<details>
<summary>docker-entrypoint.sh</summary>

[Found here](../docker-entrypoint.sh)

Runs a series of Bash commands to finish starting the server:
1. Grants the ability to exit on error
2. Moves to the `/django_apps` directory where manage.py is located
3. Collects static files and places them in the `staticfiles/` directory
    - Looks in the `static/` folder in each application (main, owners, app_name, users)
    - Looks in any directories specified by **STATICFILES_DIRS** in [settings.py](../django_apps/app_name/settings.py)
4. Generates migration files
    - Looks for any changes to the models.py files in each app and generates code to edit the database accordingly
5. Applies new migration files to the database
6. Starts Gunicorn
    - Jumps out of docker-entrypoint.sh and into gunicorn
    - Targets the django_apps application and starts it
    - Tells Gunicorn to bind to all available network interfaces (`0.0.0.0`) on port `8080`, so we can access it from outside the container
    - Specifies the number of "workers" Gunicorn will use to proces multiple requests at a time
</details>
<details>
<summary>docker-compose.yml</summary>

[Found here](../docker-compose.yml)

Tells Docker to isolate services in seperate containers and specifies ports and directories for those containers to use.

- Web Container
    - Uses the Dockerfile located in the current directory
    - Mounts (creates a live connection between) the local files and directories in the container:
        - `/django_apps`: Contains the python code that django needs to run
        - `/staticfiles`: Contains the collected buit files that Nginx needs to pass to the webpage
    - Equates (maps) port `8080` on the host computer to `8080` in the container
    - Tells the container to look for python code in `/itsecurity-app_name`
    - Ensures that **db** is running before starting **web**
    - Loads environment variables from .env
- Nginx Container
    - Uses the latest **nginx** image from Docker Hub
    - Mounts `/conf` to `/etc/nginx/conf.d` in the container to track configuration files
    - Mounts `web-app-base/staticfiles` to the Nginx HTML directory
    - Maps port `80` on the host to `80` in the container so we can access the Nginx server
    - Ensures **web** starts before starting **nginx**
- DB Container
    - Uses the latest **postgres** image from Docker Hub
    - Sets the container to automatically restart if it fails
    - Loads environment variables from .env
    - Mounts a volume of data called `db_data_app_name` to store PostgreSQL data
    - Maps port `5432` on the host to `5432` in the container so we can access the PostgreSQL database.
- db_data_app_name Volume
    - Creates a data volume so our database persists over container restarts and recreations.
</details>
</details>

---

<details>
<summary>Server Configuration</summary>

## Summary
These files configure the software and services that allow files and requests to pass between the app_name application code, web server, and client.

## Relevant Files
- All files from the **Docker Containers** section
<details>
<summary>app_name-nginx.conf</summary>

[Located here](../conf/app_name-nginx.conf)

Sets up an Nginx web server to handle requests for app_name.

- Server block
    - Tells Nginx to listen on port 80
    - Specifies that this configuration will handle requests for the server_name or ip address given
- location /static/: Defines how to handle static file requests
    - Uses an alias to map the URL path `/static/` to the local Nginx HTMl directory (like in docker-compose.yml)
- location /: Defines how to handle requests to the root URL and other paths
    - Tries to seve the requested file (`$uri`) or directory (`$uri/`), defaulting to index.html if nothing is there.
- location /api/: Handles requests starting with `/api/` by proxying them to the Django backend
    - Passes requests to the Django application in the Web container at port 8080
    - Pases the original `Host` header from the client to the backend
    - Passes the client's IP address to the backend
    - Adds the client's IP address to the proper headers for passing through proxy services
    - Lets the backend know if we're using HTTP or HTTPS
</details>
<details>
<summary>wsgi.py</summary>

[Located here](../django_apps/app_name/wsgi.py)

Sets up WSGI, which allows Gunicorn to interact with the Python project.

- Imports necessary modules from Python
- Tells Django to use the settings in [settings.py](../django_apps/app_name/settings.py)
- Creates the application that lets the WSGI server and Django pass requests and responses.

There is also this line in [settings.py](../django_apps/app_name/settings.py) that links the WSGI app to Django:

```
WSGI_APPLICATION = "app_name.wsgi.application"
```
</details>
</details>

---

<details>
<summary>Database Configuration</summary>

## Summary
These files configure the PosgreSQL database that app_name uses to track devices, vulnerabilities, etc.

With the exception of docker-compose.yml, all files in this section are generated [during setup](./01-first-setup.md) and will not be found in the github.

## Relevant Files

[docker-compose.yml](../docker-compose.yml)

<details>
<summary>init.sql</summary>

Called by [docker-compose.yml](../docker-compose.yml) during creation of the db container to run a few lines of SQL at the start.

- Creates a database user and assigns them a password
- Creates the database itself
- Gives the user it just created permission to do anything with the database
</details>
<details>
<summary>.env</summary>

Specifies "environment variables" that will be used across the Django application

- Sets the username and password the application will use to log in to the database
    - This should be the same as the values set in init.sql
- Defines the hostname where the PosgreSQL database server is located
- Sets the name of the database
    - This should be the same as the value in init.sql
- Specifies the hostname for the database
    - This should be the same as the database docker container **name** in [docker-compose.yml](../docker-compose.yml)
- Sets the port on which the PostgreSQL database is listening
    - This should be the same as the database docker container **port value** in [docker-compose.yml](../docker-compose.yml)
- Sets the directory that Django will look for python code (application code, packages, etc.)
    - This should be the same as the web docker container **environment variable** value in [docker-compose.yml](../docker-compose.yml)

</details>
<details>
<summary>local_settings.py</summary>

Extends [settings.py](../django_apps/app_name/settings.py). Mostly, it's a different file to make these settings easier to find since they either have to be set up on each machine or are secret and shouldn't be on the github.

- Sets the Secret Key that will be used for generating session tokens, encryption, etc.
- Allows the app to display full error messages ("debug mode")
- Lists all ip addresses allowed to access the web app
- Sets credentials and urls necessary for accessing the Nessus API
- Includes "toggle settings" to enable/disable certain features with local development
- Sets credentials and urls necessary for accessing ServiceNow
- Tells Django how to configure the database by referencing the .env file.
</details>
</details>


