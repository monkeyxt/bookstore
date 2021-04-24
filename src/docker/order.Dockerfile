FROM python:3

# TODO: maybe create a volume for recovery logs?
ARG NAME="order1"
RUN pip install --no-cache-dir flask requests pyyaml

COPY ./order.py .
COPY ./config.yml .

CMD [ "python", "./order.py", NAME]
