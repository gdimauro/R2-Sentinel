# Progetto: Sistema robotico di rilevamento e intervento su infestanti

**Nome in codice:** R2-Sentinel
**Versione documento:** 0.3
**Ultimo aggiornamento:** 23 agosto 2026
**Stato progetto:** Definizione architettura — stampante scelta, in acquisto

---

## 0. Come usare questo documento

Questo è il documento master del progetto. È scritto per permettere a chiunque (incluso te stesso fra sei mesi, o un collaboratore, o un'altra sessione AI) di **ricostruire il contesto completo da zero** senza dover ripercorrere conversazioni.

Regole di manutenzione:

- Ogni decisione tecnica va nel **Decision Log (§3)** con la motivazione, non solo l'esito. La motivazione è la parte che serve quando in futuro qualcuno chiede "perché non abbiamo fatto X?".
- Le cose che non sappiamo ancora vanno in **Questioni aperte (§10)**, non lasciate implicite.
- Quando una questione aperta si risolve, si sposta nel Decision Log e si aggiorna il changelog.
- Incrementare la versione documento a ogni sessione di lavoro.

### Changelog

| Ver. | Data | Modifiche |
|---|---|---|
| 0.1 | 2026-08-23 | Prima stesura. Architettura a due unità, scelta stampante, strategia produzione, BOM preliminare. |
| 0.2 | 2026-08-23 | **Stampante decisa: P2S Combo** (rivista la raccomandazione P1S). Accessori rivisti di conseguenza. Aggiunta D-11 su supporti multi-materiale, con impatto su §7.2. |
| 0.3 | 2026-08-23 | **Nome deciso: R2-Sentinel** (D-12), questione chiusa in §10. Igiene repository: riferimenti al documento master corretti, `.gitignore` e `.gitattributes` (Git LFS su `cad/export/`), primo commit. |

---

## 1. Obiettivo

Realizzare un sistema autonomo capace di:

1. **Riconoscere visivamente** bersagli infestanti su un range dimensionale molto ampio — da piccioni (~30 cm) a zanzare (~3 mm di corpo, ~15 mm di apertura alare).
2. **Intervenire fisicamente** sul bersaglio rilevato.
3. **Operare in due ambienti:** interno abitazione + balcone/terrazzo.
4. **Ricaricarsi autonomamente** e muoversi negli spazi interni.

Vincolo di realizzazione: prototipazione con **stampa 3D FDM in casa**, con ricorso a un **service esterno** solo per i componenti che l'FDM non può produrre adeguatamente.

---

## 2. Vincoli non negoziabili

Questi vincoli sono emersi dall'analisi iniziale e condizionano l'intera architettura. Non sono preferenze: sono limiti legali e di sicurezza.

### 2.1 Piccioni — solo dissuasione non cruenta

- Il piccione di città (*Columba livia*) rientra nella **fauna selvatica tutelata dalla Legge 157/1992**.
- Ucciderlo o maltrattarlo "per crudeltà o senza necessità" costituisce **reato** ai sensi del codice penale (artt. 544-bis e 727 c.p.).
- Sono ammessi **esclusivamente metodi di dissuasione non cruenti**. Alcuni comuni (es. Milano) hanno inoltre ordinanze che vietano specificamente i dissuasori pericolosi, inclusi i comuni dissuasori ad aghi.
- **Implicazione progettuale:** il payload rivolto ai piccioni deve essere non lesivo (getto d'aria, nebulizzazione, stimolo sonoro/visivo). Nessun contatto lesivo, nessun proiettile, nessuna trappola.
- **Da verificare:** regolamento del proprio comune, che può essere più restrittivo della norma nazionale.

### 2.2 Zanzare — nessun sistema laser

Il laser (approccio tipo *Photonic Fence*) è **escluso dal progetto**. Motivazione tecnica:

- Per abbattere una zanzara in volo serve un laser di **classe 4**, potenza dell'ordine dei watt.
- Su un dispositivo **mobile**, che **punta bersagli in movimento**, in ambiente domestico con persone e animali: il danno retinico è permanente e avviene in millisecondi, senza possibilità di reazione riflessa. Si aggiunge il rischio di innesco su tessuti e materiali.
- Nessuna schermatura o interlock realizzabile in autocostruzione rende accettabile questo rischio.

**Alternativa adottata:** aspirazione meccanica con esca (§4.3).

### 2.3 Alimentazione

- Il concetto iniziale di "braccetto che si collega a una presa a muro a 230 V" è **abbandonato**: complessità meccanica alta e rischio elettrico non gestibile in autocostruzione.
- **Sostituito da:** dock di ricarica a pavimento con contatti a molla e beacon IR (standard di fatto nella robotica domestica).

---

## 3. Decision Log

| # | Decisione | Motivazione | Data |
|---|---|---|---|
| D-01 | Architettura a **due unità separate** anziché un singolo robot | I due bersagli hanno requisiti incompatibili: il piccione richiede portata e mira all'aperto, la zanzara richiede prossimità e esca in interno. Un'unica macchina farebbe male entrambe le cose. | 2026-08-23 |
| D-02 | Unità balcone **fissa** (pan-tilt), non mobile | La mobilità all'aperto aggiunge tenuta stagna, vento, gestione dislivelli, senza alcun beneficio: il bersaglio si posa in punti prevedibili. | 2026-08-23 |
| D-03 | Zanzare: **attrazione, non inseguimento** | Volo erratico a 1–1,5 m/s, spesso a 2 m di quota. Un robot su ruote non intercetta. Esca (CO₂ + calore ~35 °C + octenolo) porta il bersaglio entro 20–30 cm, dove l'aspirazione funziona. | 2026-08-23 |
| D-04 | Rilevamento zanzare **acustico** come sensore primario | Il battito alare (400–600 Hz con armoniche caratteristiche) è una firma robusta rilevabile con un microfono MEMS da ~5 €. Rilevarla otticamente richiederebbe risoluzione <1 mm/pixel, cioè hardware da centinaia o migliaia di euro. Rapporto costo/efficacia incomparabile. | 2026-08-23 |
| D-05 | Camera **global shutter** per bersagli in volo | Con rolling shutter un soggetto in movimento rapido esce geometricamente deformato: il bounding box è instabile e la mira ne risente direttamente. | 2026-08-23 |
| D-06 | Attuazione pan-tilt con **stepper + riduzione a cinghia**, non servo hobby | Per colpire un bersaglio a 5 m con un getto d'aria serve una precisione angolare di ~1°. I servo hobby hanno gioco e deriva termica insufficienti; gli stepper ridotti 5:1 hanno margine abbondante. | 2026-08-23 |
| D-07 | Batteria **LiFePO4** anziché Li-ion NMC | Il robot naviga incustodito in ambiente domestico e si ricarica da solo. La chimica LiFePO4 non va in thermal runaway: è la scelta corretta per un dispositivo autonomo non sorvegliato. | 2026-08-23 |
| D-08 | Stampante: **Bambu Lab P2S Combo** | Vedi §8. Nota: la raccomandazione iniziale era la P1S, rivista al rialzo dopo aver verificato che l'AMS 2 Pro incluso nel Combo funge da essiccatore attivo e abilita i supporti multi-materiale (D-11) — due funzioni rilevanti per questo progetto, indipendenti dal multicolore. | 2026-08-23 |
| D-09 | CAD **parametrico (CadQuery)**, export STEP + STL | Lo stesso file genera la variante FDM e la variante SLS cambiando una variabile di tolleranza. Evita di mantenere due modelli divergenti. | 2026-08-23 |
| D-10 | Il **90% dei pezzi resta FDM in casa** anche in versione definitiva | Il service ha senso solo dove l'FDM fallisce fisicamente (§7). Un guscio grande costa 3–4 € in ASA stampato in casa contro 150–250 € in SLS, senza vantaggio funzionale. | 2026-08-23 |
| D-11 | Usare **interfacce di supporto in materiale diverso** (PETG sotto ASA) | L'AMS consente di stampare l'interfaccia di supporto in un materiale che non aderisce al pezzo: si stacca da sola lasciando superficie pulita. Rende stampabili in casa geometrie con sottosquadri prima destinate al service. **Impatto su §7.2: da rivalutare l'ugello convergente.** Costo: purge waste significativo a ogni cambio materiale. | 2026-08-23 |
| D-12 | Nome del progetto: **R2-Sentinel** | Chiude la prima questione aperta di §10. "Sentinel" descrive il comportamento reale di entrambe le unità — sorvegliano un'area e intervengono su un evento — senza promettere l'eliminazione del bersaglio, cosa che per i volatili sarebbe anche legalmente scorretta (§2.1). Il repository era già `R2-Sentinel`: la decisione allinea documento e repo anziché rinominare. | 2026-08-23 |

---

## 4. Architettura di sistema

### 4.1 Panoramica

```
UNITÀ A — "Balcone"                UNITÀ B — "Interno"
Fissa, pan-tilt                    Mobile su ruote
Bersaglio: piccioni                Bersaglio: zanzare
Payload: getto d'aria              Payload: aspirazione + esca
Alimentazione: rete                Alimentazione: batteria + dock
```

Le due unità condividono: stack software, toolchain CAD, approccio di detection, e possono dialogare via MQTT.

### 4.2 Unità A — Balcone / terrazzo

**Funzione:** rileva il piccione che si posa e attiva un getto d'aria compressa mirato.

**Perché funziona:** i dissuasori statici falliscono per assuefazione — il piccione impara che lo spaventapasseri è innocuo. Un intervento **contingente e mirato**, che si verifica solo quando l'animale si posa, non genera assuefazione perché mantiene l'associazione posa → conseguenza sgradevole. Ed è non lesivo, quindi conforme a §2.1.

**Componenti chiave:**
- Testa pan-tilt a 2 assi, stepper NEMA 17 con riduzione a cinghia GT2 5:1, finecorsa
- Camera RGB grandangolare per la scena + camera global shutter per il tracking
- Elettrovalvola 12 V, serbatoio 1–2 L a 5 bar, compressorino di ricarica, ugello convergente
- Carter in ASA, guarnizioni TPU, viti inox A2, pressacavi IP68

**Da valutare:** la nebulizzazione d'acqua come alternativa o complemento al getto d'aria. Più efficace ma va gestito il rapporto con i vicini e il ristagno.

### 4.3 Unità B — Interno

**Funzione:** si sposta nella stanza occupata, dispiega l'esca, rileva acusticamente le zanzare, aspira.

**Nota concettuale importante:** il robot **non insegue**. La mobilità serve a portare la trappola nel posto giusto al momento giusto (la stanza dove ci sono persone, cioè dove le zanzare convergono) e a rientrare al dock. La cattura è statica.

**Componenti chiave:**
- Base differenziale a 2 ruote motrici + ruota pazza
- Montante verticale ~120 cm che porta trappola e sensore acustico in quota (le zanzare stanno in alto, non a livello pavimento)
- Ventola centrifuga 12 V 80 mm + camera di raccolta con retina removibile
- Esca: resistenza a 35 °C + cartuccia CO₂ (alternativa a costo zero: fermentazione a lievito, ma richiede rabbocco periodico)
- LIDAR + ToF + IMU per navigazione
- Dock con contatti pogo e beacon IR

---

## 5. Bill of Materials (preliminare)

### 5.1 Calcolo

| Componente | Modello | Note | ~€ |
|---|---|---|---|
| SBC principale | Raspberry Pi 5 8 GB | | 90 |
| Acceleratore AI | AI HAT+ (Hailo-8L, 13 TOPS) | Regge YOLO11n a 30 fps | 90 |
| Microcontrollore | ESP32-S3 | Loop real-time motori/sensori; il Pi non è deterministico | 10 |

### 5.2 Visione

| Componente | Modello | Note | ~€ |
|---|---|---|---|
| Camera scena | Pi Camera Module 3 Wide (IMX708) | Detection generale | 35 |
| Camera tracking | Pi Global Shutter Camera (IMX296) | Obbligatoria per bersagli in volo — vedi D-05 | 55 |
| Ottica | C-mount 16 mm | | 30 |
| Illuminazione | Illuminatore IR 850 nm | Sagoma zanzara in controluce notturno | 20 |
| *(opzionale, alta gamma)* | Event camera Prophesee | Solo se si vuole tracking ottico serio delle zanzare | 3000+ |

### 5.3 Sensori

| Componente | Modello | Note | ~€ |
|---|---|---|---|
| Microfono | ICS-43434 o INMP441 (I2S) | FFT 300–800 Hz — sensore primario zanzare | 5 |
| LIDAR | RPLIDAR C1 | SLAM unità interna | 90 |
| ToF ×3 | VL53L5CX | Anti-ostacolo | 45 |
| IMU | BNO085 | | 30 |
| Encoder | Magnetici su ruote | Odometria | 20 |
| Ambiente | BME280 | Temp/umidità — correlano con attività zanzare | 8 |

### 5.4 Attuazione

| Componente | Modello | Note | ~€ |
|---|---|---|---|
| Trazione | 2× motoriduttore 37D 12 V 30:1 con encoder | | 80 |
| Driver trazione | DRV8871 ×2 | | 15 |
| Pan-tilt | 2× NEMA 17 + riduzione GT2 5:1 + finecorsa | Vedi D-06 | 70 |
| Getto d'aria | Elettrovalvola 12 V + serbatoio + compressore | | 90 |
| Aspirazione | Ventola centrifuga 12 V 80 mm | | 25 |
| Esca | Resistenza 35 °C + CO₂ | | 30 |

### 5.5 Alimentazione

| Componente | Modello | Note | ~€ |
|---|---|---|---|
| Batteria | LiFePO4 4S 10 Ah + BMS | Vedi D-07 | 120 |
| Convertitori | Buck 5 V e 12 V | | 20 |
| Dock | Contatti pogo + LED IR + TSOP38238 | | 15 |

### 5.6 Meccanica commerciale — NON stampare

Regola: prima di stampare o ordinare un pezzo, verificare se esiste commerciale. La meccanica di precisione comprata costa una frazione e funziona meglio.

- Cuscinetti, alberi rettificati Ø8 mm, pulegge GT2, cinghie
- Riduttori planetari per NEMA 17 (25–40 €, battono qualsiasi ingranaggio stampato)
- Corpo ottico C-mount, O-ring, pressacavi IP68
- Inserti filettati a caldo M3, viteria inox A2

---

## 6. Stack software

| Livello | Scelta |
|---|---|
| OS | Ubuntu 24.04 |
| Middleware | ROS 2 Jazzy |
| Navigazione | Nav2 |
| Mappatura | slam_toolbox |
| Livello motori | micro-ROS su ESP32 |
| Detection | Ultralytics YOLO11, export HEF per Hailo |
| Dataset | Roboflow |
| Integrazione | MQTT → Home Assistant |

**Nota sul dataset:** per i piccioni esistono dataset pubblici utilizzabili. Per le zanzare va costruito da zero — è realisticamente la parte più lunga del progetto software, stimare 2–3 settimane. Il rilevamento acustico (D-04) riduce molto la dipendenza da questo dataset.

---

## 7. Strategia di produzione

### 7.1 Cosa resta FDM in casa (anche definitivo)

- Tutti i carter e gusci, interni (PETG) ed esterni (ASA)
- Telaio base mobile, supporti motori, montante
- Camera di raccolta, condotti
- Paraurti e ruote (TPU)
- Tutte le staffe non caricate strutturalmente
- Dock di ricarica

### 7.2 Cosa mandare al service

| Pezzo | Perché | Processo |
|---|---|---|
| Corpo testa pan-tilt | Le layer lines FDM introducono gioco angolare che degrada la mira | SLS PA12 |
| Girante ventola centrifuga | Va bilanciata; l'FDM è anisotropo e vibra | SLS PA12 |
| Ugello convergente aria | Geometria interna curva, non stampabile senza supporti — **da rivalutare**: con le interfacce di supporto multi-materiale (D-11) potrebbe essere fattibile in casa. Tentare prima in FDM. | SLS o resina |
| Porta-camera / alloggiamento ottica | Tolleranze <0,1 mm sull'asse ottico | SLS o CNC alluminio |
| Cerniere e coperchi a scatto esterni | Devono flettere per migliaia di cicli senza delaminare | SLS PA12 / MJF |

### 7.3 Progettazione a doppia variante

Parametri da esporre nel CAD:

| Parametro | FDM | SLS |
|---|---|---|
| `clearance` | 0,20 mm | 0,35 mm (la polvere adiacente sinterizza, i fori escono stretti) |
| Spessore minimo parete | 1,2 mm | 0,8 mm |
| Vincoli geometrici | Direzione di stampa e supporti | Nessuno — geometrie interne libere |

**Flusso raccomandato:** prototipare in FDM *anche* i pezzi destinati al service. Si verificano montaggio e ingombri con un pezzo da 2 €, e si ordina solo a geometria congelata.

### 7.4 Service

- **Craftcloud** — aggregatore, confronta decine di fornitori sullo stesso file
- **Weerg** (IT) — SLS/MJF e CNC, tempi rapidi
- **Xometry**, **Protolabs Network** — Europa
- **JLC3DP** — circa un terzo del costo, 2–3 settimane di attesa

**Caricare sempre STEP, non STL:** molti fornitori quotano meglio e non si perdono le tolleranze.

### 7.5 Materiali

| Uso | Materiale |
|---|---|
| Prototipi rapidi di forma | PLA |
| Parti funzionali interne | PETG |
| Tutto l'esterno | **ASA** (resistenza UV) |
| Paraurti, guarnizioni, ruote | TPU 95A |
| Staffe sotto carico | PETG-CF / PA-CF |
| Pezzi definitivi da service | SLS PA12 / MJF |

---

## 8. Stampante — decisione

### 8.1 Requisiti

1. **Camera chiusa, obbligatoria.** L'unità esterna va in ASA, e l'ASA a camera aperta si delamina per ritiro differenziale. Questo esclude tutta la fascia entry-level aperta.
2. **Ugello ≥300 °C** per ASA e compositi caricati.
3. **Bassa manutenzione.** Questo è un progetto di robotica, non di stampa 3D: ogni ora spesa a tarare la stampante è un'ora sottratta al progetto vero.
4. Multicolore: **irrilevante**. Nessun pezzo di questo progetto lo richiede. Non pagare per questa feature.

### 8.2 Candidati (prezzi luglio 2026, variabili)

| Modello | Prezzo | Valutazione |
|---|---|---|
| **Bambu Lab P1S** | ~$699 | Chiusa, 300 °C, 256³ mm. La piattaforma enclosed più diffusa e con meno attriti. Ecosistema maturo. |
| Bambu Lab P2S | ~$799 (combo) | Aggiunge touch, camera AI, velocità. Il combo include il multicolore, che a noi non serve. |
| Elegoo Centauri Carbon 2 | ~$449 | Klipper aperto, hotend 350 °C, quattro colori inclusi, nessun cloud forzato. Ottimo valore, ma track record più corto: il modulo colore della prima Centauri Carbon fu promesso e poi cancellato. |
| Prusa CORE One+ | ~1.200 € | Ecosistema aperto e supporto a lungo termine. Premium di prezzo non giustificato qui. |
| Bambu Lab A1 / A1 mini | ~189 € | **Escluse:** aperte, ASA solo marginalmente supportato per stessa ammissione del produttore. |

### 8.3 Decisione: **Bambu Lab P2S Combo** ✅

Il criterio decisivo resta il requisito 3: il collo di bottiglia del progetto non sarà mai la stampante, sarà il dataset delle zanzare, la calibrazione della mira e il tuning di Nav2. La macchina deve essere un non-problema.

La raccomandazione iniziale era la P1S. È stata rivista al rialzo perché il Combo porta due funzioni che valgono su questo progetto **indipendentemente dal multicolore**, che resta irrilevante:

**a) L'AMS 2 Pro è un essiccatore attivo.** Essiccazione a 65 °C con ventilazione attiva e stoccaggio a tenuta d'aria: espelle l'umidità per circolazione esterna, non si limita al silica gel passivo. Elimina la voce "essiccatore separato" dal budget per ASA, PETG e PLA.
- **Limite noto:** alcuni filamenti richiedono temperature superiori e l'AMS 2 Pro non li asciuga completamente. Riguarda il **PA-CF**, per cui servirebbe un AMS HT o un essiccatore dedicato. Poco impattante: quei pezzi sono in gran parte destinati al service.

**b) Supporti in materiale diverso** — vedi D-11.

