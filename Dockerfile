FROM python:3.8.5

RUN apt-get update && apt-get install -y cmake

ENV PYTHONPATH=/usr/src/app/
ENV PATH="$PATH:/root/.local/bin"

WORKDIR /usr/src/app

COPY . /usr/src/app/

EXPOSE 8080

RUN pip install -e .

ENTRYPOINT ["./entry_point.sh"]
