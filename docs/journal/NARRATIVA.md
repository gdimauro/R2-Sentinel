# Materiale narrativo

Il diario tecnico registra *cosa è successo*. Questo file registra *cosa si può
raccontare*, ed è strutturato per produrre **puntate video, slide e articoli**
senza dover rileggere tutto a posteriori.

Serve perché una storia non si estrae da un registro cronologico: gli archi
narrativi attraversano mesi e si vedono solo se qualcuno li segue mentre
accadono. Chi rilegge dodici mesi di voci a fine progetto trova fatti, non
racconti.

---

## 1. Archi narrativi aperti

Ogni arco è una storia con una domanda iniziale e un pagamento differito.
**Il pagamento è la puntata.** Un arco senza pagamento non è un arco.

### A1 · Il grado che non è di nessuno
**Domanda:** perché tre mestieri diversi in una persona sola?
**Impianto:** il requisito è ~1° a 5 m. Non vive nella meccanica, né
nell'elettronica, né nel firmware: vive nel gioco della cinghia, nel
microstepping, nella rigidità del pezzo stampato e nella deriva termica
dell'ASA al sole. Diviso fra tre, diventa il problema di nessuno.
**Pagamento:** fase 2, quando il numero si misura davvero. Il grado si rispetta
o no, e la decisione D-13a viene promossa o bocciata dai fatti.
**Da riprendere:** la prima misura di ripetibilità, comprese quelle fallite.

### A2 · La corsa contro la stagione
**Domanda:** cosa succede quando il vincolo non è tecnico ma è il calendario?
**Impianto:** 23 agosto. Le zanzare finiscono a settembre. Servono venti notti.
Nessun budget, nessun agente e nessuna ottimizzazione comprimono venti notti.
**Pagamento:** immediato — o le notti si registrano, o la fase 5 slitta di un
anno e la puntata racconta un fallimento di pianificazione.
**Da riprendere:** la prima notte di registrazione. Il buio, il portatile
acceso, il livello che si muove.
**Tensione:** è l'unico arco in cui il progetto può perdere per davvero, ora.

### A3 · Il CTO che non è stato assunto
**Domanda:** di quali ruoli ha bisogno un'azienda di una persona sola e otto
agenti?
**Impianto:** richiesta di assumere «un CTO e un grafico». Entrambi rifiutati
nella forma: il primo si sarebbe sovrapposto al Chief Engineer, e la parte non
sovrapposta — strategia, budget — è dello sponsor, cioè di una persona. Il
secondo avrebbe reso decorazione un deliverable funzionale.
**Pagamento:** quando la squadra funziona o si inceppa su un confine.
**Perché interessa fuori dal progetto:** è la domanda che si stanno facendo
tutti — quale organizzazione serve davvero quando il lavoro lo fanno gli agenti.

