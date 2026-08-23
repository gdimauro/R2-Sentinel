# Vincoli di base mobile — Unità B

**Da:** `autonomy` · **A:** `mechatronics` · **Per conoscenza:** `chief-engineer`,
`compliance-safety`, `payload-fluidics`
**Fase:** 1 — consegna **prima del congelamento del telaio dell'Unità B**
**Stato:** vincoli di progetto. Ogni riga ha un numero e la derivazione fisica che lo produce.

---

## 0. Perché questa nota arriva in fase 1

Il mio lavoro è la fase 7 (navigazione e docking). Ma la fase 7 non ha modo di
correggere un telaio sbagliato: se il rapporto altezza/carreggiata è fuori
specifica, il robot si ribalta in curva e la meccanica va rifatta, non il
software. `SAFETY.md` §7.2 lo registra già come **FM-B9** (*«ribaltamento del
robot — montante di ~120 cm su base differenziale stretta … è un vincolo di
progetto meccanico, non di software di navigazione»*, voce `VA-24`).

Questa nota è l'ingresso di quel vincolo nel CAD, con i numeri.

**Che cosa NON è.** Non è un progetto di telaio. Non scelgo sezioni, materiali,
staffe o layout: quelli sono di `mechatronics`. Do i limiti entro cui il telaio
deve cadere e il modo di verificarli.

### 0.1 Il concetto che questi vincoli servono (D-03)

Il robot **non insegue**. La zanzara vola a 1–1,5 m/s in modo erratico: nessun
robot su ruote la intercetta. La mobilità serve a **portare la trappola nella
stanza giusta al momento giusto** e a **rientrare al dock**. La cattura è
statica, a robot fermo.

Conseguenza diretta sui vincoli meccanici, e va detta subito perché semplifica
la vita a tutti: **non serve velocità, non serve agilità, non serve accelerare.**
Serve non ribaltarsi, non cadere dalle scale, e riagganciare il dock 20 volte su
20. Ogni volta che un vincolo di questa nota costa velocità, il costo è
accettabile per costruzione.

---

## 1. Tabella riassuntiva dei numeri

Chi legge solo una cosa, legga questa. Le derivazioni sono nelle sezioni
indicate.

| # | Grandezza | Vincolo | §  |
|---|---|---|---|
| G-01 | Larghezza fuori tutto | **≤ 380 mm** (raccomandato 340 mm) | §3.1 |
| G-02 | Carreggiata `b` (fra i punti di contatto delle motrici) | **≥ 280 mm**, raccomandato **300 mm** | §3.1 |
| G-03 | Raggio di rotazione sul posto `R_rot` | **≤ 200 mm** (tutto il profilo inscritto) | §3.1 |
| G-04 | Ø ruota motrice | **≥ 100 mm** | §3.2 |
| G-05 | Ø ruota pazza | **≥ 75 mm** — mai sfera, mai Ø < 60 mm | §3.2 |
| G-06 | Coppia di stallo alla ruota | **≥ 2,0 N·m per ruota** | §3.3 |
| G-07 | Velocità a vuoto alla ruota | **≥ 0,70 m/s** | §3.3 |
| G-08 | Luce libera sotto il telaio | **≥ 25 mm** | §3.4 |
| **B-01** | **Altezza del baricentro `h`** | **≤ 272 mm** a carico peggiore | **§2** |
| B-02 | Posizione longitudinale del baricentro `x_cg` | **40…68 mm dietro l'assale motrice** | §2.5 |
| B-03 | Posizione laterale del baricentro | **entro ±15 mm** dalla mezzeria | §2.5 |
| B-04 | Braccio di stabilità nella direzione peggiore `d` | **≥ 110 mm** | §2.3 |
| B-05 | Angolo di ribaltamento statico misurato | **≥ 22°**, direzione peggiore, carico peggiore | §2.4 |
| B-06 | Forza di ribaltamento a 1150 mm di quota | **≥ 8 N** misurata | §2.6 |
| M-01 | Carico massimo in cima al montante (a 1150 mm) | **1,10 kg** | §7.1 |
| M-02 | Massa totale in ordine di marcia | **8…11 kg**, limite 12 kg | §7.2 |
| M-03 | Frazione di massa sotto i 150 mm | **≥ 70%** | §7.2 |
| M-04 | Prima frequenza propria del montante carico | **≥ 12 Hz** misurata | §7.3 |
| L-01 | Quota del piano di scansione LIDAR | **175 ± 5 mm** dal pavimento | §4.1 |
| L-02 | Complanarità del piano di scansione | **± 0,5°** (limite assoluto ± 1,0°) | §4.2 |
| L-03 | Occlusione angolare ammessa | **≤ 25° totali, in UN solo settore contiguo**, nel semipiano posteriore | §4.3 |
| L-04 | Campo libero attorno al LIDAR | **Ø 300 mm × ±20 mm** dal piano, tranne l'occlusore dichiarato | §4.3 |
| L-05 | Finestra/cupola trasparente davanti all'ottica | **VIETATA** | §4.4 |
| T-01 | ToF frontale centrale | h = 120 ± 5 mm, beccheggio **−22°** | §5.1 |
| T-02 | ToF frontali laterali | ±40° di imbardata, h = 120 ± 5 mm, beccheggio −15° | §5.1 |
| T-03 | Quarto ToF anti-sbalzo in cima al montante | **richiesto** (+15 €) | §5.2 |
| I-01 | Sede IMU | **sul telaio, MAI sul montante** | §5.4 |
| I-02 | Allineamento assi IMU a `base_link` | **± 1°**, con riferimenti meccanici | §5.4 |
| I-03 | Distanza IMU da motori/ventola/conduttori > 2 A | **≥ 100 mm** | §5.4 |
| I-04 | Prima frequenza propria del supporto IMU | **≥ 200 Hz** | §5.4 |
| E-01 | Risoluzione odometrica | **≤ 0,5 mm di avanzamento ruota per conteggio** | §5.5 |
| E-02 | Ø ruote motrici: differenza fra le due | **≤ 0,2 mm** misurata | §5.5 |
| E-03 | Ø ruota motrice noto e dichiarato | **± 0,25 mm** | §5.5 |
| D-01 | Finestra di cattura del dock | **± 20 mm laterali e ± 8° di imbardata** all'imbocco | §6.2 |
| D-02 | Guide del dock: distanza laterale fra i punti di presa | **≥ 150 mm** | §6.2 |
| D-03 | Piste di contatto sul dock | **≥ 20 × 20 mm** | §6.3 |
| D-04 | Corsa dei pin pogo | **≥ 3 mm**, 2 pin per polarità | §6.3 |
| D-05 | Interlock di potenza dei pin del dock | **obbligatorio, lato dock** | §6.4 |
| D-06 | Blocco unidirezionale sui pin del robot | **obbligatorio** | §6.4 |
| D-07 | Spostamento del dock sotto spinta di 40 N | **< 2 mm** | §6.5 |
| P-01 | Paraurti meccanico frontale | corsa ≥ 25 mm, scatto entro 5 mm | §5.3 |
| P-02 | Paraurti/anello cedevole in cima al montante | corsa ≥ 25 mm, scatto entro 5 mm | §5.3 |
| P-03 | Vano batteria da riservare | **220 × 150 × 90 mm, 3,2 kg** | §7.4 |

---

## 2. Baricentro — la voce critica

### 2.1 Perché è la voce critica e non una fra le tante

Il montante da ~120 cm porta trappola, ventola, esca e microfono in quota
(§4.3 di `PROJECT.md`: *«le zanzare stanno in alto, non a livello pavimento»*).
Ogni grammo lassù lavora con un braccio di 1,15 m contro una carreggiata di
0,30 m. **Il rapporto dei bracci è quasi 4:1 a sfavore.** Non esiste software di
navigazione che compensi un rapporto del genere: si compensa solo con la
geometria e con la distribuzione di massa, cioè nel CAD, cioè adesso.

### 2.2 Il poligono d'appoggio non è largo quanto la carreggiata

Questo è l'errore che voglio prevenire, perché è controintuitivo e costa un
telaio.

Su una base **differenziale a 2 motrici + 1 pazza** il poligono d'appoggio è un
**triangolo**. Il braccio di stabilità non è la mezza carreggiata (150 mm): è la
**distanza perpendicolare dalla proiezione del baricentro al lato più vicino del
triangolo**, e il lato più vicino è quello che unisce una ruota motrice alla
pazza — un lato **obliquo**.

