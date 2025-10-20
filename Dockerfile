FROM alpine:3.22.1
 
ENV WORKDIR=/app
WORKDIR $WORKDIR


RUN apk upgrade && \
apk add python3 py3-pip goaccess && \
rm -rf /var/cache/apk/*


COPY  ./requirements.txt $WORKDIR
ENV VIRTUAL_ENV=$WORKDIR/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


#RUN if [[ -z "$debbuger" ]] ; then echo "debugpy" >> $WORKDIR/requirements.txt ; fi   

RUN python3 -m venv $VIRTUAL_ENV && python3 -m pip install -r $WORKDIR/requirements.txt


#RUN if [[ -z "$debbuger" ]] ; then   DEBUG="-m debugpy --listen 0.0.0.0:5678"; fi    
#RUN echo "$VIRTUAL_ENV/bin/python3 $DEBUG $WORKDIR/app.py" >> /entrypoint.sh 
RUN echo "$VIRTUAL_ENV/bin/python3 \$@" >> /entrypoint.sh

COPY  ./*py  $WORKDIR
COPY  ./assets  $WORKDIR/assets

ENTRYPOINT ["sh","/entrypoint.sh"]

