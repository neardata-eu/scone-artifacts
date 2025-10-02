FROM ubuntu:24.04 AS builder

RUN apt-get -y update --allow-insecure-repositories
RUN apt-get -y install openjdk-11-jre
RUN java -version
RUN apt-get -y install vim
RUN apt-get -y install python3
RUN apt-get -y install python3-yaml
RUN apt-get -y install git
RUN apt-get -y install maven

ADD omb           /app/omb/
ADD prb           /app/prb/
ADD run.sh        /app/
ADD messages.py   /app/
ADD config_omb.py /app/
ADD config_prb.py /app/
ADD test_case.csv /app/

RUN git clone https://github.com/rcrane/om-benchmark.git ben
RUN cd ben && mvn clean verify package -X -DskipTests -Dspotbugs.skip=true -Dlicense.skip -Dcheckstyle.skip -Dspotless.check.skip -Djacoco.skip

FROM registry.scontain.com/sconecuratedimages/apps:18-ea-jdk-alpine-scone5.9
COPY --from=builder /app /app
COPY --from=builder /ben /ben

RUN mv /ben/package/target/openmessaging-benchmark-0.0.1-SNAPSHOT-bin.tar.gz /app/
RUN cd /app/ && tar -xzvf openmessaging-benchmark-0.0.1-SNAPSHOT-bin.tar.gz

ENV SCONE_VERSION=1
ENV SCONE_FORK=0
ENV SCONE_HEAP=12G
ENV SCONE_LOG=DEBUG

WORKDIR /app
ENTRYPOINT ["tail", "-f", "/dev/null"]
