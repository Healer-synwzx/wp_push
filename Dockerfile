FROM python:3

WORKDIR /usr/src/app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.doubanio.com/simple

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "flaskapp:app"]

