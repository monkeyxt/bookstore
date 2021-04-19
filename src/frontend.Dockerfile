FROM python:3

RUN pip install --no-cache-dir flask requests pyyaml

COPY ./frontend.py .
COPY ./config.yml .

CMD [ "python", "./frontend.py"]
