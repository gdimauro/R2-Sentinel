# Lista acquisti operativa

Ordinata **per scadenza**, non per importanza. Prezzi verificati il 23 agosto
2026: da riverificare al link prima di ordinare.

## ⚠️ Regola vincolante: tutto con fattura

Ogni acquisto va fatto con **fattura intestata**, senza eccezioni. Questo
condiziona la scelta del fornitore più del prezzo, e squalifica alcune opzioni
che sarebbero state le più economiche.

| Canale | Fattura | Nota |
|---|---|---|
| Rivenditori professionali IT (3D Store Italia, Zetalab, RS, Farnell, Mouser, Melopero, Weerg) | ✅ Sempre | **Canale preferito** |
| Fornitori UE B2B (SoundImports, Reichelt, PCE) | ✅ Con partita IVA | **Reverse charge**: comunica la P.IVA in fase d'ordine e l'IVA non viene addebitata |
| Amazon.it **con account Business** | ✅ Automatica | Da attivare una volta, poi vale per tutti gli ordini |
| Amazon.it venditore terzo senza Business | ⚠️ Variabile | Va chiesta all'ordine e non tutti la emettono |
| **Amazon.com (USA)** | ❌ No | **Non emette fattura italiana.** Scartato |
| eBay, privati, marketplace generici | ❌ Spesso no | Scartati |
| idealo, Trovaprezzi | — | Sono comparatori, non venditori: si compra dal negozio elencato |

**Prima di tutto il resto:** se non ce l'hai già, attiva un **account Amazon
Business** (gratuito) — emette fattura automaticamente e ti evita di rincorrerla
ordine per ordine.

---

## 🔴 ORA — questa settimana, perché scade

### 1. Microfono di misura calibrato USB

**Perché per primo:** non è solo il riferimento sui 400–600 Hz. Collegato a un
portatile è il **banco di registrazione di partenza**, e apre le notti prima che
Raspberry Pi e ICS-43434 esistano. La stagione delle zanzare chiude fra
settimane: è l'unico acquisto che compra tempo altrimenti perso per un anno.

