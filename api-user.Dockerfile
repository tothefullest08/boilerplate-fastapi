FROM python:3.8.3-slim

COPY ./api-user/requirements.txt /api-user/requirements.txt
COPY ./api-user/sources /api-user
WORKDIR /api-user

RUN pip3 install -r /api-user/requirements.txt

# e.g ENTRYPOINT ["python3" "sample.py"]
#     ENTRYPOINT ["gunicorn" "sample:app"]
ENTRYPOINT [""]
