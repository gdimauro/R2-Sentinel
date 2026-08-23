# Fascicoli degli agenti

Una cartella per ogni agente. **Ma non contiene i suoi deliverable: li indicizza.**

## Perché non "tutto dentro"

La richiesta iniziale era di mettere in ogni cartella tutto il lavoro
dell'agente. Non è stato fatto così, per tre ragioni concrete.

**1. I deliverable appartengono al sottosistema, non all'autore.** Il codice
acustico sta in `software/acoustic/` perché è codice acustico. Se domani
`acoustic-perception` viene diviso in due ruoli, o rinominato, o assorbito, il
codice non deve spostarsi: il sottosistema non è cambiato.

**2. Il repository ha già una struttura, ed è quella dell'architettura.**
`software/`, `cad/`, `firmware/`, `hardware/` rispecchiano `PROJECT.md` §4.
Duplicarla per autore creerebbe due gerarchie che competono, e la prima volta
che divergono nessuno sa quale sia quella buona.

**3. Alcuni deliverable hanno due autori.** Il CAD della testa pan-tilt è di
`mechatronics` ma incorpora i vincoli di `payload-fluidics` e la calibrazione di
`vision-perception`. In una gerarchia per autore non avrebbe casa.

## Cosa contiene invece un fascicolo

Ciò che è **davvero dell'agente e oggi non ha collocazione**:

| Voce | Perché qui |
|---|---|
| Mandato | Il file in `.claude/agents/` è la fonte; qui sta il collegamento e la storia delle sue modifiche |
| Criterio di FATTO e stato | Il numero da raggiungere e quanto manca |
| Consegnato | **Indice con i collegamenti**, non copie |
| Misure | I numeri che ha prodotto, con data e protocollo di misura |
| Blocchi | Da cosa dipende, e da chi |
| Verbali | Gli atti in cui è parte |
| Cronologia | Quando è stato attivato e con quale esito |

È un fascicolo personale: **indicizza e non duplica**. Un file che esiste in due
posti è un file che divergerà.
