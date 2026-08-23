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
> soddisfatta e il registro dei certificati è a **0/16**
> (`hardware/bom/README.md`). Prima verifica possibile: alla consegna dello
> schema del circuito e dei datasheet da `payload-fluidics`.

---

## 5. Stampa 3D

- L'ASA emette **stirene** durante la stampa. Stampare in locale ventilato,
  mai in camera da letto o ambiente chiuso frequentato, anche disponendo di
  filtrazione a carboni attivi integrata.
- Il filtro a carboni attivi della P2S **riduce** l'emissione, non la annulla:
  è una mitigazione, non una protezione. La ventilazione del locale resta
  obbligatoria (coerente con `docs/PROJECT.md` §8.4, che la elenca fra le buone
  pratiche — qui è un obbligo, non una buona pratica).

---

## 6. Privacy

La privacy qui **è un vincolo di sicurezza come gli altri**, non un adempimento
burocratico. Le due unità producono, insieme, il materiale più sensibile
dell'intero progetto: **la planimetria dell'abitazione** (mappe SLAM), **video
degli interni** e **settimane di audio registrato di notte in casa**.

### 6.1 Il GDPR si applica a un uso domestico? La risposta breve: dipende da dove punta l'obiettivo

**Regola.** L'**art. 2 §2 lett. c) GDPR** esclude dall'ambito di applicazione i
trattamenti effettuati da una persona fisica **per l'esercizio di attività a
carattere esclusivamente personale o domestico** (considerando 18). **[V]**

**Il limite, che è il punto che conta.** La Corte di giustizia UE, causa
**Ryneš, C-212/13, 11 dicembre 2014**, ha stabilito che una videosorveglianza
che riprende **anche solo parzialmente lo spazio pubblico non può** essere
considerata attività "esclusivamente personale o domestica", perché il
trattamento si dirige fuori dalla sfera privata di chi lo effettua. **[V]**
L'eccezione domestica va interpretata **restrittivamente**.

**Il Garante italiano** ha ribadito la regola per le telecamere private, da
ultimo con il **provvedimento n. 9949494 del 12 ottobre 2023**: l'angolo di
ripresa delle telecamere installate da persone fisiche deve essere limitato
**agli spazi di esclusiva pertinenza**, escludendo aree comuni (cortili,
pianerottoli, scale, parcheggi condivisi), aree di terzi e aree pubbliche o di
pubblico passaggio. **[V]**

### 6.2 Applicazione alle due unità

**Unità A — il balcone è il caso critico.** Una camera su un balcone che
inquadra il balcone stesso resta nell'eccezione domestica. Una camera
grandangolare che inquadra **anche** la strada, il cortile, il balcone del
vicino o le finestre di fronte **esce dall'eccezione domestica** e diventa un
trattamento soggetto al GDPR — con base giuridica, informativa e responsabilità
del titolare. E, in più, può integrare l'**art. 615-bis c.p.** (interferenze
illecite nella vita privata): *chiunque, mediante l'uso di strumenti di ripresa
visiva o sonora, si procura indebitamente notizie o immagini attinenti alla
vita privata svolgentesi nei luoghi indicati nell'art. 614*, con reclusione
**da 6 mesi a 4 anni**. **[V]** Riprendere l'interno dell'appartamento di
fronte è esattamente questo.

**Vincolo di progetto che ne discende, e che è hardware, non software [I]:**

1. La **maschera di privacy deve essere ottica o meccanica**, non solo software:
   il campo visivo va limitato **fisicamente** (paraluce, schermatura, scelta
   della focale e del punto di installazione) in modo che ciò che è fuori dalla
   pertinenza **non entri nel sensore**. Una maschera software è un file di
   configurazione: sopravvive a un aggiornamento, non a un errore.
2. La camera dell'Unità A va puntata **verso il basso e verso l'interno** della
   pertinenza. Se il campo utile richiede di inquadrare oltre, va rivista la
   posizione, non la maschera.
3. **Nessun frame che contenga spazi altrui esce dal dispositivo** e nessuno
   entra nel repository, mai, nemmeno come esempio in un README.
4. **Nessun microfono sull'Unità A.** L'esterno è dove si registra la voce dei
   vicini e dei passanti. L'Unità A non ha bisogno di audio: non lo monta.

