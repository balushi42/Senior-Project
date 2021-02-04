FROM ubuntu:18.04

RUN apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends software-properties-common \
    sudo curl wget cmake pkg-config locales git gcc-8 g++-8 build-essential \
    openssl libssl-dev libjsoncpp-dev uuid-dev zlib1g-dev libc-ares-dev\
    postgresql-server-dev-all libmariadbclient-dev libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8

WORKDIR /app

RUN git clone https://github.com/an-tao/drogon && \ 
    cd drogon && \
    git submodule update --init && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && make install 

RUN drogon_ctl create project application_name  

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    CC=gcc-8 \
    CXX=g++-8 \
    AR=gcc-ar-8 \
    RANLIB=gcc-ranlib-8 \
    BOOST_INCLUDE_DIR="${HOME}/opt/boost_1_67_0" \  
    IROOT=/install
ARG DEBIAN_FRONTEND=noninteractive

ADD deploy.sh ./app/deploy.sh  

RUN chmod +x ./app/deploy.sh  

EXPOSE 8080

CMD sh ./app/deploy.sh && tail -f /dev/null