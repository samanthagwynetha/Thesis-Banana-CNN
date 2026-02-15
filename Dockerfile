FROM python:3.11.9-slim

# Prevent Python from buffering stdout/stderr (nice for logs)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for Pillow + TensorFlow Lite
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install uv (from Astral GitHub container)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Copy dependency files first (better caching)
COPY pyproject.toml uv.lock ./

# Install Python dependencies via uv
RUN uv sync --frozen --no-dev

# Copy the rest of the project
COPY . .

EXPOSE 5000

# Use gunicorn as before, run inside uv environment
CMD ["uv", "run", "gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