Voce `VA-17` — la verifica di che cosa inquadri effettivamente il balcone
**richiede il sopralluogo e non è chiudibile a tavolino**: chiude su G-INST-A.

**Unità B — audio notturno per settimane, in casa.**

- L'esclusione domestica si applica se l'audio **resta in casa e non riguarda
  terzi**. Ma in casa entrano **ospiti**, e le conversazioni registrate senza
  che l'interessato lo sappia sono un problema che **il GDPR non risolve**:
  l'eccezione domestica esclude l'applicazione del regolamento, non la rilevanza
  penale né quella civile. [I]
- Il Garante, nel contesto della videosorveglianza, ha ritenuto la captazione
  audio **non conforme ai principi di pertinenza, non eccedenza e
  proporzionalità**. **[V]** La stessa logica, applicata qui, dice una cosa
  precisa: **registrare parlato è eccedente rispetto allo scopo**, perché lo
  scopo è rilevare un battito alare a 400–600 Hz.
- **Chi vive in casa va informato** che c'è un microfono che registra, e va
  informato **prima**, non dopo. Idem per gli ospiti che dormono in casa. Non è
  un obbligo formale: è la condizione perché il progetto resti accettabile
  dentro la famiglia. [I]

**Vincolo di progetto, e questa è la protezione "hardware" equivalente [I]:**

> **L'audio a banda piena non deve mai essere scritto su disco.**
> La protezione non è cancellare la voce dopo: è **non acquisirla in forma
> intelligibile**. Filtro **passa-banda in acquisizione** centrato sulla banda
> utile (indicativamente 200–1200 Hz), scarto del segnale fuori banda **prima**
> della scrittura, e conservazione preferibilmente di **spettrogrammi o feature**
> anziché di forme d'onda. Un file che non contiene parlato intelligibile non
> ha un problema di privacy da gestire: non ce l'ha proprio.

Stato attuale: `software/acoustic/metadati.py` implementa una **revisione
privacy manuale e dichiarativa** (`privacy.voce_riconoscibile`, `azione`,
`pubblicabile`) con un avviso quando è presente voce riconoscibile e nessuna
mitigazione. **È un buon controllo procedurale e va tenuto**, ma è
**successivo** all'acquisizione: dipende da un umano che compili un campo.
Manca il controllo **preventivo** in acquisizione. Voce `VA-18`, chiude su
**G-F6**, ed è indirizzata a `acoustic-perception`.

**Mappe SLAM.** Una mappa `slam_toolbox` **è la planimetria dell'abitazione**,
con la posizione dei mobili. Va trattata come un documento sensibile: resta
locale, non entra nel repository, non finisce in un allegato di issue, non
compare negli screenshot della documentazione. Se serve un'illustrazione per
`design-docs`, si usa una **mappa sintetica di un ambiente fittizio**.

### 6.3 Git: la history non si cancella davvero

Questa è la parte in cui il rischio è irreversibile. Un commit sbagliato di una
mappa o di un file audio **resta nella history** anche dopo un commit di
rimozione, resta nei fork, resta nelle copie clonate, e su una piattaforma
remota resta raggiungibile per SHA.

**Verifica eseguita alla data di questa revisione:**

| Controllo | Esito |
|---|---|
| File di mappe SLAM nella history | **0** — il repository non ha ancora commit |
| Riprese di interni | **0** |
| File audio con voce riconoscibile | **0** |
| Credenziali in chiaro | **0** — `software/ros2_ws/src/r2s_mqtt_bridge/config/topics.yaml` usa correttamente `credentials_env: ["R2S_MQTT_USER", "R2S_MQTT_PASS"]`, nessun segreto nel worktree |

**Ma c'è un difetto aperto, e non è piccolo. [V]**

`CONTRIBUTING.md` (sezione Privacy) afferma: *«Non committare mai mappe SLAM,
riprese di interni, o file di configurazione con credenziali. Il `.gitignore`
li blocca»*. **Il `.gitignore` attuale non li blocca.** Contiene `datasets/`,
`*.pt`, `*.onnx`, `*.hef` e `docs/journal/media/`, ma **nessuna regola** per
mappe, audio, video o segreti. La documentazione promette una protezione che
non esiste: è il tipo di difetto peggiore, perché **induce a non controllare**.

