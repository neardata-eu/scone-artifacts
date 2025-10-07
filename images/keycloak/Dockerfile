FROM registry.scontain.com/sconecuratedimages/experimental/keycloak:26-alpine3.20-sconectl-5.9.0-rc.5 AS source

LABEL SYSTEM="Keycloak Confidential Identity and Access Manager over SCONE installation"
LABEL SPONSOR="NEARDATA Consortium is part of the Horizon Science Projects of EU Commission 101092644"
LABEL MAINTAINER="Scontain GmbH https://scontain.com/"
LABEL EMAIL="info@scontain.com"

###################################
# substitute SCONECTL manifests
WORKDIR /

RUN rm -rfv /scone || true
COPY ./files/sconectl      /scone

###################################
# system configuration
RUN apk update

RUN apk add nmap mysql-client lynx vim bash less curl net-tools wget git jq diffutils

###################################
# reset Keycloak shipped configurations to use with database
WORKDIR /keycloak

###
# WARNING: configuration of user and password as well as the TLS certificate and private key embedded in
# ........ and shipped with the image are merely for demonstration and cannot be used in production
# ........ You can set these configurations for production by using the mesh.txt configuration file
# ........ For more information to setup and run the mesh of services, check documentation docs/DEPLOY_MESH.md
ENV KEYCLOAK_HOME="/keycloak"
ENV KC_BOOTSTRAP_ADMIN_USERNAME="neardatachange"
ENV KC_BOOTSTRAP_ADMIN_PASSWORD="Ch4n63Pa55w0rd"
ENV KC_DB_SCHEMA=keycloak
ENV KC_DB_URL='jdbc:mariadb://mariadb/keycloak?user=kcadmin&password=1qaz2wsx3EDC'
ENV KC_DB=mariadb
ENV KC_HTTPS_CERTIFICATE_FILE=/keycloak/cert.pem
ENV KC_HTTPS_CERTIFICATE_KEY_FILE=/keycloak/key.pem

###################################
# configuration preparation prior to sconification
RUN pwd; \
    JAVA=$JAVA_HOME/bin/java.native kc.sh build --db=$KC_DB --features=preview --features=passkeys; \
    JAVA=$JAVA_HOME/bin/java.native kc.sh show-config;

###################################
# server credentials embedded into the image
ARG CN
ENV CN $CN
RUN openssl req -x509 -newkey rsa:2048 -keyout $KC_HTTPS_CERTIFICATE_KEY_FILE -out $KC_HTTPS_CERTIFICATE_FILE -sha256 -days 365 -nodes -subj "/C=EU/ST=ES/L=Tarragona/O=Neardata/OU=Broker/CN=$CN"

###################################
# FSPF creation
WORKDIR /

COPY ./files/make_fspf.demo.sh /make_fspf.demo.sh
RUN set -eux; \
    chmod +x /make_fspf.demo.sh; \
    /make_fspf.demo.sh

###################################
WORKDIR /keycloak
ENTRYPOINT ["kc.sh"]
CMD ["kc.sh", "start-dev", "--verbose", "start", "--hostname=$CN", "--http-enabled=true", "--features=preview", "--features=passkeys"]
