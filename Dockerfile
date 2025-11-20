# ---- Production Dockerfile ----
# This Dockerfile creates a single image containing both the
# React frontend and the Flask backend.

# ---- Frontend Builder Stage ----
# This stage builds the React app into static files.
FROM node:18-alpine AS frontend-builder
WORKDIR /app
COPY ./allergy_app/package*.json ./
RUN npm install
COPY ./allergy_app ./
RUN npm run build

# ---- Backend Builder Stage ----
# This stage builds the virtual environment with all dependencies.
FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS backend-builder
RUN uv venv /opt/venv
WORKDIR /app
# Copy only necessary files to leverage Docker cache
COPY ./backend/pyproject.toml ./backend/uv.lock* ./
# Use uv pip sync to install from the lock file
RUN . /opt/venv/bin/activate && uv pip install -r pyproject.toml
COPY ./backend .
RUN . /opt/venv/bin/activate && uv pip install --no-cache-dir .

# ---- Final Production Stage ----
# This stage creates the final, lean image.
FROM python:3.13-slim
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# Set FLASK_DEBUG to false for production
ENV FLASK_DEBUG=false

# Create a non-root user
RUN useradd --create-home appuser
USER appuser
ENV APP_HOME=/home/appuser/app
WORKDIR $APP_HOME

# Copy virtual env and backend code from builder stages
COPY --from=backend-builder /opt/venv /opt/venv
# Copy the entire application, not just src
COPY --from=backend-builder --chown=appuser:appuser /app/ ./

# Copy built frontend files from the frontend-builder stage
COPY --from=frontend-builder --chown=appuser:appuser /app/build ./static

# The Flask app is configured to serve files from this 'static' directory.

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "allergy_snatcher.__main__:app"]