Voce `VA-19`, **bloccante per G-F6 e per il primo commit di materiale
acustico**, indirizzata a `software-platform` (non la applico io: verifico, non
costruisco). Patch minima richiesta:

```gitignore
# Privacy — materiale che non deve MAI entrare nella history (SAFETY.md §6)
# Mappe SLAM = planimetria dell'abitazione
maps/
*.pgm
*.posegraph
*.serialized*
# Audio e video: registrazioni ambientali e riprese di interni
recordings/
*.wav
*.flac
*.ogg
*.mp3
*.mp4
*.mov
# Rosbag: contengono immagini, audio e mappe insieme
*.db3
*.mcap
rosbag2_*/
# Credenziali
.env
*.pem
*.key
secrets.*
```

Nota su `*.pgm`: se in futuro servisse committare un'immagine `.pgm` legittima,
si aggiunge un'eccezione puntuale. Il default deve essere il divieto.

**Regola operativa, da applicare anche dopo la patch [I]:** `git status` prima
di ogni `git add`, e `git add -p` invece di `git add .` su qualunque directory
che possa contenere acquisizioni. Il `.gitignore` è una rete, non un lucchetto.

---

## 7. Modi di guasto e protezioni hardware

**Il metodo.** La domanda non è *"questa soluzione è ammissibile?"* ma
**"quale caso di guasto la rende lesiva?"**. Ogni riga deve avere una
protezione **hardware** documentata, oppure essere **esplicitamente accettata
con motivazione scritta**. Nessun modo di guasto resta senza riga.

**Perché hardware e non software.** Un limite software è un parametro: si
modifica con un commit, si perde in un aggiornamento, si azzera con un reset di
configurazione, e non protegge dal guasto del software stesso. Su un
dispositivo **non presidiato** la protezione deve sopravvivere al fallimento
del controllo. `SW` come unica colonna di protezione = riga non chiusa.

Legenda stato: **OK** protezione definita e verificata · **DA DEFINIRE**
protezione non ancora progettata · **ACCETTATO** rischio accettato con
motivazione.

### 7.1 Unità A — payload getto d'aria

| ID | Modo di guasto | Conseguenza | Protezione **hardware** richiesta | Stato |
|---|---|---|---|---|
| FM-A1 | **Getto puntato accidentalmente su una persona** (errore di detection, deriva della calibrazione, comando errato) | lesione a occhi/udito, art. 674 c.p. | **Arresti meccanici** sugli assi pan e tilt che rendono *geometricamente impossibile* uscire dal settore della propria pertinenza. Non finecorsa elettrici: **battute fisiche** | **DA DEFINIRE** `VA-08` |
| FM-A2 | **Sovrapressione del serbatoio** (pressostato guasto, compressore che non si ferma) | scoppio, ~1,2 kJ | **Valvola di sicurezza tarata** (protezione ultima) + pressostato (protezione funzionale). Due dispositivi indipendenti | **DA DEFINIRE** `VA-02` |
| FM-A3 | **Cedimento di serbatoio, tubo o raccordo** | proiezione di frammenti | Componenti certificati §4.4; tubi con **scoppio ≥ 3 × PS**; **carter di contenimento**; prova §4.6 | **DA DEFINIRE** `VA-03` |
| FM-A4 | **Elettrovalvola incollata aperta** | scarica dell'intero serbatoio sul bersaglio: da dissuasione a maltrattamento (art. 544-ter) | Elettrovalvola **normalmente chiusa** + **temporizzatore hardware monostabile** che toglie alimentazione dopo T_max indipendentemente dal firmware + **orifizio calibrato** che limita la portata istantanea per costruzione | **DA DEFINIRE** `VA-04` |
| FM-A5 | **Avvio spontaneo al ripristino della rete** dopo un blackout | getto non presidiato | Ripristino **manuale** dell'abilitazione payload + **scarico automatico del serbatoio all'accensione** | **DA DEFINIRE** `VA-05` |
| FM-A6 | **Getto o nebulizzato che raggiunge il vicino o la via** | art. 674 c.p., art. 844 c.c. | Stesso arresto meccanico di FM-A1 + **verifica della gittata reale sul posto** prima dell'abilitazione | **DA DEFINIRE** `VA-08` |
| FM-A7 | **Sovrapressione termica** — serbatoio in ASA scuro esposto al sole estivo | superamento del PS a serbatoio pieno | Coperto dalla valvola di sicurezza **purché la taratura sia scelta considerando la temperatura massima**, non quella di collaudo. Serbatoio in **ombra o schermato** | **DA DEFINIRE** `VA-02` |
| FM-A8 | **Rumore dello sparo** in orario notturno | art. 659 c.p., rapporti coi vicini | **Inibizione oraria del payload**, preferibilmente su base hardware (timer/relè), non solo software | **DA DEFINIRE** `VA-12` |
| FM-A9 | **Caduta dell'unità dal balcone** (vento, ancoraggio, rinculo del getto) | lesione grave a terzi al piano strada | **Ancoraggio meccanico dimensionato + cavo di ritenuta secondario**. Il rinculo di un getto va calcolato, non stimato | **DA DEFINIRE** `VA-07` |
| FM-A10 | **Ingaggio su nido, uova o pulli** | art. 544-ter, e danno reale | **Maschera geometrica fissa** dell'area di nidificazione, non esclusione statistica | **DA DEFINIRE** `VA-10` |
| FM-A11 | **Ingaggio su animale domestico** (gatto sul balcone, cane del vicino) | art. 544-ter, art. 638 se altrui | Distanza minima di ingaggio + classe di bersaglio ristretta + arresto meccanico | **DA DEFINIRE** `VA-09` |

