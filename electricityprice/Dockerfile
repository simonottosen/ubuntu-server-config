FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /project/
RUN pip install pipenv
COPY Pipfile /project/
RUN pipenv lock
RUN pipenv install --system --dev
COPY project/app.py /project/app.py
CMD python /project/app.py