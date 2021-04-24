# Run this file from the src directory

echo "Building frontend image..."
docker build .. -f docker/frontend.Dockerfile -t frontend

echo "Building order image..."
docker build .. -f docker/order.Dockerfile -t order

echo "Building catalog image..."
docker build .. -f docker/catalog.Dockerfile -t catalog