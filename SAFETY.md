# Sicurezza e vincoli legali

Questo documento non è una formalità. Definisce i confini del progetto e le
ragioni per cui certe soluzioni tecniche sono state **escluse deliberatamente**.
Chi forka questo repository è pregato di leggerlo prima di modificare il payload.

Questo file **è il dossier di conformità** del progetto. Insieme a
`hardware/bom/README.md` (registro dei certificati) contiene tutto ciò che va
verificato prima di una prova rischiosa o di un'installazione. Non esiste un
documento di conformità separato, per scelta: la conformità che vive in un file
a parte non viene letta.

## 0. Che cosa è e che cosa non è questo dossier

**Non è** un fascicolo tecnico per la marcatura CE. R2-Sentinel è un progetto
amatoriale, non commerciale, non immesso sul mercato. La domanda a cui questo
documento risponde è diversa e più concreta: **che cosa è lecito costruire e
installare a casa propria, e che cosa va verificato prima di ogni prova
rischiosa.**

**Notazione usata in tutto il documento.** Ogni affermazione è marcata:

| Marca | Significato |
|---|---|
| **[V]** | **Verificato** su fonte primaria o su fonte secondaria qualificata, con il riferimento citato in §10 |
| **[I]** | **Interpretazione** del maintainer sulla base delle fonti verificate. Ragionevole, non autorevole. Non è un parere legale |
| **[?]** | **Non confermato.** È una voce aperta del registro §9, non un'assenza di problema |

Le voci **[?]** hanno tutte un identificativo `VA-nn` e stanno nel registro §9.
Il criterio di chiusura dei gate è: **zero voci aperte applicabili al gate**.

### 0.1 I due gate bloccanti

Nessun altro ruolo può aggirarli.

| Gate | Che cosa blocca | Condizione di sblocco |
|---|---|---|
| **G-PRESS** | Qualunque **prova in pressione**, anche la prima messa in pressione a vuoto | §4.6 completo + tutte le voci `VA` marcate `G-PRESS` chiuse |
| **G-INST-A** | **Installazione dell'Unità A** sul balcone e ogni prova all'aperto con payload attivo | §2.4 chiusa **con gli estremi dell'atto comunale** + voci `VA` marcate `G-INST-A` chiuse |

Il gate di **fase 4** (§9 di `docs/PROJECT.md`) contiene G-PRESS e G-INST-A.
Il gate di **fase 6** contiene le voci marcate `G-F6` (esca, ricarica, privacy
acustica).

---

## 1. Nessun sistema laser

Il progetto **non include e non includerà** un sistema di abbattimento laser
(approccio tipo *Photonic Fence*).

**Motivazione tecnica:**

- Abbattere una zanzara in volo richiede un laser di **classe 4**, potenza
  dell'ordine dei watt.
- Il dispositivo è **mobile** e **punta bersagli in movimento** in ambiente
  domestico, con persone e animali presenti.
- Il danno retinico da classe 4 è **permanente** e avviene in millisecondi:
  più rapido del riflesso palpebrale. Non c'è possibilità di reazione.
- Si aggiunge il rischio di innesco su tessuti e materiali.
- Nessuna schermatura o interlock realizzabile in autocostruzione porta questo
  rischio a un livello accettabile per un dispositivo autonomo non presidiato.

**Alternativa adottata:** aspirazione meccanica con esca (CO₂ + calore ~35 °C +
octenolo). Vedi `docs/PROJECT.md` §4.3.

Pull request che introducono emettitori laser di classe 3B o superiore non
verranno accettate.

---

## 2. Piccioni — solo dissuasione non cruenta

Il payload rivolto ai volatili è **non lesivo per progetto**: getto d'aria
compressa, nebulizzazione, stimolo sonoro o visivo. Nessun contatto lesivo,
nessun proiettile, nessuna trappola.

**Quadro normativo (Italia):**

- Il piccione di città (*Columba livia*) rientra nella fauna selvatica tutelata
  dalla **Legge 157/1992**.
- Uccidere o maltrattare un animale "per crudeltà o senza necessità" costituisce
  reato ai sensi degli **artt. 544-bis e 727 c.p.**
- Sono ammessi **esclusivamente metodi di dissuasione non cruenti**.
- Diversi comuni hanno ordinanze aggiuntive che vietano specificamente i
  dissuasori pericolosi, inclusi i comuni dissuasori ad aghi.

**Chi replica il progetto fuori dall'Italia** deve verificare la normativa
locale sulla fauna selvatica prima di installare l'Unità A.

Nota di efficacia, non solo di conformità: la dissuasione **contingente e
mirata** è più efficace di quella statica, perché non genera assuefazione.
Il vincolo legale e la soluzione tecnica migliore qui coincidono.

---

## 3. Elettrico

- **Nessun collegamento diretto alla rete 230 V realizzato in autocostruzione.**
  L'idea iniziale di un braccio robotico che si collega a una presa a muro è
  stata scartata per questa ragione. La ricarica avviene tramite dock a bassa
  tensione con contatti a molla.
- Batteria **LiFePO4**, non Li-ion NMC: il dispositivo si ricarica
  autonomamente in ambiente domestico non presidiato, e la chimica LiFePO4 non
  va in thermal runaway.
- BMS obbligatorio. Nessun pacco batteria autocostruito senza protezione.

---

## 4. Aria compressa

- Serbatoio 1–2 L a 5 bar: usare **componenti certificati per pressione**, mai
  contenitori improvvisati o stampati in 3D.
- Valvola di sicurezza tarata obbligatoria.
- L'ugello non va mai puntato verso persone o animali domestici a distanza
  ravvicinata.

---

## 5. Stampa 3D

- L'ASA emette **stirene** durante la stampa. Stampare in locale ventilato,
  mai in camera da letto o ambiente chiuso frequentato, anche disponendo di
  filtrazione a carboni attivi integrata.

---

## Segnalazioni

Per problemi di sicurezza aprire una issue con label `safety`, oppure
contattare il maintainer in privato se ritieni che la divulgazione pubblica
possa creare rischio.
