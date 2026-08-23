# Sicurezza e vincoli legali

Questo documento non è una formalità. Definisce i confini del progetto e le
ragioni per cui certe soluzioni tecniche sono state **escluse deliberatamente**.
Chi forka questo repository è pregato di leggerlo prima di modificare il payload.

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
