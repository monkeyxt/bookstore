# Run this file from the src directory

# This image should be run with "docker run -p PORT:PORT order name" where PORT is the port being exposed
echo "Building frontend image..."
docker build . -f docker/frontend.Dockerfile -t frontend

# This image should be run with "docker run -p PORT:PORT order name" where name is order1, order2, and PORT is the port being exposed etc
echo "Building order image..."
docker build . -f docker/order.Dockerfile -t order

# This image should be run with "docker run -p PORT:PORT catalog name" where name is catalog1, catalog2, and PORT is the port being exposed etc
echo "Building catalog image..."
docker build . -f docker/catalog.Dockerfile -t catalog