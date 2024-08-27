# Setting Up Steesh

1. Ensure you have [Docker Desktop](https://docs.docker.com/desktop/install/linux-install/) or [Docker Engine](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) installed on your machine

2. Clone the repository on your machine
    ```
    git clone <SSH link from green Code button>
    ```
    
3. Create the following files:
    - it-secuirty-steesh/.env
        ```
        POSTGRES_PASSWORD=Your Database Password (no quotes)
        POSTGRES_USER=steesh_user
        POSTGRES_HOST=postgres-sheesh
        POSTGRES_DB=steesh
        DB_HOST=db
        DB_PORT=5432
        PYTHONPATH=/it-security-steesh
        ```
    - it-security-steesh/db_init/init.sql (you'll need to create the db_init directory as well)
        ```
        -- Creates the user and database the first time the Docker is built
        
        CREATE USER steesh_user WITH PASSWORD 'Your Database Password (in single quotes)';
        CREATE DATABASE steesh;
        GRANT ALL PRIVILEGES ON DATABASE steesh TO steesh_user;
        ```
    - it-security-steesh/steesh_app/steesh/local_settings.py
        ```
        from os import getenv
        
        SECRET_KEY = "Secret key generated in the next step"
        DEBUG = True
        ALLOWED_HOSTS = ["localhost", "127.0.0.1", "db"]
        
        # Nessus access settings
        NESSUS_ACCESS_KEY = "From Bitwarden"
        NESSUS_SECRET_KEY = "From Bitwarden"
        NESSUS_URL = "https://portscan02.usu.edu:8834"  # Full URL for nessus (including port!)
        
        # Local instance settings
        LOCAL_DB_INITIAL_RUN = True  # Set True only on initial local setup
        LOCAL_INSTANCE = True  # Set true only if developing on your own machine
        
        # ServiceNow
        SERVICENOW_BASE_URL = ""
        SERVICENOW_USERNAME = ""
        SERVICENOW_PASSWORD = ""
        
        # Setup for the database. Automatically pulls values from .env file. Defaults to second value if it can't.
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': getenv("POSTGRES_DB", 'steesh'),
                'USER': getenv("POSTGRES_USER", "steesh_user"),
                'PASSWORD': getenv("POSTGRES_PASSWORD", "DB Password if you want to hard code"),
                'HOST': getenv('DB_HOST', "db"),
                'PORT': getenv('DB_PORT', "5432"),
            }
        }
        ```
4. Set a database password in .env and init.sql

5. Generate a Django Secret Key using the following command and place it in steesh_app/steesh/local_settings.py
    ```
    python3 -c 'import secrets; print(secrets.token_hex(100))'
    ```

6. Log into your USU Bitwarden vaults and place the Nessus API keys into local_settings.py
    - The Username in the Bitwarden entry is the **Access Key**, and the Password is the **Secret Key**

7. Add your IP address to the **ALLOWED_HOSTS** array in local_settings.py

8. Open a terminal and run:
    - For MAC
        ```
        sudo docker-compose up --build
        ```
        - Some MAC users encounter a permissions or authentication error when trying to load Python and Node in the build process. In this case:
          - Navigate to your root directory
          - Run `sudo chmod -R 775 ~/.docker`
          - Return to the it-security-steesh directory
          - Run `docker-compose up --build` (no sudo)
    - For Ubuntu
        ```
        sudo docker compose up --build
        ```

9. Access the web page for the Production server in your browser at `http://127.0.0.1:8080`

## After Initial Setup
Access the Development server at `http://localhost:5173/` by running:
```
sudo npm run dev
```

Rebuild for Production by running:
```
sudo npm run build
python3 manage.py collectstatic
```
or
```
sudo docker compose down
clear
sudo docker compose up
```

If you mess things up too much, you can perform a [hard reset](./02-how-to-hard-reset.md) on your local instance.