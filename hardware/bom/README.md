# hardware/bom — BOM e registro dei certificati

Questa directory ospita due cose distinte:

1. la **distinta materiali** operativa (in arrivo — vedi roadmap in
   `docs/PROJECT.md` §9), di competenza del chief-engineer;
2. il **registro dei certificati**, qui sotto, che è parte del **dossier di
   conformità** insieme a `SAFETY.md`.

---

## Registro dei certificati

**Regola, una sola.**

> **Un componente in pressione, la batteria e il BMS non entrano nel progetto
> senza il riferimento a un datasheet o a un certificato del fabbricante, con il
> valore nominale rilevante trascritto in questa tabella.**
>
> **"Il venditore dice che regge 8 bar" non è un certificato.** Una descrizione
> di marketplace, una recensione o una scheda prodotto senza fabbricante
> identificabile **non chiudono una riga**. Il documento deve provenire dal
> fabbricante o dal distributore ufficiale e deve riportare i valori numerici.

**Che cosa registrare per ogni riga**

| Campo | Contenuto |
|---|---|
| Fabbricante / codice | nome del fabbricante e codice prodotto — non "generico su marketplace" |
| Documento | titolo del datasheet, revisione, **URL o percorso del file locale** |
| Valore nominale | il numero che conta per la sicurezza, trascritto qui (non "vedi datasheet") |
| Data verifica | quando è stato letto il documento, e da chi |

Il PDF del datasheet **non va committato** se è materiale coperto da copyright
del fabbricante: si registra l'URL, il titolo e la revisione. Se il documento
rischia di sparire, se ne conserva una copia **fuori dal repository** e qui si
annota il percorso.

---

### A. Circuito in pressione — Unità A

**Stato: 0 / 9 coperte.** Blocca **G-PRESS** (`SAFETY.md` §4.6) e la voce
`VA-03`.

| # | Componente | Valore nominale richiesto | Fabbricante / codice | Documento | Valore rilevato | Verifica | Stato |
|---|---|---|---|---|---|---|---|
| P1 | **Serbatoio 1–2 L** | PS (bar), temperatura ammissibile, volume, **pressione di prova o di scoppio** | — | — | — | — | **APERTA** |
| P2 | **Valvola di sicurezza** | **pressione di taratura**, portata di scarico, tipo | — | — | — | — | **APERTA** |
| P3 | **Riduttore di pressione** | pressione max in ingresso, campo di regolazione in uscita | — | — | — | — | **APERTA** |
| P4 | **Manometro** | fondo scala, **classe di precisione** | — | — | — | — | **APERTA** |
| P5 | **Elettrovalvola 12 V** | pressione max di esercizio, **posizione di riposo = normalmente chiusa**, coefficiente di portata, tensione | — | — | — | — | **APERTA** |
| P6 | **Tubi** | pressione di esercizio **e di scoppio** (richiesto **scoppio ≥ 3 × PS**), temperatura, raggio minimo di curvatura | — | — | — | — | **APERTA** |
| P7 | **Raccordi e innesti rapidi** | pressione max di esercizio, compatibilità con il diametro del tubo | — | — | — | — | **APERTA** |
| P8 | **Compressore di ricarica** | **pressione massima erogabile**, portata, presenza e taratura del **pressostato** | — | — | — | — | **APERTA** |
| P9 | **Ugello** | se è elemento in **pressione** o in **scarico** — determina se può essere FDM (`SAFETY.md` §4.4, `VA-06`) | — | — | — | — | **APERTA** |

**Regola dell'anello debole.** La pressione massima ammissibile del circuito è
il **minimo** dei PS delle righe P1…P9, non il PS del serbatoio. La taratura di
P2 si sceglie su quel minimo.

`PS_circuito = min(P1…P9) = ` **non determinabile: 0 righe coperte**

---

### B. Circuito in pressione — Unità B (esca CO₂)

**Stato: 0 / 2 coperte.** Blocca il gate di **fase 6**.

| # | Componente | Valore nominale richiesto | Fabbricante / codice | Documento | Valore rilevato | Verifica | Stato |
|---|---|---|---|---|---|---|---|
| P10 | **Cartuccia CO₂** | pressione della cartuccia, capacità, filettatura | — | — | — | — | **APERTA** |
| P11 | **Riduttore / erogatore CO₂** | pressione max in ingresso, pressione in uscita, **orifizio calibrato che limita la portata anche a riduttore guasto** (`VA-23`) | — | — | — | — | **APERTA** |

