FROM python:3

# TODO: maybe create a volume for recovery logs?

RUN pip install --no-cache-dir flask requests pyyaml

COPY ./order.py .
COPY ./config.yml .

CMD [ "python", "./order.py"]
