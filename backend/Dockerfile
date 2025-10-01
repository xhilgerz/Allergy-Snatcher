# ---- Builder Stage ----
# This stage builds the virtual environment with all dependencies.
FROM python:3.13-slim as builder

# 1. Install uv
RUN pip install uv

# 2. Create a virtual environment
RUN uv venv /opt/venv

# 3. Install dependencies
# This is done in a separate step to leverage Docker's layer caching.
# The layer will be rebuilt only if pyproject.toml changes.
WORKDIR /app
COPY . .
RUN . /opt/venv/bin/activate && \
    uv pip install --no-cache-dir .

# ---- Final Stage ----
# This stage creates the final, lean image.
FROM python:3.13-slim

# Set environment variables to use the virtual environment
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create a non-root user for security
RUN useradd --create-home appuser
WORKDIR /home/appuser/app
USER appuser

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy your application code
COPY --chown=appuser:appuser ./ .

# Expose the port your application runs on (5000 as per docker-compose)
EXPOSE 5000

# Command to run your application
# This assumes you are using Flask's development server.
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