### 7.2 Unità B — payload esca e aspirazione

| ID | Modo di guasto | Conseguenza | Protezione **hardware** richiesta | Stato |
|---|---|---|---|---|
| FM-B1 | **Esca surriscaldata** — la resistenza a 35 °C resta accesa tutta la notte; guasto del controllo di temperatura = riscaldatore a piena potenza incustodito | incendio | **Doppia barriera:** (a) **dimensionamento intrinsecamente sicuro** — la resistenza, a duty 100% in aria ferma, non deve poter superare una temperatura di superficie sicura; (b) **termofusibile o termostato bimetallico in serie**, indipendente dal microcontrollore. Materiali non combustibili nel raggio | **DA DEFINIRE** `VA-20` |
| FM-B2 | **Ricarica su contatti ossidati o parziali** | resistenza di contatto → punto caldo, arco, danno al dock | Contatti **dorati**; **limitazione hardware di corrente** (PTC ripristinabile o fusibile); **dock in tensione solo a robot agganciato** tramite interlock meccanico (reed/microswitch), così i pin esposti non sono mai in tensione | **DA DEFINIRE** `VA-21` |
| FM-B3 | **Pin del dock cortocircuitati** da un oggetto metallico, un animale domestico o un bambino | ustione, arco, incendio | Stesso interlock di FM-B2: **è la ragione principale per cui serve**, più della corrosione | **DA DEFINIRE** `VA-21` |
| FM-B4 | **Sovraccarica della batteria** per guasto del BMS | danno alle celle, rischio termico | **Caricabatterie con tensione di uscita fisicamente ≤ 14,6 V**: la sovraccarica diventa impossibile anche a BMS guasto (§3.2) | **DA DEFINIRE** `VA-13` |
| FM-B5 | **Cortocircuito del pacco** (cablaggio schiacciato, urto) | correnti di centinaia di A | **Fusibile sul positivo, adiacente al morsetto** | **DA DEFINIRE** `VA-13` |
| FM-B6 | **Carica sotto 0 °C** | *lithium plating*, danno permanente | **Protezione di temperatura del BMS** dichiarata a datasheet | **DA DEFINIRE** `VA-13` |
| FM-B7 | **Dita o coda di animale nella girante** della ventola centrifuga | lesione | **Griglia con maglia < 5 mm** su aspirazione e mandata, fissata con viti e non a scatto | **DA DEFINIRE** `VA-22` |
| FM-B8 | **Rilascio incontrollato di CO₂** da cartuccia in ambiente chiuso | accumulo in stanza chiusa | **Orifizio calibrato** che limita per costruzione la portata massima anche a riduttore guasto + **calcolo del caso peggiore** su volume minimo di stanza | **DA DEFINIRE** `VA-23` |
| FM-B9 | **Ribaltamento del robot** — montante di ~120 cm su base differenziale stretta | urto, caduta su persona, incendio se coinvolge la batteria | **Geometria e baricentro**: il rapporto altezza/carreggiata va verificato con prova di inclinazione, non stimato. È un vincolo **di progetto meccanico**, non di software di navigazione | **DA DEFINIRE** `VA-24` |
| FM-B10 | **Caduta dalle scale** | come sopra | Sensori di dislivello **e** limitazione della velocità; se i sensori sono l'unica protezione, va scritto come rischio accettato | **DA DEFINIRE** `VA-25` |
| FM-B11 | **Registrazione di conversazioni** riconoscibili | art. 615-bis c.p., §6.2 | Filtro **passa-banda in acquisizione** e non conservazione della banda piena | **DA DEFINIRE** `VA-18` |
| FM-B12 | **Fermentazione a lievito** come alternativa CO₂ (opzione in `docs/PROJECT.md` §10) | contenitore in pressione **improvvisato**, muffe, rovesciamento | Se adottata: **sfiato permanente non intercettabile** — un contenitore chiuso che fermenta è un recipiente in pressione non certificato, cioè esattamente ciò che §4.1 vieta | **DA DEFINIRE** `VA-26` |

