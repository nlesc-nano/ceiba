FROM python:3.8.5

RUN apt-get update && apt-get install -y cmake

RUN pip install --user pipenv

ENV PYTHONPATH=/usr/src/app/
ENV PATH="$PATH:/root/.local/bin"

WORKDIR /usr/src/app

COPY Pipfile /usr/src/app/

RUN pipenv install

COPY . /usr/src/app/

EXPOSE 8080

CMD ["insilico-server"]
