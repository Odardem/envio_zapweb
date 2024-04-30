FROM alpine:3.18
LABEL MAINTAINER = "Vinicius Linux"
RUN mkdir /whats && mkdir /whats/app
COPY run.py /whats
COPY config.py /whats
COPY requirements.txt /whats
COPY app /whats/app
RUN apk add --update python3 tzdata firefox &&\
    ln -sf python3 /usr/bin/python &&\
    cp /usr/share/zoneinfo/America/Bahia /etc/localtime &&\
    echo "America/Bahia" > /etc/timezone &&\
    apk del tzdata && rm -rf /var/cache/apk/*
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install -r /whats/requirements.txt
EXPOSE 5000/tcp
WORKDIR /whats
CMD waitress-serve --host=* --port=5000 --no-ipv6 app:app
