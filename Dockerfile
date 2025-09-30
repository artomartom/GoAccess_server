FROM debian:bookworm
 
ENV WORKDIR=/app
WORKDIR $WORKDIR


ENV TZ="Europe/Moscow"
ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU.UTF-8
ENV LC_ALL=ru_RU.UTF-8
ENV VIRTUAL_ENV=$WORKDIR/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

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

COPY  ./requirements.txt $WORKDIR
RUN python3 -m venv $VIRTUAL_ENV && python3 -m pip install -r $WORKDIR/requirements.txt

COPY  ./*py  $WORKDIR
COPY  ./assets  $WORKDIR/assets

ARG debbuger
RUN if [[ -z "$debbuger" ]] ; then python3 -m pip install debugpy; fi  && \
    if [[ -z "$debbuger" ]] ; then DEBUG="-m debugpy --listen 0.0.0.0:5678"; fi
#docker build   -t goaccess_server-debug .


RUN echo "#!/bin/sh" >> $WORKDIR/entrypoint.sh && chmod +x $WORKDIR/entrypoint.sh
RUN echo "$VIRTUAL_ENV/bin/python3 $DEBUG $WORKDIR/app.py" >> ./entrypoint.sh 
ENTRYPOINT ["./entrypoint.sh"]

