# Piano economico dell'azienda virtuale

**Versione:** 0.1 · **Data:** 23 agosto 2026
**Stato:** prima stesura — i costi in token derivano da una sola misura reale, il resto è stima da calibrare

---

## 1. Le tre valute

L'errore che questo documento evita è contabilizzare una risorsa sola. R2-Sentinel
consuma tre cose che non si convertono l'una nell'altra.

| Valuta | Compra | Non compra |
|---|---|---|
| **Token** | Analisi, codice, protocolli di misura, documentazione, decisioni istruite | Un anemometro. Una cinghia montata. Una notte di registrazione. |
| **Euro** | Stampante, BOM, strumenti di misura, service SLS | Il tempo per usarli |
| **Ore-persona e calendario** | Assemblaggio, cablaggio, misura, riprese, raccolta dataset | Nulla le sostituisce, e il calendario non si compra affatto |

**La regola che ne discende:** prima di spendere token su una fase, verificare
che le altre due valute siano disponibili per quella fase. Far progettare a
`payload-fluidics` un ugello perfetto mentre l'anemometro non è stato ordinato
significa aver pagato un progetto che nessuno può validare.

### La valuta veramente scarsa

Non è nessuna delle tre: è il **calendario**, che è l'unica non rinnovabile.

La finestra stagionale delle zanzare (§10 di PROJECT.md) si chiude fra poche
settimane. Nessun budget di token e nessun euro la riaprono. Un piano economico
che non mette questa voce in cima è un piano che ottimizza il costo mentre
perde un anno.

---

## 2. Il libro paga

### Misura reale disponibile

Una sola, e va detto quale è per non spacciare stime per dati:

| Operazione | Token | Note |
|---|---|---|
| Costruzione della squadra (chief-engineer, 6 agenti + aggiornamento documento) | **83.366** | 16 chiamate di strumenti, 9 minuti |

Tutto il resto sotto è **stima**, da sostituire con misure appena disponibili.
Il giornale registra il consumo reale di ogni sessione perché questa tabella
si calibri da sola.

### Costo stimato per tipo di sessione

| Tipo di lavoro | Token stimati | Agenti tipici |
|---|---|---|
| Istruttoria o comparazione (normativa, scelta componente) | 30–60k | `compliance-safety`, `payload-fluidics` |
| Scrittura di codice con test | 50–150k | `vision-perception`, `autonomy`, `software-platform` |
| Iterazione CAD parametrico | 40–100k | `mechatronics` |
| Verifica o revisione | 20–40k | `compliance-safety`, `chief-engineer` |
| Riorganizzazione o arbitrato di confine | 60–100k | `chief-engineer` |
| Documentazione di un modulo congelato | 40–80k | `design-docs` |
| Orchestrazione multi-agente su un problema aperto | 300k–1M+ | più agenti in parallelo |

**Piano: Claude Max 20× (200 $/mese).** Cambia la natura della prima valuta:
su abbonamento **i token non si pagano a consumo, si pagano in tetto di
frequenza**. Non esiste un costo marginale per token — esiste una finestra
mobile di 5 ore e un tetto settimanale condivisi con la chat. Il budget
giornaliero non è quindi una spesa, è **una quota di capienza**: spenderlo tutto
non costa di più, ma esaurire la finestra blocca il lavoro fino al reset.

Conseguenza pratica: l'unico spreco reale è il lavoro **da rifare**, perché
consuma capienza senza produrre nulla. Un mandato vago costa più di una
sessione lunga.

**Budget deciso: 750.000 token/giorno** (23 agosto 2026). Comprano circa
**6–12 sessioni di lavoro reale**, oppure **una singola indagine multi-agente**
su un problema che non si riesce a chiudere altrimenti. Non si accumula: il
valore sta nel *quando* si spende. Il consuntivo giornaliero è in `LEDGER.md`.

---

## 3. Il capitale in euro

