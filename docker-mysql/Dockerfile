FROM mysql:8-debian AS sqlbuilder

RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3.9-dev \
    python3.9-venv python3-pip python3-wheel build-essential libssl-dev libmysqlclient-dev \
    software-properties-common && apt-get clean

RUN python3.9 -m venv /root/venv && chmod -R 777 /root
ENV PATH="/root/venv/bin:$PATH"

WORKDIR /root/app
COPY ["setup.py",  "README.md", "requirements-mysqldb.txt", "requirements.txt", "/root/app/"]
COPY src /root/app/src

RUN /root/venv/bin/python -m pip install --no-cache-dir wheel
RUN /root/venv/bin/python -m pip install --no-cache-dir -r /root/app/requirements.txt && \
    /root/venv/bin/python -m pip install --no-cache-dir -r /root/app/requirements-mysqldb.txt && \
    /root/venv/bin/python /root/app/setup.py install


# ----------------MYSQL BUILD----------------

FROM mysql:8-debian as mysql

EXPOSE 3306

USER root

RUN apt update && apt upgrade -y && apt install -y --no-install-recommends crudini \
    cron python3.9 python3.9-dev python3-pip libssl-dev libmysqlclient-dev && apt-get clean

COPY --from=sqlbuilder /root/venv /root/venv
ENV PYTHONBUFFERED=1
ENV VIRTUAL_ENV=/root/venv
ENV PATH="/root/venv/bin:$PATH"

WORKDIR /root/app

COPY ["setup.py",  "README.md", "requirements-mysqldb.txt", "requirements.txt", "/root/app/"]
COPY src ./src

RUN python3 setup.py install

COPY docker-mysql/configure-db.sh /docker-entrypoint-initdb.d/

RUN chmod -R 777 /root && chmod -R 777 /docker-entrypoint-initdb.d/configure-db.sh

WORKDIR /root