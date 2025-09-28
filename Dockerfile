FROM debian:bookworm
 
WORKDIR /app/

ENV TZ="Europe/Moscow"
ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU.UTF-8
ENV LC_ALL=ru_RU.UTF-8

RUN apt update && apt upgrade -y && \
apt install locales -y && \
echo "locales locales/default_environment_locale select ru_RU.UTF-8" | debconf-set-selections && \
echo "locales locales/locales_to_be_generated multiselect ru_RU.UTF-8 UTF-8" | debconf-set-selections && \
sed -i -e 's/# en_US.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
locale-gen ru_RU.UTF-8 && \
update-locale LANG=ru_RU.UTF-8 && \
dpkg-reconfigure --frontend noninteractive locales && apt clean

RUN	apt install goaccess -y  && \
apt install python3 -y  && \
apt install python3-pip -y && \
apt install python3-venv -y  && \
apt clean 

COPY  ./requirements.txt  /app/


ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m venv $VIRTUAL_ENV && python3 -m pip install -r /app/requirements.txt

COPY  ./*py  /app/
COPY  ./assets  /app/assets


RUN echo "#!/bin/bash \n $VIRTUAL_ENV/bin/python3 /app/app.py" > ./entrypoint.sh && chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

