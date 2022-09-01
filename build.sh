#!/bin/sh

mkdir -p build

# build the backend
# aka copy files
echo "building backend..."
mkdir -p build/backend/
cp backend/main.py build/backend
echo "done building backend"

# build the frontend
# aka run npm build and then copy the result
echo -n "building frontend..."
mkdir -p build/frontend
cd frontend
npm install
npm run build
cd ..
cp -r frontend/build/**  build/frontend
echo "done building frontend"

# copy over the run script
cp run.py build

# copy configuration templates
cp backend-config.template.json build/backend-config.json
