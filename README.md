# R2-Sentinel

> Sistema robotico open source per il rilevamento e l'intervento su infestanti
> domestici, su due unità specializzate: dissuasione non cruenta dei volatili
> all'esterno, cattura delle zanzare all'interno.

**Stato:** 🟡 Definizione architettura — nessun hardware assemblato

> ⚠️ **Leggi [SAFETY.md](SAFETY.md) prima di replicare o modificare questo
> progetto.** Contiene vincoli di sicurezza e legali che condizionano
> l'architettura, incluse le ragioni per cui l'approccio laser è escluso.

---

## Il problema

Riconoscere e gestire bersagli su un range dimensionale di due ordini di
grandezza — dal piccione (~30 cm) alla zanzara (~3 mm) — con un unico sistema
non funziona. I due bersagli hanno requisiti di percezione e di intervento
incompatibili.

Da qui la scelta architetturale centrale: **due unità separate**.

| | Unità A — "Balcone" | Unità B — "Interno" |
|---|---|---|
| Forma | Fissa, testa pan-tilt | Mobile su ruote |
| Bersaglio | Volatili | Zanzare |
| Percezione | Visione (YOLO su acceleratore NPU) | Acustica (battito alare 400–600 Hz) |
| Intervento | Getto d'aria mirato, non lesivo | Aspirazione con esca |
| Alimentazione | Rete | Batteria LiFePO4 + dock |

## Due idee controintuitive

**Non si insegue la zanzara, la si attira.** Vola erratica a 1–1,5 m/s, spesso
a 2 m di quota: nessun robot su ruote la intercetta. CO₂, calore a 35 °C e
octenolo la portano entro 20–30 cm, dove una ventola la risucchia. La mobilità
serve a portare la trappola nella stanza giusta, non a rincorrere.

**Il sensore migliore per le zanzare costa 5 €, non 300.** Rilevarle
otticamente richiede risoluzione sotto 1 mm/pixel. Il battito alare è invece
una firma spettrale robusta, rilevabile con un microfono MEMS I2S e una FFT.

## Struttura del repository

```
docs/          Documento di progetto master — inizia da qui
cad/src/       Sorgenti CadQuery parametrici (diffabili)
cad/export/    STEP e STL generati (Git LFS)
firmware/      ESP32-S3 — loop real-time motori e sensori
software/      ROS 2, visione, rilevamento acustico
hardware/bom/  Distinta base
```

## Documentazione

Il documento di riferimento è **[docs/PROJECT.md](docs/PROJECT.md)**.
Contiene architettura, BOM, stack software, strategia di produzione e un
**Decision Log** che registra ogni scelta tecnica con la sua motivazione.

Se contribuisci: le decisioni vanno nel Decision Log **con il perché**, non
solo con l'esito. È la parte che serve tra sei mesi.

## Produzione

Progetto pensato per stampa FDM domestica (Bambu Lab P2S), con ricorso a
service esterno (SLS PA12) solo per i pochi pezzi dove l'FDM fallisce
fisicamente. Il CAD è parametrico e genera entrambe le varianti cambiando una
variabile di tolleranza. Vedi PROJECT.md §7.

## Licenze

Questo progetto usa tre licenze, come da prassi per l'open hardware:

| Ambito | Licenza |
|---|---|
| Software e firmware | MIT — [LICENSE-software](LICENSE-software) |
| Hardware e CAD | CERN-OHL-W v2 — [LICENSE-hardware](LICENSE-hardware) |
| Documentazione | CC BY-SA 4.0 — [LICENSE-docs](LICENSE-docs) |

## Stato dei moduli

- [ ] Testa pan-tilt — CAD
- [ ] Testa pan-tilt — assemblaggio e misura precisione angolare
- [ ] Detection volatili
- [ ] Unità A integrata
- [ ] Rilevamento acustico zanzare
- [ ] Trappola con esca
- [ ] Base mobile e navigazione
- [ ] Unità B integrata

## Disclaimer

Progetto amatoriale fornito senza garanzia. Chi lo replica è responsabile della
conformità alla normativa del proprio paese in materia di fauna selvatica,
sicurezza elettrica e apparecchi in pressione.
