FROM python:3.12

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./src /src/

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]