**Vantaggi aggiuntivi verificati:**
- Estrusore e ugello **già in acciaio temprato** di serie, pensati per i caricati in fibra → non servono ugelli temprati aftermarket
- **Quick-swap hotend a una clip**, senza scollegare cablaggi → cambio 0,4 ↔ 0,6 immediato
- **Adaptive Airflow** con alette + filtro a carbone integrato → il problema stirene dell'ASA è molto più contenuto rispetto alla P1S
- Nessun riscaldamento attivo della camera, ma un flap che commuta tra circolazione interna ed esterna: sufficiente per l'ASA
- Rilevamento guasti AI (spaghetti, grumi su ugello) → utile nelle stampe lunghe non presidiate
- Estrusore servo PMSM con rilevamento intasamenti in tempo reale

### 8.4 Accessori

| Accessorio | Stato | Perché |
|---|---|---|
| **Alimentatore ufficiale Bambu per AMS** (~30 €) | **Necessario** | Senza, avviando l'asciugatura la stampante non può riscaldare piatto/hotend né muovere gli assi: la priorità di alimentazione va all'AMS. Serve per asciugare *e* stampare in parallelo. |
| **Ugello 0,6 mm** | Consigliato | Dimezza i tempi sui pezzi strutturali dove il dettaglio fine è inutile |
| Piatti aggiuntivi (PEI liscio + testurizzato) | Consigliato | Evita fermi macchina tra le stampe |
| ~~Essiccatore separato~~ | **Non serve** | Incluso nell'AMS 2 Pro (eccetto PA-CF) |
| ~~Ugelli temprati~~ | **Non serve** | Di serie sulla P2S |
| Ventilazione del locale | Buona pratica | Il filtro integrato riduce molto il problema, ma il locale va comunque ventilato |

