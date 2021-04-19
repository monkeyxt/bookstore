FROM python:3

RUN pip install --no-cache-dir flask requests pyyaml

COPY ./catalog.py .
COPY ./config.yml .

CMD [ "python", "./catalog.py"]
