---
data: 2026-08-23
fase: 0
agenti: [chief-engineer]
decisioni: [D-12, D-13, D-14, D-15]
media: []
---

# Giorno zero: da uno scheletro di cartelle a una squadra di otto

## Cosa doveva succedere

Sistemare un link rotto nel README.

## Cosa è successo davvero

Il repository esisteva già come struttura — otto cartelle, tre licenze, un
documento master da 21 KB con undici decisioni tecniche già motivate — ma
**non aveva ancora un solo commit**. E il README si apriva con
`# [NOME PROGETTO]`.

La sessione è passata per quattro fasi, in quest'ordine.

### 1. Igiene

Il link rotto non era uno. Il documento master era stato rinominato da
`PROGETTO.md` a `PROJECT.md` senza aggiornare i riferimenti: **dodici
occorrenze in dieci file**, inclusi tutti i README segnaposto delle
sottocartelle. Corretti in blocco.

Poi il nome. La cartella si chiamava già `R2-Sentinel`, il documento diceva
`(da definire)`. Chiuderla è stata la prima decisione registrata della
sessione (**D-12**), e la motivazione conta più dell'esito: *«Sentinel»
descrive il comportamento reale — sorveglia e interviene su un evento —
senza promettere l'eliminazione del bersaglio, che per i volatili sarebbe
anche legalmente scorretto.* Il nome è vincolato dalla L.157/1992 tanto
quanto il payload.

Primo commit: `ef9ef44`, 16 file. Repository pubblicato.

### 2. La domanda giusta al momento giusto

Avevo scritto un agente chiamato `project-manager` con il compito di
costruire la squadra. La domanda che è arrivata — *«chi ha il ruolo di
costruire la squadra? che nome ha un ruolo istituzionale di questo tipo?»* —
ha mostrato che il nome era sbagliato.

Un project manager gestisce tempi, budget e stakeholder; il ruolo che deriva
la squadra dalla decomposizione del sistema è il **Chief Engineer** — lo
*shusa* Toyota, che possiede il prodotto da capo a fondo con responsabilità
totale e autorità formale scarsa. L'artefatto che produce ha un nome preciso:
dalla WBS si deriva la **OBS**, la struttura organizzativa.

Rinominato. È stata la correzione più economica della giornata: due righe di
frontmatter prima che qualcuno ci lavorasse sopra.

### 3. La squadra

Baseline passata al Chief Engineer: cinque specialisti più lui, organizzati
**per macchina e non per disciplina** — perché Unità A (visione, meccanica di
precisione, mira) e Unità B (DSP, navigazione, fluidodinamica) condividono
pochissimo.

Un confine l'ho lasciato deliberatamente aperto: il payload fluidico esiste su
entrambe le unità. Il Chief Engineer ha deciso per un **ruolo unico
trasversale** (D-14), contro l'organizzazione per macchina, con tre ragioni:
è la stessa fisica, concentra i rischi più seri (5 bar, CO₂, resistenza accesa
di notte), e il numero che governa l'Unità A è fluidodinamico e non meccanico.
Ha anche scritto il costo che accetta: è l'unico specialista a cavallo delle
due catene parallele, quindi un potenziale collo di bottiglia.

Poi la richiesta di assumere «un CTO e un grafico». Rifiutati **nella forma,
non nella sostanza** (D-15): un CTO si sarebbe sovrapposto quasi interamente
al Chief Engineer, e la parte che non si sovrappone — strategia, budget,
buy-vs-build — è dello sponsor, cioè della persona, non di un agente. Il
«grafico» avrebbe trasformato in decorazione un deliverable che in open
hardware è funzionale. Sono diventati `software-platform` e `design-docs`.

Otto agenti più il Chief Engineer.

### 4. La scoperta che cambia il piano

Nel report finale il Chief Engineer ha registrato una questione che nessuno
aveva visto, e che non è tecnica:

> In Italia le zanzare sono attive circa da maggio a settembre/ottobre. Alla
> data di questo documento la finestra è **quasi chiusa**: se la raccolta non
> parte entro poche settimane, la fase 5 slitta di **un anno intero**.

Il dataset acustico è vincolato dal calendario, non dallo sforzo. Nessuna
risorsa aggiuntiva comprime venti notti di registrazione. È l'unico elemento
del progetto che, se rimandato, non costa settimane ma stagioni — e la
raccomandazione che ne discende ribalta la roadmap: attivare
`acoustic-perception` **subito**, non in fase 5, su un solo deliverable —
*un registratore che gira stanotte* — prima che il resto dell'Unità B esista.

Seconda scoperta, meno drammatica e altrettanto concreta: i criteri di FATTO
degli agenti richiedono anemometro, reticolo a 5 m, analizzatore logico e
riferimento acustico. **Nessuno di questi è in BOM.** Senza strumenti, nessun
numero è misurabile e nessun gate chiude.

## Cosa non ha funzionato

**Ho accusato il Chief Engineer di un errore che non aveva commesso.** Avevo
verificato che il changelog annunciasse decisioni D-13 e D-14 assenti dal
documento, e l'ho segnalato come «lavoro dichiarato e non fatto». Era falso:
l'agente stava ancora scrivendo, e la mia verifica era arrivata a metà del suo
lavoro. Ho controllato uno stato transitorio e l'ho trattato come definitivo.

Vale la pena registrarlo perché è un errore strutturale del lavorare con
agenti asincroni, non una svista: **lo stato di un lavoro in corso non è un
risultato.** Il costo qui è stato nullo, ma la stessa logica applicata a una
misura di laboratorio produce un dato sbagliato pubblicato.

## Cosa ho imparato

- **Le decisioni di sequenza valgono più di quelle di architettura.** Tutte le
  scelte tecniche di oggi sono reversibili; la finestra stagionale no.
- **Un vincolo legale è un vincolo di progetto.** La non cruentezza non è una
  postilla etica: determina il payload, il nome e persino cosa il sistema può
  promettere di fare.
- **Il nome sbagliato di un ruolo produce il mandato sbagliato.** `project-manager`
  avrebbe generato una squadra per discipline; `chief-engineer` l'ha generata
  per confini di sistema.

## Da rifare diversamente

- Verificare il lavoro di un agente **solo dopo** la sua notifica di
  completamento, mai a metà.
- La cattura media doveva iniziare oggi e non è iniziata: di questa giornata
  non esiste una sola immagine. Il primo materiale recuperabile sarà
  l'arrivo della stampante.
