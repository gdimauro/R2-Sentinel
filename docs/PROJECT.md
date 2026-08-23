# Progetto: Sistema robotico di rilevamento e intervento su infestanti

**Nome in codice:** R2-Sentinel
**Versione documento:** 0.7
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
| 0.4 | 2026-08-23 | **Squadra di specialisti definita** (D-13): sei agenti in `.claude/agents/`, ciascuno con criterio di FATTO misurabile e handoff espliciti. **Payload fluidico assegnato a un ruolo unico trasversale** `payload-fluidics` (D-14). Quattro nuove questioni aperte in §10, fra cui la **finestra stagionale del dataset zanzare**, che è il bloccante di calendario principale del progetto. |
| 0.5 | 2026-08-23 | Squadra estesa a **otto agenti** (D-15): aggiunti `software-platform` (workspace ROS 2, CI, riproducibilità, Git LFS, MQTT→Home Assistant) e `design-docs` (documentazione come deliverable replicabile). Entrambi erano stati richiesti come “CTO” e “grafico” e **rifiutati in quella forma**, con la motivazione in D-15. Ridefinito il confine sulla documentazione fra chief-engineer e `design-docs`, che modifica D-13. |
| 0.6 | 2026-08-23 | Aggiunto **`retrospective`**, nono agente (D-16): sintesi serale, lezioni apprese e proposte di emendamento ai mandati. Copre un'area che prima non era di nessuno — il **miglioramento continuo della squadra**. Vincolo di governance: **propone e non applica**, con l'eccezione che le proposte sul mandato del chief-engineer vanno allo sponsor e non a lui. Richiesto come «agente HR», **rinominato**: è kaizen, non risorse umane. |
| 0.7 | 2026-08-23 | **Correzione normativa** dal primo ciclo di `compliance-safety`: §2.1 e §11 citavano il testo **previgente** degli artt. 544-bis e 727 c.p., riscritti dalla **L. 6 giugno 2025 n. 82** in vigore dal 1º luglio 2025 (D-17). Nuova **§2.4**: tre norme mai considerate — artt. 674 e 659 c.p., art. 1122 c.c. — che vincolano l'Unità A **più di quelle sugli animali** (D-18). **Arresti meccanici** di settore sul pan-tilt (D-19, estende D-06) e **caricabatterie a tensione fisicamente limitata** (D-20, estende D-07). Serbatoio **fuori PED e fuori D.M. 329/2004**: la marcatura CE-PED non va pretesa (D-21). §10: vincolo di sfiato sulla fermentazione e rilievo del balcone. |

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

- Il piccione di città (*Columba livia*) rientra nella **fauna selvatica tutelata dalla Legge 157/1992**. Non è specie cacciabile (art. 18) e il controllo della fauna selvatica è riservato alle Regioni (art. 19): non è un'attività che un privato possa svolgere in proprio.
- **Quadro penale aggiornato alla L. 6 giugno 2025 n. 82 («legge Brambilla»), in vigore dal 1º luglio 2025**, che ha riscritto il Titolo IX-bis del codice penale. Le versioni di questo documento fino alla 0.6 citavano il **testo previgente**: vedi D-17.

| Norma | Condotta | Pena vigente |
|---|---|---|
| **art. 544-bis c.p.** | cagionare la morte di un animale **per crudeltà o senza necessità** | reclusione **6 mesi – 3 anni**, **congiunta** a multa **5.000 – 30.000 €** |
| art. 544-bis c. 2 | con **sevizie** o prolungando volutamente le sofferenze | reclusione **1 – 4 anni** + multa **10.000 – 60.000 €** |
| **art. 727 c.p.** | abbandono; detenzione in condizioni produttive di gravi sofferenze | arresto fino a **1 anno** o ammenda **5.000 – 10.000 €** |

