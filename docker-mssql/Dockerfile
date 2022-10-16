FROM ubuntu:20.04 AS builder

USER root
WORKDIR /root
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y python3.9 python3.9-dev \
    python3.9-venv python3-pip python3-wheel build-essential unixodbc-dev \
    && apt-get clean

RUN python3.9 -m venv /root/venv
ENV PATH="/root/venv/bin:$PATH"

COPY ["requirements.txt", "requirements-mssql.txt",  "/root/"]
RUN /root/venv/bin/python -m pip install --no-cache-dir wheel
RUN /root/venv/bin/python -m pip install --no-cache-dir -r requirements.txt & \
    /root/venv/bin/python -m pip install --no-cache-dir -r requirements-mssql.txt

FROM mcr.microsoft.com/mssql/server:2019-latest as mssql

ENV DB_HOST=localhost
ENV ACCEPT_EULA=Y

EXPOSE 1433
USER root

RUN apt update && apt upgrade -y && ACCEPT_EULA=Y DEBIAN_FRONTEND=noninteractive apt install -y \
    cron crudini unixodbc-dev msodbcsql18 python3.9 python3.9-dev \
    python3-pip python3.9-venv \
    && echo PATH="$PATH:/opt/mssql-tools/bin" >> ~/.bash_profile \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
    && apt-get clean

COPY --from=builder /root/venv /root/venv
ENV PYTHONBUFFERED=1
ENV VIRTUAL_ENV=/root/venv
ENV PATH="/root/venv/bin:$PATH"

COPY docker-mssql/*.sh /usr/scripts/

RUN chmod +x /usr/scripts/entrypoint.sh && chmod +x /usr/scripts/configure-db.sh

WORKDIR /root/app

COPY ["setup.py", "README.md", "requirements.txt", "requirements-mssql.txt", "/root/app/"]
COPY src ./src

RUN /root/venv/bin/python setup.py install

WORKDIR /root

ENTRYPOINT ["/usr/scripts/entrypoint.sh"]