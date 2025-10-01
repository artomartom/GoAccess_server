FROM alpine:3.22.1
 
ENV WORKDIR=/app
WORKDIR $WORKDIR

ENV VIRTUAL_ENV=$WORKDIR/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apk upgrade && \
apk add python3 py3-pip goaccess && \
rm -rf /var/cache/apk/*


COPY  ./requirements.txt $WORKDIR
RUN python3 -m venv $VIRTUAL_ENV && python3 -m pip install -r $WORKDIR/requirements.txt

COPY  ./*py  $WORKDIR
COPY  ./assets  $WORKDIR/assets

#ARG debbuger
#RUN if [[ -z "$debbuger" ]] ; then python3 -m pip install debugpy; fi  && \
#    if [[ -z "$debbuger" ]] ; then DEBUG="-m debugpy --listen 0.0.0.0:5678"; fi
#docker build   -t goaccess_server-debug .


RUN echo "#!/bin/sh" >> $WORKDIR/entrypoint.sh && chmod +x $WORKDIR/entrypoint.sh
RUN echo "$VIRTUAL_ENV/bin/python3 $DEBUG $WORKDIR/app.py" >> ./entrypoint.sh 
ENTRYPOINT ["./entrypoint.sh"]

