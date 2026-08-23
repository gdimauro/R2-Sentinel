# Piattaforma software — manuale operativo

Proprietario: `software-platform`. Questo documento descrive **come si costruisce
e come si verifica** il software di R2-Sentinel. Il *perche'* delle scelte sta
nel Decision Log (`docs/PROJECT.md` §3), non qui.

Criterio guida: **se un risultato non si riproduce su una macchina pulita con un
comando, non e' un risultato — e' un aneddoto.**

---

## 1. Primo giorno

```bash
git clone <repo> && cd R2-Sentinel
./scripts/bootstrap.sh
```

Un comando. Ubuntu 24.04. Al termine hai: workspace ROS 2 Jazzy compilato,
toolchain ESP-IDF installata, ambiente Python di piattaforma, hook git attivi.
Budget: 30 minuti.

Su macOS o Windows lo script si ferma prima di ROS e ti indirizza al container:

```bash
make docker-shell     # Ubuntu 24.04 vergine con il repo montato
make verify-clean     # bootstrap completo in container, due volte
```

Se `bootstrap.sh` fallisce, **non aggiustare a mano sulla tua macchina**: e' un
difetto dello script e va corretto li', altrimenti fallira' anche al prossimo.

### Cosa fa, passo per passo

| Passo | Script | Cosa installa |
|---|---|---|
| 1 | `scripts/setup/10_system.sh` | pacchetti apt, regole udev per ESP32 |
| 2 | `scripts/setup/20_git_lfs.sh` | git-lfs + verifica del **gate 0** |
| 3 | `scripts/setup/30_ros2.sh` | ROS 2 Jazzy, Nav2, slam_toolbox, rosdep |
| 4 | `scripts/setup/40_python.sh` | `.venv` con gli strumenti di piattaforma |
| 5 | `scripts/setup/50_esp_idf.sh` | ESP-IDF alla versione di `firmware/toolchain.yaml` |
| 6 | `scripts/setup/60_workspace.sh` | `colcon build` + verifica dei 6 pacchetti |
| — | `scripts/setup/70_git_hooks.sh` | `core.hooksPath` sugli hook versionati |

Ogni passo si rilancia da solo: `./scripts/bootstrap.sh --only ros`.

---

## 2. Comandi

`make help` li elenca tutti. I cinque che userai davvero:

| Comando | Cosa fa |
|---|---|
| `make check` | igiene del repository + schema MQTT + gate 0 |
| `make test` | test che non richiedono hardware |
| `make fatto ROLE=<ruolo>` | esegue i criteri di FATTO di un ruolo |
| `make build` | ricompila il workspace |
| `make firmware` | compila il firmware ESP32-S3 da zero |

---

## 3. Cosa non entra nel repository

Non e' una preferenza di ordine: e' privacy e igiene della history.
**Da Git la history non si cancella davvero.**

| Categoria | Dove sta invece |
|---|---|
| Pesi (`*.pt`, `*.onnx`, `*.hef`) | `models/MANIFEST.yaml` → `make models` |
| Dataset | fuori dal repo; l'indice, che e' testo, resta versionato |
| Mappe SLAM (`*.pgm`, `*.posegraph`) | solo sul dispositivo: sono la planimetria di casa |
| Audio e riprese di interni | solo sul dispositivo |
| Credenziali | variabili d'ambiente (`R2S_MQTT_USER`, `R2S_MQTT_PASS`) |
| Export CAD (`*.step`, `*.stl`) | nel repo **ma via Git LFS** |

Tre barriere, in quest'ordine:

1. `.gitignore` — evita l'errore distratto
2. hook `pre-commit` — blocca prima che il commit esista
3. CI (`scripts/ci/check_hygiene.py`) — blocca la PR

Se ti accorgi che qualcosa di privato e' **gia'** stato committato: non
rimuoverlo con un commit successivo. Fermati, avvisa il chief-engineer, si
valuta un rewrite della history. Se sono credenziali, revocale subito.

