# Pull base image
FROM python:3.7
# Set environment varibles
WORKDIR /code/
# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv lock
RUN pipenv install --system --dev
COPY . /code/
EXPOSE 8000
CMD ["python", "fetchwaitingtime.py"]
