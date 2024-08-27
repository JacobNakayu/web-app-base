# Front-end File Configuration

The front-end of Steesh is mainly handled by Vite and Vue, but there is some interation with Django for the production server. This file will cover the general flow of requests and files in the Development and Production environments.

## The Development Server

The Vite Development Server is a fast and dynamic environment designed so you can see the changes you make to frontend code on the fly. It is much more simple than the full production server, and is likely less secure and robust.

<details>
<summary> Relevant Files </summary>

````
it-security-steesh/

├── index.html

├── package.json

├── vite.config.js

└── src/

    ├── App.vue

    ├── main.js

    └── styles/

        ├── base.scss

````
</details>
<details>
<summary> How it Works </summary>

### npm run dev
This command is an alias for `vite --mode development`, as set in [package.json](../package.json)

1. Vite loads [index.html](../index.html)
    - index.html is the Entrypoint file specified under the `input:` section of [vite.config.js](../vite.config.js)
2. **index.html** calls [main.js](../src/main.js) inside a `<div>` with `id="app"`
3. **main.js** imports the code from [App.vue](../src/App.vue) and the general styling from [base.scss](../src/styles/base.scss)
4. **main.js** mounts all the code from **App.vue** to any sections in **index.html** with `id="app"`
    - **App.vue** is essentially just a combination of html, js, and css that defines a single piece of the webpage
5. Vite makes the newly built webpage available at `http://localhost:5173`
    - Since Vite is dynamically rendering the page, any changes made to any of the relevant .js, .html, .css, or .vue files is immediately implemented once you save the file.
</details>

## The Production Server

The Production Server has the full application, including the frontend, backend, database, integration with Nginx, and so forth. It is more robust and has a few more steps that need to happen to implement changes.

<details>
<summary> Relevant Files </summary>

````
it-security-steesh/
├── index.html
├── package.json
├── vite.config.js
└── staticfiles/
└── conf/
    ├── nginx.conf
└── src/
    ├── App.vue
    ├── main.js
    └── styles/
        ├── base.scss
    └── router
        ├── router.js
└── steesh_app/
    ├── manage.py
    └── steesh/
        ├── settings.py
        ├── wsgi.py
└── vite_build
````
</details>
<details>
<summary> How it Works </summary>

### npm run build

This command is an alias for `vite build --mode production`, as set in [package.json](../package.json)

1. Vite takes [index.html](../index.html) and all files called therein, processes them, and outputs the "built" code to files in the `/vite_build` directory called `index.html`, `js/index.js` and `assets/index.css`
    - **index.html** is set as the Entrypoint file using the `input:` setting in [vite.config.js](../vite.config.js)
    - The only difference between the built and unbuilt **index.html** files is that the filepaths are changed to reference the other built files instead of the originals in the [/src](../src/) directory
    - The built .js and .css files are named and placed using the patterns specified in the `output:` section of **vite.config.js**

### manage.py collectstatic

2. Django takes all files from `/static` directories in the apps (as defined by the **INSTALLED_APPS** section of [settings.py](../steesh_app/steesh/settings.py)) and copies them to the `/staticfiles` directory.
    - Django automatically looks in the `/static` directory of each app
    - You can specify extra directories to look for static files in by using the **STATICFILES_DIRS** settings in **settings.py**. For example, if you want to have a directory with all the images and logos you use.
    - Static files are collected to the directory specified by the **STATIC_ROOT** setting in **settings.py**, which is `/staticfiles` in this case.

### exec gunicorn steesh_app.steesh.wsgi:application --bind 0.0.0.0:8080 --workers 3

3. Gunicorn starts the server and web application, binding the Django back-end to port `8080`.
4. With the server started, Nginx begins listening on Port 80 (as specified in [nginx.conf](../conf/nginx.conf) and [docker-compose.yml](../docker-compose.yml))
    - Nginx processes the front-end requests for Vite and Vue and sends any back-end requests to Gunicorn and WSGI for the Django application
5. Vite serves [index.html](../index.html) as the entrypoint (as specified in [vite.config.js](../vite.config.js))
    - **index.html** calls for [main.js](../src/main.js), which calls for [base.scss](../src/styles/base.scss) and [App.Vue](../src/App.vue) to form the baseline of the website
