# Verbali — registro di protocollo

Archivio formale delle **decisioni** e delle **contestazioni** del progetto.
Ogni voce ha un numero di protocollo, è immutabile e verificabile.

---

## 1. Perché un registro separato dal Decision Log

Non si sovrappongono, e la differenza è la ragione per cui questo esiste.

| | Decision Log (`PROJECT.md` §3) | Verbali (questa cartella) |
|---|---|---|
| Contiene | l'esito e la motivazione | **l'istruttoria completa** |
| Riporta | ciò che è stato deciso | anche ciò che è stato **respinto**, e da chi |
| Forma | una riga di tabella | un atto con parti, fatti, verifiche, dispositivo |
| Muta | sì, si riscrive e si corregge | **mai**: si corregge solo con un nuovo verbale |
| Risponde a | «perché abbiamo fatto così?» | «chi ha sostenuto cosa, e su quali prove?» |

Il Decision Log è l'indice delle conclusioni. Il registro è l'archivio degli
atti. Un verbale può contenere una contestazione **respinta**, che nel Decision
Log non comparirà mai — ed è spesso la parte che serve rileggere.

## 2. Numerazione

`VRB-AAAA-NNNN` — progressivo per anno, **mai riusato, mai rinumerato**.
Il numero si ottiene solo con `scripts/protocolla.py`, che lo assegna in modo
atomico leggendo il registro: assegnarlo a mano produce collisioni.

```bash
python3 scripts/protocolla.py "Titolo del verbale" --tipo contestazione
```

## 3. Immutabilità — è il punto di tutto

**Un verbale protocollato non si modifica mai.** Nemmeno per correggere un
refuso, nemmeno se si scopre che era sbagliato.

Se un verbale è errato o superato, si emette un **nuovo verbale** che lo cita e
ne dichiara l'effetto: `rettifica`, `integra`, `revoca`. Il vecchio resta
nell'archivio con il suo errore, che è esattamente ciò che serve fra sei mesi
quando qualcuno chiederà come si è arrivati a quella conclusione.

La regola è verificata automaticamente: `REGISTRO.md` conserva l'**impronta
SHA-256** di ogni verbale, e `scripts/ci/check_verbali.py` fallisce se
un'impronta non corrisponde. La CI blocca la modifica di un atto già
protocollato.

## 4. Cosa merita un verbale

**Sempre:**
- Una **contestazione** di un agente a una scelta di architettura o di BOM
- Una decisione che modifica `PROJECT.md` §2 (vincoli) o §4 (architettura)
- Un **gate negato** o concesso da `compliance-safety`
- Un rischio residuo **accettato per iscritto** dallo sponsor
- Un emendamento a un mandato di agente

**Mai:**
- Il lavoro ordinario di un agente — quello sta nel giornale
- Una scelta reversibile a costo nullo
- Una discussione senza esito: un verbale registra un atto, non una conversazione

## 5. Struttura di un verbale

```markdown
---
protocollo: VRB-2026-0001
data: 2026-08-24
tipo: contestazione | decisione | gate | accettazione-rischio | emendamento
parti: [chi solleva, chi arbitra]
oggetto: una riga
riferimenti: [D-14, §4.3, VRB-2026-0000]
esito: accolta | respinta | parzialmente accolta | in attesa
---

# VRB-2026-0001 · Titolo

## Fatto
Che cosa è accaduto, in ordine cronologico.

## Posizione di chi solleva
Con i numeri e le fonti.

## Verifica indipendente
Chi ha ricontrollato, come, con quale esito. Se nessuno ha verificato, dirlo.

## Posizione contraria
Se esiste. Se non esiste, dirlo: un verbale senza contraddittorio va segnalato.

## Dispositivo
La decisione, e cosa cambia operativamente.

## Effetti
File toccati, decisioni del Decision Log create o modificate, azioni aperte.
```

## 6. Chi verbalizza

- Le **contestazioni** le verbalizza il `chief-engineer`, che è l'arbitro.
- I **gate** li verbalizza `compliance-safety`, che è l'unico a poterli negare.
- Gli **emendamenti ai mandati** li verbalizza `retrospective`.
- Le **accettazioni di rischio** le verbalizza il coordinamento, ma valgono solo
  con l'assenso esplicito dello sponsor, citato testualmente nel verbale.

Nessuno verbalizza un atto in cui è l'unica parte. Se il `chief-engineer` è
parte in causa, verbalizza il coordinamento e la decisione va allo sponsor —
stessa logica dell'eccezione di governance di D-16.
