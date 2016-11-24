FROM ubuntu:14.04

MAINTAINER Mitul Patel <mitul428@gmail.com>

LABEL version="v1.0"

RUN mkdir demo

# Update the repository sources list
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y  software-properties-common && \
    add-apt-repository ppa:webupd8team/java -y && \
    apt-get update && \
    echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections && \
    apt-get install -y oracle-java7-installer && \
    apt-get clean


# Install software 
RUN apt-get install -y git && \
	apt-get install -y wget && \
	apt-get install -y zip && \
	apt-get install -y gzip && \
	apt-get install -y alien


# Install BBmap
RUN wget https://sourceforge.net/projects/bbmap/files/BBMap_36.62.tar.gz && \ 
	tar -zxvf BBMap_36.62.tar.gz && \
	rm BBMap_36.62.tar.gz 
	

ENV PATH /bbmap:$PATH
ENV PATH /usr/local/bin:$PATH

RUN chmod -R +x /demo

#CMD ["bash", "/bbmap/stats.sh"]

ENTRYPOINT ["/bbmap/stats.sh"]