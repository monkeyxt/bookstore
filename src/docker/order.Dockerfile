FROM python:3

RUN pip install --no-cache-dir flask requests pyyaml

COPY ./order.py .
COPY ./config.yml .
RUN mkdir databases

ENTRYPOINT [ "python", "./order.py"]
