#!/bin/bash

echo "Starting FastAPI server..."

cd backend
uvicorn main:app \
  --host 0.0.0.0 \
  --port ${PORT:-8000}
