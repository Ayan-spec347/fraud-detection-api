# 1. Use an official, lightweight Python runtime as a parent image
FROM python:3.11-slim

# 2. Set environment variables to optimize Python behavior inside the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy only the requirements first to take advantage of Docker layer caching
COPY requirements.txt /app/

# 5. Install the dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code into the container
# This mirrors your exact local directory structure into /app
COPY api/ /app/api/
COPY models/ /app/models/

# 7. Inform Docker that the container listens on port 8000 at runtime
EXPOSE 8000

# 8. Define the command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]