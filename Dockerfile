FROM ubuntu:20.04 AS builder

ARG DEBIAN_FRONTEND=noninteractive
USER root

RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3.9-dev python3.9-venv python3-pip python3-wheel build-essential unixodbc-dev \
    && apt-get clean

RUN python3.9 -m venv /root/venv
ENV PATH="/root/venv/bin:$PATH"

COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

FROM mcr.microsoft.com/mssql/server:2019-latest as mssql

ENV DB_HOST=localhost
ENV ACCEPT_EULA=Y

EXPOSE 1433
USER root

RUN apt update && apt upgrade -y && ACCEPT_EULA=Y apt install -y \
    curl cron unixodbc-dev msodbcsql18 python3.9 python3.9-dev python3-pip python3.9-venv \
    && curl https://bootstrap.pypa.io/get-pip.py | python3 \
    && echo PATH="$PATH:/opt/mssql-tools/bin" >> ~/.bash_profile \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
    && apt-get clean

COPY --from=builder /root/venv /root/venv
ENV PYTHONBUFFERED=1
ENV VIRTUAL_ENV=/root/venv
ENV PATH="/root/venv/bin:$PATH"

COPY scripts /usr/scripts

RUN chmod +x /usr/scripts/entrypoint.sh && chmod +x /usr/scripts/configure-db.sh

WORKDIR /root/app

COPY setup.py .
COPY README.md .
COPY requirements.txt .
COPY src ./src

RUN pip3 install --no-cache-dir -r requirements.txt && python3 setup.py install

WORKDIR /root

ENTRYPOINT ["/usr/scripts/entrypoint.sh"]