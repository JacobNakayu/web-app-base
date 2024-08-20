# Dockerfile

# Sets up the docker environment in two main stages: Vue and Django. Django has two sub-stages of node and Python


# Stage 1: Install Node.js and Build the Vue Application
FROM node:22 AS build_stage

# Create and set the working directory
WORKDIR /web-app-base

# Mount the application code to the Docker image
COPY . .

# Install Dependencies
RUN echo "Install Node.js dependencies"
RUN npm install

# Build the Vite application
RUN echo "Generate Vite build"
RUN npm run build

# Stage 2: Set up Nginx and copy built assets
FROM nginx:latest AS nginx_stage

# Clear all default nginx files
RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy all build artifacts from the build_stage so nginx can find them
COPY --from=build_stage /web-app-base/vite_build /usr/share/nginx/html

# Load our custom nginx configuration files
COPY conf /etc/nginx

# Stage 3: Set up Django and Gunicorn
FROM python:3.11
WORKDIR /web-app-base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the entrypoint script to the container
COPY docker-entrypoint.sh /web-app-base/docker-entrypoint.sh

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django application code and build artifacts
COPY --from=build_stage /web-app-base/django_apps /web-app-base/django_apps
COPY --from=build_stage /web-app-base/vite_build /web-app-base/vite_build


# Install Gunicorn
RUN pip install gunicorn

# Expose port for Gunicorn and Nginx
EXPOSE 8080
EXPOSE 80

# runs the production server
ENTRYPOINT ["./docker-entrypoint.sh"]

