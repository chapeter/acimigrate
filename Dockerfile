# VERSION 1.0
FROM dockercisco/acitoolkit 
MAINTAINER Chad Peterson, chapeter@cisco.com

WORKDIR /opt
RUN git clone http://github.com/chapeter/acimigrate
WORKDIR acimigrate
RUN pip install -r requirements.txt
EXPOSE 8000
CMD [ "python", "./main.py" ]
