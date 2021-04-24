# Run this file from the src directory

echo "Building frontend image..."
docker build .. -f docker/frontend.Dockerfile -t frontend

# This image should be run with "docker run order [name]" where name is order1, order2, etc
echo "Building order image..."
docker build .. -f docker/order.Dockerfile -t order

# This image should be run with "docker run catalog [name]" where name is catalog1, catalog2, etc
echo "Building catalog image..."
docker build .. -f docker/catalog.Dockerfile -t catalog