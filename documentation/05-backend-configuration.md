### exec gunicorn steesh_app.steesh.wsgi:application --bind 0.0.0.0:8080 --workers 3

3. Gunicorn starts the server and web application at port `8080`
4. When you go to http://localhost:8080/ or any variation thereof, Django checks for the URL pattern in [urls.py](../steesh_app/steesh/urls.py)
    - Django defines url patterns as anything after the port number and "/"
    - In the case of http://localhost:8080/, the pattern it looks for is simply "" since there is nothing after the slash.
5. If **urls.py** contains the URL pattern, it will redirect Django to the proper View in [views.py](../steesh_app/main/views/views.py)
    - In the case of URL pattern "", Django goes to the "Homepage" view
6. The View specifies the HTML template to render for the page
    - IN the case of the "Homepage" view, `index.html` is requested
7. The webpage looks for an HTML file with a matching name in every directory listed in the **TEMPLATES** section of [settings.py](../steesh_app/steesh/settings.py)
8. The webpage renders the HTML and sends a request to Nginx for any Javascript or CSS files that the HTML calls for
9. Nginx gives the webpage the static files from its static folder (which we make into a live copy of `/staticfiles` in [docker-compose.yml](../docker-compose.yml))

<summary>urls.py</summary>

Found [here](../steesh_app/steesh/urls.py)

This file tells Django what Views or Requests to run when an HTTP or HTTPS request comes in. Used mainly for the back-end API and SQL requests since we're using Vue-Router for the front-end.

Since we have multiple "applications" (Main, Owners, etc.), we give each app its own `urls.py` and then import them into the main file as needed and based on a url prefix (for example, "/owners/" or "").

Each URL path has three parts
- The text pattern in the URL
- The view to run from [views.py](../steesh_app/main/views/views.py)
- The name of the page

</details>
<details>
<summary>views.py</summary>

The most common view file is located [here](../steesh_app/main/views/views.py)

This file tells Django what HTML template to associate with each URL pattern (if necessary).

Each View is in the format of a python function. Each function:
- Takes a web request as an argument
- Returns the rendered request and HTML file

You can add more code to have each view do additional back-end work before rendering the page.
</details>