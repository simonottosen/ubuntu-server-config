# Pull base image
FROM python:3.7
# Set environment varibles
WORKDIR /code/
# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system --dev
COPY .cph/ /code/
EXPOSE 8000
CMD ["python", "fetchwaitingtime.py"]
