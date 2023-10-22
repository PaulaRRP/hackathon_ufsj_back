FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app

ENV PORT 5000

EXPOSE 5000

WORKDIR $APP_HOME

COPY . ./

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org  --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app