---

### C. Batteria, BMS e alimentazione

**Stato: 0 / 5 coperte.** Blocca il gate di **fase 6** e le voci `VA-13`,
`VA-15`.

| # | Componente | Valore nominale richiesto | Fabbricante / codice | Documento | Valore rilevato | Verifica | Stato |
|---|---|---|---|---|---|---|---|
| E1 | **Celle LiFePO4** (4S, 10 Ah) | chimica **LiFePO4** dichiarata, capacità, corrente di scarica continua e di picco, **range di temperatura di carica**, riferimento a **IEC 62133-2** o equivalente | — | — | — | — | **APERTA** |
| E2 | **BMS 4S** | **corrente di protezione** (scarica e carica), soglia di **sovratensione di cella**, soglia di **sottotensione di cella**, protezione da **cortocircuito** con tempo d'intervento, **protezione di temperatura**, bilanciamento | — | — | — | — | **APERTA** |
| E3 | **Caricabatterie** | **tensione massima di uscita ≤ 14,6 V**, profilo CC/CV, corrente, marcatura CE, uscita **SELV** | — | — | — | — | **APERTA** |
| E4 | **Fusibile / PTC del pacco** | corrente nominale, corrente d'interruzione, posizione (adiacente al positivo) | — | — | — | — | **APERTA** |
| E5 | **Alimentatore di rete Unità A** (esterno) | tensione e corrente, marcatura CE, uscita SELV, **grado IP** adeguato all'esterno | — | — | — | — | **APERTA** |

**Verifica architetturale richiesta oltre ai datasheet** (`SAFETY.md` §3.2):
la tensione massima di uscita di **E3** deve essere **fisicamente** ≤ 14,6 V,
in modo che la sovraccarica sia impossibile anche a **E2 guasto**. Se l'unica
protezione contro la sovraccarica è il BMS, la riga non è chiusa anche a
datasheet presente.

---

### D. Riepilogo copertura

| Blocco | Coperte | Totali | Gate bloccato |
|---|---|---|---|
| A — pressione Unità A | **0** | 9 | G-PRESS, fase 4 |
| B — pressione Unità B | **0** | 2 | fase 6 |
| C — batteria / elettrico | **0** | 5 | fase 6 |
| **Totale** | **0** | **16** | |

**Copertura certificati: 0 %.** Il criterio di FATTO richiede **100 %** prima
di G-PRESS e prima del gate di fase 6. Il valore è riportato anche nella voce
`VA-03` del registro in `SAFETY.md` §9: le due cifre devono restare allineate.

---

### E. Registro delle prove in pressione

Da compilare durante il protocollo `SAFETY.md` §4.6. Una prova non registrata
è una prova non fatta.

| Data | Prova | Pressione target | Esito | Perdite rilevate | Note | Operatore |
|---|---|---|---|---|---|---|
| — | *(nessuna prova eseguita: G-PRESS non concesso)* | — | — | — | — | — |

---

### F. Strumenti di misura necessari alla verifica

Segnalati come mancanti in `docs/PROJECT.md` §10 e ripresi qui perché **senza
di essi il protocollo §4.6 non è eseguibile** (voce `VA-30`).

| Strumento | Serve per | Stato |
|---|---|---|
| **Manometro di riferimento indipendente** da quello del circuito | P-06 (prova della valvola di sicurezza) e P-08 (salita a gradini). Verificare la valvola con lo stesso manometro del circuito significa fidarsi di uno strumento non confrontato | **NON IN BOM** |
| **Anemometro** (filo caldo o ventolina) | velocità del getto al bersaglio (`VA-11`) e portata di aspirazione | **NON IN BOM** |
| **Occhiali di protezione** | obbligatori durante ogni prova in pressione (`SAFETY.md` §4.5) | **NON IN BOM** |
| **Termometro a contatto o termocamera** | verifica della temperatura di superficie dell'esca a duty 100 % (FM-B1) | **NON IN BOM** |
| **Inclinometro o piano inclinabile** | prova di stabilità al ribaltamento dell'Unità B (FM-B9) | **NON IN BOM** |
