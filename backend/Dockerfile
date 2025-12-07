# ---- Builder Stage ----
# This stage builds the virtual environment with all dependencies.
FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS builder

# 2. Create a virtual environment
RUN uv venv /opt/venv --system-site-packages


# 3. Install dependencies
# This is done in a separate step to leverage Docker's layer caching.
# The layer will be rebuilt only if pyproject.toml changes.
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN . /opt/venv/bin/activate && \
    uv pip install -r pyproject.toml
COPY . .
RUN . /opt/venv/bin/activate && \
    uv pip install --no-cache-dir .

# ---- Final Stage ----
# This stage creates the final, lean image.
FROM python:3.13-bookworm

# Set environment variables to use the virtual environment
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create a non-root user for security
RUN useradd --create-home appuser
WORKDIR /home/appuser/app
USER appuser
ENV COOKIE_SECURE=False
# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy your application code
COPY --chown=appuser:appuser ./ .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "allergy_snatcher:main"]
