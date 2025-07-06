FROM python:3.11-slim-bookworm

COPY  ./.*py  /app/
COPY  ./*txt /app/
COPY  ./*env  /app/

WORKDIR /app/



 
RUN apt update && apt upgrade -y && \
	mkdir /reports/ && \ 
	apt install goaccess -y  && \
  	python3 -m pip install --upgrade pip && \
  	python3 -m pip install   -r requirements.txt  
#	apt install locales  -y    
#	locale-gen ru_RU.UTF-8 
#	update-locale LANG=ru_RU.UTF-8

#RUN localedef --inputfile ru_RU --force --charmap UTF-8 --alias-file /usr/share/locale/locale.alias ru_RU.UTF-8
# https://www.gnu.org/software/libc/manual/html_node/Locale-Categories.html
#ENV \
#  LC_COLLATE=ru_RU.utf8 \
#  LC_CTYPE=ru_RU.utf8 \
#  LC_MONETARY=ru_RU.utf8 \
#  LC_NUMERIC=ru_RU.utf8 \
#  LC_TIME=ru_RU.utf8 \
#  LC_MESSAGES=ru_RU.utf8 \
#  LC_ALL=ru_RU.utf8 \
#  LANG=ru_RU.utf8	
#

#echo "ru_RU.UTF-8 UTF-8" | tee -a /etc/locale.gen

CMD ["/usr/local/bin/python3", "/app/main.py"]
#CMD ["tail", "-f", "/dev/null"]
