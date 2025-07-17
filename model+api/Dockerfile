# $DEL_BEGIN

# FROM python:3.10.6

WORKDIR /prod

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY CNN CNN
COPY fast_api fast_api
COPY functions functions

CMD uvicorn fast_api.api:app --host 0.0.0.0 --port $PORT

# # $DEL_END
