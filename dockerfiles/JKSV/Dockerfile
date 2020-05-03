FROM devkitpro/devkita64:20200405

RUN dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/JKSV

ENTRYPOINT ["make", "-j8"]
