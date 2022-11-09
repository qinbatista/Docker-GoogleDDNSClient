FROM python:3.7-alpine

ARG Username
ARG Password
ARG domain_name

#add file
ADD * ./
RUN apk add --update curl
#update pip
RUN pip install --upgrade pip
RUN pip install -r ./requirements

#set google key and secret
RUN echo ${Username} > Username.txt
RUN echo ${Password} > Password.txt
RUN echo ${domain_name} > domain_name.txt

WORKDIR /
CMD ["python","/GoogleDDNSClient.py"]