Con la geometria plausibile (motrici in `(0, ±150)`, pazza posteriore in
`(−170, 0)`, baricentro in `(−55, 0)`, quote in mm, `x` positivo in avanti):

```
d = (b/2)·(L − |x_cg|) / √((b/2)² + L²)
  = 150 · (170 − 55) / √(150² + 170²)
  = 17250 / 226,7  =  76 mm
```

**76 mm, non 150 mm.** Metà di quello che si immagina guardando la carreggiata.
Con `h = 272 mm` l'angolo di ribaltamento scende a **15,6°** e la spinta laterale
che rovescia il robot, applicata in cima al montante, vale **5,3 N** — poco più
di **mezzo chilo di spinta**. Un gatto che ci si struscia contro.

### 2.3 Che cosa chiedo: un quarto punto, e costa 10 €

**Raccomandazione: 2 ruote motrici + 2 pazze posteriori + 1 pattino
anti-ribaltamento anteriore non portante.**

È una **deviazione dichiarata** dall'architettura «2 motrici + 1 pazza» di
§4.3. La propongo con i numeri, non per gusto:

| Configurazione | Braccio `d` peggiore | Angolo a `h`=272 mm | Spinta di ribaltamento a 1,15 m (8,5 kg) | `v_max` ammessa (§2.7) |
|---|---|---|---|---|
| 2 motrici + **1** pazza `(−170, 0)` | **76 mm** | 15,6° | **5,3 N** | **0,26 m/s** |
| 2 motrici + 1 pazza a `(−250, 0)` | 98 mm | 19,8° | 6,9 N | 0,33 m/s |
| 2 motrici + **2** pazze `(−170, ±120)` | **115 mm** | **22,9°** | **8,1 N** | **0,39 m/s** |
| (riferimento irraggiungibile: mezza carreggiata) | 150 mm | 28,9° | 10,9 N | 0,52 m/s |

Le due pazze posteriori **raddoppiano il margine di ribaltamento e portano la
velocità utile da 0,26 a 0,39 m/s**, cioè accorciano di un terzo il tempo di
rientro al dock, che è un mio criterio di FATTO (≤ 3 min).

**Il pattino anteriore** è un rullino di Ø ≥ 40 mm con **luce da terra 4 mm**,
**non portante in condizioni normali**. Non è un quarto appoggio: è un arresto
meccanico contro il beccheggio in frenata. Entra in contatto solo oltre
~1,4 m/s², cioè in urto o arresto d'emergenza. Così la base resta a 4 punti in
esercizio normale (odometria pulita) e ha un fine corsa fisico nel caso di
guasto. Luce 4 mm e Ø ≥ 40 mm perché un pattino strisciante si pianta sulle
soglie: deve rotolare.

**Obiezione prevedibile e sua risposta.** Quattro punti a terra sono
iperstatici e il robot può dondolare su pavimento irregolare, sporcando
l'odometria. Vero, e il rimedio non è togliere un punto: è il vincolo **G-09**
— *ciascuna ruota motrice deve restare caricata ≥ 20% del peso totale in ogni
condizione*, verificabile con due bilance da bagno sotto le ruote. Con
pneumatici in gomma dura la cedevolezza del battistrada assorbe le irregolarità
domestiche senza scaricare una motrice.

**Se `mechatronics` decide comunque per una sola pazza**, la decisione è
legittima ma non è gratuita: valgono la riga 1 della tabella, `v_max` scende a
**0,26 m/s**, e la riga va scritta nel Decision Log con il costo accettato. Non
la contesto oltre: la registro.

### 2.4 Il numero: `h ≤ 272 mm`

Requisito di accettazione: **angolo di ribaltamento statico misurato ≥ 22°**
nella direzione peggiore, a carico peggiore (batteria montata, camera di
raccolta e cartuccia CO₂ installate).

```
h_max = d / tan(22°) = 110 / 0,404 = 272 mm
```

con `d = 110 mm` (§2.3, configurazione raccomandata, arrotondata per difetto da
115).

**Perché 22° e non 30°.** 30° è il valore che si cita per abitudine dai carrelli
industriali. Qui è irraggiungibile e citarlo servirebbe solo a farlo violare in
silenzio. 22° è il valore che ho derivato dal margine di energia, che è il
criterio fisicamente corretto per un urto:

Energia necessaria per portare il baricentro sopra lo spigolo di ribaltamento:

```
ΔE = m·g·(√(h² + d²) − h) = 8,5 · 9,81 · (√(0,272² + 0,110²) − 0,272) = 1,79 J
```

Energia cinetica alla velocità massima di transito (0,35 m/s):

```
E_k = ½·m·v² = ½ · 8,5 · 0,35² = 0,52 J
```

**Margine 3,4×**, e il modello è già conservativo perché assume che il 100%
dell'energia cinetica traslatoria si converta in rotazione di ribaltamento, cosa
che in un urto reale non accade. 22° non è un numero di comodo: è il numero che
tiene quel margine sopra 3 alla velocità che mi serve.

### 2.5 Posizione del baricentro

- **Laterale (B-03): entro ±15 mm dalla mezzeria.** Un baricentro fuori asse
  consuma direttamente il braccio `d`: 15 mm di sbilanciamento sono il 14% del
  margine. Vale anche come vincolo di montaggio: la cartuccia CO₂ e la batteria
  non vanno «dove c'era posto».
- **Longitudinale (B-02): 40…68 mm dietro l'assale motrice.**
  - Limite inferiore 40 mm: sotto, il pattino anteriore entra in contatto già a
    1,4 m/s² e diventa un appoggio permanente invece che un arresto di
    emergenza. `x_cg ≥ a·h/g` con `a` = 1,44 m/s² dà 40 mm.
  - Limite superiore 68 mm: le pazze non devono portare più del **40%** del
    peso, altrimenti la trazione perde aderenza sul passaggio
    parquet→piastrella. `x_cg ≤ 0,40 · L_pazza = 0,40 · 170 = 68 mm`.
  - **Target: 55 mm.**

### 2.6 Il rischio che nessun numero elimina, e va dichiarato

Con la geometria migliore raggiungibile, la spinta laterale che rovescia il
robot applicata in cima al montante è **8,1 N — circa 800 grammi**. Un bambino,
un cane che passa, una tenda che si impiglia.

**Questo non si risolve con la geometria**, perché il braccio di una spinta
esterna è l'altezza del punto di spinta (1,15 m), non l'altezza del baricentro.
Aumentare la massa aiuta solo linearmente: portare il robot da 8,5 a 11 kg porta
la soglia da 8,1 a 10,5 N. Non cambia la natura del problema.

Va quindi **accettato esplicitamente come rischio residuo** e compensato:

1. **Rilevamento di inclinazione via IMU**: oltre **20°** di rollio o beccheggio
   → arresto motori e diseccitazione del payload (resistenza esca, ventola,
   CO₂) entro **200 ms**. Questa parte è mia e la implemento in fase 7.
2. **Niente parti calde, taglienti o sporgenti sopra i 400 mm**: se cade, cade
   su qualcuno. Vincolo per `mechatronics` e `payload-fluidics`.
3. **Massa in cima limitata a 1,10 kg** (§7.1): l'energia potenziale disponibile
   nella caduta resta sotto ~20 J.
4. Voce da aggiungere a `SAFETY.md` §7.2 come chiusura parziale di **VA-24**:
   la protezione non è l'angolo (che è insufficiente), è la combinazione
   angolo + cutoff inerziale + limitazione della massa in quota. Lo segnalo a
   `compliance-safety`; non lo scrivo io.

**Verifica richiesta (chiude VA-24):** prova di spinta con dinamometro a molla
applicato a 1150 mm, in 8 direzioni a 45°, a carico peggiore. **Forza minima
registrata ≥ 8 N.** Costa dieci minuti e un dinamometro da 15 €.

### 2.7 Il legame fra baricentro e velocità: la formula da tenere

Se la geometria finale non rispetta B-01, **non serve rifare il telaio: si
abbassa la velocità.** La relazione, indipendente dalla massa, è:

```
v_max = √( 2·g·(√(h² + d²) − h) / 3 )        [margine di energia 3×]
```

Consegno la formula perché `mechatronics` possa vedere, mentre disegna, che cosa
costa in fase 7 ogni millimetro di baricentro guadagnato o perso. Esempi:

