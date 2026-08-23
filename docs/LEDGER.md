# Libro mastro

Contabilità giornaliera delle tre valute del progetto (vedi `BUSINESS.md` §1).
Aggiornato a ogni sessione di lavoro. **Ciò che è misurato è marcato come
misurato; ciò che è stimato è marcato come stimato.** Non si mescolano.

---

## 1. Metodo

**Cosa è misurabile con precisione:** il consumo di ogni agente lanciato in
sessione, che riporta il proprio totale a fine esecuzione.

**Cosa non lo è, oggi:** il consumo della sessione principale (la conversazione
di coordinamento). Non c'è un contatore per-turno esposto. Va richiesto a fine
giornata con `/cost`, oppure ricavato dal budget residuo, e trascritto qui.

**Regola:** una riga senza fonte del dato è una riga inutile. Ogni voce dichiara
se viene da un report di agente (**M**, misurato), da `/cost` (**M**), o da
stima (**S**).

---

## 2. Registro giornaliero — token

| Data | Voce | Token | Fonte | Prodotto |
|---|---|---|---|---|
| 2026-08-23 | `chief-engineer` — costruzione squadra, 6 agenti + D-13/D-14 + §10 | 83.366 | M | 6 file agente, 2 decisioni, 4 questioni aperte |
| 2026-08-23 | `chief-engineer` — addendum, `software-platform` + `design-docs` + D-15 | *non rilevato* | — | 2 file agente, 1 decisione |
| 2026-08-23 | Sessione principale — igiene repo, primo commit, squadra, sinottico, giornale, piano economico | *da rilevare con* `/cost` | — | 3 PR-equivalenti di documenti, 1 artefatto pubblicato |
| | **Totale misurato del giorno** | **83.366** | | *parziale — due voci non rilevate* |

> ⚠ **Debito contabile del giorno 1.** Due voci su tre non sono state rilevate
> perché la contabilità è stata istituita a giornata in corso. È il tipo di
> buco che rende inutile un libro mastro se si ripete: da domani ogni sessione
> si chiude rilevando il consumo **prima** di terminare.

### Consuntivo contro stima

| Operazione | Stima in `BUSINESS.md` | Reale | Scarto |
|---|---|---|---|
| Riorganizzazione / arbitrato di confine (`chief-engineer`) | 60–100k | 83.366 | dentro la forchetta |

---

## 3. Acquisti — da fare

Ordinati per **ciò che sblocca**, non per costo.

### Priorità 1 — sblocca la verificabilità di tutto

Senza questi, nessun criterio di FATTO è misurabile e **nessuna fase si può
dichiarare chiusa**, per quanto lavoro sia stato fatto.

| # | Voce | Perché | € stimato | Stato |
|---|---|---|---|---|
| S-01 | Anemometro a filo caldo 0–30 m/s, con datalog CSV e attacco treppiede | Getto d'aria 8–25 m/s a 5 m su griglia 5×5 (25 punti) e aspirazione ≥2,0 m/s a 25 cm | 250–400 | Da ordinare |
| S-02 | Analizzatore logico USB 8 canali 24 MHz | Jitter del loop firmware ≤100 µs a 1 kHz | 10–25 | Da ordinare |
| S-03 | Microfono di misura calibrato USB (classe UMIK-1) | Riferimento per il microfono MEMS I2S sui 400–600 Hz e misura del rumore di fondo | 120–160 | Da ordinare |
| S-04 | Modulo laser + treppiede + bersaglio stampato | Riferimento angolare a 5 m — **si costruisce, non si compra** | 20–40 | Da costruire |

### Priorità 2 — quando parte la fase 0

| # | Voce | € | Stato |
|---|---|---|---|
| S-05 | Bambu Lab P2S Combo + alimentatore AMS + ugello 0,6 + piatti + filamento | ~975 | Deciso (D-08), in acquisto |

### Priorità 3 — a geometria congelata

| # | Voce | € | Stato |
|---|---|---|---|
| S-06 | BOM elettronica e meccanica (§5 di PROJECT.md) | ~993 | Non ordinare prima della fase 1 |
| S-07 | Service SLS per i pezzi che l'FDM non può fare (§7.2) | da quotare | Solo a geometria congelata |

### Escluso salvo ripensamento

| Voce | € | Motivo |
|---|---|---|
| Event camera Prophesee | 3.000+ | D-04 rende il tracking ottico delle zanzare non necessario |

---

## 4. Acquisti — fatti

*(nessuno alla data odierna)*

| Data | Voce | € | Fornitore | Note |
|---|---|---|---|---|

---

## 5. Totali

| | € |
|---|---|
| Speso a oggi | **0** |
| Impegnato priorità 1 (strumenti) | 400–625 |
| Impegnato priorità 2 (stampante) | ~975 |
| Previsto priorità 3 (BOM) | ~993 |
| **Capitale totale previsto** | **~2.400–2.600** |

Nota: il capitale previsto è **superiore** alla stima di `BUSINESS.md` (~1.970)
perché quella non comprendeva gli strumenti di misura. Questa è la cifra da
usare.

---

## 6. Ore-persona e calendario

La terza valuta, che non si compra.

| Voce | Stato |
|---|---|
| **Finestra stagionale zanzare** | ⚠ **Si chiude fra poche settimane.** Nessun budget la riapre. |
| Ore di assemblaggio e misura | Non ancora stimate — da fare a valle della fase 1 |
| Riprese per il documentario | ⚠ Nessuna a oggi. Il primo materiale recuperabile è l'arrivo della stampante. |
