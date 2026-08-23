# Macchina VERGINE Ubuntu 24.04. Volutamente quasi vuota: se il bootstrap ha
# bisogno di qualcosa, deve installarselo lui. Ogni pacchetto messo qui e' un
# passo manuale nascosto che sulla macchina di un collaboratore non ci sara'.
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive TZ=Europe/Rome

# Il minimo per fare git clone ed eseguire uno script. Niente altro.
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends \
        ca-certificates git sudo locales tzdata \
    && rm -rf /var/lib/apt/lists/*

# Utente non root con sudo: e' la situazione reale di chi installa.
RUN useradd -m -s /bin/bash dev && echo 'dev ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/dev
USER dev
WORKDIR /home/dev/R2-Sentinel
CMD ["/bin/bash"]
