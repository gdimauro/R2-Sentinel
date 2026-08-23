# Libro mastro

Contabilità giornaliera delle tre valute del progetto (vedi `BUSINESS.md` §1).
Aggiornato a ogni sessione di lavoro. **Ciò che è misurato è marcato come
misurato; ciò che è stimato è marcato come stimato.** Non si mescolano.

---

## 1. Metodo

**Cosa è misurabile con precisione:** il consumo di ogni agente lanciato in
sessione, che riporta il proprio totale a fine esecuzione.

**Cosa non lo è, oggi:** il consumo della sessione principale (la conversazione
di coordinamento). Non c'è un contatore per-turno esposto. Va richiesto a fine
giornata con `/cost`, oppure ricavato dal budget residuo, e trascritto qui.

**Regola:** una riga senza fonte del dato è una riga inutile. Ogni voce dichiara
se viene da un report di agente (**M**, misurato), da `/cost` (**M**), o da
stima (**S**).

**Piano: Claude Max 20× (200 $/mese).** I token non hanno costo marginale: si
consuma **capienza** (finestra mobile di 5 ore + tetto settimanale), non denaro.
Il libro mastro li conta comunque, perché la capienza esaurita blocca il lavoro
esattamente come farebbe un budget finito.

**Budget: monte settimanale di ~5.250.000 token** (dal 2026-08-24; prima era
750.000/giorno). Non si accumula fra una settimana e l'altra — la capienza non
spesa evapora — ma **dentro la settimana si sposta liberamente**: una giornata
intensa seguita da giornate ferme è la forma attesa, non uno sforamento.

Il numero da sorvegliare è **quanto resta della settimana rispetto ai giorni al
reset**, non il consumo del giorno. Non si accumula:
il non speso è perso, quindi il valore sta nel *quando* si spende, non nel
risparmiare.

---

## 2. Registro giornaliero — token

| Data | Voce | Token | Fonte | Prodotto |
|---|---|---|---|---|
| 2026-08-23 | `chief-engineer` — costruzione squadra, 6 agenti + D-13/D-14 + §10 | 83.366 | M | 6 file agente, 2 decisioni, 4 questioni aperte |
| 2026-08-23 | `chief-engineer` — addendum, `software-platform` + `design-docs` + D-15 | *non rilevato* | — | 2 file agente, 1 decisione |
| 2026-08-23 | Sessione principale — igiene repo, primo commit, squadra, sinottico, giornale, piano economico | *da rilevare con* `/cost` | — | 3 PR-equivalenti di documenti, 1 artefatto pubblicato |
| | **Totale misurato del giorno** | **83.366** | | *parziale — due voci non rilevate* |
| | **Budget giornaliero** | **750.000** | | ~9 operazioni da 83k, o 5–15 sessioni di lavoro |

### ⚠ Perché il budget giornaliero è stato sostituito

Il tetto era **750.000 token/giorno**. I soli agenti misurati fanno **322.870**,
ma tre voci non sono state rilevate e — soprattutto — **la capienza settimanale
si è esaurita nel pomeriggio**, con reset annunciato al 25 agosto. Il consumo
reale della giornata è quindi molto oltre i 750k.

La causa è identificabile: **quattro agenti lanciati in parallelo**. Il costo
non era visibile al momento del lancio, e il tetto giornaliero non lo ha
intercettato perché il vincolo vero è la **finestra mobile di 5 ore**, non il
totale del giorno.

**Prima conseguenza (24 agosto):** il contatore giornaliero è stato sostituito
da un monte settimanale, perché non misurava il vincolo reale.

**Seconda conseguenza (P-04, in attesa di decisione dello sponsor):**
massimo **due agenti in parallelo**, salvo motivazione esplicita. E ciò che il
coordinamento può fare in linea — come la verifica dell'ammanco del 9%, chiusa
con una prova sintetica in pochi secondi — non va delegato a un agente.

> ⚠ **Debito contabile del giorno 1.** Due voci su tre non sono state rilevate
> perché la contabilità è stata istituita a giornata in corso. È il tipo di
> buco che rende inutile un libro mastro se si ripete: da domani ogni sessione
> si chiude rilevando il consumo **prima** di terminare.

