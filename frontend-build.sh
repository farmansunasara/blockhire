#!/bin/bash
# Frontend build script for Render deployment

echo "Starting frontend build process..."
cd frontend

echo "Installing dependencies..."
npm install

echo "Building Next.js application..."
npm run build

echo "Frontend build completed successfully!"
