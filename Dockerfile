FROM ubuntu:latest

RUN apt-get -y update
RUN apt-get install python3 -y
RUN apt-get -y install python3-pip -y

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip3 install -r requirements.txt
ADD . /app/

ENTRYPOINT [ "python3" ]
CMD ["application.py"]