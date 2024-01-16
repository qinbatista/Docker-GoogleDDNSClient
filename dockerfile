FROM python:3.7-alpine


#[Start] GoogleDDNS--------------------------------------------------
ARG GOOGLE_USERNAME_V6
ARG GOOGLE_PASSWORD_V6
ARG DOMAIN_NAME_V6
ARG GOOGLE_USERNAME_V4
ARG GOOGLE_PASSWORD_V4
ARG DOMAIN_NAME_V4

RUN echo ${GOOGLE_USERNAME_V6} > GOOGLE_USERNAME_V6
RUN echo ${GOOGLE_PASSWORD_V6} > GOOGLE_PASSWORD_V6
RUN echo ${DOMAIN_NAME_V6} > DOMAIN_NAME_V6
RUN echo ${GOOGLE_USERNAME_V4} > GOOGLE_USERNAME_V4
RUN echo ${GOOGLE_PASSWORD_V4} > GOOGLE_PASSWORD_V4
RUN echo ${DOMAIN_NAME_V4} > DOMAIN_NAME_V4

#[End] GoogleDDNS-----------------------------------------------------

#add file
ADD * ./
RUN apk add --update curl
#update pip
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

WORKDIR /
CMD ["python","/GoogleDDNSClient.py"]
