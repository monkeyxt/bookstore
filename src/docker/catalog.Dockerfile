FROM python:3

ARG NAME="catalog1"
RUN pip install --no-cache-dir flask requests pyyaml

COPY ./catalog.py .
COPY ./config.yml .

CMD [ "python", "./catalog.py", NAME]
