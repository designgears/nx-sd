FROM devkitpro/devkita64:20200405

RUN dkp-pacman -Syu libnx --noconfirm
RUN dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/sys-clk/sysmodule

ENTRYPOINT ["make", "-j8"]