### 7.3 Trasversali

| ID | Modo di guasto | Protezione **hardware** richiesta | Stato |
|---|---|---|---|
| FM-X1 | **Perdita del controllo software** (crash del Pi, kernel panic, deadlock ROS 2) con payload abilitato | **Watchdog hardware** che diseccita l'alimentazione del payload in assenza di heartbeat. Un watchdog implementato nello stesso software che può bloccarsi non è un watchdog | **DA DEFINIRE** `VA-27` |
| FM-X2 | **Arresto d'emergenza non raggiungibile** | **Interruttore fisico di sgancio del payload** su ciascuna unità, accessibile senza smontare nulla e riconoscibile al buio | **DA DEFINIRE** `VA-28` |
| FM-X3 | **Stampa ASA non presidiata** con emissione di stirene in ambiente | Ventilazione del locale (§5). Il rilevamento guasti AI della stampante è una mitigazione dell'incendio, non dell'emissione | **ACCETTATO** — rischio noto, mitigato da ventilazione obbligatoria e filtro; nessun presidio continuo richiesto |

**Righe accettate: 1 su 26.** Le altre 25 sono aperte. Questa tabella è
l'ingresso principale del registro §9.

---

## 8. Conformità delle pull request sul payload

Regola: **0 pull request sul payload chiuse senza una nota di conformità nel
dossier.** "Payload" significa: circuito in pressione, ugello, logica di
ingaggio, esca, riscaldatore, aspirazione, batteria, dock, acquisizione audio o
video.

Una PR sul payload è completa quando, oltre al Decision Log richiesto da
`CONTRIBUTING.md`, riporta:

1. **quale modo di guasto di §7 tocca** (o dichiara di introdurne uno nuovo, e
   allora lo aggiunge alla tabella);
2. **quale protezione hardware** lo copre dopo la modifica;
3. se la modifica **riduce** una protezione esistente, la motivazione e la
   compensazione.

Una PR che modifica il payload e non tocca né §7 né §9 è **incompleta per
definizione**, allo stesso titolo di una che non aggiorna il Decision Log.

Nota per `payload-fluidics` e `mechatronics`, detta una volta sola: le proposte
con **emettitori laser di classe 3B o superiore** (§1) **vengono respinte, non
discusse**. Non è una posizione negoziabile né un invito ad argomentare.

---

## 9. Registro delle voci aperte

Questo è il registro. Il criterio di FATTO è **zero voci aperte applicabili al
gate**. Finché una riga applicabile è aperta, **il gate non passa**.

Colonna **Gate**: `G-PRESS` prova in pressione · `G-INST-A` installazione
Unità A (fase 4) · `G-F6` gate di fase 6 · `—` nessun gate, ma va comunque
chiusa.

