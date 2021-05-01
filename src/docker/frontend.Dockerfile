FROM python:3

RUN pip install --no-cache-dir flask requests pyyaml apscheduler

COPY ./frontend.py .
COPY ./config.yml .
RUN mkdir logs

ENTRYPOINT [ "python", "./frontend.py"]
