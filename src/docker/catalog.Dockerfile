FROM python:3

RUN pip install --no-cache-dir flask requests pyyaml

COPY ./catalog.py .
COPY ./config.yml .
RUN mkdir databases

ENTRYPOINT [ "python", "./catalog.py"]
