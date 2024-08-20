# Front-end File Configuration

The front-end of app_name is mainly handled by Vite and Vue, but there is some interation with Django for the production server. This file will cover the general flow of requests and files in the Development and Production environments.

## The Development Server

The Vite Development Server is a fast and dynamic environment designed so you can see the changes you make to frontend code on the fly. It is much more simple than the full production server, and is likely less secure and robust.

<details>
<summary> Relevant Files </summary>

````
web-app-base/

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
web-app-base/
├── index.html
├── package.json
├── vite.config.js
└── staticfiles/
└── conf/
    ├── app_name-nginx.conf
└── src/
    ├── App.vue
    ├── main.js
    └── styles/
        ├── base.scss
└── django_apps/
    ├── manage.py
    └── main
        ├── urls.py
        └── views/
            ├── views.py
    └── app_name/
        ├── settings.py
        ├── urls.py
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

2. Django takes all files from the `/vite_build` directory as well as any files in `/static` directories in the apps (as defined by the **INSTALLED_APPS** section of [settings.py](../django_apps/app_name/settings.py)) and copies them to the `/staticfiles` directory.
    - Django automatically looks in the `/static` directory of each app
    - It looks in `/vite_build` because that is specified in the **STATICFILES_DIRS** setting. This setting should always include the **outDir** directory from [vite.config.js](../vite.config.js)
    - Static files are collected to the directory specified by the **STATIC_ROOT** setting in **settings.py**, which is `/staticfiles` in this case.

### exec gunicorn django_apps.app_name.wsgi:application --bind 0.0.0.0:8080 --workers 3

3. Gunicorn starts the server and web application at port `8080`
4. When you go to http://localhost:8080/ or any variation thereof, Django checks for the URL pattern in [urls.py](../django_apps/app_name/urls.py)
    - Django defines url patterns as anything after the port number and "/"
    - In the case of http://localhost:8080/, the pattern it looks for is simply "" since there is nothing after the slash.
5. If **urls.py** contains the URL pattern, it will redirect Django to the proper View in [views.py](../django_apps/main/views/views.py)
    - In the case of URL pattern "", Django goes to the "Homepage" view
6. The View specifies the HTML template to render for the page
    - IN the case of the "Homepage" view, `index.html` is requested
7. The webpage looks for an HTML file with a matching name in every directory listed in the **TEMPLATES** section of [settings.py](../django_apps/app_name/settings.py)
8. The webpage renders the HTML and sends a request to Nginx for any Javascript or CSS files that the HTML calls for
9. Nginx gives the webpage the static files from its static folder (which we make into a live copy of `/staticfiles` in [docker-compose.yml](../docker-compose.yml))

</details>

## Detailed File Descriptions

<details>
<summary>App.vue</summary>

Found [here](../src/App.vue)

Vue files are essentially all the code for one part of a web page packaged into one file. It includes three sections:
- An HTML section for the actual content of the piece
- A JS section that includes all the relevant functions
- A CSS section for specific styling that differs from the main style sheet

</details>
<details>
<summary>settings.py</summary>

Declares all settings Django will use for the project.

### Static Files
- Sets the Base Directory to be two directories higher than wherever settings.py is (in this case, `/web-app-base`)
- Sets all static files to be placed at the `/static/` url in the website
- Tells Django to look for built or static files in the `/vite_build` directory when `collectstatic` is run
- Tells Django to collect static files in the `/staticfiles` directory

### Installed Apps
- Specifies what modules Django counts as an "application" and can be referenced internally

### Middleware
- Declares which frameworks Django should use to process requests

### Other
- Tells Django to work with WSGI using the app set up by [wsgi.py](../django_apps/app_name/wsgi.py)
- Tells Django that URL patterns are defined in the [urls.py](../django_apps/app_name/urls.py) file
- Tells Django to look for HTML template files in `/web-app-base` and any directory called `/templates` within anything defined as an Installed App
- Sets language, time zone, etc.
- Imports all settings from local_settings.py
</details>
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
<summary> package.json </summary>

This file specifies what packages and software should be included in the frontend code.

The second section, titled `scripts`, maps the commands `npm run build` and `npm run dev` to their Vite equivalents.

</details>
<details>
<summary>urls.py</summary>

Found [here](../django_apps/app_name/urls.py)

This file tells Django what Views to run when an HTP or HTTP request comes in. 

Since we have multiple "applications" (Main, Owners, etc.), we give each app its own `urls.py` and then import them into the main file as needed and based on a url prefix (for example, "/owners/" or "").

Each URL path has three parts
- The text pattern in the URL
- The view to run from [views.py](../django_apps/main/views/views.py)
- The name of the page

</details>
<details>
<summary>views.py</summary>

The most common view file is located [here](../django_apps/main/views/views.py)

This file tells Django what HTML template to associate with each URL pattern (if necessary).

Each View is in the format of a python function. Each function:
- Takes a web request as an argument
- Returns the rendered request and HTML file

You can add more code to have each view do additional back-end work before rendering the page.
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

