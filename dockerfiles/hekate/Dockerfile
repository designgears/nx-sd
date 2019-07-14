FROM devkitpro/devkita64_devkitarm:20190510

ENV DEVKITARM=${DEVKITPRO}/devkitARM

COPY ./compile.sh /compile.sh

RUN chmod a+x /compile.sh

RUN dkp-pacman -Syyu --noconfirm --needed && \
    dkp-pacman -Scc --noconfirm

RUN apt update && \
    apt -y install gcc python

RUN git clone https://github.com/SciresM/hactool.git
RUN git clone https://github.com/m4xw/emuMMC.git

WORKDIR /hactool

RUN cp config.mk.template config.mk && \
    make -j8

WORKDIR /emuMMC

RUN make -j8 && \
    /hactool/hactool -t kip emummc.kip --uncompressed emummc_unpacked.kip && \
    python tools/kip1converter.py emummc_unpacked.kip emummc.data && \
    cat emummc.caps emummc.data > emummc.kipm

WORKDIR /developer/components/hekate

ENTRYPOINT ["/compile.sh"]