| Voce | € | Stato |
|---|---|---|
| BOM elettronica e meccanica (§5) | ~993 | Preliminare |
| Stampante P2S Combo + accessori + primo filamento | ~975 | Decisa (D-08), in acquisto |
| **Strumenti di misura** | **da quantificare** | **Non in BOM — bloccante** |
| Service SLS (pezzi che l'FDM non può fare) | da quantificare | Solo a geometria congelata |
| *Event camera (opzionale)* | *3.000+* | *Da escludere salvo ripensamento* |
| **Totale noto** | **~1.970** | |

### La voce che manca e blocca tutto

I criteri di FATTO degli otto agenti richiedono strumentazione che il BOM non
prevede: **reticolo di riferimento a 5 m, anemometro, analizzatore logico,
riferimento acustico**. Senza, nessun numero è misurabile e **nessun gate
chiude** — cioè: si può spendere l'intero budget di token e non poter
dichiarare finita neanche una fase.

È la prima spesa in euro da fare, prima del BOM principale.

---

## 4. Allocazione per fase

Le fasi non consumano le tre valute nella stessa proporzione. Questo dice
*quando* servono i soldi e *quando* servono i token.

| Fase | Token | Euro | Ore tue | Nota |
|---|---|---|---|---|
| 0 · Setup | basso | **alto** | **alto** | Si compra e si tara. Gli agenti servono poco. |
| 1 · CAD pan-tilt | **alto** | basso | medio | Iterazione parametrica: è qui che i token rendono di più |
| 2 · Pan-tilt fisico | basso | medio | **alto** | Montaggio e misura sono tuoi |
| 3 · Visione | **molto alto** | basso | medio | Dataset e training sono la voce più cara in token |
| 4 · Integrazione A | medio | medio | **alto** | |
| 5 · Acustica | **alto** | basso | **alto** | **Vincolata dal calendario: da anticipare** |
| 6 · Trappola | medio | medio | **alto** | Efficacia misurata su notti reali |
| 7 · Base mobile | **molto alto** | medio | medio | Il tuning di Nav2 è notoriamente lungo |
| 8 · Integrazione B | medio | basso | alto | |

**Conseguenza di allocazione:** le fasi 0 e 2 non giustificano un budget alto di
token. Le fasi 3 e 7 lo giustificano tutto. La fase 5 va anticipata a
prescindere dal budget, perché il costo del ritardo non si misura in token.

---

## 5. Regole di spesa

1. **Non si spendono token su una fase le cui altre due valute non sono pronte.**
2. **Un agente non riceve un mandato vago.** Un mandato vago produce lavoro che
   va rifatto: è la prima causa di spreco.
3. **La verifica del lavoro di un agente avviene a completamento, mai a metà**
   (lezione del 23 agosto, registrata nel giornale). Verificare uno stato
   transitorio produce correzioni inutili, e le correzioni costano.
4. **L'orchestrazione multi-agente è per i problemi aperti, non per quelli
   noti.** Costa da 5 a 10 volte una sessione singola: si usa quando il modo
   di risolvere non è noto, non per fare prima.
5. **Ogni sessione registra il proprio consumo nel giornale.** Senza consuntivo
   questa tabella non si calibra e resta un esercizio.
6. **Il budget non speso non si accumula come merito.** Se una giornata di
   budget non è servita, la fase era sbagliata, non il budget.

---

## 6. Che cosa sarebbe l'utile

Un progetto che oggi non vende non ha ricavi, quindi «utile» va definito o la
contabilità non significa niente. Le unità di ritorno sono tre:

- **Gate chiusi** — una fase con i suoi numeri misurati è l'unico avanzamento
  reale. Costo per gate chiuso è l'indicatore principale.
- **Decisioni irreversibili prese bene** — una scelta di architettura sbagliata
  scoperta in fase 7 costa più di tutto il budget di token del progetto.
- **Materiale narrativo catturato** — il giornale e le riprese sono un asset
  che si deprezza a zero se non raccolto nel momento, e che ha un valore
  indipendente dal successo tecnico del robot.

---

## 7. Commerciale — perimetro, non ancora piano

Marketing, go-to-market, e-commerce e distribuzione sono rimandati per scelta.
Si registrano qui i **due vincoli strutturali** che ne condizioneranno ogni
versione, perché sono già stati decisi e non sono reversibili a costo zero.

**a) Le licenze scelte rendono il prodotto legittimamente clonabile.**
`CERN-OHL-W v2` è una licenza fortemente reciproca: chiunque può costruire e
**vendere** R2-Sentinel, a patto di ridistribuire le modifiche. È la scelta
corretta per l'open hardware ed è già registrata nel README, ma esclude ogni
modello di business fondato sull'esclusiva. I modelli compatibili sono altri:
vendita di kit e unità assemblate, vendita dei soli pezzi difficili da
produrre, servizi, contenuti. Da decidere *prima* di parlare di canali.

**b) Vendere non è replicare.** Un dispositivo commerciale che agisce su fauna
protetta, con un recipiente a 5 bar, alimentazione di rete in esterno,
batteria al litio e telecamere in ambiente domestico entra in un perimetro
completamente diverso da un progetto amatoriale: marcatura CE, direttiva
attrezzature a pressione, sicurezza elettrica, GDPR, responsabilità da
prodotto. Non è un ostacolo insormontabile, è **un secondo progetto** con un
budget proprio, e va pianificato come tale e non come un'estensione di questo.

Il momento giusto per aprire questa sezione è dopo il gate della **fase 4**:
prima non esiste un prodotto di cui parlare.
