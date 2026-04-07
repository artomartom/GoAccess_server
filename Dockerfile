FROM alpine:3.22.1

ENV WORKDIR=/app
WORKDIR $WORKDIR


RUN REPO="https://mirror.yandex.ru/mirrors/alpine/v$(egrep -o '^[0-9]+\.[0-9]+' /etc/alpine-release)" && \
OPTIONS="--repositories-file /dev/null -X "$REPO/main" -X "$REPO/community" --no-cache" && \
apk upgrade $OPTIONS && \
apk add $OPTIONS  python3 py3-pip goaccess curl

COPY  ./requirements.txt $WORKDIR
ENV VIRTUAL_ENV=$WORKDIR/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
 
ARG INSTALL_DEBUGPY=false

ENV ENV_INSTALL_DEBUGPY=$INSTALL_DEBUGPY

RUN if [ "${ENV_INSTALL_DEBUGPY}" = "true" ]; then echo "debugpy" >> $WORKDIR/requirements.txt ; fi

RUN python3 -m venv $VIRTUAL_ENV && python3 -m pip install -r $WORKDIR/requirements.txt

RUN echo "$VIRTUAL_ENV/bin/python3 \$@" >> /entrypoint.sh

COPY  ./*py  $WORKDIR
COPY  ./assets  $WORKDIR/assets

ENTRYPOINT ["sh","/entrypoint.sh"]