| ID | Voce aperta | Chi la chiude | Gate | Condizione di chiusura | Stato |
|---|---|---|---|---|---|
| **VA-01** | `docs/PROJECT.md` §2.1 e §11 citano il testo **previgente** degli artt. 544-bis e 727 c.p. La L. 82/2025 li ha riscritti dal 1º luglio 2025 | chief-engineer | — | Aggiornamento di §2.1 e §11 con pene vigenti e richiamo alla L. 82/2025 | **APERTA** |
| **VA-02** | Valvola di sicurezza: **taratura non determinata**, componente non scelto | `payload-fluidics` | G-PRESS | Valore di taratura calcolato con la regola dell'anello debole (§4.4), componente con datasheet a registro, taratura provata (P-06) | **APERTA** |
| **VA-03** | **Nessun componente in pressione, né la batteria, né il BMS hanno un datasheet a registro.** Copertura certificati: **0/16** | `payload-fluidics` + `mechatronics` | G-PRESS, G-F6 | 16/16 righe di `hardware/bom/README.md` coperte | **APERTA** |
| **VA-04** | Limitazione **hardware** della durata del getto (FM-A4) inesistente | `payload-fluidics` + `mechatronics` | G-PRESS, G-INST-A | Schema del monostabile o del temporizzatore, e valore di T_max motivato | **APERTA** |
| **VA-05** | Comportamento del payload al **ripristino della rete** non definito | `mechatronics` | G-INST-A | Riabilitazione manuale documentata + scarico all'accensione | **APERTA** |
| **VA-06** | Non è definito **dove passi il confine di pressione** nel circuito, quindi non si sa se l'ugello FDM sia parte in pressione | `payload-fluidics` | G-PRESS | Schema con confine di pressione marcato | **APERTA** |
| **VA-07** | **Ancoraggio e rinculo** dell'Unità A non calcolati (FM-A9) | `mechatronics` | G-INST-A | Calcolo della spinta di reazione + specifica dell'ancoraggio e della ritenuta | **APERTA** |
| **VA-08** | **Arresti meccanici** del settore pan-tilt non previsti in D-06 né nel CAD | `mechatronics` | G-INST-A | Battute fisiche nel CAD + verifica sul posto della gittata reale | **APERTA** |
| **VA-09** | **Distanza minima di ingaggio** non definita né imposta via hardware | `payload-fluidics` + `vision-perception` | G-INST-A | Valore motivato e meccanismo che lo impone | **APERTA** |
| **VA-10** | Nessuna regola di **esclusione di nidi, uova e pulli** | `vision-perception` | G-INST-A | Maschera geometrica fissa documentata | **APERTA** |
| **VA-11** | **Soglia di dissuasione efficace e non lesiva** del getto non convalidata (già in `docs/PROJECT.md` §10) | `payload-fluidics` | G-INST-A | Misura su eventi reali, oppure accettazione scritta del limite di pressione come protezione sostitutiva | **APERTA** |
| **VA-12** | **Inibizione oraria** del payload non prevista (FM-A8) | `mechatronics` + `autonomy` | G-INST-A | Fascia oraria definita e meccanismo di inibizione | **APERTA** |
| **VA-13** | **Batteria, BMS e caricabatterie**: nessun datasheet a registro, soglie del BMS non dichiarate, architettura di carica a singolo punto di guasto | `mechatronics` + `autonomy` | G-F6 | Righe elettriche di `hardware/bom/README.md` coperte + caricabatterie con V_max ≤ 14,6 V + fusibile a schema | **APERTA** |
| **VA-14** | Non è noto se l'alimentazione dell'Unità A richieda **un nuovo circuito fisso** (D.M. 37/2008 → impresa abilitata + DiCo) o solo una presa esistente | **utente** | G-INST-A | Risposta: presa esistente idonea, oppure DiCo di impresa abilitata | **APERTA** |
| **VA-15** | **Grado IP** dell'alimentatore esterno e presenza del **differenziale 30 mA** sul circuito non verificati | **utente** + `mechatronics` | G-INST-A | Verifica sul quadro + scelta dell'alimentatore | **APERTA** |
| **VA-16** | Applicabilità del **Reg. UE 2023/1230** (macchine) a un dispositivo autocostruito **privato e non professionale**: non confermata | compliance | — | Approfondimento su fonte primaria o parere. Non blocca i gate: gli obblighi sostanziali sono già imposti da questo dossier | **APERTA** |
| **VA-17** | **Che cosa inquadri effettivamente la camera dal balcone** — non determinabile a tavolino | **utente** + compliance | G-INST-A | Sopralluogo con foto del campo visivo reale; limitazione **ottica/meccanica** se entra spazio altrui | **APERTA** |
| **VA-18** | **Filtro passa-banda in acquisizione** assente: l'audio a banda piena è scrivibile su disco. La revisione privacy esistente è manuale e successiva | `acoustic-perception` | G-F6 | Filtro in acquisizione + non conservazione della banda piena + prova che il parlato non sia intelligibile nel materiale conservato | **APERTA** |
| **VA-19** | **`.gitignore` non blocca** mappe SLAM, audio, video e segreti, mentre `CONTRIBUTING.md` afferma il contrario | `software-platform` | G-F6 | Patch di §6.3 applicata; `CONTRIBUTING.md` resta valido | **APERTA** |
| **VA-20** | **Esca**: nessuna protezione termica indipendente dal microcontrollore (FM-B1) | `payload-fluidics` + `mechatronics` | G-F6 | Termofusibile/bimetallico a schema **e** dimensionamento intrinsecamente sicuro | **APERTA** |
| **VA-21** | **Dock**: pin sempre in tensione, nessun interlock, nessuna limitazione hardware di corrente | `autonomy` + `mechatronics` | G-F6 | Interlock + PTC/fusibile a schema | **APERTA** |
| **VA-22** | **Protezione della girante** non specificata | `payload-fluidics` | G-F6 | Griglia < 5 mm a disegno, fissaggio a vite | **APERTA** |
| **VA-23** | **CO₂**: portata massima e caso peggiore in stanza chiusa non calcolati | `payload-fluidics` | G-F6 | Orifizio calibrato + calcolo su volume minimo di stanza | **APERTA** |
| **VA-24** | **Stabilità al ribaltamento** del montante da 120 cm non verificata | `mechatronics` | G-F6 | Prova di inclinazione con angolo misurato | **APERTA** |
| **VA-25** | Protezione **anticaduta dalle scale**: solo sensoristica, nessuna barriera fisica | `autonomy` | G-F6 | Limitazione di velocità documentata, oppure accettazione scritta del rischio | **APERTA** |
| **VA-26** | Opzione **fermentazione a lievito**: se scelta, è un recipiente in pressione improvvisato | chief-engineer | G-F6 | Sfiato permanente non intercettabile, oppure esclusione dell'opzione | **APERTA** |
| **VA-27** | **Watchdog hardware** del payload assente | `mechatronics` | G-PRESS, G-F6 | Schema del watchdog che diseccita il payload | **APERTA** |
| **VA-28** | **Arresto d'emergenza fisico** non previsto su nessuna delle due unità | `mechatronics` | G-PRESS, G-F6 | Interruttore a schema e in posizione accessibile | **APERTA** |
| **VA-29** | **Comune di installazione non noto**: §2.4 non compilabile | **utente** | G-INST-A | Nome del comune, poi compilazione della checklist C-01…C-13 con gli estremi degli atti | **APERTA** |
| **VA-30** | **Strumenti di misura non in BOM** (già in `docs/PROJECT.md` §10). Senza **manometro di riferimento indipendente** e **anemometro** non sono eseguibili né P-06/P-08 né VA-11 | chief-engineer | G-PRESS | Strumenti in BOM e disponibili | **APERTA** |

