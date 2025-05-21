# Use a lightweight Python image
FROM python:slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV PATH="/root/.local/bin:$PATH"
# Set the working directory
WORKDIR /app

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get install -y curl build-essential\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 


# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | sh


# Copy the application code
COPY . .
ENV PYTHONPATH="/app"

# Install dependencies and project
RUN uv pip install --no-cache-dir --system .


# Train the model before running the application
RUN python pipeline/training_pipeline.py

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the app
CMD ["python", "main.py"]