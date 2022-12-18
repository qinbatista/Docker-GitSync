FROM python:3.8.5-alpine

ARG aws_key
ARG aws_secret

ADD * /
RUN ls

#install curl
RUN apk add --update curl wget

#install python3 packages
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirement


#folder for GitRepositories
VOLUME [ "/GitRepositories","/download"]

WORKDIR /root
CMD  ["python3","/GitSync.py"]