**Conteggio alla data: 30 voci, 0 chiuse.**
Per gate: **G-PRESS 8** · **G-INST-A 13** · **G-F6 13** · senza gate 2 (alcune
voci contano su più gate).

---

## 10. Fonti verificate

Elenco delle fonti effettivamente consultate per le affermazioni marcate **[V]**.
Le fonti secondarie sono qualificate come tali. Consultazione: **agosto 2026**.

**Fauna e diritto penale degli animali**
- L. 11 febbraio 1992 n. 157 — testo: <https://nocacciaselvaggia.lipu.it/assets/legge_157_1992.pdf>
- Art. 19 L. 157/1992, controllo della fauna: <https://temi.camera.it/leg19/post/ontrollo-e-contenimento-fauna-selvatica.html>
- Status del colombo di città, Cass. pen. n. 2598/2004, art. 19 e metodi ecologici (fonte secondaria qualificata, Animal Law Italia): <https://ali.ong/rivista/diritto/piccioni-in-citta-normativa-e-gestione/>
- L. 6 giugno 2025 n. 82, riforma dei reati contro gli animali, in vigore dal 1º luglio 2025 — dossier parlamentare: <https://temi.camera.it/leg19/provvedimento/reati-contro-gli-animali.html>
- Testo vigente dell'art. 544-bis c.p.: <https://www.brocardi.it/codice-penale/libro-secondo/titolo-ix-bis/art544bis.html>
- Art. 615-bis c.p.: <https://www.brocardi.it/codice-penale/libro-secondo/titolo-xii/capo-iii/sezione-iv/art615bis.html>
- Art. 674 c.p., getto pericoloso di cose: <https://www.brocardi.it/codice-penale/libro-terzo/titolo-i/capo-i/sezione-ii/art674.html>
- Art. 1122 c.c., opere su parti di proprietà individuale: <https://www.brocardi.it/codice-civile/libro-terzo/titolo-vii/capo-ii/art1122.html>
- Esempio di regolamento comunale restrittivo (Milano) — regolamento in PDF: <https://www.comune.milano.it/documents/20118/253355/Regolamento+per+il+Benessere+e+la+tutela+degli+animali+del+Comune+di+Milano.pdf>