6. When someone enters the website or changes the URL they are at, Nginx checks [router.js](../src/router/router.js) for a matching URL pattern and serves the appropriate Vue file.

</details>

## Detailed File Descriptions

<details>
<summary>App.vue</summary>

Found [here](../src/App.vue)

Vue files are essentially all the code for one part of a web page packaged into one file. It includes three sections:
- An HTML section for the actual content of the piece
- A JS section that includes all the relevant functions
- A CSS section for specific styling that differs from the main style sheet

App.vue specifically serves as the base view of the application since it is the one mounted to [index.html](../index.html) through [main.js](../src/main.js).
- App.vue contains the navigation menu as well as a section where Views will be rendered.

</details>
<details>
<summary>manage.py</summary>

Found [here](../steesh_app/manage.py)

I don't really understand how exactly this file works, but it's what lets you run commands like `collectstatic` to get the static files and `shell` to access the CLI directly.

</details>
<details>
<summary>nginx.conf</summary>

[Located here](../conf/nginx.conf)

Sets up an Nginx web server to handle requests and front-end for Steesh.

- Establishes there will be 1 "worker"
- Sets each worker to handle up to 1024 connections at once
- http block (how the server handles HTTP requests)
    - Gives Nginx a list of file formats (MIME types) that it will need to know how to process
    - Sets the default file type for Nginx to process a file as if it doesn't match any other MIME type
    - Sets where access and error logs will be written
    - Enables file transmission so Nginx can send files directly from the disk to the network
    - Tells Nginx to wait until it has a full packet of data and then send it immediately over TCP (nopush and nodelay)
    - Sets idle connections to close after 65 seconds
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
<summary> package.json </summary>

This file specifies what packages and software should be included in the frontend code.

The second section, titled `scripts`, maps the commands `npm run build` and `npm run dev` to their Vite equivalents.

</details>
<details>
<summary>router.js</summary>

Found [here](../src/router/router.js)

This file tells Vue how to map Vue files to URL patterns.

- Imports all relevant Vue files
- Associates URL patterns with Vue files
- Creates the Vue-Router instance and defines its properties
    - createWebHistory: Enables HTML5 history mode (navigation will happen without reloading the page)
    - import.meta.env.BASE_URL: Ensures that Vue generates urls based on the base URL of the site
    - routes: Gives the router the array of routes we defined earlier

</details>
<details>
<summary>settings.py</summary>

Declares all settings Django will use for the project.

### Static Files
- Sets the Base Directory to be two directories higher than wherever settings.py is (in this case, `/it-security-steesh`)
- Sets all static files to be placed at the `/static/` url in the website
- Tells Django to look for built or static files in the `/vite_build` directory when `collectstatic` is run
- Tells Django to collect static files in the `/staticfiles` directory

### Installed Apps
- Specifies what modules Django counts as an "application" and can be referenced internally

### Middleware
- Declares which frameworks Django should use to process requests

### Other
- Tells Django to work with WSGI using the app set up by [wsgi.py](../steesh_app/steesh/wsgi.py)
- Tells Django that URL patterns are defined in the [urls.py](../steesh_app/steesh/urls.py) file
- Tells Django to look for HTML template files in `/it-security-steesh` and any directory called `/templates` within anything defined as an Installed App
- Sets language, time zone, etc.
- Imports all settings from local_settings.py
</details>
<details>
<summary> vite.config.js </summary>

Found [here](../vite.config.js)

This file configures the custom settings for how Vite and Vue will interact with the project.

- Imports Vite and Vue
- Checks whether the server is running in **Production Mode**. 
    - If so, injects `/static/` at the beginning of every file path listed within the file specified at `input:` during build
    - Otherwise (if in **Dev Mode**), leaves `/static/` off
- Includes Vue
- Sets up a slot for a baseline style sheet (unused since currently, the main style sheet is imported in index.html)
- Specifies "build options"
    - Files built by Vite will be placed in the `vite_build` directory
    - The outDir directory will be emptied each time the production build command is run so there are no old straggler files
    - Sets the "entrypont" for the site (where Vite will start processing before including or jumping to other files)
    - Specifies how Vite should name files it outputs to the outDir directory once they're built

</details>

