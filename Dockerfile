# Multi-stage build for complete petrol station management system
FROM node:20-alpine as frontend-build

WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package*.json ./
COPY frontend/pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

# Copy frontend source and build
COPY frontend/ ./
RUN pnpm run build

# Python backend stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./

# Copy built frontend assets
COPY --from=frontend-build /app/frontend/dist ./static

# Create instance directory and copy database
RUN mkdir -p instance
COPY backend/petrol_station.db ./instance/

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["python", "app.py"]