**Attrezzature a pressione**
- Direttiva PED 2014/68/UE: <https://eur-lex.europa.eu/legal-content/IT/TXT/PDF/?uri=CELEX:32014L0068>
- Art. 4 §3 PED, corretta prassi costruttiva e assenza di marcatura CE: <https://www.certifico.com/marcatura-ce/documenti-marcatura-ce/direttiva-ped-dichiarazione-corretta-prassi-costruttiva>
- D.Lgs. 15 febbraio 2016 n. 26, attuazione PED: <https://olympus.uniurb.it/index.php?option=com_content&view=article&id=14774>
- D.M. 1 dicembre 2004 n. 329, art. 1 e art. 2 (esclusioni, lett. i): <https://www.ambientediritto.it/Legislazione/Sicurezzalavoro/2004/dm%202004%20n.%20329.htm>
- Rischi dell'aria compressa (occhi, udito, embolia gassosa): <https://www.puntosicuro.it/lavoratori-C-73/i-rischi-dell-aria-compressa-pistole-di-soffiaggio-raccordi-AR-9991/>

**Elettrico**
- D.M. 37/2008, obbligo di impresa abilitata e Dichiarazione di Conformità: <https://impianti.tech/dichiarazione-conformita-dm-37-08/>
- CEI 64-8, differenziale 30 mA e regola dell'arte richiamata da L. 186/1968 e D.M. 37/2008: <https://hager.com/it/formazione-e-supporto/normative/norma-cei-64-8-impianti-elettrici-residenziali>
- Reg. UE 2023/1230 (macchine), ambito di applicazione: <https://www.certifico.com/macchine/regolamento-ue-2023-1230>
- Obblighi dell'autocostruttore di macchine per uso proprio (fonte secondaria, contesto aziendale): <https://www.ssafety.it/marcatura-ce-macchine-autocostruite/>

**Privacy**
- GDPR art. 2 §2 lett. c) e considerando 18; CGUE **Ryneš C-212/13** dell'11 dicembre 2014: <https://www.diritto.it/garante-privacy-videocamere-private-verso-pubblico/>
- Garante per la protezione dei dati personali, provvedimento **n. 9949494 del 12 ottobre 2023**: <https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/9949494>
- Videosorveglianza, sezione tematica del Garante: <https://www.garanteprivacy.it/temi/videosorveglianza>

**Avvertenza.** Questo dossier è redatto da un non giurista sulla base di fonti
pubbliche. Le righe **[I]** sono interpretazioni ragionevoli, non pareri
legali. Per le decisioni con esposizione verso terzi — installazione
sull'esterno, riprese che escono dalla pertinenza, danni a persone — un parere
professionale costa meno di un procedimento.

---

## Segnalazioni

Per problemi di sicurezza aprire una issue con label `safety`, oppure
contattare il maintainer in privato se ritieni che la divulgazione pubblica
possa creare rischio.