### Consuntivo contro stima

| Operazione | Stima in `BUSINESS.md` | Reale | Scarto |
|---|---|---|---|
| Riorganizzazione / arbitrato di confine (`chief-engineer`) | 60–100k | 83.366 | dentro la forchetta |

---

## 3. Acquisti — da fare

Ordinati per **ciò che sblocca**, non per costo.

### Priorità 1 — scade

> **Correzione del 23 agosto, seconda stesura.** La prima versione ordinava gli
> acquisti per *ciò che sbloccano*. È l'ordine sbagliato: l'anemometro serve al
> gate della fase 4, che è a mesi di distanza, mentre la finestra stagionale
> delle zanzare si chiude fra settimane. **L'ordine corretto è per scadenza.**

Il microfono di misura non serve solo come riferimento: è anche il **banco di
registrazione di partenza**. Collegato a un portatile permette di iniziare le
notti *questa settimana*, mentre l'ICS-43434 e il Raspberry Pi non sono ancora
stati ordinati. È l'unico acquisto che compra tempo che altrimenti si perde.

| # | Voce | Perché | € stimato | Stato |
|---|---|---|---|---|
| S-03 | **Microfono di misura calibrato USB** (classe UMIK-1) | Riferimento sui 400–600 Hz **e banco di registrazione immediato**: apre le notti prima che il resto dell'Unità B esista | 120–160 | ⚠ **Ordinare per primo** |

### Priorità 2 — sblocca la verificabilità, ma non scade

Senza questi, nessun criterio di FATTO è misurabile e **nessuna fase si può
dichiarare chiusa**. Servono però ai gate delle fasi 2 e 4, non a settembre.

| # | Voce | Perché | € stimato | Stato |
|---|---|---|---|---|
| S-01 | Anemometro a filo caldo 0–30 m/s, datalog CSV, attacco treppiede | Getto 8–25 m/s a 5 m su griglia 5×5 e aspirazione ≥2,0 m/s a 25 cm. **Mai vicino all'ugello: a 5 bar il convergente va in flusso critico** | 250–400 | Serve al gate F4 |
| S-02 | Analizzatore logico USB 8 canali 24 MHz | Jitter del loop firmware ≤100 µs a 1 kHz | 10–25 | Serve al gate F2 |
| S-04 | Modulo laser + treppiede + bersaglio stampato | Riferimento angolare a 5 m — **si costruisce, non si compra** | 20–40 | Serve al gate F2 |

### Priorità 3 — quando parte la fase 0

| # | Voce | € | Stato |
|---|---|---|---|
| S-05 | Bambu Lab P2S Combo + alimentatore AMS + ugello 0,6 + piatti + filamento | ~975 | Deciso (D-08), in acquisto |

### Priorità 3-bis — materiali e consumabili (ricorrente)

> **Voce mancante nella prima stesura.** Il piano contava la stampante ma non i
> materiali, se non come «primo stock» dentro i 975 €. È una sottostima: il
> filamento è un **costo ricorrente per tutta la durata del progetto**, non un
> acquisto iniziale.

**Set di partenza — fase 0**, i cinque materiali che §7.5 prescrive:

| Materiale | Uso | kg | € |
|---|---|---|---|
| PLA | Prototipi rapidi di forma | 1 | ~22 |
| PETG | Parti funzionali interne **e interfacce di supporto sotto ASA (D-11)** | 2 | ~55 |
| ASA | Tutto l'esterno, resistenza UV | 1 | ~38 |
| TPU 95A | Paraurti, guarnizioni, ruote | 1 | ~40 |
| **Totale set di partenza** | | **5** | **~155** |

**Caricati — dalla fase 2**, solo staffe sotto carico:

| Materiale | Nota | € |
|---|---|---|
| PETG-CF | Staffe strutturali | ~50 |
| PA-CF | *L'AMS 2 Pro non lo asciuga adeguatamente (§8.3)* — valutare se serve davvero o se va al service | ~80 |

