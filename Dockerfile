FROM alpine:3.22.1

ENV WORKDIR=/app
WORKDIR $WORKDIR

RUN apk upgrade && \
apk add python3 py3-pip goaccess curl && \
rm -rf /var/cache/apk/*

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

HEALTHCHECK --interval=60s --timeout=10s --retries=3 --start-period=10s\
  CMD curl -4f http://localhost:3050/health || exit 1

ENTRYPOINT ["sh","/entrypoint.sh"]

