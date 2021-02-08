FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV AIRFLOW_HOME = ~/airflow

WORKDIR /code

ADD requirements.txt /code/

RUN pip install -r requirements.txt
RUN airflow db init

COPY . /code/
EXPOSE 8080
CMD ["sh", "scripts/production/deploy.sh"]