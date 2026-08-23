# Giornale di bordo

Registro cronologico e narrativo del progetto R2-Sentinel, mantenuto per
produrre a fine progetto **articoli, presentazioni e materiale documentaristico**.

## Perché esiste, dato che c'è già il Decision Log

Non si sovrappongono. Servono a due cose diverse e si perdono in due modi diversi.

| | Decision Log (`PROJECT.md` §3) | Giornale (questa cartella) |
|---|---|---|
| Risponde a | *Perché abbiamo fatto così?* | *Com'è andata?* |
| Registra | l'esito e la motivazione | il percorso, i tentativi, gli errori |
| Ordine | per numero di decisione | cronologico |
| Sopravvive | alla riscrittura | solo se scritto quando accade |
| Serve a | chi eredita il progetto | chi lo racconta |

Il Decision Log tiene le decisioni **giuste**. Il giornale tiene anche quelle
**sbagliate** — che sono la parte interessante da raccontare, e l'unica che
non si può ricostruire dopo, perché il repository conserva solo ciò che ha vinto.

## La regola del materiale irrecuperabile

C'è un'asimmetria che governa tutto il resto:

> **Un articolo si scrive a posteriori. Un documentario no.**

Testo, numeri e ragionamenti sono ricostruibili dal repository e dal Decision
Log anche fra un anno. **Immagini, video e audio no.** La stampante che esce
dalla scatola, la prima stampa che si delamina, il balcone ancora vuoto, il
rumore del primo pan-tilt che si muove: se non sono ripresi nel momento in cui
accadono, non esistono più.

Vale la stessa logica del dataset zanzare (§10 di PROJECT.md): **vincolato dal
calendario, non dallo sforzo.** Nessuna quantità di lavoro futuro recupera una
ripresa non fatta.

**Conseguenza operativa:** la cattura media parte alla fase 0, non alla fase 4.

## Cosa catturare, sempre

Prima di ogni sessione di lavoro fisico:

- [ ] **Stato iniziale** — una foto di com'è prima di toccare niente
- [ ] **Il processo**, non solo il risultato — le mani che lavorano, non il pezzo finito
- [ ] **I fallimenti** — il pezzo deformato, la stampa fallita, il test che non passa.
      Sono il materiale narrativo migliore e quello che si butta per istinto: **non buttarlo**
- [ ] **Audio ambientale** — motori, ventole, il battito alare registrato.
      Un documentario senza suono di presa diretta si sente
- [ ] **Numeri sullo schermo** — le misure mentre appaiono, non ritrascritte dopo
- [ ] **Stato finale**, dalla stessa inquadratura dello stato iniziale

Regola pratica: **gira più del necessario e non cancellare niente.** Lo spazio
disco costa meno di una ripresa impossibile da rifare.

## Struttura

```
docs/journal/
  README.md              questo file
  AAAA-MM-GG-titolo.md   una voce per sessione di lavoro
  media/                 foto, video, audio — fuori da Git, vedi sotto
```

**I media non vanno nel repository.** Sono grandi e binari. `docs/journal/media/`
è in `.gitignore`: tienili in un archivio separato con backup, e nelle voci
referenziali per nome file. Il giornale registra *che quella ripresa esiste e
dove sta*, non la ripresa.

## Formato di una voce

```markdown
---
data: 2026-08-23
fase: 0
agenti: [mechatronics, chief-engineer]
decisioni: [D-08, D-11]
media: [IMG_0412.jpg, primo-warping.mp4]
---

# Titolo che dice cosa è successo

## Cosa doveva succedere
## Cosa è successo davvero
## Cosa non ha funzionato
## Cosa ho imparato
## Da rifare diversamente
```

Le sezioni **«cosa non ha funzionato»** e **«da rifare diversamente»** non sono
opzionali. Una voce senza di esse è un comunicato stampa, non un giornale, e
fra un anno non servirà a nessuno.

## Le tre regole che tengono in vita un giornale

1. **Scrivi lo stesso giorno.** Una voce scritta la settimana dopo è già una
   ricostruzione: i dettagli che rendono un racconto vivo sono i primi a sparire.
2. **Ammetti gli errori per esteso.** Un giornale che registra solo successi è
   inutile per scrivere e imbarazzante da leggere.
3. **Scrivi male piuttosto che non scrivere.** Una voce sciatta si riscrive,
   una voce mancante no. La revisione è di `design-docs`, non tua.

## Responsabilità

- **Ogni agente** registra la propria sessione di lavoro il giorno stesso.
- **`design-docs`** cura il giornale, ne verifica la continuità e ne ricava
  articoli, slide e materiale documentaristico.
- **`chief-engineer`** non lo possiede: il giornale racconta anche i suoi errori,
  e chi è raccontato non tiene la penna.
