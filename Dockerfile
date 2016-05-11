# VERSION 1.0
FROM dockercisco/acitoolkit
MAINTAINER Chad Peterson, chapeter@cisco.com

#install tools
#RUN apt-get update
RUN apt-get install python-dev
RUN apt-get -y install autoconf g++ python2.7-dev libxml2-dev libxslt1-dev zlib1g-dev
RUN apt-get -y install build-essential libssl-dev
RUN apt-get -y install libffi-dev
#RUN apt-get -y install git python-pip 
RUN pip install --upgrade pip



#install download and run acimigrate
WORKDIR /opt
RUN git clone -b docker http://github.com/chapeter/acimigrate
WORKDIR acimigrate
RUN pip install -r requirements.txt
EXPOSE 8000
CMD [ "python", "./main.py" ]
