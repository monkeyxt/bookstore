FROM python:3

RUN pip install --no-cache-dir flask requests pyyaml apscheduler

COPY ./frontend.py .
COPY ./config.yml .

CMD [ "python", "./frontend.py"]