| `d` [mm] | `h` [mm] | `v_max` [m/s] | Tempo di rientro da 12 m di percorso |
|---|---|---|---|
| 76 | 300 | 0,24 | 50 s + manovra |
| 76 | 272 | 0,26 | 46 s + manovra |
| 110 | 300 | 0,36 | 33 s + manovra |
| 110 | 272 | 0,39 | 31 s + manovra |
| 150 | 272 | 0,52 | 23 s + manovra |

Il criterio ≤ 3 min di rientro medio regge in tutti i casi. Cede il criterio
implicito di **reattività**: sotto 0,25 m/s il robot diventa percettibilmente
lento e il tempo di occupazione del corridoio cresce.

### 2.8 Come si misura il baricentro (procedura per `mechatronics`)

Non accetto un baricentro calcolato dal CAD: il CAD non conosce i cablaggi, il
nastro, le viti in più e la cartuccia CO₂ montata storta.

1. **Longitudinale.** Bilancia sotto le pazze, robot in piano: `x_cg = R_pazze ·
   L_pazza / W`. Precisione richiesta: ± 5 mm.
2. **Altezza.** Piano inclinabile, angolo `α` noto (usare l'IMU stessa o una
   livella digitale da 10 €), bilancia sotto l'appoggio a valle. Da due letture
   a `α` = 0° e `α` = 15° si ricava `h`. Precisione richiesta: ± 10 mm.
3. **Accettazione.** Prova di inclinazione fino al ribaltamento su piano
   inclinabile, con il robot trattenuto da una cinghia: **angolo registrato ≥ 22°
   nella direzione peggiore**. È esattamente la prova che `VA-24` chiede.

---

## 3. Geometria di trazione

### 3.1 Larghezza, carreggiata, raggio di rotazione

**G-01 — Larghezza fuori tutto ≤ 380 mm, raccomandato 340 mm.**

Derivazione. Il passaggio più stretto di un'abitazione è una porta interna con
**600 mm di luce netta** (bagno o ripostiglio). Perché Nav2 pianifichi
attraverso quella apertura e la percorra senza strisciare servono, per lato:

| Voce | mm per lato |
|---|---|
| Errore di localizzazione AMCL, 2σ | 50 |
| Errore di inseguimento del controllore a bassa velocità | 30 |
| Margine di inflazione minimo perché il varco non venga chiuso in costmap | 30 |
| **Totale** | **110** |

`600 − 2 · 110 = 380 mm`. Il valore raccomandato di 340 mm lascia 130 mm per
lato e rende il passaggio robusto anche con la porta socchiusa o con uno zerbino.

**G-02 — Carreggiata `b` ≥ 280 mm, raccomandato 300 mm.** Con 340 mm fuori tutto
e ruote da 25–30 mm di larghezza montate a sbalzo, `b` = 300 mm chiude
esattamente: piani mediani a ±150, esterno ruota a ±165, carter 8 mm → 346 mm.
Ogni millimetro di carreggiata è margine di ribaltamento: **non barattare `b`
per estetica del carter.**

**G-03 — Raggio di rotazione sul posto ≤ 200 mm.** L'intero profilo del robot,
montante e paraurti compresi, deve essere inscritto in un cilindro di raggio
200 mm centrato sulla **mezzeria dell'assale motrice**. Motivo: dichiaro a Nav2
un `robot_radius` circolare e il robot deve poter ruotare sul posto in un
corridoio senza spazzare nulla. Un profilo ovale con la coda a 250 mm mi
costringe a un footprint poligonale, che rende il *rotate in place* dei recovery
behavior inaffidabile — e il recovery è un mio criterio di FATTO (sblocco entro
60 s su 10 blocchi).

**Corollario:** l'asse di rotazione (mezzeria dell'assale) deve coincidere con
il centro del profilo entro **± 20 mm**.

### 3.2 Ruote

**G-04 — Ø ruota motrice ≥ 100 mm.** Derivazione dallo scavalcamento di soglia.
La forza necessaria per far salire una ruota rigida di raggio `R` su un gradino
di altezza `s`, con carico normale `N`:

```
F/N = √(s·(2R − s)) / (R − s)
```

Caso di progetto `s` = 15 mm (soglia in marmo o alluminio di porta interna,
bordo di tappeto):

| Ø ruota | F/N | Verdetto |
|---|---|---|
| 65 mm | 1,55 | irrealizzabile |
| 80 mm | 1,25 | marginale |
| **100 mm** | **1,02** | **accettabile** |
| 120 mm | 0,88 | migliore, ma alza il mozzo e con esso il telaio |

**G-05 — Ø ruota pazza ≥ 75 mm; Ø 60 mm è il minimo assoluto; sfera vietata.**
Con la stessa formula, una pazza da Ø 32 mm su una soglia da 15 mm dà
`F/N = 1,73` e per giunta con carico ridotto: **si pianta**. Una pazza a sfera
(*ball caster*) raccoglie capelli e peli di animale e si blocca: è la prima
causa di intervento manuale nei robot domestici. Vietata.

**G-05b — protezione anti-capelli.** Su pazze e motrici, il gioco fra ruota e
forcella/telaio deve essere **≤ 1,5 mm** (non ci entra il capello) **oppure
≥ 6 mm** con accesso per la pulizia (ci entra ma si toglie). La zona intermedia
è quella che intasa. Ogni pazza smontabile con **una sola vite, senza smontare
altro**.

**G-05c — pazze in coda, non in testa.** Le pazze vanno **dietro**: le motrici
scavalcano la soglia per prime e poi *trascinano* le pazze oltre. Una pazza
anteriore va *spinta* contro il gradino ed è il modo di guasto tipico
dell'impuntamento. Il beccheggio in frenata è coperto dal pattino anteriore
(§2.3), non da una pazza portante.

### 3.3 Motorizzazione — il 30:1 in BOM non basta

**Questo è un reperto, non un vincolo di stile.** §5.4 di `PROJECT.md` prevede
`2× motoriduttore 37D 12 V 30:1`. Con quel rapporto e ruote da 100 mm:

| Grandezza | 30:1 (BOM) | 70:1 (richiesto) |
|---|---|---|
| Coppia di stallo per motore | ~0,83 N·m | ~1,96 N·m |
| Forza di trazione di stallo (2 ruote, R = 50 mm) | **33 N** | **78 N** |
| Velocità a vuoto alla ruota | 1,83 m/s | 0,79 m/s |
| Forza richiesta per soglia 15 mm (60% di 8,5 kg sulle motrici) | **51 N** | 51 N |
| **Esito** | **non scavalca** | scavalca con margine 1,5× |

Requisiti, espressi in coppia e non in codice prodotto perché la scelta è di
`mechatronics`:

- **G-06 — coppia di stallo ≥ 2,0 N·m per ruota** (margine ≥ 1,5× sulla soglia
  da 15 mm a massa massima).
- **G-06b — coppia continuativa ≥ 1,2 N·m per ruota.** Serve per il rotolamento
  su tappeto: coefficiente di resistenza 0,15–0,25 su moquette a pelo medio, che
  a 11 kg significa 16–27 N di forza continua, cioè 0,4–0,7 N·m per ruota. Con
  1,2 N·m si resta sotto il 60% della continua nominale e i motori non scaldano.
- **G-07 — velocità a vuoto alla ruota ≥ 0,70 m/s.** La velocità di transito è
  0,35 m/s (§2.7): lavorare al 50% della velocità a vuoto tiene i motori in una
  zona di rendimento e di risoluzione PWM ragionevole. Sotto il 30% il controllo
  di velocità a bassa andatura (docking a 0,05 m/s) diventa scattoso.
- **G-07b — nessun freno di stazionamento richiesto**, ma il riduttore deve
  trattenere il robot fermo su pendenza fino a 3° a motori diseccitati. Vedi
  §5.6: durante l'ascolto acustico i driver vanno **spenti**, non tenuti a
  PWM = 0.

### 3.4 Luce libera e sotto-scocca

**G-08 — luce libera sotto il telaio ≥ 25 mm** (esclusi ruote e pattino). Soglia
di progetto 15 mm + beccheggio durante lo scavalcamento + compressione del pelo
del tappeto. **Nessun cavo, connettore o vite sporgente sotto il piano di
fondo**: quello che sporge sotto strappa e si impiglia.

**G-08b — fondo chiuso e liscio.** Un fondo aperto sopra i motori raccoglie
polvere e peli fino a bloccare gli alberi.

---

## 4. LIDAR — RPLIDAR C1

È il vincolo più spesso violato dal disegno del carter, quindi lo scrivo con più
dettaglio degli altri.

### 4.1 Quota di montaggio: piano di scansione a 175 ± 5 mm

