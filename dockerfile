FROM python:3.8.5-alpine

ARG aws_key
ARG aws_secret

ADD * /
RUN ls

#install curl
RUN apk update
RUN apk -y install curl

#install python3 packages
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirement


#install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
RUN aws configure set aws_access_key_id ${aws_key}
RUN aws configure set aws_secret_access_key ${aws_secret}
RUN aws configure set default.region us-west-2
RUN aws configure set region us-west-2 --profile testing
RUN echo ${aws_key} > aws_key.txt
RUN echo ${aws_secret} > aws_secret.txt



#folder for GitRepositories
VOLUME [ "/GitRepositories"]

WORKDIR /root
CMD  ["python3","/GitSync.py"]