**Budget stampante completa: ~950–1000 €** (P2S Combo + alimentatore AMS + ugello 0,6 + piatti + primo stock filamento).

### 8.5 Note operative all'arrivo

- Rimuovere l'essiccante dal sacchetto sigillato **prima** di inserirlo nell'AMS (errore comune)
- Non bloccare le prese d'aria dell'AMS: aspirazione sotto, scarico dietro
- Usare **solo** l'alimentatore ufficiale — i danni da adattatori di terze parti non sono coperti da garanzia
- Attivare "protezione riscaldamento inattivo" e "rilevamento apertura porta"
- Prima di stampare ASA: asciugare il filamento, chiudere la porta, verificare che il flap sia in circolazione interna

---

## 9. Roadmap

| Fase | Obiettivo | Deliverable |
|---|---|---|
| **0. Setup** | Stampante operativa, profili materiali tarati | Provini di calibrazione in PLA, PETG, ASA + test interfaccia di supporto PETG-sotto-ASA (D-11) |
| **1. CAD testa pan-tilt** | Primo modulo parametrico | File CadQuery + STEP/STL, variante FDM e SLS |
| **2. Pan-tilt fisico** | Testa montata e mossa da ESP32 | Precisione angolare misurata, target ~1° |
| **3. Visione base** | Detection piccioni su video | YOLO11 su Hailo, fps e accuratezza misurati |
| **4. Integrazione Unità A** | Rilevamento → mira → getto | Prototipo funzionante da balcone |
| **5. Rilevamento acustico** | Firma zanzara classificata | FFT + classificatore, tasso di falsi positivi |
| **6. Trappola** | Cattura statica con esca | Efficacia misurata su n notti |
| **7. Base mobile** | Navigazione + docking | Nav2 + rientro autonomo |
| **8. Integrazione Unità B** | Sistema completo interno | |

