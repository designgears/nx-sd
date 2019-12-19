FROM devkitpro/devkita64_devkitarm:20190720

ENV PATH=/usr/local/bin:/usr/local:$PATH

RUN dkp-pacman -Scc --noconfirm

RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install zlib1g-dev libbz2-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev -y

WORKDIR /usr/src

RUN wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
RUN tar xzf Python-3.7.2.tgz

WORKDIR /usr/src/Python-3.7.2

RUN ./configure
RUN make altinstall
RUN ln -s /usr/local/bin/python3.7 /usr/local/bin/python3

WORKDIR /developer/components/Checkpoint

ENTRYPOINT ["make", "-j8", "switch"]
