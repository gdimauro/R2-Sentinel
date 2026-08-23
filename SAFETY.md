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

## 2. Volatili — solo dissuasione non cruenta

Il payload rivolto ai volatili è **non lesivo per progetto**: getto d'aria
compressa, nebulizzazione, stimolo sonoro o visivo. Nessun contatto lesivo,
nessun proiettile, nessuna trappola.

### 2.1 Quadro nazionale — che cosa è chiuso

Questa parte è **chiusa**. Non richiede il nome del comune per essere applicata.

**a) Il colombo di città è fauna selvatica tutelata. [V]**

- La **L. 11 febbraio 1992 n. 157** protegge la fauna selvatica omeoterma; il
  suo art. 1 la qualifica come *patrimonio indisponibile dello Stato*.
- Il colombo di città (*Columba livia* forma *domestica*) vive in stato di
  naturale libertà ed è stato ricondotto alla fauna selvatica tutelata dalla
  **Cass. pen. sez. III n. 2598/2004**, che distingue il colombo urbano dai
  colombi viaggiatori e da quelli allevati, che restano domestici. **[V]**
- Non è specie cacciabile: non compare nell'elenco dell'art. 18 L. 157/1992.
  **[V]**

**b) Il contenimento è competenza pubblica, non del privato. [V]**

L'**art. 19 L. 157/1992** riserva il controllo della fauna selvatica alle
Regioni, che devono **privilegiare i metodi ecologici** su parere dell'istituto
scientifico nazionale (oggi ISPRA); solo se questi risultano inefficaci sono
ammessi piani di abbattimento, **eseguiti da personale pubblico abilitato**.
Il TAR Emilia-Romagna (2011) ha confermato che i colombi non possono essere
contenuti se non con metodi ecologici.

**Conseguenza diretta per questo progetto [I]:** un privato **non può in alcun
caso** catturare, abbattere o contenere numericamente i colombi. Può soltanto
**allontanarli dalla propria pertinenza**. R2-Sentinel è un dispositivo di
**allontanamento**, non di controllo demografico, e la documentazione non deve
mai descriverlo altrimenti. Questa è anche la ragione per cui il nome
"Sentinel" è corretto e "eliminazione del bersaglio" no (cfr. D-12).

**c) Il quadro penale è cambiato il 1º luglio 2025. Il repository citava il
testo previgente. [V]**