Le fasi 1–4 e 5–8 sono largamente parallelizzabili se ti interessa: sono due macchine indipendenti.

---

## 10. Questioni aperte

- [ ] **Budget complessivo target** — non ancora definito; condiziona l'eventuale event camera e il ricorso al service SLS (la scelta stampante è chiusa in D-08)
- [ ] Regolamento comunale specifico sui dissuasori (§2.1) — da verificare
- [ ] Unità A: getto d'aria, nebulizzazione, o entrambi
- [ ] Esca CO₂: cartuccia (comoda, ricorrente) vs fermentazione (gratis, manutenzione)
- [ ] Autonomia target dell'Unità B — determina il dimensionamento batteria
- [ ] L'Unità A va alimentata da rete o autonoma? (rete è molto più semplice se c'è una presa esterna)
- [ ] Strategia di raccolta dataset zanzare
- [ ] Da quale modulo CAD partire: testa pan-tilt (raccomandato) o telaio base mobile
- [ ] Gestione dello svuotamento della camera di raccolta

---

## 11. Riferimenti

**Normativa**
- Legge 157/1992 — fauna selvatica
- Artt. 544-bis, 727 c.p. — uccisione e maltrattamento di animali
- Ordinanze comunali locali sui dissuasori

**Tecnici**
- Frequenza battito alare *Culex* / *Aedes*: 400–600 Hz
- Velocità di volo zanzara: 1–1,5 m/s
- Precisione angolare richiesta a 5 m per getto mirato: ~1°

**Fornitori**
- Craftcloud, Weerg, Xometry, Protolabs Network, JLC3DP