- **Il cambio di paradigma conta più dell'inasprimento delle pene.** Il bene giuridico tutelato non è più il *sentimento umano* verso gli animali, ma **l'animale come essere senziente e vittima diretta del reato**. Conseguenza pratica per questo progetto: l'argomento «non se n'è accorto nessuno, nessuno si è offeso» **non ha più alcun valore difensivo** — rileva l'effetto sull'animale, non la percezione di chi guarda. Ogni valutazione di ammissibilità del payload va fatta su questo criterio.
- Rafforza **D-12**: il nome del progetto non promette l'eliminazione del bersaglio. Era la scelta corretta già con la norma previgente, lo è a maggior ragione con quella vigente.
- Sono ammessi **esclusivamente metodi di dissuasione non cruenti**. Alcuni comuni (es. Milano) hanno inoltre ordinanze che vietano specificamente i dissuasori pericolosi, inclusi i comuni dissuasori ad aghi.
- **Implicazione progettuale:** il payload rivolto ai piccioni deve essere non lesivo (getto d'aria, nebulizzazione, stimolo sonoro/visivo). Nessun contatto lesivo, nessun proiettile, nessuna trappola.
- **Da verificare:** regolamento del proprio comune, che può essere più restrittivo della norma nazionale.
- **Attenzione:** il vincolo più stringente sull'Unità A **non è questo**. Vedi **§2.4**.

### 2.2 Zanzare — nessun sistema laser

Il laser (approccio tipo *Photonic Fence*) è **escluso dal progetto**. Motivazione tecnica:

- Per abbattere una zanzara in volo serve un laser di **classe 4**, potenza dell'ordine dei watt.
- Su un dispositivo **mobile**, che **punta bersagli in movimento**, in ambiente domestico con persone e animali: il danno retinico è permanente e avviene in millisecondi, senza possibilità di reazione riflessa. Si aggiunge il rischio di innesco su tessuti e materiali.
- Nessuna schermatura o interlock realizzabile in autocostruzione rende accettabile questo rischio.

**Alternativa adottata:** aspirazione meccanica con esca (§4.3).

### 2.3 Alimentazione

- Il concetto iniziale di "braccetto che si collega a una presa a muro a 230 V" è **abbandonato**: complessità meccanica alta e rischio elettrico non gestibile in autocostruzione.
- **Sostituito da:** dock di ricarica a pavimento con contatti a molla e beacon IR (standard di fatto nella robotica domestica).

### 2.4 Unità A — vicinato e spazio pubblico

Tre norme che il progetto non aveva considerato fino alla versione 0.6, e che **vincolano l'Unità A più di quelle sulla fauna** (D-18). Non riguardano l'animale: riguardano *dove finisce* ciò che l'apparecchio emette.

- **art. 674 c.p. — getto pericoloso di cose.** Punisce chi getta o versa, in luogo di pubblico transito o in luogo privato di comune o altrui uso, cose atte a **offendere, imbrattare o molestare** persone. Un getto d'aria o d'acqua da un balcone che raggiunge la strada, il cortile o il balcone del vicino **ricade letteralmente nella fattispecie**. È la norma più concretamente rischiosa dell'intero progetto, e vincola la **direzione ammessa** del payload, non solo la sua intensità: è quindi un **requisito di progetto della testa pan-tilt** (D-19), non un avvertimento d'uso.
- **art. 659 c.p. — disturbo delle occupazioni o del riposo.** Un dissuasore **acustico** attivo di notte è esattamente la condotta descritta. **Il dissuasore sonoro è escluso in orario notturno**, e l'inibizione oraria va realizzata preferibilmente su base hardware.
- **art. 1122 c.c.** — l'installazione su balcone non deve pregiudicare stabilità, sicurezza o decoro architettonico, ed è comunque **dovuta preventiva notizia all'amministratore di condominio**, che ne riferisce all'assemblea. L'assemblea non autorizza, ma può agire per inibire. È un adempimento **preventivo**: farlo dopo l'installazione non sana nulla.


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
| D-13 | Squadra di **sei agenti specialisti** in `.claude/agents/` *(estesa a otto da D-15)*: `mechatronics`, `vision-perception`, `acoustic-perception`, `autonomy`, `payload-fluidics`, `compliance-safety` — più il `chief-engineer` che li coordina | La squadra è derivata dalla decomposizione del sistema, non dalle discipline accademiche. Tre ragioni strutturali. **(a) CAD, elettronica e firmware stanno in un ruolo solo** (`mechatronics`): il requisito duro di ~1° a 5 m (D-06) non vive in nessuno dei tre mestieri, vive nel gioco della cinghia, nel microstepping, nella rigidità del pezzo stampato e nella deriva termica dell'ASA al sole, tutti insieme. Diviso fra tre agenti diventa il problema di nessuno e ognuno lo dichiara rispettato nel proprio dominio. **(b) L'organizzazione è per macchina, non per disciplina**: Unità A (visione, meccanica di precisione, mira) e Unità B (DSP, navigazione, fluidodinamica dell'esca) condividono pochissimo oltre alla base comune, e §9 osserva già che le fasi 1–4 e 5–8 sono parallelizzabili. Il chief-engineer è l'unico ponte. **(c) `acoustic-perception` entra in fase 1, non in fase 5**: il suo lavoro è vincolato dal calendario e non dallo sforzo — servono notti di registrazione e nessuna aggiunta di risorse le comprime. Entra presto per **iniziare a raccogliere**, non per costruire il classificatore. È l'unica decisione di sequenza che sposta davvero la data di consegna. **Ruoli deliberatamente non creati:** integrazione di sistema, misura, BOM/approvvigionamento e manutenzione della documentazione restano del chief-engineer, perché sono le funzioni che rendono confrontabili i risultati degli altri — **il punto sulla documentazione è stato poi ridefinito da D-15**, che separa il *perché* (Decision Log e testo di questo documento, che restano del chief-engineer) dal *come replicarlo* (schemi, sequenze di assemblaggio, presentazione pubblica, che passano a `design-docs`) e delegarle significherebbe perdere l'unico punto in cui il sistema è visto intero; nessun ruolo di puro processo o coordinamento, perché il coordinamento è il chief-engineer; nessun ruolo separato per la produzione e la stampa 3D, perché chi progetta il pezzo deve subire il vincolo di stampabilità (D-10, D-11) invece di scaricarlo a valle. **Regole di qualità imposte a ogni file agente:** un criterio di FATTO espresso in numeri o test, handoff espliciti in entrata e in uscita, `tools` al minimo indispensabile, e i vincoli non negoziabili del progetto copiati dentro il file dove si applicano — un vincolo che non è nel prompt di un agente non verrà rispettato. `compliance-safety` è l'unico senza `Write` né `Bash`: verifica e non costruisce, e un verificatore che scrive anche la soluzione smette di essere un verificatore. | 2026-08-23 |
| D-14 | Il **payload fluidico di entrambe le unità è di un ruolo unico trasversale**, `payload-fluidics`, anziché diviso fra i due equipaggi | Scartata l'alternativa di assegnare il getto d'aria all'equipaggio dell'Unità A e l'aspirazione con esca a quello dell'Unità B, che sarebbe stata coerente con l'organizzazione per macchina (D-13b). Tre ragioni la superano. **(1) È la stessa fisica**: getto libero comprimibile in uscita da un ugello convergente, flusso di cattura in ingresso a una bocca di aspirazione e pennacchio di diffusione dell'esca sono lo stesso mestiere — geometria di condotto, portata, decadimento del getto con la distanza. Diviso in due, quel mestiere viene imparato due volte e male. **(2) Concentra i rischi fisici più seri del progetto**: serbatoio a 5 bar, cartuccia CO₂, resistenza a 35 °C sempre accesa di notte. La competenza sugli apparecchi in pressione (SAFETY.md §4) non si può fare a metà in due equipaggi: duplicarla significa diluirla. **(3) Il numero che governa l'Unità A è un numero fluidodinamico**, non meccanico né di visione: quanta velocità d'aria deve arrivare sul bersaglio a 5 m perché il piccione se ne vada restando ampiamente sotto qualunque soglia di lesività (§2.1). Nessun altro ruolo ha gli strumenti per determinarlo e misurarlo. **Costo accettato:** è l'unico specialista che attraversa entrambe le unità, quindi è un potenziale collo di bottiglia fra le due catene di fasi parallele (1–4 e 5–8) e va sorvegliato dal chief-engineer. **Confine tagliato per contenerlo:** `payload-fluidics` possiede la fluidica e i sorgenti CAD dei soli pezzi fluidici (ugello, girante); struttura, carter e staffe restano a `mechatronics`; la verifica normativa e la certificazione dei componenti in pressione restano a `compliance-safety`, che lo verifica e non coincide con lui. | 2026-08-23 |
| D-15 | Squadra estesa a **otto agenti** con `software-platform` e `design-docs`. Entrambi erano stati richiesti come **“un CTO” e “un grafico”** e sono stati **rifiutati in quella forma**, non nella sostanza | **Perché non un CTO.** Un ruolo di direzione tecnica si sarebbe sovrapposto quasi interamente al chief-engineer, che già possiede architettura, confini, misura e Decision Log: due proprietari della stessa cosa significa nessun proprietario, ed è esattamente l’errore che D-13a evita sul requisito di ~1°. La parte che *non* si sovrappone — strategia, budget, buy-vs-build, priorità fra le due unità — è dello **sponsor del progetto**, non di un agente: è lui a decidere quanto spendere e cosa vale la pena costruire, e §10 registra infatti il budget complessivo come questione aperta a lui. Il buco reale non era la direzione: era la **pratica software condivisa** — workspace ROS 2, CI, harness di test, riproducibilità di Ubuntu 24.04 + Jazzy + ESP-IDF, pesi dei modelli tenuti fuori dal repository, **Git LFS su `cad/export/`, che `.gitattributes` già instrada ma che non funziona perché `git-lfs` non è installato**, e il livello MQTT → Home Assistant (§6). Sono cose che tutti e cinque gli specialisti consumano e che nessuno di loro ha mandato di costruire: lasciate a loro, verrebbero costruite quattro volte e in modo divergente. Quindi `software-platform`, ruolo tecnico con deliverable eseguibili, non ruolo di direzione. **Perché non un grafico.** In un progetto chiuso la documentazione è un residuo estetico; in un **open hardware con tre licenze separate e l’ambizione dichiarata di essere replicato** è il prodotto stesso: uno schema di cablaggio incompleto non è un difetto di gusto, è un progetto non replicabile. Chiamarlo “grafico” avrebbe declassato a decorazione un deliverable funzionale e ne avrebbe reso impossibile la misura. `design-docs` è quindi definito su un criterio di FATTO comportamentale e non estetico: **un terzo che non ha mai visto il progetto assembla il modulo con la sola documentazione, senza fare domande** — e ogni domanda posta è contata come difetto. **Confine con il chief-engineer, che modifica D-13:** il chief-engineer possiede le decisioni e il **perché** (Decision Log §3 e testo di questo documento); `design-docs` possiede il **come replicarlo** (schemi di cablaggio, sequenze di assemblaggio, schede pezzo, diagrammi, sinottico, README e presentazione pubblica). Cita il Decision Log, non lo riscrive. **Confine con `software-platform`:** questo genera gli artefatti automatici (distinta pezzi, schema dei topic, esiti dei test), `design-docs` li consuma anziché trascriverli, così non divergono. | 2026-08-23 |
| D-16 | Aggiunto **`retrospective`**, nono agente: sintesi serale, lezioni apprese e **proposte di emendamento ai mandati**. Richiesto dallo sponsor come «un agente HR o altro» e **rinominato** | **Perché non «HR».** Non si assume nessuno, non si valuta nessuno, non ci sono persone da gestire: c'è una sola persona nel progetto ed è lo sponsor stesso. La funzione reale è **kaizen** — osservare come si comportano i mandati sul campo e correggerli — e il suo oggetto di studio non sono gli agenti ma **i file che li definiscono**. Chiamarlo HR avrebbe importato un modello di valutazione del personale che qui non ha referente e avrebbe mancato il deliverable vero. **Perché serviva un ruolo.** La copertura cambia: fino a D-15 il **miglioramento continuo non era di nessuno**. Ogni agente vede la propria giornata, il chief-engineer vede il sistema tecnico; nessuno vedeva il comportamento della squadra **nel tempo**. La distinzione operativa che nessun altro può fare: *un errore capitato una volta è un fatto e finisce nel giornale; capitato due volte è un difetto di mandato* — il file dell'agente non lo preveniva e va emendato. **Non è una cerimonia:** `AGILE.md` §6 esclude la retrospettiva come riunione, e resta escluso — `retrospective` non convoca nulla, legge ciò che è già scritto (report, giornale, libro mastro, board) e ne ricava sintesi e proposte. **Vincolo di governance — propone e non applica.** Gli emendamenti ai file in `.claude/agents/` li applica il chief-engineer. La ragione è il precedente di **D-14**, che tiene `compliance-safety` separato da `payload-fluidics` con una frase sola: *se coincidessero, il verificatore sarebbe il progettista*. Qui vale all'incontrario: il chief-engineer ha **scritto tutti i mandati**, quindi non può essere anche l'unico a giudicare se funzionano. Due mani diverse su ogni emendamento. **Eccezione esplicita, senza la quale la regola non tiene:** le proposte di emendamento al mandato **del chief-engineer stesso non passano dal chief-engineer** — vanno allo **sponsor**, per una via che il chief-engineer non controlla (una riga in `docs/AZIONI-SPONSOR.md`, che lo sponsor legge ogni giorno nel rapporto). Senza l'eccezione l'unico ruolo autorizzato ad applicare gli emendamenti sarebbe anche l'unico giudice di quelli che riguardano sé stesso, cioè esattamente la coincidenza fra verificatore e progettista che D-14 vieta: il ciclo si chiuderebbe su sé stesso. Il chief-engineer viene informato che la proposta esiste, ma non ha voce sul suo esito. Per simmetria, le proposte sul mandato di `retrospective` seguono la stessa via. **Confine con `design-docs`:** il giornale resta suo (cura, continuità, estrazione narrativa) e `retrospective` non riscrive le voci altrui — le **legge** e ci aggiunge solo la sintesi serale; una voce riscritta da terzi non è più una testimonianza. **Confine con lo sponsor:** priorità, budget e decisioni di §10 restano suoi (`AGILE.md` §5); `retrospective` non è un project manager e non facilita nulla. | 2026-08-23 |
| D-17 | **Quadro penale sugli animali aggiornato alla L. 6 giugno 2025 n. 82** («legge Brambilla»), in vigore dal 1º luglio 2025. §2.1 e §11 riscritte. **È una correzione, non un'aggiunta: il progetto citava norme superate** | Primo reperto del primo ciclo di `compliance-safety`, verificato in modo indipendente. Fino alla versione 0.6 il documento riportava il testo **previgente** dell'art. 544-bis (4 mesi–2 anni), superato da oltre un anno: la pena vigente è **reclusione 6 mesi–3 anni congiunta a multa 5.000–30.000 €**, con aggravante fino a 4 anni e multa raddoppiata in caso di sevizie. **Ma la parte che cambia il progetto non sono le pene: è il bene giuridico tutelato.** Non è più il *sentimento umano* verso gli animali, ma **l'animale come essere senziente e vittima diretta del reato**. Conseguenza operativa e non teorica: cade ogni argomento del tipo «non se n'è accorto nessuno, nessuno si è offeso» — rileva l'effetto sull'animale, non la percezione di chi guarda. Ogni valutazione di ammissibilità del payload va rifatta su questo criterio, e `payload-fluidics` deve dimostrare la non lesività **sull'animale**, non l'assenza di lamentele. **Rafforza D-12:** il nome del progetto non promette l'eliminazione del bersaglio; era la scelta corretta già con la norma previgente e lo è a maggior ragione ora. **Lezione di metodo, che vale oltre questo caso:** un vincolo legale citato una volta e mai riverificato invecchia in silenzio, e nessuno se ne accorge finché non serve. La verifica periodica delle norme citate è di `compliance-safety` e va rifatta a ogni gate, non una volta sola. | 2026-08-23 |
| D-18 | **Il vincolo dominante sull'Unità A non è la norma sugli animali: è l'art. 674 c.p.** Nuova §2.4 con artt. 674 e 659 c.p. e art. 1122 c.c. | Tre norme che nessuno aveva considerato in sedici decisioni precedenti, e che vincolano l'Unità A **più di quelle sulla fauna**, perché non riguardano l'animale ma **dove finisce ciò che l'apparecchio emette**. **Art. 674 c.p. (getto pericoloso di cose):** punisce chi getta o versa, in luogo di pubblico transito o in luogo privato di comune o altrui uso, cose atte a offendere, imbrattare o **molestare** persone. Un getto d'aria o d'acqua da un balcone che raggiunga la strada, il cortile o il balcone del vicino **vi ricade letteralmente**. È il ribaltamento concettuale della giornata: fino a qui il progetto aveva trattato la sicurezza del payload come una questione di **intensità** (quanta velocità d'aria è non lesiva). L'art. 674 la rende anche e soprattutto una questione di **direzione** — un getto perfettamente innocuo per intensità resta illecito se esce dalla propria pertinenza. Da qui D-19. **Art. 659 c.p. (disturbo del riposo):** un dissuasore acustico notturno è esattamente la condotta descritta → il dissuasore sonoro è **escluso in orario notturno**, con inibizione preferibilmente hardware. Chiude in negativo una delle opzioni di payload che §2.1 elencava come ammissibili. **Art. 1122 c.c.:** preventiva notizia all'amministratore di condominio, **dovuta**. È un adempimento preventivo: farlo dopo l'installazione non sana nulla, ed è a costo zero solo se fatto prima. Scartata l'ipotesi di trattarle come avvertenze d'uso in `SAFETY.md`: sarebbero arrivate a CAD congelato. Diventano requisiti di progetto di fase 1. | 2026-08-23 |
| D-19 | **Limitazione del settore angolare pan-tilt con arresti meccanici**, non con un limite software. Estende **D-06** | Un limite scritto in un file di configurazione **non è una protezione**: si perde in un aggiornamento, si aggira con un parametro, non sopravvive a un firmware ricaricato male, e non è dimostrabile a un terzo. La protezione deve essere **geometrica**: battute fisiche che rendono *impossibile* uscire dal settore, non finecorsa elettrici — che sono sensori, non arresti. **Ha una doppia motivazione, ed è la ragione per cui è una decisione e non un dettaglio costruttivo:** (1) **mira** — un settore limitato riduce l'escursione utile e quindi l'errore accumulato sulla catena di riduzione, a beneficio del requisito di ~1° a 5 m di D-06; (2) **art. 674 c.p.** (D-18) — è l'unico modo per garantire che il getto non possa raggiungere la via o la proprietà del vicino nemmeno in caso di errore di detection, deriva di calibrazione o comando errato. Due requisiti indipendenti che chiedono la stessa cosa: quando accade, la cosa si fa. **Impatto immediato su fase 1:** il settore ammesso dipende dalla geometria del balcone reale, che non è ancora rilevata — vedi §10. `mechatronics` non può congelare il CAD della testa prima di quel rilievo, e `payload-fluidics` deve verificare la **gittata reale sul posto** prima di qualunque abilitazione. | 2026-08-23 |
| D-20 | **Caricabatterie fisicamente incapace di superare 14,6 V**, come seconda barriera indipendente. Estende **D-07** | D-07 aveva scelto la chimica LiFePO4 perché non va in thermal runaway, ma lasciava implicito che il BMS fosse *la* protezione. Correzione: su un dispositivo che **carica di notte, in casa, incustodito**, il BMS è la **seconda** protezione, non la prima. La prima deve essere l'impossibilità fisica della condizione pericolosa: un alimentatore la cui tensione a vuoto non possa eccedere **14,6 V** (4S LiFePO4 a 3,65 V/cella) non può sovraccaricare il pacco nemmeno se il BMS fallisce. Due barriere indipendenti, nessuna delle quali affidata al software. È lo **stesso principio di D-19** applicato all'elettrico: la protezione che conta è quella che rende la condizione pericolosa impossibile, non quella che la rileva e reagisce. Vale la pena notare che il progetto ha ora due decisioni che dicono la stessa cosa in due domini diversi — è un principio di progettazione, non due coincidenze. | 2026-08-23 |
| D-21 | Serbatoio aria: **non pretendere la marcatura CE-PED**, pretendere il **datasheet**. Il recipiente è fuori PED e fuori D.M. 329/2004 | Risultato **controintuitivo** e per questo registrato: l'istinto è chiedere «il pezzo più certificato possibile». I numeri dicono altro. Con PS = 5 bar e V = 2 L si ha **PS·V = 10 bar·L**, sotto la soglia di **50 bar·L** della direttiva 2014/68/UE (PED); e V ≤ 25 L tiene il recipiente fuori dall'obbligo di verifica periodica del **D.M. 329/2004**. Il recipiente è quindi legittimamente **fuori dal campo di applicazione** di entrambe. **Conseguenza pratica:** pretendere la marcatura CE-PED significa cercare un documento **che non esiste** — si scarterebbero fornitori corretti, si ritarderebbero gli acquisti e, nel caso peggiore, si accetterebbe una marcatura fasulla scambiandola per garanzia. Il documento da pretendere è il **datasheet** con pressione di esercizio e di scoppio dichiarate. **Non è però innocuo, e la conclusione non va letta come un via libera:** l'energia immagazzinata è di **1,2–2,2 kJ**. Restano non negoziabili la **valvola di sicurezza tarata**, i componenti certificati per pressione e il divieto assoluto di recipienti stampati in 3D (SAFETY.md §4). Fuori dall'obbligo normativo non significa fuori dal rischio: significa soltanto che la sicurezza qui è a carico del progetto e non di un ente terzo. | 2026-08-23 |

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
- [ ] Esca CO₂: cartuccia (comoda, ricorrente) vs fermentazione (gratis, manutenzione). **Vincolo sulla scelta, non nota a margine (D-21):** la fermentazione a lievito **è un recipiente in pressione improvvisato** — produce gas in continuo in un contenitore chiuso, senza valvola tarata e senza pressione di scoppio dichiarata. È ammissibile **solo** con **sfiato permanente non intercettabile** (non una valvola, non un tappo che si possa stringere: un'apertura che non può essere chiusa nemmeno per errore). Va deciso **prima** di dimensionare la camera dell'esca, perché cambia la geometria del contenitore: deciderlo dopo significa rifarla.
- [ ] Autonomia target dell'Unità B — determina il dimensionamento batteria
- [ ] L'Unità A va alimentata da rete o autonoma? (rete è molto più semplice se c'è una presa esterna)
- [ ] Strategia di raccolta dataset zanzare
- [ ] Da quale modulo CAD partire: testa pan-tilt (raccomandato) o telaio base mobile
- [ ] Gestione dello svuotamento della camera di raccolta
- [ ] **Finestra stagionale del dataset zanzare** — aperta con D-13. La raccolta è vincolata dal calendario e non dallo sforzo, e in Italia le zanzare sono attive circa da maggio a settembre/ottobre. Alla data di questo documento (23 agosto 2026) la finestra è **quasi chiusa**: se la raccolta non parte entro poche settimane, la fase 5 slitta di un anno intero, non di qualche settimana. Va deciso subito se aprire un banco di registrazione minimo *prima* che il resto dell'Unità B esista.
- [ ] **Strumenti di misura non ancora in BOM** — i criteri di FATTO degli agenti richiedono strumentazione che §5 non prevede: reticolo di riferimento a 5 m e supporto per la misura angolare, anemometro (a filo caldo o a ventolina) per getto e aspirazione, analizzatore logico o equivalente per il jitter del loop firmware, riferimento acustico per calibrare il microfono. Senza, i numeri non sono misurabili e i gate non chiudono. Da quantificare e aggiungere al BOM.
- [ ] **Soglia di dissuasione efficace del getto d'aria** — la letteratura non fornisce un valore di velocità dell'aria al bersaglio che dissuada il piccione senza essere lesivo. L'intervallo 8–25 m/s a 5 m assunto nel criterio di FATTO di `payload-fluidics` è una stima di primo tentativo da confermare sperimentalmente su eventi reali, non un dato acquisito.
- [ ] **Autocontaminazione acustica dell'Unità B** — la ventola centrifuga da 80 mm sta a pochi centimetri dal microfono I2S e la sua banda può sovrapporsi ai 400–600 Hz del battito alare (D-04). Se la sovrapposizione è significativa serve un ciclo alternato ascolto/aspirazione, con impatto sull'efficacia di cattura. Da misurare prima di congelare il montante.
- [ ] **Soggetti per il test del terzo** — aperta con D-15. Il criterio di FATTO di `design-docs` richiede **≥2 persone diverse** che non hanno mai visto il progetto e che assemblino un modulo con la sola documentazione. Non è ancora definito chi siano né come reclutarli, e senza di loro quel criterio non è verificabile: va risolto prima del congelamento del primo modulo, non dopo.
- [ ] **Rilievo geometrico del balcone di installazione** — aperta con D-18 e D-19, ed è **bloccante per la fase 1**. Il settore angolare ammesso della testa pan-tilt discende dall'art. 674 c.p.: il getto non deve poter raggiungere la via, il cortile o la proprietà del vicino. Quel settore non è deducibile a tavolino — dipende da quota, esposizione, distanza dai confini e da cosa c'è sotto e di fronte. Serve un rilievo con misure e foto **prima** che `mechatronics` congeli il CAD della testa, perché le **battute meccaniche** (D-19) sono geometria del pezzo e non un parametro modificabile dopo. Da esso discende anche la verifica di gittata reale sul posto che `payload-fluidics` deve eseguire prima di qualunque abilitazione.

---

## 11. Riferimenti

**Normativa** *(aggiornata alla L. 82/2025 — vedi D-17; il dossier completo con le fonti è in `SAFETY.md`)*
- **L. 6 giugno 2025 n. 82** («legge Brambilla»), in vigore dal **1º luglio 2025** — riforma dei reati contro gli animali, riscrive il Titolo IX-bis c.p.
- Artt. **544-bis** (uccisione: 6 mesi–3 anni + multa 5.000–30.000 €) e **727** c.p., **nel testo vigente**
- **Legge 157/1992** — fauna selvatica; art. 18 specie cacciabili, art. 19 controllo riservato alle Regioni
- **Art. 674 c.p.** — getto pericoloso di cose: il vincolo dominante sull'Unità A (§2.4)
- **Art. 659 c.p.** — disturbo del riposo: esclude il dissuasore acustico notturno
- **Art. 1122 c.c.** — preventiva notizia all'amministratore di condominio
- **Dir. 2014/68/UE (PED)** e **D.M. 329/2004** — apparecchi in pressione: il serbatoio del progetto ne è **fuori**, vedi D-21
- Ordinanze comunali locali sui dissuasori

**Tecnici**
- Frequenza battito alare *Culex* / *Aedes*: 400–600 Hz
- Velocità di volo zanzara: 1–1,5 m/s
- Precisione angolare richiesta a 5 m per getto mirato: ~1°

**Fornitori**
- Craftcloud, Weerg, Xometry, Protolabs Network, JLC3DP
