
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

# Install system dependencies (including Tesseract and its dependencies)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and set up a virtual environment
RUN useradd --create-home appuser && \
    python -m venv /opt/venv && \
    chown -R appuser:appuser /opt/venv

# Set the working directory in the container
WORKDIR /app
ENV PYTHONPATH=/app
RUN chown appuser:appuser /app

# Switch to the non-root user
USER appuser

# Copy the requirements file into the container at /app
COPY --chown=appuser:appuser requirements.txt /app/

# Install Python dependencies inside the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY --chown=appuser:appuser . /app/

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the application using uvicorn
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
