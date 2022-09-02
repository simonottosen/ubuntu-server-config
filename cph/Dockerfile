# Pull base image
FROM python:3.7
# Set environment varibles
RUN echo $POSTGRES_PASSWORD > environment
RUN echo $POSTGRES_DB >> environment
RUN echo $POSTGRES_USER >> environment
RUN echo $POSTGRES_PORT >> environment
WORKDIR /code/
# Install dependencies
RUN pip install pipenv
COPY Pipfile /code/
COPY environment /code/
RUN pipenv lock
RUN pipenv install --system --dev
COPY fetchwaitingtime.py /code/fetchwaitingtime.py
COPY cphairportqueue-firebase-key.json /code/cphairportqueue-firebase-key.json
RUN apt-get update && apt-get -y install cron nano
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
CMD ["cron", "-f"]



POSTGRES_PASSWORD=QEfaqBHkitiJqqLs
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PORT=5432
