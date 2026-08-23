# Dossier di conformita'

**Proprietario del contenuto: `compliance-safety`.** Questa directory e la sua
esistenza sono di `software-platform`; cio' che ci sta dentro no.

## A cosa serve

Il criterio di FATTO di `compliance-safety` dice: **0 pull request sul payload
chiuse senza una nota di conformita' nel dossier**. Perche' quel criterio sia
verificabile e non un'abitudine, la nota deve essere un file, non un ricordo.

## Come funziona il gate

`scripts/ci/check_compliance_gate.py` gira su ogni PR. Se il diff tocca payload,
BOM o `SAFETY.md`, la CI **fallisce** a meno che la PR:

1. aggiunga o modifichi un file in questa directory, **oppure**
2. porti l'etichetta `conformita-ok`, apposta da `compliance-safety`.

La forma 1 e' preferibile: lascia una traccia leggibile fra un anno.
La CI non entra nel merito e non sa se la nota sia buona: verifica che esista.
Il giudizio resta di `compliance-safety`.

## Nome dei file

`NNNN-<argomento>.md`, per esempio `0001-valvola-sicurezza-6bar.md`.

## Contenuto minimo

- Cosa e' stato verificato e su quale versione (commit o tag)
- Riferimenti normativi o certificati, con estremi
- Voci ancora aperte, se ce ne sono, ciascuna con chi la chiude e entro quando
- Verdetto esplicito: conforme / conforme con riserva / non conforme