| Dove | Note |
|---|---|
| [SoundImports (UE, Paesi Bassi)](https://www.soundimports.eu/en/minidsp-umik-1.html) | ✅ **Consigliato** — intra-UE, nessuna dogana, fattura B2B con reverse charge indicando la P.IVA |
| ~~[Amazon.com (USA)](https://www.amazon.com/miniDSP-UMIK-1-Measurement-Calibrated-Microphone/dp/B00N4Q25R8)~~ | ❌ **Scartato: nessuna fattura italiana**, più dogana |
| [Cross-Spectrum (USA)](https://cross-spectrum.com/measurement/calibrated_umik.html) | Calibrazione estesa, ma extra-UE: verifica fattura e dogana prima |

**~120–160 €.** Verifica che includa il **file di calibrazione individuale**: è
quello che lo rende un riferimento, non il microfono in sé.

> Serve anche un cavalletto e, se registri lontano dal portatile, una prolunga
> USB attiva. Il treppiedino incluso è da tavolo.

---

## 🟠 SUBITO DOPO — sblocca la fase 0

### 2. Stampante — Bambu Lab P2S Combo

Decisa in D-08. **Buona notizia: costa meno della stima.**

| Dove | Prezzo | Note |
|---|---|---|
| [idealo — confronto prezzi](https://www.idealo.it/confronta-prezzi/208041246/bambu-lab-p2s-combo.html) | **767,88 €** | Il miglior prezzo rilevato |
| [3D Store Italia](https://www.3dstoreitalia.com/products/bambu-lab-p2s-stampante-3d) | — | **Rivenditore ufficiale Bambu Lab in Italia**, Garanzia Italia e assistenza certificata |
| [3D Store Monza](https://www.3dstoremonza.it/prodotto/bambu-lab-p2s-combo/) | — | Alternativa italiana |

**Raccomandazione:** se la differenza è contenuta, prendila dal rivenditore
ufficiale italiano. Su una macchina che deve essere «un non-problema» (§8.3
di PROJECT.md), assistenza e garanzia locali valgono più di venti euro.

**Da aggiungere allo stesso ordine — non dimenticarli:**

| Accessorio | ~€ | Perché |
|---|---|---|
| **Alimentatore ufficiale Bambu per AMS** | ~30 | **Necessario.** Senza, mentre l'AMS asciuga la stampante non può scaldare il piatto né muovere gli assi |
| Ugello 0,6 mm | ~20 | Dimezza i tempi sui pezzi strutturali |
| Piatto PEI aggiuntivo (liscio + testurizzato) | ~40 | Evita fermi macchina fra una stampa e l'altra |

### 3. Filamenti — set di partenza

I cinque materiali che §7.5 prescrive. **PETG in doppia quantità** perché serve
anche come interfaccia di supporto sotto l'ASA (D-11).

| Materiale | kg | Uso | ~€ |
|---|---|---|---|
| PLA | 1 | Prototipi rapidi di forma | 22 |
| PETG | 2 | Parti interne **+ interfacce di supporto** | 55 |
| ASA | 1 | Tutto l'esterno, resistenza UV | 38 |
| TPU 95A | 1 | Paraurti, guarnizioni, ruote | 40 |
| | **5** | | **~155** |

| Dove | Note |
|---|---|
| [3D Store Italia](https://www.3dstoreitalia.com/) | Gamma XTESA con PETG, ASA, TPU — stesso ordine della stampante |
| [Bambu Lab store](https://eu.store.bambulab.com/) | I profili Bambu sono pretarati: meno tempo perso a calibrare |
| [Reichelt](https://www.reichelt.com/it/it/shop/prodotto/filamento_tpu-95a_1_75_mm_blu_traslucido_1_kg-422827) | eSUN TPU 95A |
| [Trovaprezzi](https://www.trovaprezzi.it/prezzo_accessori-stampanti_filamento_tpu.aspx) | Confronto |

> **Per l'ASA prendi profili Bambu se puoi.** L'ASA è il materiale che dà più
> problemi e ogni ora di taratura è sottratta al progetto vero (§8.1, requisito 3).

---

## 🟡 AI GATE — servono, ma non scadono

### 4. Anemometro a filo caldo — gate fase 4

Prendi **0–30 m/s**, non 0–25: il criterio è 8–25 m/s e col fondo scala a 25
lavori appiccicato al limite.

| Modello | Dove | Note |
|---|---|---|
| **PCE-423N** ✅ | [PCE Instruments](https://www.pce-instruments.com/italiano/strumento-di-misura/misuratore/anemometro-a-filo-caldo-pce-instruments-anemometro-a-filo-caldo-pce-423n-det_5994244.htm) · [Zetalab](https://www.zetalab.it/prodotto/anemometro-a-filo-caldo-pce-423n/) · [ManoMano](https://www.manomano.it/p/anemometro-a-filo-caldo-pce-instruments-pce-423-3416479) | 0–30 m/s, sonda telescopica 426 mm, **log CSV e attacco treppiede** — servono per ripetere la griglia 5×5 |
| ~~Multicomp MP780109~~ | [Farnell](https://it.farnell.com/multicomp-pro/mp780109/anemometro-term-filo-caldo-0-1/dp/3257361) | **Scartato:** 0,1–25 m/s |
| ~~RS PRO AM-4204~~ | [RS](https://it.rs-online.com/web/p/anemometri/3270640) | **Scartato:** 20 m/s |

**~250–400 €.**

> ⚠️ **La sonda non va mai avvicinata all'ugello.** Un convergente a 5 bar va in
> flusso critico: all'uscita sei intorno ai 300 m/s e il filo caldo si brucia
> all'istante. Si misura **solo a 5 metri**.

### 5. Analizzatore logico — gate fase 2

Serve a vedere un loop da 1 kHz con jitter ≤100 µs. Un clone da 24 MHz
sovracampiona 24.000 volte: **non spendere di più.**

| Dove | ~€ | Fattura |
|---|---|---|
| [robotstore.it](https://www.robotstore.it/en/Analizzatore-Logico-USB-8-canali-a-24MHz) | 10–25 | ✅ **Consigliato** — rivenditore italiano |
| [SEENGREAT su Amazon.it](https://www.amazon.it/SEENGREAT-Analyzer-CY7C68013A-PulseView-campionamento/dp/B0CNXHBDXX) | 10–25 | ⚠️ Solo con account Business |
| [Alternativa Amazon.it](https://www.amazon.it/Analyzer-Digital-Pocket-Channel-Memory/dp/B08MXZYMJ5) | 10–25 | ⚠️ Solo con account Business |

Su un pezzo da 15 € la fattura vale più dei due euro di differenza: prendi
l'italiano.

### 6. Riferimento angolare — **si costruisce**

1° a 5 m = **87,3 mm**. Non comprare strumenti: un modulo laser sulla testa
pan-tilt, un bersaglio stampato con griglia da 10 mm, un treppiede. Fotografi il
punto e misuri in pixel — risoluzione migliore di qualsiasi strumento in fascia
economica, e ripetibile. **~20–40 € di materiale.**

---

## ⚪ FASE 1 — non ordinare prima

Il BOM di §5 (~993 €) va congelato dal `chief-engineer` **dopo** che il CAD
esiste. Ordinare prima significa comprare il componente sbagliato.

Fornitori italiani di riferimento per quando sarà il momento:
[Melopero](https://www.melopero.com/) (Raspberry Pi e HAT),
[RS Components](https://it.rs-online.com/), [Farnell](https://it.farnell.com/),
[Mouser](https://www.mouser.it/) (sensori, elettronica).

Service SLS per i pezzi di §7.2: [Weerg](https://www.weerg.com/) (Italia, tempi
rapidi), [Craftcloud](https://craftcloud3d.com/) (aggregatore),
[JLC3DP](https://jlc3dp.com/) (un terzo del costo, 2–3 settimane).

---

## Riepilogo

| Quando | Cosa | ~€ |
|---|---|---|
| 🔴 Questa settimana | Microfono di misura | 120–160 |
| 🟠 Subito dopo | Stampante + accessori + filamenti | ~1.010 |
| 🟡 Ai gate | Anemometro, analizzatore, materiale per il bersaglio | 280–465 |
| ⚪ Fase 1 | BOM | ~993 |
| | **Totale** | **~2.400–2.630** |

**Conserva tutte le fatture** in un archivio unico: il libro mastro registra la
voce, ma l'originale serve altrove. Ogni acquisto va segnato in `LEDGER.md` §4
con fornitore, importo, data e **estremi della fattura**.

Più il consumo ricorrente di filamento sull'arco del progetto (250–500 €,
purge waste di D-11 incluso) e il service SLS, da quotare a geometria congelata.