**Consumo per la durata del progetto:** i gusci dell'Unità A e il telaio
dell'Unità B sono pezzi grandi, e ogni iterazione di prototipazione si ristampa.
Stima realistica **8–15 kg complessivi**, cioè **250–500 €** di filamento sull'intero
progetto, set di partenza incluso.

**Sovrapprezzo da purge waste (D-11).** Le interfacce di supporto in materiale
diverso comportano uno spurgo a ogni cambio: sui pezzi multi-materiale il
consumo effettivo può salire del **20–40%** rispetto al peso del pezzo. È il
costo esplicitamente accettato in D-11, ma finora non era stato messo a
bilancio.

**Consumabili minori:** alcol isopropilico, stick di adesione, ricambio ugelli
0,4/0,6 — ~50 € sull'arco del progetto.

---

### Priorità 4 — a geometria congelata

| # | Voce | € | Stato |
|---|---|---|---|
| S-06 | BOM elettronica e meccanica (§5 di PROJECT.md) | ~993 | Non ordinare prima della fase 1 |
| S-07 | Service SLS per i pezzi che l'FDM non può fare (§7.2) | da quotare | Solo a geometria congelata |

### Escluso salvo ripensamento

| Voce | € | Motivo |
|---|---|---|
| Event camera Prophesee | 3.000+ | D-04 rende il tracking ottico delle zanzare non necessario |

---

## 4. Acquisti — fatti

*(nessuno alla data odierna)*

**Tutti gli acquisti vanno fatti con fattura intestata** — vedi `ACQUISTI.md`.
Una riga senza estremi di fattura è una riga incompleta.

| Data | Voce | € | Fornitore | N. fattura | Note |
|---|---|---|---|---|---|

---

## 5. Totali

| Voce | € |
|---|---|
| Speso a oggi | **0** |
| Strumenti di misura (S-01..S-04) | 400–625 |
| Stampante e accessori | ~975 |
| **Materiali e consumabili, intero progetto** | **300–550** |
| BOM elettronica e meccanica | ~993 |
| Service SLS | da quotare |
| **Capitale totale previsto** | **~2.670–3.140** |

**Due correzioni rispetto a `BUSINESS.md` (~1.970),** entrambe per voci che
quella stima non comprendeva:

1. **Strumenti di misura** (+400–625) — senza, nessun gate chiude.
2. **Materiali e consumabili** (+300–550) — il filamento è ricorrente, non
   un acquisto iniziale, e il purge waste di D-11 lo aggrava.

La cifra da usare per pianificare è **~2.700–3.100 €**, esclusi service SLS e
imprevisti.

---

## 6. Che cosa compra il budget di oggi

Il progetto è in fase 0: comprare la stampante e tarare i profili è **euro e ore
tue**, non token. Il rischio del budget giornaliero è quindi di restare inutilizzato
proprio ora — e non si accumula.

Quattro lavori sono eseguibili **oggi, con zero hardware**:

| Agente | Lavoro | Token stimati |
|---|---|---|
| `software-platform` | Scheletro workspace ROS 2, CI, Git LFS, harness — tutto ciò su cui gli altri poi girano | 100–150k |
| `acoustic-perception` | Catena di registrazione e analisi pronta *prima* che il microfono arrivi | 80–120k |
| `compliance-safety` | Istruttoria del regolamento comunale (§10) — pura ricerca | 40–60k |
| `payload-fluidics` | Comparativa getto d'aria contro nebulizzazione (§10) — pura analisi | 60–100k |
| | **Totale** | **280–430k** |

Restano 320–470k di margine per la giornata. Il criterio non è consumarli: è
che nessuna di queste quattro voci resti ferma per mancanza di budget.

---

## 7. Ore-persona e calendario

La terza valuta, che non si compra.

| Voce | Stato |
|---|---|
| **Finestra stagionale zanzare** | ⚠ **Si chiude fra poche settimane.** Nessun budget la riapre. |
| Ore di assemblaggio e misura | Non ancora stimate — da fare a valle della fase 1 |
| Riprese per il documentario | ⚠ Nessuna a oggi. Il primo materiale recuperabile è l'arrivo della stampante. |
