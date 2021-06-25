FROM mcr.microsoft.com/mssql/server:2019-latest

ENV DB_HOST=localhost

EXPOSE 1433
USER root


ADD ./scripts /usr/scripts
ADD ./app /root/app

RUN apt-get update && apt-get install -y dos2unix unixodbc-dev msodbcsql17 python3-pip nano curl \
    && curl https://bootstrap.pypa.io/get-pip.py | python3 \
    && echo PATH="$PATH:/opt/mssql-tools/bin" >> ~/.bash_profile \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
    && chmod +x /usr/scripts/entrypoint.sh && chmod +x /usr/scripts/configure-db.sh \
    && dos2unix /usr/scripts/* && mkdir -p /root/config && python3 -m pip install --upgrade pyodbc sqlalchemy pandas numpy requirements

WORKDIR /root/config


ENTRYPOINT ["/usr/scripts/entrypoint.sh"]