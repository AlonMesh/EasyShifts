FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY Backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY Backend/ ./Backend/

# Set PYTHONPATH
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Run the server
CMD ["python", "-m", "Backend.Server"]
