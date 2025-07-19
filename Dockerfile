FROM debian:bookworm

COPY  ./.*py  /app/
COPY  ./*txt /app/
COPY  ./*env  /app/

WORKDIR /app/ 

ENV TZ="Europe/Moscow"
ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU.UTF-8
ENV LC_ALL=ru_RU.UTF-8 


RUN apt update && apt upgrade -y && \
	mkdir /reports/ && \ 
	apt install goaccess -y  && \
	apt install python3 -y   && \ 
	apt install python3-pip -y && \
  	#python3 -m pip install --upgrade pip  && \ 
	apt install python3-dotenv -y && \ 
	apt install python3-flask -y && \ 
  	#python3 -m pip install   -r requirements.txt  && \ 
	apt install locales -y && \
    echo "locales locales/default_environment_locale select ru_RU.UTF-8" | debconf-set-selections && \ 
    echo "locales locales/locales_to_be_generated multiselect ru_RU.UTF-8 UTF-8" | debconf-set-selections && \ 
    sed -i -e 's/# en_US.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \ 
    locale-gen ru_RU.UTF-8 && \ 
    update-locale LANG=ru_RU.UTF-8 && \ 
    dpkg-reconfigure --frontend noninteractive locales  

 

	
 
#ENTRYPOINT   ["bash"]
ENTRYPOINT   ["/usr/bin/python3", "/app/app.py"]
