FROM python:3.11.9-slim

# Prevents Python from buffering stdout/stderr (useful for logs)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose port if your Flask app uses 5000
EXPOSE 5000