### A4 · Non si uccide il piccione
**Domanda:** cosa succede a un progetto quando la legge è un vincolo di
progettazione e non una postilla?
**Impianto:** L.157/1992 e artt. 544-bis e 727 c.p. La legge determina il
payload (non lesivo), il nome (che non promette l'eliminazione) e persino cosa
il sistema può dichiarare di fare.
**Pagamento:** fase 4, quando il getto va tarato fra «efficace» e «non lesivo»
senza un dato di letteratura che dica dove sta il confine.

### A5 · Il sensore da cinque euro
**Domanda:** perché il microfono batte la telecamera da 3.000 €?
**Impianto:** D-04. Vedere una zanzara richiede meno di 1 mm/pixel. Sentirla
richiede un MEMS da 5 € e una FFT, perché il battito alare a 400–600 Hz è una
firma spettrale robusta.
**Pagamento:** fase 5, con il tasso di falsi positivi misurato.
**È la puntata più divulgativa:** il principio — *cambia il senso, non il
budget* — si capisce senza sapere niente di robotica.

### A6 · Le tre valute
**Domanda:** quanto costa far lavorare un'azienda di agenti?
**Impianto:** token, euro e calendario non si convertono l'uno nell'altro.
Il primo consuntivo reale è 83.366 token per costruire la squadra. Il budget è
750.000 al giorno e non si accumula.
**Pagamento:** continuo — `LEDGER.md` è la fonte, e lo scarto fra stima e
consuntivo è la storia.

---

## 2. Registro dei momenti

Episodi brevi, datati e specifici. Sono i **beat** di una puntata: quelli che
si citano testualmente. Vanno annotati quando accadono, perché il dettaglio che
li rende vivi è la prima cosa che si dimentica.

| Data | Momento | Perché funziona | Arco |
|---|---|---|---|
| 2026-08-23 | Il README si apriva con `# [NOME PROGETTO]` e il repository non aveva **un solo commit** | Apertura perfetta: un progetto che esiste come idea completa e come storia zero | — |
| 2026-08-23 | «Che nome ha un ruolo istituzionale di questo tipo?» — e un agente viene rinominato da `project-manager` a `chief-engineer` prima che qualcuno ci lavori sopra | La correzione più economica della giornata. Il nome sbagliato di un ruolo produce il mandato sbagliato | A3 |
| 2026-08-23 | Accuso il Chief Engineer di aver dichiarato lavoro non fatto. Stava ancora scrivendo | Errore mio, non suo: ho letto uno stato transitorio come definitivo. È il rischio strutturale del lavorare con agenti asincroni | A3 |
| 2026-08-23 | La finestra stagionale emerge **dentro un report di routine**, non da un'analisi dedicata | Il vincolo più grave del progetto arriva di lato, mentre si parlava d'altro | A2 |
| 2026-08-23 | Otto criteri di FATTO tutti numerici — e nessuno strumento in BOM per misurarli | Si può fare tutto giusto e non poter dichiarare finito niente | A6 |
| 2026-08-23 | I materiali non erano a bilancio. Se ne accorge **l'utente**, non gli agenti | Contrappunto necessario: la squadra di agenti aveva un buco che ha visto una persona | A6 |
| 2026-08-23 | Il cruscotto non si apre nel browser di VS Code: non è autenticato | Piccolo, ma è il genere di attrito reale che i racconti sull'IA omettono sempre | A6 |
| 2026-08-23 | «Già devo provvedere a procurare i soldi per comprarti i token» | **Il momento migliore finora.** Descrive un'azienda ruotata di novanta gradi: il personale non prende stipendio ma consuma capienza, e l'unico dipendente con un corpo è il proprietario | A6 |
| 2026-08-23 | Un agente viene bloccato dai safeguard dell'API con flag `[bio]` — stava calcolando la soglia di **non lesività** che la legge impone | Il vincolo di sicurezza e il sospetto di pericolosità coincidono sullo stesso tema | A4 |
| 2026-08-23 | «Gli acquisti vanno fatti con fattura rigorosamente» — e metà della lista d'acquisto decade, non per prezzo ma per canale | Otto agenti e nessuno aveva chiesto in che perimetro amministrativo si opera | A6 |

---

## 3. Piano di ripresa

Cosa filmare, fase per fase. **La regola è quella del giornale: il testo si
ricostruisce, la ripresa no.**

| Fase | Da riprendere assolutamente | Perché è irripetibile |
|---|---|---|
| **0** | La stampante che esce dalla scatola. La prima stampa. La **prima stampa fallita**. Il primo provino ASA che si delamina | Accade una volta sola e si butta per istinto |
| **1** | Lo schermo mentre il CAD parametrico genera le due varianti cambiando una variabile | È il concetto di D-09 reso visibile in tre secondi |
| **2** | Il primo movimento del pan-tilt. Il laser sul bersaglio a 5 m. Le venti ripetizioni, **anche quelle fuori tolleranza** | Il momento in cui A1 viene pagato |
| **3** | Il primo bounding box su un piccione vero, dal balcone | |
| **4** | La prima raffica. Il piccione che se ne va — o che resta | Il verdetto su A4, e non è detto che vada bene |
| **5** | La prima notte: buio, portatile acceso, livello che si muove. Lo spettro con il picco a 400–600 Hz che emerge dal rumore | Il pagamento di A2 e A5 insieme. Se salta la stagione, questa ripresa non esiste per un anno |
| **6** | La retina della camera di raccolta, al mattino | |
| **7** | Il primo rientro autonomo al dock | |

**Audio di presa diretta, sempre.** Gli stepper, la ventola, la raffica, il
battito alare registrato. Un documentario su una macchina che *ascolta* non può
avere audio ricostruito.

---

## 4. Formati d'uscita

| Formato | Taglio | Materiale che richiede |
|---|---|---|
| **Puntata video** | Un arco per puntata, con il suo pagamento. A5 e A2 sono i più autonomi | Riprese, audio di presa diretta, schermate in movimento |
| **Articolo** | Una decisione e il suo perché. Il Decision Log è già la scaletta | Solo testo — ricostruibile a posteriori |
| **Slide** | A3 e A6 funzionano come intervento su organizzazione ed economia degli agenti | Diagrammi da `design-docs`, numeri da `LEDGER.md` |
| **Documentario** | Tutti gli archi intrecciati sull'arco stagionale | **Tutto il materiale, dall'inizio.** È il formato che non tollera buchi |

---

## 5. Regola di manutenzione

Ogni voce di diario chiude chiedendosi: **c'è un momento da registrare qui?**
Se sì va nella tabella §2 lo stesso giorno, con la data e il perché funziona.

Un momento annotato una settimana dopo è già una parafrasi.