---

## 4. Git LFS — gate 0

`.gitattributes` instrada `*.step`, `*.stp`, `*.stl`, `*.3mf`, `*.f3d` (e le
varianti maiuscole) verso LFS. **Quei filtri sono inerti se `git-lfs` non e'
installato**: il file entrerebbe in history come binario grezzo.

```bash
make lfs          # verifica ambiente, .gitattributes e history, con prova end-to-end
```

La prova crea un repository temporaneo, committa un finto `.step` da 1 MB e
verifica che l'oggetto in history sia un puntatore sotto i 200 byte.

---

## 5. Harness dei criteri di FATTO

Ogni criterio di FATTO dei ruoli ha **un comando**. Il registro e'
`tests/fatto/registry.yaml`.

```bash
./scripts/fatto.sh                     # tutto cio' che gira senza banco
./scripts/fatto.sh mechatronics        # un ruolo
./scripts/fatto.sh --list              # elenco con stato
./scripts/fatto.sh --coverage          # copertura per ruolo
R2S_BENCH=1 ./scripts/fatto.sh ...     # include le prove da banco
```

Tre regole di condotta dell'harness:

1. **Uno stub non passa mai.** Se il test non e' scritto, lo stato e' NON
   IMPLEMENTATO. Un verde falso e' peggio di un rosso.
2. **Una prova da banco senza banco viene SALTATA con il motivo**, mai fallita
   in silenzio e mai passata.
3. **Un criterio bloccato da una questione aperta lo dichiara** (`blocked_by`).

### Aggiungere un criterio

Aggiungi una voce al registro con `id`, `role`, `criterio`, `metric`, `kind`
(`ci`/`bench`/`manual`), `status` e `command`. `tests/ci/test_registry_integrity.py`
verifica che il registro resti coerente e che ogni criterio abbia un comando.

### Test da banco

Marca con `@pytest.mark.bench` e `@pytest.mark.hardware("<dispositivo>")`.
In CI vengono saltati con il motivo scritto nel report. Esempio completo:
`tests/bench/test_example_bench.py`.

### Misure fatte a mano

```bash
scripts/measure/record.py --criterio mech-g0-warping --valore 0.22 --note "provino 3"
```

Il dato finisce in `measurements/<criterio>.yaml` con data e operatore, e il
comando verifica la soglia presa dal registro. Un numero senza data e senza
operatore non e' una misura.

---

## 6. CI

`.github/workflows/ci.yml`, budget 10 minuti per PR, quattro job in parallelo:

| Job | Cosa verifica |
|---|---|
| `hygiene` | gate 0, igiene del diff, history, Decision Log, nota di conformita', schema MQTT |
| `host-tests` | test senza hardware, lint, copertura dell'harness |
| `ros2-build` | `colcon build` + `colcon test` in container Jazzy |
| `firmware` | il firmware ESP32-S3 compila da zero |

La CI **fallisce** se nel diff compare: un peso, un dataset, una mappa SLAM, un
file audio, una credenziale, un export CAD non passato da LFS, un binario oltre
5 MB, un cambio architetturale senza riga nel Decision Log, un topic MQTT non
documentato, o una modifica al payload senza traccia della nota di conformita'.

Ognuna di queste regole ha un test che la prova **a fallire**:
`tests/ci/test_hygiene_rules.py`.

`.github/workflows/reproducibility.yml` verifica ogni notte il bootstrap su
container vergine, **due volte**.

---

## 7. MQTT

Il livello MQTT e' il confine fra le due unita' e il mondo. Sorgente unica:
`software/ros2_ws/src/r2s_mqtt_bridge/config/topics.yaml`.
Documentazione **generata**: [`docs/interfaces/MQTT.md`](interfaces/MQTT.md)
(`make mqtt-docs`).

Non descrivere un topic altrove: la CI fallisce se il codice usa un topic che
non e' nello schema, e se la documentazione generata e' disallineata.