Non è l'altezza della scatola: è la quota del **piano ottico** dichiarata dal
costruttore, misurata dal pavimento a robot in ordine di marcia.

Derivazione — che cosa sta sopra e che cosa sta sotto, in un'abitazione:

| Quota | Che cosa c'è | Chi lo deve vedere |
|---|---|---|
| 0–20 mm | cavi, soglie, tappeti, ciabatte piatte | ToF frontali (§5.1) |
| 20–120 mm | scarpe, ciotole per animali, giocattoli, battiscopa | ToF frontali |
| **175 mm** | **piano LIDAR** | — |
| 150–400 mm | gambe di sedia e tavolo, basi di divano e letto, termosifoni | **LIDAR** |
| 400–900 mm | piani di tavolo (72–76 cm), scrivanie, sedute (45 cm), banconi (90 cm) | nessuno → **§5.2** |
| ~1150 mm | **payload in cima al montante** | nessuno → **§5.2** |

- **Sotto 175 mm** non si può scendere di molto: sotto ~120 mm il piano
  intercetta i battiscopa e la mappa diventa una mappa di battiscopa e di
  ciabatte, con pochissime superfici verticali stabili per lo scan matching.
- **Sopra 175 mm** non si può salire di molto restando dentro la scocca: a
  250 mm il piano passa sopra le basi dei divani e sotto i piani dei tavoli,
  cioè nella fascia in cui una gamba di sedia inclinata è al suo punto più
  sottile e più obliquo — il ritorno peggiore possibile.
- 175 mm tiene inoltre il sensore **dentro l'ingombro della base**, protetto
  dagli urti, e coerente con la prassi dei robot domestici commerciali.

**Il valore misurato va dichiarato a me con precisione ± 2 mm**: finisce nella
trasformata statica `base_link → laser` dell'URDF.

### 4.2 Complanarità: ± 0,5°

**L-02 — il piano di scansione deve essere parallelo al pavimento entro ± 0,5°**,
limite assoluto ± 1,0°.

Derivazione: la portata dichiarata del C1 è 12 m. Con il piano a 175 mm e un
errore di beccheggio verso il basso di `θ`, il raggio incontra il pavimento a
`0,175 / tan θ`:

| Errore | Distanza a cui il raggio tocca il pavimento |
|---|---|
| 0,5° | 20,0 m — fuori portata, innocuo |
| 1,0° | 10,0 m — al limite della portata |
| **1,5°** | **6,7 m** — **il pavimento diventa un muro fantasma** |

Un muro fantasma a 6,7 m distrugge sia la mappa sia la costmap globale, e il
sintomo (il robot si ferma davanti al nulla) verrà attribuito al software per
giorni. Verificare con una livella digitale sulla scocca del sensore, non «a
occhio».

Lo stesso vale per il **rollio**: ± 0,5°.

### 4.3 Campo libero — 335° utili, con l'occlusione in un pezzo solo

**L-04 — nessuna struttura entro un cilindro di Ø 300 mm centrato sull'asse del
LIDAR, esteso ± 20 mm sopra e sotto il piano di scansione**, con l'unica
eccezione dell'occlusore dichiarato.

**L-03 — occlusione angolare ≤ 25° totali, in UN SOLO settore contiguo,
compreso nel semipiano posteriore (180° ± 20°).**

Il montante deve attraversare il piano di scansione: è inevitabile e non lo
contesto. Contesto il **modo**:

- **Un settore cieco contiguo e noto lo gestisco**: filtro `angle_min`/
  `angle_max` o `laser_filters` a scatola, `slam_toolbox` lavora benissimo con
  335° — molti robot commerciali montano LIDAR da 270°.
- **Quattro montanti sottili di carter distribuiti sul giro non li gestisco**:
  producono ritorni spuri a bearing casuali, alcuni ritorni «buoni» a 6 cm che
  non posso distinguere dal reale, e corrompono la mappa in modo intermittente.
  Il costo si paga tutto in fase 7, in giorni di debug su un difetto meccanico.

Vincolo geometrico che ne discende: montante **singolo**, sulla mezzeria
posteriore, e distanza dall'asse LIDAR

```
d_montante ≥ (larghezza_montante / 2) / tan(12,5°)
```

→ per un montante da 30 mm: **≥ 68 mm**; per uno da 40 mm: **≥ 90 mm**.

**L-03b — l'occlusore deve essere opaco e nero opaco.** Una superficie lucida o
chiara a 7 cm dal sensore genera ritorni saturati e riflessioni interne. Nero
opaco (ASA nero, non lucidato) o rivestito con feltro adesivo.

**L-03c — il settore occluso va dichiarato a me in gradi, ± 1°**, misurato sul
robot montato, non calcolato dal CAD.

### 4.4 Divieto esplicito: nessuna finestra trasparente

**L-05 — è vietata qualunque cupola, finestra, plexiglass o pellicola davanti
all'ottica del LIDAR.**

Il motivo è che un carter «pulito» con una fascia trasparente è esattamente ciò
che verrà proposto, e produce: riflessioni interne a distanza fissa, un anello
permanente di ritorni fra 5 e 15 cm (la portata minima del C1 è 5 cm), perdita
di portata per assorbimento, e opacizzazione progressiva da polvere. Se serve
protezione meccanica, si usa un **anello rigido opaco sopra e sotto** il piano
di scansione, mai davanti.

### 4.5 Posizione rispetto all'asse di rotazione

**L-06 — asse del LIDAR sulla mezzeria longitudinale entro ± 3 mm**, e a
distanza **≤ 120 mm** dall'asse di rotazione (mezzeria dell'assale motrice), con
il valore **dichiarato a ± 2 mm**.

Motivo: durante la rotazione sul posto un LIDAR fuori asse descrive un arco, e
la scansione va de-skewata con l'odometria. Un offset noto a 2 mm lo compenso;
un offset ignoto o variabile no, e si presenta come «i muri si sdoppiano quando
ruota».

---

## 5. ToF, IMU, paraurti, encoder

### 5.1 I tre VL53L5CX in BOM — collocazione

Caratteristiche rilevanti: 8×8 zone, FoV ~45°×45°, portata utile realistica
in interno illuminato **~2 m** (4 m dichiarati su bersaglio bianco al buio),
**~0,6 m su moquette scura**, portata minima ~2 cm.

| Sensore | Posizione | Beccheggio | Imbardata | Funzione |
|---|---|---|---|---|
| **ToF-C** | frontale centrale, **h = 120 ± 5 mm** | **−22°** | 0° | dislivello + ostacoli sotto il piano LIDAR |
| **ToF-L** | frontale sinistro, h = 120 ± 5 mm | −15° | **−40°** | spigolo anteriore sinistro, dislivello in curva |
| **ToF-R** | frontale destro, h = 120 ± 5 mm | −15° | **+40°** | idem, a destra |

Derivazione del beccheggio di ToF-C. Con FoV verticale 45° e asse a −22°, i
raggi coprono da 0° a −44°. Il raggio a −44° tocca il pavimento a
`120 / tan(44°) = 124 mm` davanti al sensore; il raggio orizzontale vede
lontano. Copertura del pavimento da **124 mm all'infinito**, con le righe basse
utilizzabili per il dislivello e quelle alte per l'ostacolo basso.

**Criterio di accettazione verificabile (T-01b):** con il robot fermo su
pavimento piano, **almeno 3 righe di zone devono restituire il pavimento a
distanze comprese fra 100 e 350 mm dal punto di contatto a terra più avanzato.**
Se non accade, il beccheggio è sbagliato e il rilevamento di dislivello non
chiude il criterio «0 cadute in 2 h».

Perché 350 mm bastano: a 0,15 m/s (velocità imposta in zona non mappata o
prossima a un dislivello noto) lo spazio di arresto è
`v²/2a = 0,0225/2 = 11 mm`, più 35 mm di latenza di catena (100 ms). 350 mm
danno un margine di 7×.

