FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV DASH_DEBUG_MODE False
ENV PYTHONDONTWRITEBYTECODE 1
RUN pip install pipenv
COPY ./app /app
WORKDIR /app
RUN pipenv lock
RUN pipenv install --system --dev
EXPOSE 8050
CMD ["gunicorn", "-b", "0.0.0.0:8050", "--reload", "app:server"]