La **L. 6 giugno 2025 n. 82** ("legge Brambilla"), in vigore dal **1º luglio
2025**, ha riscritto il Titolo IX-bis del Libro II c.p., che ora si intitola
**"Dei delitti contro gli animali"** (non più "contro il sentimento per gli
animali"). Testo vigente rilevante:

| Norma | Fattispecie | Pena vigente (post L. 82/2025) |
|---|---|---|
| **art. 544-bis c.p.** | Chiunque, **per crudeltà o senza necessità**, cagiona la morte di un animale | reclusione **6 mesi – 3 anni** + multa **5.000 – 30.000 €** |
| art. 544-bis c.2 | se con **sevizie** o prolungando volutamente le sofferenze | reclusione **1 – 4 anni** + multa **10.000 – 60.000 €** |
| **art. 544-ter c.p.** | Chiunque, per crudeltà o senza necessità, **cagiona una lesione** a un animale **ovvero lo sottopone a sevizie o a comportamenti, fatiche o lavori insopportabili per le sue caratteristiche etologiche** | reclusione **6 mesi – 2 anni** **e** multa **5.000 – 30.000 €** (la multa era alternativa, ora è cumulativa) |
| **art. 638 c.p.** | Uccisione o danneggiamento di **animali altrui** | reclusione **1 – 4 anni** |
| **art. 727 c.p.** | Abbandono; detenzione in condizioni incompatibili con la natura dell'animale e produttive di gravi sofferenze | arresto fino a 1 anno o ammenda **5.000 – 10.000 €** |

**Le pene sono più che raddoppiate rispetto al testo citato finora in
`docs/PROJECT.md` §2.1 e §11.** Questa è una segnalazione al chief-engineer:
il documento master va allineato (voce `VA-01`).

### 2.2 Il getto d'aria è ammissibile? Sì, a condizioni. E c'è una soglia.

**La norma rilevante non è l'art. 544-bis (uccisione), è l'art. 544-ter.** [I]
La fattispecie che un dissuasore attivo può realisticamente integrare non è la
morte dell'animale, è la **lesione** o il **sottoporlo a comportamenti
insopportabili per le sue caratteristiche etologiche**. Da qui discendono tre
condizioni, e ognuna è una soglia misurabile o verificabile:

**Condizione 1 — nessuna lesione fisica.** Il getto non deve poter causare
lesione. Vanno esclusi per costruzione:
- particolato, sabbia, ghiaccio, additivi o qualunque cosa trasportata dal
  getto che non sia aria o acqua nebulizzata pulita;
- contatto dell'ugello o di parti meccaniche con l'animale;
- getto a distanza ravvicinata (< 1 m), dove la pressione dinamica sull'occhio
  del volatile non è trascurabile. **Va imposto un raggio minimo di ingaggio
  hardware**, non solo software (`VA-09`).

**Condizione 2 — la soglia è la fuga, non la persistenza.** [I] Un getto che
**allontana** è dissuasione. Un getto che continua su un animale che non riesce
ad allontanarsi — perché intrappolato, ferito, nidificante o giovane non
volante — smette di essere dissuasione e diventa "comportamento insopportabile
per le caratteristiche etologiche". **Regole di ingaggio che ne discendono, e
che sono vincolanti per `vision-perception` e `payload-fluidics`:**

- **Durata massima del singolo getto limitata via hardware** (§7, FM-A4).
- **Numero massimo di ripetizioni sullo stesso bersaglio**, dopo il quale il
  sistema smette e segnala, invece di insistere. Un bersaglio che non si sposta
  dopo N tentativi non è un bersaglio da insistere: è un animale che **non
  può** spostarsi.
- **Nessun ingaggio su nido, uova o pulli.** Se il rilevatore non è in grado di
  distinguerli, l'area va esclusa geometricamente (maschera fissa) e non
  statisticamente. Voce `VA-10`.
- **Nessun ingaggio notturno** su volatili posati al buio: l'animale in riposo
  notturno che viene ripetutamente disturbato è il caso di scuola dello stress
  senza via di fuga. [I]

**Condizione 3 — "senza necessità".** [I] Entrambi gli articoli richiedono che
il fatto sia commesso "per crudeltà o **senza necessità**". La difesa della
propria abitazione dall'imbrattamento e dal rischio igienico è una necessità
riconoscibile, **purché il mezzo sia proporzionato e non lesivo**. È quindi
utile — e va fatto — **documentare il problema** (foto del guano, danni,
frequenza) prima dell'installazione: è ciò che rende la misura "necessaria" e
proporzionata invece che gratuita. Costo: cinque minuti. Valore: sostanziale.

**Esiste una soglia numerica di velocità dell'aria oltre la quale il getto è
maltrattamento? [?]** **No, non nella normativa, e non ne abbiamo trovata una
in letteratura.** L'intervallo 8–25 m/s a 5 m assunto in `payload-fluidics`
resta una **stima non convalidata** (voce `VA-11`, già aperta in
`docs/PROJECT.md` §10). Finché non è convalidata, la protezione non è il
numero: è il **limite di pressione fisico del serbatoio** e la **durata
limitata via hardware**, che rendono il getto non lesivo *per costruzione* a
prescindere dal valore esatto.

### 2.3 Le altre norme che colpiscono l'Unità A, e che nessuno aveva citato

Non riguardano l'animale. Riguardano **le persone e i vicini**, e sono più
probabili nella pratica.

| Norma | Perché ci riguarda | Marca |
|---|---|---|
| **art. 674 c.p.** — getto pericoloso di cose | Punisce chi *getta o versa, in un luogo di pubblico transito o in un luogo privato ma di comune o altrui uso, cose atte a offendere o imbrattare o molestare persone*. Un getto d'aria o d'acqua da un balcone che raggiunge la strada, il cortile o il balcone del vicino **ricade letteralmente nella fattispecie**. È la norma più concretamente rischiosa dell'intero progetto. | [V] la norma, [I] l'applicazione |
| **art. 844 c.c.** — immissioni | Rumore, spruzzi d'acqua e vibrazioni verso il fondo del vicino, oltre la normale tollerabilità, sono illecito civile. Rilevante soprattutto per la variante a nebulizzazione. | [V] |
| **art. 659 c.p.** — disturbo delle occupazioni o del riposo | Un dissuasore **acustico** che opera di notte è esattamente la condotta descritta. **Il dissuasore sonoro va escluso in orario notturno.** | [V] la norma, [I] l'applicazione |
| **art. 638 c.p.** — animali altrui | Un colombo viaggiatore **ha un proprietario** e non è fauna selvatica (Cass. 2598/2004). Colpirne uno è un'ipotesi diversa e più grave. Argomento in più per la non lesività assoluta del payload. | [V] |
| **art. 1122 c.c.** — opere su parti di proprietà individuale | L'installazione sul balcone non deve pregiudicare **stabilità, sicurezza o decoro architettonico**; è comunque **dovuta preventiva notizia all'amministratore**, che ne riferisce all'assemblea. L'assemblea non autorizza, ma può agire per inibire. | [V] |

**Conseguenza di progetto, vincolante [I]:** il settore angolare dell'Unità A
deve essere limitato **meccanicamente** (arresti fisici sugli assi pan e tilt),
non solo per software, in modo che sia **geometricamente impossibile** dirigere
il getto fuori dalla propria pertinenza. Un limite software è un parametro di
configurazione; un arresto meccanico è una legge fisica. Voce `VA-08`.

### 2.4 Regolamento comunale — CHIUSURA RICHIESTA, BLOCCA G-INST-A

> **STATO: APERTA.** Il comune di installazione **non è noto al momento della
> stesura**. Milano è citato in `docs/PROJECT.md` §2.1 **solo come esempio** di
> ordinanza restrittiva e **non è il comune di installazione**.
>
> Questa sezione va compilata **con gli estremi dell'atto** — tipo di atto,
> organo, numero, data, articolo, comma, e il testo del divieto — prima di
> qualunque installazione dell'Unità A. Una ricerca generica ("ho cercato su
> internet e sembra si possa") **non chiude questa voce**.

**Perché è bloccante e non formale.** La L. 157/1992 è il **minimo nazionale**.
Diversi comuni vietano specificamente i dissuasori pericolosi. Esempio
verificato: il **Comune di Milano** ammette i dissuasori meccanici solo se le
loro caratteristiche non provocano lesioni agli animali e, per le nuove
installazioni e le sostituzioni, **vieta i dissuasori a punte salvo sommità
piatta o arrotondata e flessibile**, e vieta le reti a maglie tali da far
impigliare uccelli e chirotteri. **[V]** L'atto di riferimento è il
*Regolamento per il benessere e la tutela degli animali del Comune di Milano*;
il numero e la data della delibera di approvazione risultano da fonte
secondaria e **non sono stati confermati su fonte primaria** — motivo per cui
qui non li riportiamo come verificati. **[?]**

Il punto rilevante per noi è diverso e più insidioso: **molti regolamenti
comunali sono scritti presupponendo dissuasori passivi** (punte, reti, cavi,
gel). Un dissuasore **attivo** che emette un getto può non essere previsto — e
"non previsto" non significa "permesso". Va accertato caso per caso.

#### Checklist comunale — da compilare

Compilare **tutte** le righe. Una riga senza risposta è una voce aperta.

| # | Domanda | Dove cercare | Risposta / estremi dell'atto | Esito |
|---|---|---|---|---|
| C-01 | Esiste un **regolamento comunale per la tutela / il benessere degli animali**? | Sito del comune → *Statuto e regolamenti* / *Amministrazione trasparente → Atti generali* | | ☐ |
| C-02 | Quale **articolo** disciplina i **dissuasori per volatili**? Che formula usa (vieta i "cruenti"? i "pericolosi"? elenca i soli ammessi?) | idem | | ☐ |
| C-03 | Il regolamento ammette **solo dissuasori meccanici/passivi**, o consente anche dispositivi **attivi**? Se elenca tassativamente gli ammessi, **un dissuasore attivo non elencato è da considerarsi non ammesso** [I] | idem | | ☐ |
| C-04 | Esiste un divieto o un limite per i **dissuasori acustici / sonori**? | regolamento animali + regolamento di polizia urbana | | ☐ |
| C-05 | Il **regolamento di polizia urbana** vieta di **gettare o versare acqua/liquidi da balconi e finestre**, o di innaffiare in orari o modi che raggiungano il suolo pubblico? (è la norma che colpisce la variante a nebulizzazione, ed è quasi sempre presente) | *Regolamento di polizia urbana* / *di polizia urbana e sicurezza urbana* | | ☐ |
| C-06 | Esiste una **classificazione acustica del territorio comunale** e quali sono i limiti in periodo notturno per la zona dell'immobile? | *Piano di classificazione acustica* comunale | | ☐ |
| C-07 | Il **regolamento comunale d'igiene** ha un capitolo sugli **animali sinantropi / colombi** (obblighi dei proprietari di immobili, chiusura di cavità, divieto di alimentazione)? | *Regolamento comunale d'igiene*, spesso di derivazione ASL | | ☐ |
| C-08 | Esistono **ordinanze sindacali vigenti** su colombi, alimentazione dei volatili o obblighi antintrusione a carico dei proprietari? | *Albo pretorio online* → ordinanze; cercare anche le ordinanze contingibili e urgenti degli ultimi 5 anni | | ☐ |
| C-09 | Il **regolamento edilizio** richiede un titolo o una comunicazione per **installazioni su balconi/facciate visibili dalla pubblica via**? | *Regolamento edilizio* comunale | | ☐ |
| C-10 | L'immobile è in **zona vincolata** (centro storico, vincolo paesaggistico o su bene culturale)? In tal caso l'installazione visibile può richiedere autorizzazione ai sensi del **D.Lgs. 42/2004** — **da verificare, non confermato** [?] | ufficio tecnico / SUE del comune | | ☐ |
| C-11 | Chi è l'**autorità competente** per il colombo di città sul territorio (Città Metropolitana / Provincia, ASL veterinaria) e ha emesso **linee guida** sui dissuasori ammessi? | sito Città Metropolitana/Provincia, ATS/ASL | | ☐ |
| C-12 | Il **regolamento condominiale** (contrattuale o assembleare) vieta installazioni su balconi, apparecchi rumorosi, o modifiche dell'aspetto esterno? | copia del regolamento + verbali d'assemblea | | ☐ |
| C-13 | È stata data **preventiva notizia all'amministratore** ai sensi dell'**art. 1122 c.c.**? Data e forma (raccomandata/PEC) | | | ☐ |

**Come porre la domanda al comune.** Non chiedere "posso installare un
dissuasore?": la risposta sarà generica e non chiuderà nulla. Chiedere per
iscritto (URP o PEC), citando la propria via, **queste tre cose**:

1. gli **estremi e il testo vigente** dell'articolo del regolamento comunale
   che disciplina i dissuasori per volatili;
2. se sia ammesso un dissuasore **attivo e non lesivo** (getto d'aria a bassa
   pressione, comandato da un rilevatore, orientato esclusivamente entro la
   proprietà privata), o se siano ammessi **solo** dissuasori passivi;
3. se vi siano **ordinanze vigenti** in materia di colombi applicabili
   all'indirizzo indicato.

Conservare la risposta scritta. **La risposta scritta dell'ufficio è ciò che
chiude questa voce**, insieme agli estremi dell'atto.

#### Formato di chiusura richiesto

Quando compilata, questa sezione deve leggersi così (esempio di **forma**, non
di contenuto):

> *Comune di ……, `Regolamento ……`, approvato con Deliberazione del Consiglio
> Comunale n. …… del ……, art. …… comma ……: «testo del divieto».*
> *Riscontro URP prot. n. …… del ……, agli atti del progetto.*
> *Esito: l'Unità A **è / non è** ammissibile; condizioni: ……*
> *Verificato da …… il …… — fonte consultata il ……*

### 2.5 Fuori dall'Italia

**Chi replica il progetto fuori dall'Italia** deve verificare la normativa
locale sulla fauna selvatica **prima** di installare l'Unità A. In diversi
ordinamenti *Columba livia* ha uno status differente, in entrambe le direzioni:
più tutelato in alcuni paesi, esplicitamente non tutelato in altri. Il vincolo
di non lesività resta comunque la scelta corretta per default.

### 2.6 Nota di efficacia, non solo di conformità

La dissuasione **contingente e mirata** è **anche più efficace** di quella
statica, perché non genera assuefazione: il dissuasore fisso viene imparato e
ignorato, l'evento imprevedibile associato alla posa no. Il vincolo legale e la
soluzione tecnica migliore **coincidono**. Questo va detto esplicitamente,
perché un vincolo percepito come ostacolo prima o poi viene aggirato, mentre un
vincolo che è anche la scelta ingegneristica migliore no.

---

## 3. Elettrico

### 3.1 Principi non negoziabili

- **Nessun collegamento diretto alla rete 230 V realizzato in autocostruzione.**
  L'idea iniziale di un braccio robotico che si collega a una presa a muro è
  stata scartata per questa ragione. La ricarica avviene tramite dock a bassa
  tensione con contatti a molla.
- Batteria **LiFePO4**, non Li-ion NMC: il dispositivo si ricarica
  autonomamente in ambiente domestico non presidiato, e la chimica LiFePO4 non
  va in thermal runaway (D-07).
- **BMS obbligatorio.** Nessun pacco batteria autocostruito senza protezione.

### 3.2 Batteria LiFePO4 4S 10 Ah — che cosa va verificato

Il pacco è **4S**: 12,8 V nominali, **14,6 V di fine carica** (3,65 V/cella).
Energia immagazzinata ≈ **128 Wh**. Non è un accumulo trascurabile: è
paragonabile a un utensile da giardino a batteria, e sta in casa, incustodito,
in carica.

| Cosa | Requisito | Dove si registra |
|---|---|---|
| Celle | Chimica **LiFePO4** dichiarata dal fabbricante; datasheet con capacità, corrente di scarica continua e di picco, range di temperatura di **carica** (tipicamente 0…45 °C — la carica sotto zero è il modo di guasto meno noto e più insidioso) | `hardware/bom/README.md` |
| Certificazione celle | Riferimento a **IEC 62133-2** o equivalente dichiarato dal fornitore. **[?]** Se il fornitore non lo fornisce, il fornitore va cambiato, non la regola | idem |
| BMS | **Soglie dichiarate a datasheet**: sovratensione di cella, sottotensione di cella, sovracorrente di scarica, sovracorrente di carica, protezione da cortocircuito con tempo d'intervento, **protezione di temperatura**, bilanciamento | idem |
| Caricabatterie | Alimentatore **marcato CE**, uscita **SELV**, profilo **CC/CV con tensione massima fisicamente ≤ 14,6 V** | idem |
| Fusibile | Fusibile o portafusibile **sul positivo del pacco**, il più vicino possibile al morsetto, dimensionato sotto la corrente di picco ammessa dalle celle | idem |

**Principio di verifica per esclusione, applicato qui [I]:** il BMS **non è la
protezione, è la seconda protezione**. La prima protezione deve essere il
caricabatterie, la cui tensione di uscita è **fisicamente incapace** di
superare i 14,6 V. Così, se il BMS si guasta, il pacco non si sovraccarica lo
stesso. Un'architettura in cui l'unica cosa che impedisce la sovraccarica è un
MOSFET del BMS è un'architettura a singolo punto di guasto su un dispositivo
che carica di notte in casa. Voce `VA-13`.

**La carica a bassa temperatura è vietata** [I]: caricare LiFePO4 sotto 0 °C
provoca *lithium plating* e danno permanente. Il dock dell'Unità B è in
ambiente interno, quindi il rischio è basso, ma **la protezione di temperatura
del BMS deve essere presente e dichiarata**, non presunta.

### 3.3 Alimentazione di rete dell'Unità A (esterno)

L'Unità A è alimentata da rete (§4.1 di `docs/PROJECT.md`). L'alimentazione è
**all'aperto**, ed è la parte elettricamente più pericolosa del progetto —
molto più della batteria.

**Regole [I], fondate sulle norme citate:**

1. **L'autocostruzione si ferma a valle di un alimentatore commerciale marcato
   CE con uscita SELV.** A monte c'è impianto, non progetto: nessun cablaggio
   230 V autocostruito, nessuna morsettiera 230 V in una scatola stampata in 3D,
   nessun alimentatore aperto.
2. **Realizzare o modificare un circuito fisso** (una nuova presa esterna, una
   derivazione sul balcone) **non è fai-da-te**: il **D.M. 37/2008** riserva
   progettazione e installazione degli impianti negli edifici a **imprese
   abilitate**, che rilasciano la **Dichiarazione di Conformità (DiCo)**. **[V]**
   Collegare un apparecchio con spina a una presa esistente non è "impianto";
   aggiungere la presa lo è. Voce `VA-14`.
3. La **CEI 64-8** è la regola dell'arte richiamata dalla L. 186/1968 e dal
   D.M. 37/2008. **[V]** Per il circuito che alimenta l'Unità A:
   - **interruttore differenziale da 30 mA** a protezione della presa esterna;
   - **grado IP adeguato all'installazione all'aperto** per presa, alimentatore
     e passaggi cavo (i pressacavi IP68 già in BOM riguardano il carter, non la
     presa);
   - percorso cavo protetto meccanicamente e non calpestabile.
4. **Nessuna prova all'aperto con il payload attivo sotto pioggia**, e
   scollegamento dell'alimentazione durante le manutenzioni.

Il livello IP dell'alimentatore esterno e il valore del differenziale esistente
sull'impianto **non sono noti**: voce `VA-15`, chiude su G-INST-A.

### 3.4 Marcatura CE: una precisazione onesta

Il progetto **non prepara una marcatura CE** e non ne ha bisogno finché il
dispositivo non viene immesso sul mercato. **Va però detto che il punto non è
del tutto banale [?]:** per le **macchine**, la dottrina prevalente sostiene che
gli obblighi si applichino anche a chi costruisce **per uso proprio**, perché
la *messa in servizio* è equiparata all'immissione sul mercato, e in tal caso
l'autocostruttore assume il ruolo di fabbricante. **[V]** La letteratura
consultata riguarda però l'**uso in azienda**; **non abbiamo trovato conferma**
che l'obbligo si estenda a un dispositivo **puramente privato, hobbistico e non
professionale**. Voce `VA-16`.

**Che cosa cambia in pratica, comunque poco [I]:** anche nell'ipotesi peggiore,
gli obblighi sostanziali sono quelli che questo dossier già impone —
valutazione dei rischi, protezioni, istruzioni, conservazione della
documentazione. Ciò che manca sarebbe la formalizzazione. **La responsabilità
civile e penale per danni a terzi grava comunque interamente sul costruttore, a
prescindere dalla marcatura.** Questa frase va tenuta a mente più di tutte le
altre di questo documento.

---

## 4. Aria compressa

### 4.1 Regole invariate

- Serbatoio 1–2 L a 5 bar: usare **componenti certificati per pressione**, mai
  contenitori improvvisati o stampati in 3D.
- Valvola di sicurezza tarata obbligatoria.
- L'ugello non va mai puntato verso persone o animali domestici a distanza
  ravvicinata.

### 4.2 Inquadramento normativo del serbatoio — chiuso

Caso di progetto: **V = 1–2 L, PS = 5 bar, fluido aria (gruppo 2)**.
`PS · V = 5 – 10 bar·L`.

| Norma | Si applica? | Perché |
|---|---|---|
| **Direttiva PED 2014/68/UE** (in Italia **D.Lgs. 26/2016**) | **NO** | Per i recipienti destinati a gas del **gruppo 2**, la direttiva si applica quando **V > 1 L e PS·V > 50 bar·L**, oppure PS > 1000 bar. Il nostro caso è **5–10 bar·L**, un fattore 5–10 sotto la soglia. **[V]** |
| **PED art. 4 §3** — corretta prassi costruttiva | **SÌ** | Le attrezzature sotto soglia **devono comunque essere progettate e fabbricate secondo la corretta prassi costruttiva** in uso in uno Stato membro, che assicuri la sicurezza d'uso, e **corredate di istruzioni sufficienti**. **Non recano la marcatura CE** in forza della PED. **[V]** |
| **D.M. 329/2004** — messa in servizio e verifiche periodiche | **NO** | L'art. 2 comma 1 lett. i) esclude i recipienti **di capacità ≤ 25 L** (e, se PS ≤ 12 bar, ≤ 50 L). Con 1–2 L siamo largamente esclusi: **nessuna denuncia INAIL/CIVA, nessuna verifica periodica obbligatoria**. **[V]** |
| **D.Lgs. 81/2008** | **NO** [I] | Non c'è datore di lavoro né lavoratore: è un'abitazione privata. Restano applicabili le norme civili e penali generali. |

**Conseguenza operativa da capire bene, perché è controintuitiva [I]:** il
serbatoio che compreremo **legittimamente non avrà una marcatura CE-PED**, e
questo *non* è un difetto. Pretendere una marcatura PED su un recipiente da 2 L
è chiedere una cosa che la norma non prevede. **Ciò che va preteso è
diverso:** un **datasheet del fabbricante** che dichiari `PS` (pressione
massima ammissibile), la **temperatura ammissibile**, e — quando disponibile —
la **pressione di prova o di scoppio**. Il registro dei certificati è in
`hardware/bom/README.md`.

> **"Il venditore dice che regge 8 bar" non è un certificato.** Un annuncio di
> marketplace non è un datasheet. Se il componente non ha un documento del
> fabbricante con i valori nominali, il componente non entra nel circuito in
> pressione. Nessuna eccezione: questo è il punto in cui il dossier vale o non
> vale nulla.

### 4.3 Quanta energia c'è davvero nel serbatoio

Calcolo del maintainer, **non un dato normativo** [I]. 2 L a 5 bar relativi
(6 bar assoluti), espansione fino all'atmosfera:

- **espansione adiabatica** (rottura istantanea, caso realistico): ≈ **1,2 kJ**
- **espansione isoterma** (limite superiore): ≈ **2,2 kJ**

Per confronto, l'energia alla bocca di una pistola da 9 mm è dell'ordine di
**0,5 kJ**. **Il serbatoio contiene da due a quattro volte quell'energia.** Non
è un palloncino. Questo giustifica per intero le procedure di §4.6, che
altrimenti sembrerebbero sproporzionate per "due litri d'aria".

### 4.4 Che cosa deve essere certificato, e con quale valore

Elenco vincolante. Il dettaglio e lo stato riga per riga stanno in
`hardware/bom/README.md`.

| Componente | Valore nominale che DEVE risultare dal documento |
|---|---|
| Serbatoio | PS, temperatura ammissibile, volume, **pressione di prova o di scoppio** |
| Valvola di sicurezza | **pressione di taratura**, portata di scarico, tipo (a molla, ricomponibile) |
| Riduttore di pressione | pressione max in ingresso, campo di regolazione in uscita |
| Manometro | fondo scala, **classe di precisione**, campo di lavoro |
| Elettrovalvola | pressione max di esercizio, tensione, **coefficiente di portata**, posizione di riposo (**deve essere normalmente chiusa**) |
| Tubi | **pressione di esercizio e pressione di scoppio** (rapporto minimo richiesto: **scoppio ≥ 3 × PS**), temperatura, raggio di curvatura minimo |
| Raccordi e innesti | pressione max di esercizio, compatibilità con il tubo |
| Compressore | **pressione massima erogabile**, portata, presenza e taratura del **pressostato** |
| Cartuccia CO₂ e riduttore (Unità B) | pressione della cartuccia, pressione max in ingresso del riduttore, **orifizio calibrato in uscita** |

**Regola dell'anello debole [I]:** la pressione massima del circuito è quella
del **componente con il PS più basso**, non quella del serbatoio. La taratura
della valvola di sicurezza va scelta **su quel valore**, non sul serbatoio.

**Regola strutturale [I]:** nessun pezzo stampato in 3D può essere in
contenimento di pressione. L'FDM è anisotropo e si delamina fra i layer, e la
delaminazione è progressiva e invisibile. L'ugello convergente in FDM
(`docs/PROJECT.md` §7.2, D-11) è ammissibile **solo a valle dell'ugello
strozzato, in scarico verso l'atmosfera** e mai come parte in pressione a monte.
Se la geometria dell'ugello ne fa un elemento in pressione, torna al service.
Voce `VA-06` — la richiesta a `payload-fluidics` è di **dichiarare dove passa
il confine di pressione** nello schema del circuito.

### 4.5 Rischi per le persone — l'aria compressa non è innocua

Documentati in letteratura di sicurezza sul lavoro **[V]**:

- lesioni a **occhi e viso** da getto diretto o da materiale proiettato;
- danno **all'udito** per esposizione al rumore del getto;
- lesioni a **polmoni ed esofago** da getto diretto su bocca o naso;
- **embolia gassosa** se l'aria compressa penetra attraverso la pelle o vasi
  superficiali.

Ne discendono le regole d'uso: **occhiali di protezione obbligatori** durante
ogni prova; **mai puntare il getto su sé stessi o su altri, per scherzo o per
prova**; l'ugello mai a distanza ravvicinata da persone o animali domestici.

### 4.6 G-PRESS — protocollo prima della PRIMA messa in pressione

**Nessuna di queste righe è facoltativa. Finché una casella è vuota, non
concedo l'assenso scritto e la prova non parte.**

**Prerequisiti documentali**

- [ ] P-01 — Schema del circuito in pressione ricevuto da `payload-fluidics`,
      con indicato **dove passa il confine di pressione**
- [ ] P-02 — **100% delle righe** della tabella §4.4 coperte in
      `hardware/bom/README.md` con datasheet e valore nominale
- [ ] P-03 — Pressione massima del circuito determinata con la **regola
      dell'anello debole**, e taratura della valvola di sicurezza scelta su
      quel valore e **documentata**
- [ ] P-04 — Il **compressore non può fisicamente superare** la pressione di
      taratura: pressostato tarato **e** verifica che la pressione massima
      erogabile a pressostato guasto resti sotto il PS dell'anello debole. Se
      non lo è, serve un secondo dispositivo
- [ ] P-05 — Calcolo di **non lesività del getto** ricevuto da
      `payload-fluidics` (velocità al bersaglio, distanza minima di ingaggio)

**Prove sul circuito montato, in quest'ordine**

- [ ] P-06 — **Prova della valvola di sicurezza per prima**, prima di ogni
      altra prova: si verifica che scarichi effettivamente alla pressione di
      taratura, con manometro indipendente. Una valvola mai provata è una
      valvola di cui si presume il funzionamento
- [ ] P-07 — **Prova di tenuta preferibilmente idraulica, non pneumatica.**
      L'acqua è incomprimibile: in caso di cedimento rilascia energia
      trascurabile, l'aria rilascia i ~1,2 kJ di §4.3. Dove la prova idraulica
      non è praticabile (elettrovalvola, elettronica), va isolato il tratto e
      la ragione va scritta
- [ ] P-08 — **Salita a gradini**: 1 → 2 → 3 → 4 → 5 bar, con sosta di almeno
      5 minuti per gradino e controllo della caduta di pressione al manometro
- [ ] P-09 — **Ricerca perdite con acqua saponata** su tutti i raccordi a ogni
      gradino
- [ ] P-10 — Prova condotta con **barriera fisica** interposta (una lastra
      rigida, un mobile robusto), **nessuna persona nel raggio**, comando a
      distanza, **occhiali di protezione**
- [ ] P-11 — **Prima prova di getto a serbatoio parziale** (≤ 2 bar) e ugello
      diretto in direzione sicura
- [ ] P-12 — Valori misurati, foto del circuito e data **registrati in
      `hardware/bom/README.md`**

**Prima di ogni prova successiva**

- [ ] P-13 — Ispezione visiva di tubi e raccordi (screpolature, rigonfiamenti,
      raccordi allentati)
- [ ] P-14 — **Serbatoio scaricato a fine sessione.** Un serbatoio lasciato in
      pressione in un'abitazione è un accumulo d'energia non presidiato

**Assenso scritto:** una volta completato, l'esito va scritto qui sotto con la
data. Finché questa riga è vuota, G-PRESS è chiuso.

> **G-PRESS — assenso: NON CONCESSO.** Motivazione: nessuna riga P-01…P-12 è
> soddisfatta; il registro dei certificati è a **0/14**. Prima verifica
> possibile: alla consegna dello schema del circuito da `payload-fluidics`.

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
