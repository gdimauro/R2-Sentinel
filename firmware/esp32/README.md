# firmware/esp32

Firmware ESP32-S3. **Owner del contenuto: `mechatronics`.**
Questo scheletro e' di `software-platform` e serve a garantire che la toolchain
si ricostruisca e che il firmware compili da zero.

## Costruire

```bash
./scripts/bootstrap.sh --only idf     # una volta sola, installa ESP-IDF
. "$IDF_PATH/export.sh"               # oppure: get_idf
cd firmware/esp32 && idf.py build
```

Oppure, senza pensarci:

```bash
make firmware
```

## Versioni

Fissate in [`firmware/toolchain.yaml`](../toolchain.yaml). Non aggiornarle in
locale: e' un cambio di piattaforma e passa dal Decision Log (§3).

## Cosa NON committare

`sdkconfig` (generato) e `build/` sono in `.gitignore`.
I default condivisi stanno in `sdkconfig.defaults`, che invece e' versionato.
