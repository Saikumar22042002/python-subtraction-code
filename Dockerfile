# Stage 1: Builder
# This stage installs dependencies into a wheelhouse.
FROM python:3.11-slim as builder

WORKDIR /app

# Install build tools
RUN pip install --upgrade pip

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# Stage 2: Final image
# This stage creates the final, lean production image.
FROM python:3.11-slim

WORKDIR /app

# Create a non-root user
RUN addgroup --system nonroot && adduser --system --ingroup nonroot nobody

# Copy built wheels and install them
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application code
COPY app.py .

# Set non-root user
USER nobody

# Expose the application port
EXPOSE 5000

# Command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
