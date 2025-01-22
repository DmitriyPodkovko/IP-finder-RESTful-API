FROM oraclelinux:8 AS oracle-client

RUN  dnf -y install oracle-instantclient-release-el8 && \
     dnf -y install oracle-instantclient-basic oracle-instantclient-devel oracle-instantclient-sqlplus && \
     rm -rf /var/cache/dnf

FROM python:3.11-alpine
LABEL maintainer="PDA"

WORKDIR /IP-finder-RESTful-API

# Set environment variables
# This prevents Python from writing out *.pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

COPY . .

RUN apk add --update --upgrade --no-cache --virtual .tmp-build-deps \
    gcc musl-dev libaio gcompat cifs-utils && \
    # If need libcap for setcap
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
    # If necessary, install the required capabilities for mount.cifs \
    # setcap cap_sys_admin+ep /usr/sbin/mount.cifs
    # Clean up build dependencies
    # apk del .tmp-build-deps

# Copying the Oracle client from the first image
COPY --from=oracle-client /usr/lib/oracle /usr/lib/oracle

ENV LD_LIBRARY_PATH=/usr/lib/oracle/21/client64/lib

CMD ["sqlplus", "-v"]

EXPOSE 8248

ENTRYPOINT ["sh", "entrypoint.sh"]