**T-01c — nessun vetro, nessuna pellicola davanti ai ToF** senza una finestra
progettata secondo le note applicative del costruttore (apertura svasata,
intercapedine d'aria, calibrazione di crosstalk). Un ToF dietro a un pezzo di
plexiglass incollato legge la propria copertura.

### 5.2 Chiedo un quarto ToF, e dico perché

**T-03 — quarto VL53L5CX in cima al montante, a ~1050 mm, frontale, beccheggio
−10°. Costo: +15 €.**

Il buco è nella tabella di §4.1: **fra 400 e 1150 mm non guarda nessuno.** Il
LIDAR è a 175 mm, i ToF guardano in basso, e il montante è alto 1,2 m. Il modo
di guasto è concreto e frequente:

> Il robot passa sotto il bordo di un tavolo, di una scrivania o di un letto. La
> base ci passa, il LIDAR non vede il piano, Nav2 pianifica correttamente
> attraverso lo spazio libero fra le gambe — **e il montante colpisce il piano
> del tavolo a 75 cm.** Con 8,5 kg a 0,35 m/s e un braccio di 0,75 m, il robot
> si ribalta.

Questo è **FM-B9** che si realizza per una via che la tabella di `SAFETY.md`
non nomina. Il quarto ToF è la protezione funzionale; la protezione hardware è
il paraurti di §5.3. Chiedo entrambi: SAFETY.md §7 è esplicito sul fatto che
`SW` come unica colonna di protezione è una riga non chiusa.

Se il quarto sensore non viene approvato, la conseguenza sulla navigazione è
che devo **vietare a priori tutte le aree sotto arredi** con zone di
esclusione disegnate a mano sulla mappa dopo il primo rilievo. Funziona, ma è
una protezione software che dipende da un file di configurazione — cioè
esattamente ciò che `SAFETY.md` §7 rifiuta — e va allora accettata per iscritto.

### 5.3 Paraurti — le protezioni hardware

Servono perché **il LIDAR non vede il vetro e non vede gli specchi**: attraversa
i primi e viene deviato dai secondi, producendo mappe con stanze fantasma.
Nessun sensore ottico in BOM risolve il problema. L'ultima linea di difesa è
meccanica.

**P-01 — paraurti frontale sulla base.**

| Parametro | Valore | Derivazione |
|---|---|---|
| Copertura angolare | ≥ ±60° | copre lo spigolo anteriore che tocca per primo in curva |
| Corsa complessiva | **≥ 25 mm** | a 0,35 m/s con 60 ms di latenza il robot percorre 21 mm dopo lo scatto |
| Scatto del microswitch | entro i primi **5 mm** | lascia 20 mm di corsa utile dopo il comando di arresto |
| Forza di scatto | **3…8 N** | sotto 3 N scatta su una tenda; sopra 8 N non protegge dal ribaltamento |
| Forza a fine corsa | ≤ 25 N | limita il danno all'arredo e al robot |
| Microswitch | **2, sinistro e destro, in serie all'abilitazione hardware dei driver** | dà anche la direzione dell'urto, che uso nel recovery |
| Quota massima | ≤ 155 mm | non deve entrare nel piano di scansione LIDAR (175 mm) |

**P-02 — anello cedevole in cima al montante**, quota 1050–1150 mm, stessi
parametri di corsa e scatto, **1 microswitch**, in serie alla stessa
abilitazione. È la protezione hardware contro l'urto del montante (§5.2). A
0,20 m/s — velocità che io impongo appena il ToF di testa vede qualcosa entro
800 mm — la corsa necessaria dopo lo scatto è 12 mm, coperta.

L'abilitazione dei driver deve essere **hardware**: un ingresso di enable dei
DRV8871 che il microswitch apre direttamente, non un GPIO letto dal firmware.
Un paraurti che passa dal software non protegge dal blocco del software
(`SAFETY.md` FM-X1).

### 5.4 IMU BNO085

| ID | Vincolo | Derivazione |
|---|---|---|
| **I-01** | **Sul telaio, MAI sul montante** | il montante è una trave a mensola che oscilla a 5–12 Hz (§7.3). Un'IMU in cima legge l'oscillazione come moto del corpo e la inietta nell'EKF: l'odometria fusa diventa peggiore di quella dei soli encoder |
| **I-02** | Assi allineati a `base_link` entro **± 1°**, con **due spine di riferimento** sul supporto | 1° di errore di beccheggio proietta 0,17 m/s² di gravità sull'asse longitudinale: è un'accelerazione falsa 5× più grande di quella reale in transito. Le spine servono perché io possa calibrare il residuo una volta e fidarmene dopo ogni smontaggio |
| **I-03** | ≥ **100 mm** da motoriduttori, ventola centrifuga e da qualunque conduttore che porti > 2 A; coppie di potenza **ritorte** | un conduttore a 2 A genera ~2,7 µT a 150 mm, contro i ~24 µT della componente orizzontale del campo terrestre in Italia: **6° di errore di heading**. I magneti dei motori sono peggio |
| **I-04** | Prima frequenza propria del supporto ≥ **200 Hz** | supporto rigido e vincolato, non un pannello stampato sottile. Sotto 200 Hz il supporto entra in risonanza con la frequenza di passaggio pala della ventola da 80 mm |
| **I-05** | Vicino all'asse di rotazione: **≤ 60 mm** in pianta | riduce le accelerazioni centrifughe e tangenziali spurie durante la rotazione sul posto |

**Decisione software collegata, che registro nel Decision Log:** userò il
BNO085 in modalità **senza magnetometro** (*game rotation vector*), fondendo
l'imbardata con l'odometria a ruote nell'EKF. Il magnetometro in un robot con
due motori a 12 V, una ventola e un pacco batteria a 50 cm non è recuperabile
con nessuna distanza realizzabile in 340 mm di larghezza. Scartata l'alternativa
(calibrazione hard/soft iron): richiede una rotazione di calibrazione a ogni
avvio ed è invalidata da qualunque oggetto ferromagnetico in casa — un
termosifone, un frigorifero, una struttura in cemento armato.

**Conseguenza per `mechatronics`:** I-03 resta comunque richiesto per il rumore
sull'accelerometro, ma non è più critico al grado che sarebbe stato con il
magnetometro attivo. È un vincolo che ho allentato io, non uno che avete
guadagnato: se in futuro qualcuno riattiva il magnetometro, torna a 300 mm e non
è realizzabile.

### 5.5 Encoder e odometria

Il criterio di FATTO di fase 7 richiede una mappa di ≥ 60 m² con **errore di
chiusura d'anello ≤ 10 cm**. Un anello in un appartamento da 60 m² è un percorso
di **35–40 m**. Un errore di scala `ε` produce un errore di chiusura `ε · 40 m`:

```
ε ≤ 0,10 m / 40 m = 0,25%
```

Da qui, e sono vincoli meccanici, non software:

- **E-03 — il diametro effettivo della ruota va misurato e dichiarato a
  ± 0,25 mm** su Ø 100 mm. Il valore nominale del venditore non serve.
- **E-02 — le due ruote motrici devono differire in diametro di ≤ 0,2 mm.** Una
  differenza maggiore produce una curvatura sistematica che l'EKF interpreta
  come una rotazione reale. Stesso lotto, misurate entrambe.
- **E-04 — battistrada in gomma o TPU di durezza ≥ 70 Shore A, mai schiuma.** Il
  raggio di rotolamento di un pneumatico morbido cambia con il carico e con il
  fondo: 1 mm di schiacciamento su 50 mm di raggio è il 2% di errore di scala,
  8× fuori specifica.
- **E-01 — risoluzione ≤ 0,5 mm di avanzamento ruota per conteggio.**
  Derivazione: l'aggancio al dock richiede ± 3° di imbardata; su una carreggiata
  di 300 mm, 0,5° corrispondono a 2,6 mm di avanzamento differenziale, e per
  risolverli servono almeno 4 conteggi → 0,65 mm/conteggio. Con un encoder da
  64 CPR sull'albero motore, riduzione 70:1 e Ø 100 mm si ottengono
  0,07 mm/conteggio: **abbondante, purché la quadratura sia decodificata ×4 nel
  firmware.** Questo lo chiedo a `mechatronics` come requisito sul livello
  micro-ROS: `×4`, non `×1`.
- **E-05 — la carreggiata effettiva `b` va dichiarata a ± 2 mm.** La calibrerò
  poi con UMBmark sul pavimento reale, ma parto dal valore misurato.

### 5.6 Requisito acustico che tocca la meccanica

`acoustic-perception` chiede silenzio durante l'ascolto. Ne discende un vincolo
che è elettromeccanico e va nel telaio:

**A-01 — deve esistere un segnale di abilitazione hardware dei driver di
trazione che tolga completamente corrente ai motori.** Non basta comandare
velocità zero: un motore tenuto in coppia da un anello di controllo a PWM emette
armoniche udibili. Durante la sessione di ascolto pubblico lo stato `stazionamento`
e i driver vanno **disabilitati**, non azzerati. Il robot resta fermo per attrito
del riduttore (G-07b).

**A-02 — ventola centrifuga isolata dal telaio con gommini antivibranti**,
trasmissibilità < 0,2 sopra i 60 Hz. Serve a me (rumore sull'accelerometro,
§5.4 I-04) e a `acoustic-perception` (autocontaminazione, questione aperta di
§10). È lo stesso pezzo che risolve due problemi di due ruoli diversi.

---

## 6. Dock — il requisito più duro

La navigazione senza rientro è un robot morto sul pavimento. Progetto il docking
per primo e per ultimo.

### 6.1 Che cosa garantisce la navigazione, onestamente

Questa è la parte che di solito non viene detta e che fa fallire il dock.

| Fase dell'avvicinamento | Errore di posa che garantisco |
|---|---|
| Arrivo al *staging point* a 1,0 m dal dock (Nav2 + AMCL) | ± 80 mm laterali, ± 10° |
| Ultimi 300 mm, guida su beacon IR a 0,05 m/s | **± 15 mm laterali, ± 5°** |
| **Contatto dei pin** | **± 5 mm laterali, ± 3°** ← criterio di FATTO |

**La navigazione non arriva a ± 5 mm.** Nessuna base differenziale ci arriva a
sensori. Il salto dagli ± 15 mm / ± 5° del sensore agli ± 5 mm / ± 3° dei
contatti **lo deve fare la geometria meccanica del dock**, con un imbocco
autocentrante. Se il dock è una piastra piatta con due contatti, i 20/20 non
sono raggiungibili e il criterio di fase 7 fallisce per un motivo meccanico.

### 6.2 Che cosa deve fare la meccanica: una coppia di imbardata, non una spinta laterale

Punto non ovvio: **una base differenziale non può traslare lateralmente.** Per
farla scorrere di lato servono ~66 N (attrito laterale dei pneumatici, µ ≈ 0,8
su 8,5 kg). Un imbuto che spinge di lato **non centra il robot: lo blocca.**

Quello che il robot fa senza sforzo è **ruotare** attorno a un punto, perché le
ruote rotolano. Quindi:

- **D-02 — le guide del dock devono ingaggiare DUE punti sul robot, distanti fra
  loro ≥ 150 mm lateralmente.** La differenza di penetrazione fra i due punti
  genera una coppia di imbardata che raddrizza il robot mentre avanza. Un solo
  punto centrale genera solo forza laterale, e quella non serve.
- **D-01 — finestra di cattura all'imbocco: ± 20 mm laterali e ± 8° di
  imbardata.** È il mio errore garantito (± 15 mm / ± 5°) con un 30% di margine.
- **Rampe a semiangolo 12…18°**, chiusura di 20 mm su una corsa di ≥ 80 mm.
- **I punti di presa sul robot devono essere rullini o pattini in POM/PTFE**, non
  spigoli di pezzo stampato: l'ASA su ASA striscia, si scalda e si segna, e dopo
  cinquanta agganci la geometria è cambiata.
- **Ultimi 30 mm con ≥ 3 mm di cedevolezza** (molla o gomma), così il robot si
  siede senza mandare i motori in stallo contro un arresto rigido.
- **Le rampe non devono sollevare nessuna ruota motrice.** Una motrice
  scaricata perde trazione proprio nell'istante in cui serve.

### 6.3 Contatti

| ID | Vincolo | Derivazione |
|---|---|---|
| **D-03** | Piste sul dock **≥ 20 × 20 mm** | residuo ± 5 mm laterali + ± 3° su 60 mm di interasse pin (± 1,6 mm) + ± 3 mm longitudinali + punta pin 2 mm → 20 mm dà ± 8 mm di margine |
| **D-04** | **Corsa dei pin pogo ≥ 3 mm**, forza 1,5…3 N ciascuno, **2 pin per polarità** | la corsa assorbe la tolleranza verticale e l'usura; due pin danno ridondanza contro un contatto sporco |
| D-04b | Placcatura **oro** su pin e piste | `SAFETY.md` FM-B2: contatto ossidato → resistenza → punto caldo |
| D-04c | Resistenza di contatto **≤ 30 mΩ per polarità, misurata a 3 A** | a 3 A e 30 mΩ si dissipano 0,27 W per polarità in un contatto piccolo: è il limite accettabile |
| D-04d | Distanza fra le polarità **≥ 15 mm** e **nervatura isolante alta ≥ 5 mm** fra esse | una moneta da 2 € misura 25,75 mm e scavalca 15 mm di aria: la nervatura è ciò che impedisce a un oggetto piatto di toccare entrambe |
| D-04e | Corrente di progetto **3 A** (0,3 C su pacco da 10 Ah) | pin da **≥ 5 A** nominali, declassati |

### 6.4 Interlock — chiude `VA-21`, copre FM-B2 e FM-B3

`SAFETY.md` FM-B3: *«pin del dock cortocircuitati da un oggetto metallico, un
animale domestico o un bambino → ustione, arco, incendio»*. È la ragione
principale dell'interlock, più della corrosione.

**D-05 — interlock LATO DOCK, obbligatorio.**
- Microswitch o reed **azionato dalla presenza fisica del robot in sede**, in
  serie al comando di un relè o MOSFET che collega l'alimentatore alle piste.
- **Le piste sono morte finché il robot non è seduto.** Non «a bassa tensione
  quindi innocue»: 14,6 V su un cortocircuito franco attraverso un anello o una
  chiave sono ustione da contatto in secondi.
- Il sensore va **schermato meccanicamente** in modo che non sia azionabile da
  una mano, da una zampa o da un oggetto infilato: incassato, non accessibile.
- **Limitazione hardware di corrente** in serie: PTC ripristinabile o fusibile,
  tarato sopra i 3 A di carica e sotto la corrente che scalda le piste.

**D-06 — blocco unidirezionale LATO ROBOT, obbligatorio. Questo manca in tutte
le versioni del documento e non è coperto da FM-B2/FM-B3.**

I pin del **robot** sono collegati alla batteria. Quando il robot è **fuori dal
dock**, i suoi contatti esposti sono in tensione, e un oggetto metallico che li
tocca **cortocircuita direttamente il pacco LiFePO4**. Un pacco 4S 10 Ah eroga
correnti di centinaia di ampere in cortocircuito. È lo stesso modo di guasto di
FM-B3 ma sulla faccia opposta, e il robot gira per casa mentre il dock sta
fermo.

Richiesto: **elemento di blocco in serie fra i contatti del robot e il pacco** —
diodo ideale o MOSFET back-to-back comandato — che conduca **solo verso il
pacco** e **solo su comando di carica**. In aggiunta al fusibile adiacente al
morsetto già richiesto da FM-B5.

**Logica di ricarica (mia, per `compliance-safety`).** La consegno qui perché
determina i segnali che chiedo alla meccanica:
- non comando mai la carica se il BMS segnala anomalia (temperatura, cella,
  bilanciamento): **fail-safe, il robot resta in dock scarico e lo segnala via
  MQTT**;
- non maschero mai un guasto di contatto con un ritentativo infinito: **massimo
  3 tentativi di aggancio**, poi arresto in posizione e segnalazione. Un robot
  che sbatte contro il dock per otto ore è un guasto che si trasforma in un
  incendio;
- richiedo dalla meccanica **due segnali distinti**: `seduto` (il microswitch di
  interlock) e `in_carica` (corrente misurata > 0,2 A). Se `seduto` è vero e
  `in_carica` resta falso per 10 s, il contatto è sporco: retrocedo e riprovo,
  contando i tentativi.

### 6.5 Installazione del dock

| ID | Vincolo | Derivazione |
|---|---|---|
| **D-07** | Spostamento del dock **< 2 mm sotto una spinta orizzontale di 40 N** | nell'imbocco il robot spinge fino a ~35 N. Un dock che scivola di 10 mm rende i 20/20 impossibili: la geometria cambia a ogni aggancio |
| D-08 | Su **pavimento duro**, mai su tappeto | su moquette la geometria dell'imbocco affonda e cambia |
| D-09 | Spazio libero **1200 mm davanti, 400 mm per lato** | serve per allinearsi a 1 m, e per arretrare di 500 mm e riprovare dopo un aggancio fallito |
| D-10 | Ricevitori IR sul robot: **2, distanti ≥ 120 mm**, alla stessa quota degli emettitori del dock, **h = 90 ± 10 mm** | la distanza fra i ricevitori è ciò che dà il bearing differenziale. 90 mm sta sopra il battiscopa e sotto la maggior parte degli arredi |
| D-11 | Cappuccio parasole sui ricevitori: FoV verticale **± 15°**, orizzontale **± 45°** | il TSOP38238 satura con la luce solare e con i telecomandi IR di casa. Senza cappuccio il dock non funziona nel pomeriggio |
| D-12 | Alimentatore del dock: **≥ 60 W, uscita fisicamente ≤ 14,6 V** | 44 W di carica a 3 A + ~15 W di payload attivo in dock (§7.5). Il limite di 14,6 V è **D-20**, non negoziabile |

---

## 7. Massa e carico

### 7.1 Carico massimo in cima al montante: 1,10 kg

Ipotesi di partenza, da confermare con le masse reali:

| Elemento | Massa | Quota del suo baricentro |
|---|---|---|
| Base completa (telaio, motori, ruote, batteria 4S 10 Ah, Pi 5 + Hailo, driver, convertitori) | 6,5 kg | 75 mm |
| Montante nudo con staffe e cablaggio | 0,9 kg | 600 mm |
| **Payload di testa** (trappola, ventola, camera di raccolta, esca, microfono) | **`m_t`** | **1150 mm** |

Imponendo `h ≤ 272 mm` (B-01):

```
m_t ≤ (h_max · M₀ − N₀) / (H_t − h_max)
    = (0,272 · 7,4 − 1,0275) / (1,150 − 0,272)
    = 0,9853 / 0,878
    = 1,12 kg
```

**M-01 = 1,10 kg**, arrotondato per difetto.

Sensibilità alla quota del payload — `payload-fluidics` e `mechatronics` la
useranno per barattare:

| Quota del payload `H_t` | Carico massimo ammesso |
|---|---|
| 1000 mm | 1,35 kg |
| 1100 mm | 1,19 kg |
| **1150 mm** | **1,10 kg** |
| 1250 mm | 0,98 kg |
| 1350 mm | 0,91 kg |

**Il cambio in valuta che conta.** Per compensare **1 kg aggiunto in cima**
servono **4,3 kg di zavorra a 75 mm** per riportare il baricentro dov'era. Ogni
chilogrammo in quota alza il baricentro di **~106 mm**; ogni chilogrammo in
basso lo abbassa di **~25 mm**. Il cambio è 4,3 a 1 e non è negoziabile: è
geometria.

**Proposta a `payload-fluidics`, che riduce il problema invece di spostarlo:**
mettere **cartuccia CO₂ e riduttore nella base** e portare la CO₂ in quota con
un tubo da 4 mm. La perdita di carico su 1,2 m di tubo per una portata di CO₂ di
qualche centinaio di ml/min è trascurabile, e si guadagnano 200–250 g in cima
(cioè 25 mm di baricentro), si abbassa il confine di pressione dentro la base
dove è ispezionabile, e la cartuccia sta lontana dalla parte che cade se il robot
si rovescia. La **ventola deve restare in testa** — la bocca di aspirazione deve
essere dove è il flusso di cattura — ma va isolata con gommini (A-02).

### 7.2 Massa totale

**M-02 — 8…11 kg in ordine di marcia, limite superiore 12 kg.**

- **Limite inferiore 8 kg**, e non è un refuso: la forza che ribalta il robot è
  proporzionale alla massa (§2.6). Un robot leggero con un montante alto è
  **meno** sicuro, non più. La massa va cercata, purché stia in basso.
- **Limite superiore 11–12 kg** per tre ragioni indipendenti: la trazione
  richiesta per la soglia (§3.3) cresce linearmente; l'utente deve poterlo
  sollevare (serve una **maniglia sul telaio, sopra il baricentro, presa
  ≥ 100 mm**); l'energia rilasciata in un ribaltamento a 12 kg è ~20 J.

**M-03 — almeno il 70% della massa sotto i 150 mm.** È la forma sintetica di
B-01: se il 70% della massa sta sotto 150 mm, il baricentro cade nella fascia
giusta quasi automaticamente.

### 7.3 Rigidezza del montante

**M-04 — prima frequenza propria di flessione del montante **carico** ≥ 12 Hz,
misurata.**

Derivazione. Un profilo in alluminio 20×20 con 1 kg in cima a 1,15 m ha una
rigidezza a mensola `k = 3EI/L³ ≈ 1200 N/m`, cioè **f₁ ≈ 5,5 Hz** e 8 mm di
freccia sotto 1 g laterale. A 5,5 Hz:

- ogni soglia scavalcata eccita l'oscillazione, che poi dura secondi;
- l'oscillazione entra nell'IMU (§5.4) e nell'odometria fusa;
- il piano di scansione del LIDAR non ne risente (il LIDAR sta sulla base), ma
  la posa di stazionamento richiesta da `payload-fluidics` non è «ferma»
  finché il montante oscilla;
- il microfono in cima raccoglie rumore strutturale.

12 Hz richiede una rigidezza ~4,7× maggiore, cioè `I ≥ 4·10⁻⁸ m⁴`: un profilo
**30×30** o un montante **a due travi** collegate. La scelta è di
`mechatronics`; il numero è mio.

**Misura:** colpo secco in testa al montante, registrazione dell'accelerometro
posto temporaneamente in cima, FFT. Dieci minuti, nessuna strumentazione oltre
a quella già in BOM.

### 7.4 Il vano batteria va riservato, non dimensionato

L'autonomia target dell'Unità B è **una questione aperta di §10** e non la
risolvo con un'assunzione silenziosa. La risolvo riservando il volume, così che
la decisione non richieda un secondo telaio.

**P-03 — riservare nella base un vano da 220 × 150 × 90 mm per un pacco fino a
3,2 kg, con il baricentro del vano ≤ 80 mm dal pavimento.**

È il doppio abbondante del pacco 4S 10 Ah di §5.5. **Nota controintuitiva ma
utile:** una batteria più grande **migliora** la stabilità, perché aggiunge
massa in basso. Passare da 1,3 a 3,0 kg di pacco abbassa il baricentro di ~25 mm
e **alza il carico ammesso in cima da 1,10 a ~1,50 kg**. L'autonomia e la
stabilità tirano nella stessa direzione: è l'unico punto di questa nota in cui
due vincoli non sono in conflitto.

### 7.5 Consumo — numero calcolato, non misurato

Lo dichiaro come **calcolato** e lo porto al chief-engineer come tale, non come
misura. La misura è di fase 7 e non è anticipabile.

| Voce | Transito | Stazionamento con esca attiva |
|---|---|---|
| Pi 5 + AI HAT+ | 12 W | 9 W |
| LIDAR C1 | 2 W | 2 W (o 0 se spento in stazionamento) |
| Motori (2×) | 15 W | 0 W |
| Ventola centrifuga | 0 W | 6 W |
| Resistenza esca 35 °C | 5 W | 6 W |
| ESP32, ToF, IMU, microfono | 2 W | 2 W |
| Perdite di conversione (10%) | 3,6 W | 2,5 W |
| **Totale** | **~40 W** | **~28 W** |

Profilo d'uso realistico (10% transito, 90% stazionamento): **~29 W medi**.

Con il pacco di §5.5 (128 Wh, 80% di DoD utile = 102 Wh): **~3,5 h**. Una notte
di 8 ore richiederebbe ~300 Wh installati, cioè ~3,0 kg e ~2,5 L: da qui il
vano P-03.

**Alternativa che elimina il problema, e che è mia da proporre.** Se il dock
alimenta il payload (D-12: ≥ 60 W), il robot **cattura mentre carica**, fermo
nella stanza dove sta il dock. La mobilità serve allora solo a cambiare stanza
quando le persone si spostano — che è esattamente D-03 — e non a garantire
l'autonomia notturna. Ciclo: 45 min fuori (22 Wh consumati) e 45 min in dock
(29 Wh reintegrati a 3 A): **il bilancio è positivo**, il pacco da 10 Ah basta,
si risparmiano ~1,7 kg e ~180 €, e la cattura non si ferma mai. Lo porto al
chief-engineer come voce di Decision Log, non lo decido io da solo perché tocca
il BOM.

---

## 8. Che cosa NON posso ancora determinare

Elenco esplicito, con la dipendenza. Nessuna di queste è risolta con
un'assunzione.

| # | Incognita | Da cosa dipende | Chi la sblocca |
|---|---|---|---|
| A-01 | **Autonomia reale in minuti** | consumo misurato di resistenza esca e ventola, che oggi non esiste; §7.5 è un calcolo | `payload-fluidics` + misura in fase 7 |
| A-02 | **Baricentro reale** | masse e posizioni reali, cablaggi compresi. Il CAD non basta (§2.8) | `mechatronics`, alla prima base montata |
| A-03 | **Se `d` = 110 mm è raggiungibile** | dalla scelta 1 pazza / 2 pazze, che non è mia | `mechatronics` |
| A-04 | **Se 3 ToF bastano** o servono 4 | dall'arredo reale dell'abitazione. Un appartamento senza tavoli bassi non ha il problema di §5.2 | rilievo dell'abitazione (§9) |
| A-05 | **Se il criterio 60 m² / 10 cm è raggiungibile** | dal numero di specchi e vetrate. Il LIDAR li attraversa o ci si specchia, e nessun sensore in BOM li risolve | rilievo dell'abitazione |
| A-06 | **Dove va il dock** e se le luci di D-09 sono disponibili | planimetria reale | rilievo + utente |
| A-07 | **Se la ventola in testa è compatibile con l'ascolto** | già questione aperta di §10 (autocontaminazione acustica). Se non lo è, la ventola scende nella base e il carico in cima cambia | `acoustic-perception` |
| A-08 | **Se i motoriduttori 30:1 in BOM vanno sostituiti** | dai datasheet, che `VA-03` registra come inesistenti (copertura 0/16). Il mio calcolo di §3.3 usa valori tipici di catalogo | `mechatronics` + `chief-engineer` |
| A-09 | **Soglia massima scavalcabile reale** | misura sul pavimento reale, non simulazione | fase 7 |
| A-10 | **Rumore emesso dalla trazione durante il transito** | interessa `acoustic-perception` se il transito avviene mentre qualcuno dorme | misura in fase 7 |

**Una simulazione non chiude nessuna di queste righe.** Gazebo mi serve a
debuggare la macchina a stati del docking e i recovery behavior; non certifica
un numero. Ogni valore di questa nota che verrà usato per accettare qualcosa
dovrà essere rimisurato sul pavimento reale.

---

## 9. Richieste che escono da questa nota

### 9.1 A `mechatronics`

1. Rispettare i vincoli della tabella §1, o **contestarli con un numero**.
2. Riscontro sulla configurazione 2 pazze + pattino (§2.3): se resta 1 pazza,
   accetto, ma la conseguenza `v_max` = 0,26 m/s va registrata.
3. Misurare e dichiarare: quota e complanarità del piano LIDAR, settore occluso,
   diametri ruota, carreggiata, baricentro, angolo di ribaltamento, frequenza
   propria del montante.
4. Livello motori micro-ROS: **quadratura decodificata ×4**, e un **ingresso di
   abilitazione hardware dei driver** cablato in serie ai microswitch dei
   paraurti e comandabile per il silenzio acustico (A-01 di §5.6).
5. Interlock del dock (D-05) e blocco unidirezionale lato robot (D-06).

### 9.2 A `chief-engineer` — voci per il Decision Log §3

Non le scrivo io in `PROJECT.md`. Le propongo con la motivazione e con ciò che
ho scartato:

| Proposta | Motivazione sintetica | Scartato |
|---|---|---|
| **Base a 2 motrici + 2 pazze posteriori + pattino anti-ribaltamento anteriore** | su un triangolo d'appoggio il braccio di stabilità peggiore è 76 mm, non 150: raddoppia con il quarto punto e la velocità utile passa da 0,26 a 0,39 m/s | 1 sola pazza (accettabile ma costa un terzo del tempo di rientro); base a 4 motrici (costo, complessità, slittamento) |
| **Angolo di ribaltamento di accettazione 22°, non 30°** | 30° è irraggiungibile con un montante da 1,2 m su 300 mm di carreggiata; 22° è il valore che tiene un margine di energia 3,4× alla velocità di transito | 30° «da manuale», che sarebbe stato violato in silenzio |
| **`v_max` = 0,35 m/s legata al baricentro dalla formula di §2.7** | il robot non insegue (D-03): la velocità non ha valore funzionale, e barattarla contro il margine di ribaltamento è sempre conveniente | velocità fissa indipendente dalla geometria |
| **IMU senza magnetometro, imbardata fusa con odometria** | 2 motori, ventola e pacco batteria in 340 mm rendono il campo magnetico inutilizzabile: 6° di errore a 150 mm da un conduttore a 2 A | calibrazione hard/soft iron (invalidata da qualunque arredo ferromagnetico) |
| **Motoriduttori con coppia di stallo ≥ 2,0 N·m per ruota** | il 30:1 di §5.4 dà 33 N contro i 51 N richiesti per una soglia da 15 mm: non scavalca | il 30:1 in BOM |
| **Quarto VL53L5CX in cima al montante (+15 €)** | fra 400 e 1150 mm non guarda nessun sensore, e il montante colpisce i piani dei tavoli: è FM-B9 per una via non censita | sole zone di esclusione software (protezione che vive in un file di configurazione: `SAFETY.md` §7 la rifiuta) |
| **Payload di testa in dock alimentato dal dock, ciclo 45/45 min** | elimina il dimensionamento della batteria per la notte intera, risparmia ~1,7 kg e ~180 €, e la cattura non si ferma | pacco da 300 Wh (3 kg, +180 €) |

### 9.3 A `chief-engineer` — voci per §10

1. **Rilievo dell'abitazione — bloccante per la fase 7, utile già in fase 1.**
   È il gemello del rilievo del balcone già aperto in §10. Serve: luce netta di
   ogni porta, altezza delle soglie, tipo di pavimento stanza per stanza,
   presenza e posizione di scale e dislivelli, specchi e vetrate a tutta altezza,
   arredi con luce inferiore fra 150 e 1200 mm, e almeno due posizioni candidate
   per il dock con le luci di D-09. Senza questo rilievo i criteri «60 m² con
   chiusura ≤ 10 cm» e «0 cadute in 2 h» non sono nemmeno pianificabili.
2. **Autonomia target dell'Unità B** (già aperta): la porto avanti con il
   calcolo di §7.5 — ~29 W medi, ~3,5 h con il pacco attuale — e con la proposta
   del ciclo 45/45 che la renderebbe irrilevante. **Il numero misurato arriva in
   fase 7.**
3. **Copertura del rischio residuo di ribaltamento per spinta esterna**
   (§2.6): 8 N a 1,15 m è la soglia migliore raggiungibile. Va accettato per
   iscritto o va rinunciato al montante da 120 cm. Non esiste una terza via.

### 9.4 A `compliance-safety`

- §6.4 propone la chiusura di **`VA-21`** (interlock del dock) e aggiunge un
  modo di guasto **non presente** in §7.2: **i pin del robot sono in tensione
  quando il robot è fuori dal dock** — cortocircuito diretto del pacco 4S 10 Ah
  su un oggetto metallico. Chiedo che venga censito.
- §2.6 propone il completamento di **`VA-24`**: l'angolo da solo non basta;
  la protezione è angolo ≥ 22° **più** cutoff inerziale a 20° **più**
  limitazione della massa in quota a 1,10 kg.
- §5.3 propone la copertura di **`VA-25`** (anticaduta): non solo sensoristica —
  paraurti hardware in serie all'abilitazione dei driver e limitazione di
  velocità a 0,15 m/s in prossimità di dislivelli mappati. Resta un rischio
  accettato la prima scoperta di una scala non mappata, che dipende dai soli ToF.

### 9.5 A `payload-fluidics`

- **1,10 kg** a 1150 mm è tutto il budget di massa in testa (§7.1). Con la
  ventola isolata su gommini.
- Cartuccia CO₂ e riduttore **nella base**, tubo da 4 mm in quota (§7.1).
- La posa di stazionamento e i segnali di inizio/fine sessione li specifico in
  un documento separato in fase 7; qui conta solo che il robot **fermo** significa
  driver disabilitati (§5.6) e montante che non oscilla (§7.3, M-04).

---

## 10. Nota di privacy, che vale da subito

Le mappe `slam_toolbox` prodotte in fase 7 **sono la planimetria
dell'abitazione**. Non entrano nel repository, non entrano in un allegato di
issue, non entrano in uno screenshot di documentazione. `SAFETY.md` §6.3 rileva
che il `.gitignore` attuale **non le blocca** (voce `VA-19`): finché quella
patch non è applicata, la rete non c'è e il controllo è manuale — `git status`
prima di ogni `git add`, mai `git add .`. La history di Git non si cancella
davvero.

Lo stesso vale per il rilievo dell'abitazione richiesto in §9.3: **misure sì,
planimetria no**, e nessuna foto di interni nel repository.
