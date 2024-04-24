FROM alpine:3.18
LABEL MAINTAINER = "Vinicius Linux"
#ADD crontab /etc/crontabs/node-cron
#RUN chmod 0644 /etc/crontabs/node-cron
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
#CMD ["/bin/sh"]
#RUN cp /projeto/src/db/conn.exemple.js /projeto/src/db/conn.js
#RUN  echo "00	00-22	*	*	*       /usr/bin/npm --prefix /projeto run allimport" >> /etc/crontabs/root
#RUN  echo "00	13	*	*	*       /usr/bin/npm --prefix /projeto run deletelog" >> /etc/crontabs/root
#RUN npm i
#RUN  echo "00	22	*	*	*       /usr/bin/npm --prefix /projeto run allimportcasino" >> /etc/crontabs/root
#CMD crond -f
#CMD [ "crond" ,"-f", " ]