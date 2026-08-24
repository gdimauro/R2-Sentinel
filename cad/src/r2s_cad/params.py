"""R2-Sentinel — testa pan-tilt dell'Unita' A: UNICO punto dei parametri.

Questo modulo e' l'unico posto del CAD in cui compare un numero. I moduli
in `parts/` non contengono costanti geometriche: ricevono un `Params` e ne
leggono i campi. Se trovi un numero magico dentro `parts/`, e' un difetto.

Doppia variante (D-09, PROJECT.md §7.3)
--------------------------------------
Un solo sorgente genera la variante FDM e la variante SLS. Le UNICHE
differenze ammesse fra le due sono elencate in `VARIANT_DECLARED_FIELDS`.
`check_variants.py` verifica che a valle non ne compaiano altre: se una
geometria diverge per un motivo non dichiarato, il controllo fallisce.

Sistema di riferimento meccanico (consegna a `vision-perception`)
-----------------------------------------------------------------
Convenzione ROS REP-103, destrorsa.

  origine O = intersezione dell'asse pan con l'asse tilt
  +X = avanti,  con pan = 0 e tilt = 0
  +Y = a sinistra
  +Z = in alto, coincidente con l'asse pan
  asse tilt = retta per O parallela a Y

  pan  = imbardata attorno a +Z, positiva antioraria vista dall'alto
  tilt = ELEVAZIONE, positiva verso l'alto (tilt = -pitch REP-103)

L'origine e' un punto fisico solo se i due assi si intersecano davvero.
Vedi `axes_offset_max_mm`: e' un requisito di precisione, non un dettaglio.

Riferimenti al documento master: D-06 (precisione ~1°), D-09 (doppia
variante), D-18 e D-19 (arresti meccanici e art. 674 c.p.), D-20 (barriera
fisica anziche' software), §5.6 (meccanica commerciale), §7.2 e §7.3.
SAFETY.md §2.2 `VA-09` (raggio minimo di ingaggio hardware) e §2.3 `VA-08`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, fields, replace
from typing import Literal

Variant = Literal["fdm", "sls"]

# --------------------------------------------------------------------------
# Campi che POSSONO differire fra variante FDM e variante SLS.
# Ogni altra differenza fra i due export e' un difetto, non una scelta.
# (criterio di FATTO gate fase 1)
# --------------------------------------------------------------------------
VARIANT_DECLARED_FIELDS: tuple[str, ...] = (
    "variant",
    "clearance",
    "wall_min",
    "hole_comp",
    "fillet_min",
)


@dataclass(frozen=True)
class Params:
    """Tutti i parametri della testa pan-tilt. Congelato: usa `replace()`."""

    # ======================================================================
    # 1. VARIANTE DI PROCESSO  (PROJECT.md §7.3)
    # ======================================================================
    variant: Variant = "fdm"

    #: gioco di accoppiamento nominale sui giochi funzionali [mm]
    clearance: float = 0.20
    #: spessore minimo di parete ammesso dal processo [mm]
    wall_min: float = 1.2
    #: compensazione sul diametro dei fori passanti [mm sul diametro].
    #: FDM: il foro esce STRETTO per elephant-foot e sovraestrusione interna.
    #: SLS: il foro esce STRETTO perche' la polvere adiacente sinterizza.
    hole_comp: float = 0.20
    #: raggio minimo di raccordo applicabile senza rovinare la stampabilita'
    fillet_min: float = 0.8

    # ======================================================================
    # 2. CATENA CINEMATICA  (D-06 — stepper + cinghia GT2, NON servo)
    # ======================================================================
    #: passo della cinghia [mm]. GT2 = 2 mm.
    belt_pitch: float = 2.0
    #: larghezza cinghia [mm]
    belt_width: float = 6.0
    #: denti puleggia motrice (calettata sul NEMA 17)
    pulley_drive_teeth: int = 16
    #: denti puleggia condotta (calettata sull'albero di uscita)
    pulley_driven_teeth: int = 80
    #: larghezza mozzo + flange della puleggia condotta [mm]
    pulley_driven_width: float = 16.0
    #: foro della puleggia condotta [mm] — deve valere `shaft_d`
    pulley_driven_bore: float = 8.0

    #: passo angolare intero del motore [°/step]
    motor_step_deg: float = 1.8
    #: microstepping del driver (TMC2209/TMC5160)
    microsteps: int = 16
    #: errore di posizionamento del passo-passo in microstepping, riferito
    #: all'ALBERO MOTORE, come frazione di passo intero. Valore tipico di
    #: catalogo per motore caricato: NON e' una misura. Va riconfermato in
    #: fase 2 e finche' non lo e' resta una stima dichiarata (§10).
    motor_ustep_accuracy_fullstep: float = 0.10

    # ======================================================================
    # 3. MECCANICA COMMERCIALE  (§5.6 — NON stampare)
    # ======================================================================
    #: albero rettificato Ø8 h6 (acciaio inox o cromato), commerciale
    shaft_d: float = 8.0
    #: cuscinetto 608ZZ: 8 x 22 x 7
    bearing_id: float = 8.0
    bearing_od: float = 22.0
    bearing_w: float = 7.0
    #: interasse fra i due cuscinetti dello stesso asse [mm].
    #: Governa la rigidezza in momento: raddoppiarlo dimezza la reazione.
    pan_bearing_span: float = 45.0
    tilt_bearing_span: float = 96.0

    #: NEMA 17 — flangia 42,3 mm, interasse fori 31 mm, pilota Ø22
    nema_flange: float = 42.3
    nema_bolt_pitch: float = 31.0
    nema_pilot_d: float = 22.0
    nema_shaft_d: float = 5.0
    nema_bolt_d: float = 3.0
    #: lunghezza corpo motore [mm] — 17HS4401 (40 mm) come riferimento
    nema_body_len: float = 40.0

    # viteria: inox A2, inserti filettati a caldo M3 (§4.2, §5.6)
    m3_insert_d: float = 4.6      # inserto a caldo M3 standard, Ø esterno
    m3_insert_len: float = 5.8
    m3_clear_d: float = 3.4
    m4_clear_d: float = 4.5
    m5_clear_d: float = 5.5
    m6_clear_d: float = 6.6

    # ======================================================================
    # 4. ARRESTI MECCANICI DI SETTORE  (D-19 + art. 674 c.p. — D-18)
    # ======================================================================
    # Regolabili in installazione: il settore ammesso dipende dal balcone
    # reale, non ancora rilevato (§10). La GEOMETRIA e' congelabile, la
    # REGOLAZIONE no. Grossolana a fori indicizzati (chiusura di FORMA) +
    # fine a vite di battuta. Nessun serraggio ad attrito: l'ASA a 50 °C
    # al sole rilassa il precarico e un morsetto ad attrito scorre.
    # ----------------------------------------------------------------------
    #: raggio della circonferenza dei fori indicizzati, asse pan [mm]
    pan_stop_bolt_circle_r: float = 58.0
    #: raggio della circonferenza dei fori indicizzati, asse tilt [mm]
    tilt_stop_bolt_circle_r: float = 34.0
    #: passo angolare della regolazione grossolana [°]
    stop_coarse_step_deg: float = 12.0
    #: corsa utile della vite di battuta M6 [mm] -> regolazione fine
    stop_screw_travel: float = 14.0
    #: margine richiesto: la corsa fine deve coprire il passo grossolano
    stop_fine_coverage_min: float = 1.15
    #: raggio della faccia di battuta del nottolino [mm]
    pan_stop_dog_r: float = 55.0
    tilt_stop_dog_r: float = 31.0
    #: sezione del nottolino [mm] — larghezza x altezza
    stop_dog_w: float = 10.0
    stop_dog_h: float = 12.0
    #: sbalzo del nottolino oltre la sua radice [mm]
    stop_dog_reach: float = 12.0

    # INVILUPPO MECCANICO — l'estensione entro cui gli arresti sono
    # regolabili. Fuori da qui non si va nemmeno smontando gli arresti.
    pan_envelope_deg: float = 120.0          # ±, limite = ansa di servizio cavi
    tilt_envelope_up_deg: float = 70.0
    tilt_envelope_down_deg: float = -45.0    # vedi `min_engagement_range_m`

    #: settore di TARATURA di primo impianto [°]. Provvisorio: da rifare
    #: sul balcone reale prima dell'abilitazione del getto (§10, D-19).
    pan_sector_cw_deg: float = -60.0
    pan_sector_ccw_deg: float = 60.0
    tilt_sector_down_deg: float = -20.0
    tilt_sector_up_deg: float = 55.0

    # ======================================================================
    # 5. VINCOLI DI SICUREZZA CHE DIVENTANO GEOMETRIA
    # ======================================================================
    #: quota dell'origine O da terra, in installazione [mm]. IPOTESI: il
    #: valore vero esce dal rilievo del balcone (§10).
    mount_height_mm: float = 1200.0
    #: SAFETY.md §2.2 `VA-09`: raggio minimo di ingaggio, imposto HARDWARE.
    #: L'arresto di tilt inferiore non deve permettere che il getto
    #: intercetti il piano di calpestio a meno di questa distanza.
    min_engagement_range_m: float = 1.0
    #: distanza di progetto del bersaglio [m] — su cui si converte ° <-> mm
    design_range_m: float = 5.0
    #: budget di errore di puntamento RMS [°] (D-06, criterio di FATTO)
    pointing_rms_budget_deg: float = 1.0
    #: budget di gioco totale riferito all'uscita [°] (criterio di FATTO)
    backlash_budget_deg: float = 0.3
    #: scostamento massimo ammesso fra asse pan e asse tilt [mm].
    #: Se gli assi non si intersecano, l'offset `e` produce un errore di
    #: puntamento e/(range) che NON e' calibrabile via angoli soli.
    axes_offset_max_mm: float = 10.0
    #: margine angolare fra finecorsa (sensore) e arresto (legge fisica) [°]
    endstop_margin_deg: float = 2.0

    # ======================================================================
    # 6. VANO BATTERIA  (Unita' A autonoma — decisione sponsor 2026-08-24)
    # ======================================================================
    # NON e' un dimensionamento: e' un VOLUME RISERVATO. La capacita' del
    # pacco e la strategia di ricarica sono A-20, aperta. Il vano sta nella
    # BASE FISSA: massa ferma, non caricata sugli assi, baricentro basso.
    # Chimica LiFePO4 obbligatoria (D-07), BMS obbligatorio, e nessuna
    # carica sopra ~45 °C -> il vano e' un problema termico, non un buco.
    # ----------------------------------------------------------------------
    batt_bay_l: float = 190.0
    batt_bay_w: float = 120.0
    batt_bay_h: float = 80.0
    #: massa massima del pacco che il vano e i fissaggi devono reggere [kg]
    batt_bay_mass_max_kg: float = 3.0
    #: intercapedine ventilata dello schermo solare [mm] (camino passivo)
    shroud_gap: float = 12.0
    #: larghezza delle feritoie del camino [mm] — sotto i 4 mm servono a
    #: poco, sopra i 6 entrano insetti e pioggia battente
    vent_slot_w: float = 4.0
    #: altezza del labirinto antipioggia sulle feritoie [mm]
    vent_baffle_h: float = 10.0
    #: predisposizione ventola 40x40x10 sul vano (estrazione forzata)
    batt_fan_size: float = 40.0
    #: paratia di separazione batteria <-> compressore/elettronica di potenza
    batt_bulkhead_t: float = 3.0

    # ======================================================================
    # 7. PAYLOAD OTTICO E FLUIDICO — volumi RISERVATI
    # ======================================================================
    # Le quote vere arrivano da `vision-perception` (asse ottico, tolleranze
    # <0,1 mm, campo libero) e da `payload-fluidics` (ugello, elettrovalvola,
    # reazione del getto). Finche' non arrivano, questi sono INVOLUCRI, non
    # interfacce congelate. Il flag `TO_CONFIRM` sotto li marca.
    # ----------------------------------------------------------------------
    optics_plate_l: float = 110.0
    optics_plate_w: float = 90.0
    optics_plate_t: float = 6.0
    #: griglia di fori per inserti M3 sulla piastra ottica [mm]
    optics_grid_pitch: float = 10.0
    #: foratura Pi Camera Module 3 / GS: TO_CONFIRM con vision-perception
    picam_hole_dx: float = 21.0
    picam_hole_dy: float = 12.5
    picam_hole_d: float = 2.4
    #: involucro riservato al corpo ottico C-mount 16 mm [mm]
    cmount_env_d: float = 34.0
    cmount_env_len: float = 60.0
    #: involucro riservato all'elettrovalvola 12 V sul gruppo tilt [mm]
    valve_env_l: float = 60.0
    valve_env_w: float = 32.0
    valve_env_h: float = 45.0
    #: diametro esterno del tubo pneumatico che sale alla testa [mm]
    air_tube_od: float = 8.0
    #: forza di reazione del getto sul gruppo tilt [N]. IPOTESI DICHIARATA:
    #: `payload-fluidics` non ha ancora consegnato il carico. Il valore
    #: influenza le sezioni, non l'architettura: sotto ~10 N il progetto
    #: non cambia. Sopra, va rivisto `shaft_d`. Vedi §10.
    jet_reaction_n: float = 5.0
    #: braccio della reazione rispetto all'asse tilt [mm]
    jet_reaction_arm: float = 70.0

    # ======================================================================
    # 8. TENUTA E CARTER
    # ======================================================================
    #: sezione del cordone O-ring / guarnizione TPU stampata [mm]
    seal_cord_d: float = 3.0
    #: profondita' della gola di tenuta [mm] (schiacciamento ~25%)
    seal_groove_depth: float = 2.2
    #: larghezza della gola [mm]
    seal_groove_w: float = 3.6
    #: gioco radiale del labirinto a gronda sul giunto pan [mm]
    labyrinth_gap: float = 1.5
    #: numero di pieghe del labirinto
    labyrinth_folds: int = 3
    #: foro per pressacavo IP68 M12 [mm]
    gland_hole_d: float = 12.5

    # ======================================================================
    # 9. STRUTTURA
    # ======================================================================
    #: spessore parete strutturale nominale [mm] (>= wall_min per costruzione)
    wall: float = 3.0
    #: spessore delle nervature [mm]
    rib_t: float = 2.4
    #: spessore del collare di serraggio della sede cuscinetto [mm]
    clamp_wall: float = 4.0
    #: larghezza del taglio del collare [mm] — dipende dalla variante
    clamp_slot_w: float = 1.6
    #: corsa delle asole di tensionamento cinghia [mm]
    tensioner_travel: float = 8.0
    #: piede di fissaggio della base
    foot_hole_d: float = 6.6
    base_l: float = 210.0
    base_w: float = 150.0

    # ======================================================================
    # 10. MATERIALI (densita' per il calcolo massa dal modello)
    # ======================================================================
    #: densita' ASA [g/cm3] — esterno, resistente a UV
    rho_asa: float = 1.07
    #: densita' PA12 SLS [g/cm3]
    rho_pa12: float = 1.01
    #: riempimento tipico FDM per pezzi strutturali (frazione)
    fdm_infill: float = 0.40

    # ------------------------------------------------------------------
    # grandezze derivate — nessun numero, solo relazioni
    # ------------------------------------------------------------------
    @property
    def ratio(self) -> float:
        """Rapporto di riduzione della catena a cinghia."""
        return self.pulley_driven_teeth / self.pulley_drive_teeth

    @property
    def pulley_drive_pd(self) -> float:
        """Diametro primitivo puleggia motrice [mm]."""
        return self.pulley_drive_teeth * self.belt_pitch / math.pi

    @property
    def pulley_driven_pd(self) -> float:
        """Diametro primitivo puleggia condotta [mm]."""
        return self.pulley_driven_teeth * self.belt_pitch / math.pi

    @property
    def centre_distance(self) -> float:
        """Interasse nominale motore <-> albero di uscita [mm].

        Scelto per lasciare gioco fra flangia motore e puleggia condotta,
        piu' la corsa del tenditore. Non e' un numero libero: e' il minimo
        geometricamente montabile piu' meta' corsa del tenditore.
        """
        min_cd = self.pulley_driven_pd / 2 + self.nema_flange / 2 + 4.0
        return min_cd + self.tensioner_travel / 2

    @property
    def deg_per_ustep(self) -> float:
        """Risoluzione angolare all'uscita [°/microstep]."""
        return self.motor_step_deg / self.microsteps / self.ratio

    @property
    def ustep_accuracy_out_deg(self) -> float:
        """Errore di microstepping riportato all'uscita [°].

        E' la ragione vera della riduzione 5:1 (D-06): non la coppia, ma la
        divisione per `ratio` dell'errore intrinseco del passo-passo.
        """
        return self.motor_step_deg * self.motor_ustep_accuracy_fullstep / self.ratio

    @property
    def belt_slack_budget_mm(self) -> float:
        """Gioco totale ammesso della cinghia [mm].

        Il budget di backlash all'uscita, riportato ad arco sul raggio
        primitivo della puleggia condotta. E' IL numero che il tenditore
        deve garantire, ed e' misurabile con un comparatore.
        """
        return math.radians(self.backlash_budget_deg) * self.pulley_driven_pd / 2

    @property
    def mm_per_deg_at_range(self) -> float:
        """Scostamento lineare alla distanza di progetto [mm/°]."""
        return math.radians(1.0) * self.design_range_m * 1000.0

    @property
    def axes_offset_error_deg(self) -> float:
        """Errore di puntamento dovuto al massimo scostamento fra assi [°]."""
        return math.degrees(self.axes_offset_max_mm / (self.design_range_m * 1000.0))

    @property
    def tilt_down_limit_from_safety_deg(self) -> float:
        """Arresto di tilt inferiore imposto da `VA-09` [°].

        E' l'angolo sotto il quale il getto intercetterebbe il piano di
        calpestio a meno del raggio minimo di ingaggio. Discende dalla
        quota di installazione: non e' un numero scelto.
        """
        return -math.degrees(
            math.atan2(self.mount_height_mm / 1000.0, self.min_engagement_range_m)
        )

    @property
    def stop_fine_range_pan_deg(self) -> float:
        """Escursione della regolazione fine a vite, asse pan [°]."""
        return math.degrees(self.stop_screw_travel / self.pan_stop_bolt_circle_r)

    @property
    def stop_fine_range_tilt_deg(self) -> float:
        """Escursione della regolazione fine a vite, asse tilt [°]."""
        return math.degrees(self.stop_screw_travel / self.tilt_stop_bolt_circle_r)

    @property
    def stop_dog_force_n(self) -> float:
        """Forza sull'arresto se il motore spinge a coppia di tenuta piena.

        Ipotesi: coppia di tenuta NEMA 17 = 0,40 N·m (valore tipico di
        catalogo del 17HS4401, DA RICONFERMARE sul datasheet ordinato —
        stessa lezione di D-24).
        """
        holding_nm = 0.40
        return holding_nm * self.ratio / (self.pan_stop_dog_r / 1000.0)

    @property
    def bearing_seat_d(self) -> float:
        """Diametro della sede del cuscinetto [mm].

        Il collare di serraggio recupera la tolleranza di processo: la
        sede si stampa larga di `clearance` e la vite la chiude. E' cio'
        che rende il corpo testa candidabile all'FDM (vedi README).
        """
        return self.bearing_od + self.clearance

    @property
    def shaft_hole_d(self) -> float:
        """Foro di passaggio libero per l'albero Ø8 [mm]."""
        return self.shaft_d + 2 * self.clearance

    def hole(self, nominal: float) -> float:
        """Diametro da modellare per ottenere `nominal` dopo il processo."""
        return nominal + self.hole_comp

    @property
    def density(self) -> float:
        """Densita' effettiva del pezzo nella variante corrente [g/cm3]."""
        if self.variant == "sls":
            return self.rho_pa12
        return self.rho_asa * self.fdm_infill + self.rho_asa * (1 - self.fdm_infill) * 0.0 \
            if False else self.rho_asa * self.fdm_infill

    def declared_diff(self, other: "Params") -> dict[str, tuple]:
        """Differenze fra due `Params`, per il controllo di doppia variante."""
        out: dict[str, tuple] = {}
        for f in fields(self):
            a, b = getattr(self, f.name), getattr(other, f.name)
            if a != b:
                out[f.name] = (a, b)
        return out


# --------------------------------------------------------------------------
# Le due varianti. UNICO punto in cui `clearance` e `wall_min` sono scritti.
# PROJECT.md §7.3 ne dichiara due; `hole_comp` e `fillet_min` sono la terza
# e la quarta differenza necessaria e vanno registrate nel Decision Log.
# --------------------------------------------------------------------------
_VARIANT_TABLE: dict[str, dict[str, float | str]] = {
    "fdm": dict(variant="fdm", clearance=0.20, wall_min=1.2, hole_comp=0.20, fillet_min=0.8),
    "sls": dict(variant="sls", clearance=0.35, wall_min=0.8, hole_comp=0.30, fillet_min=0.4),
}


def make_params(variant: Variant = "fdm", **overrides) -> Params:
    """Costruisce i parametri per la variante richiesta.

    `overrides` serve alle prove di sensibilita' (per esempio spostare il
    settore degli arresti dopo il rilievo del balcone) senza toccare il
    sorgente. Non serve a creare una terza variante di processo.
    """
    if variant not in _VARIANT_TABLE:
        raise ValueError(f"variante sconosciuta: {variant!r}")
    p = Params(**_VARIANT_TABLE[variant])  # type: ignore[arg-type]
    if overrides:
        p = replace(p, **overrides)
    validate(p)
    return p


# --------------------------------------------------------------------------
# Validazione: i vincoli che non devono poter essere violati modificando
# un numero. Un parametro sbagliato deve far fallire la generazione, non
# produrre un pezzo silenziosamente fuori specifica.
# --------------------------------------------------------------------------
class ParamError(ValueError):
    """Un parametro viola un vincolo di progetto."""


def validate(p: Params) -> None:
    err: list[str] = []

    # --- processo ---------------------------------------------------------
    if p.wall < p.wall_min:
        err.append(f"wall {p.wall} < wall_min {p.wall_min} della variante {p.variant}")
    if p.rib_t < p.wall_min:
        err.append(f"rib_t {p.rib_t} < wall_min {p.wall_min}")
    if p.clamp_slot_w <= 2 * p.clearance:
        err.append("clamp_slot_w deve superare due volte clearance, altrimenti il collare non chiude")

    # --- catena cinematica (D-06) -----------------------------------------
    if p.ratio < 4.0:
        err.append(f"rapporto {p.ratio:.2f} < 4: D-06 prescrive una riduzione, non un accoppiamento diretto")
    if p.pulley_driven_bore != p.shaft_d:
        err.append("il foro della puleggia condotta deve valere shaft_d: la puleggia va sull'albero rettificato")
    # la risoluzione non deve essere il termine dominante dell'errore
    if p.deg_per_ustep > p.pointing_rms_budget_deg / 10:
        err.append(
            f"risoluzione {p.deg_per_ustep:.4f}°/µstep troppo grossolana rispetto al budget "
            f"{p.pointing_rms_budget_deg}° (serve >= 10x di margine)"
        )
    if p.ustep_accuracy_out_deg > p.pointing_rms_budget_deg / 4:
        err.append(
            f"errore di microstepping all'uscita {p.ustep_accuracy_out_deg:.3f}° oltre 1/4 del budget"
        )
    if p.axes_offset_error_deg > p.pointing_rms_budget_deg / 5:
        err.append(
            f"scostamento assi {p.axes_offset_max_mm} mm -> {p.axes_offset_error_deg:.3f}° "
            f"a {p.design_range_m} m: oltre 1/5 del budget"
        )

    # --- arresti meccanici (D-19 / art. 674 c.p.) -------------------------
    # la regolazione fine deve COPRIRE il passo grossolano, altrimenti
    # esistono settori non impostabili: buchi in una protezione legale.
    for nome, fine in (("pan", p.stop_fine_range_pan_deg), ("tilt", p.stop_fine_range_tilt_deg)):
        if fine < p.stop_coarse_step_deg * p.stop_fine_coverage_min:
            err.append(
                f"arresti {nome}: regolazione fine {fine:.1f}° non copre il passo grossolano "
                f"{p.stop_coarse_step_deg}° con margine {p.stop_fine_coverage_min}x — "
                f"esisterebbero settori non impostabili"
            )
    if p.pan_sector_ccw_deg > p.pan_envelope_deg or p.pan_sector_cw_deg < -p.pan_envelope_deg:
        err.append("il settore di taratura pan esce dall'inviluppo meccanico")
    if p.tilt_sector_up_deg > p.tilt_envelope_up_deg or p.tilt_sector_down_deg < p.tilt_envelope_down_deg:
        err.append("il settore di taratura tilt esce dall'inviluppo meccanico")
    if p.endstop_margin_deg <= p.deg_per_ustep * 4:
        err.append("margine finecorsa-arresto troppo stretto rispetto alla risoluzione")

    # --- SAFETY.md §2.2 VA-09: raggio minimo di ingaggio HARDWARE ---------
    # L'inviluppo di tilt verso il basso non deve poter puntare il piano di
    # calpestio a meno di `min_engagement_range_m`. E' un vincolo di
    # sicurezza reso geometria: nessun software puo' violarlo.
    limite = p.tilt_down_limit_from_safety_deg
    if p.tilt_envelope_down_deg < limite:
        err.append(
            f"VA-09 violato: inviluppo tilt {p.tilt_envelope_down_deg}° oltre il limite "
            f"{limite:.1f}° imposto dal raggio minimo di ingaggio "
            f"{p.min_engagement_range_m} m a quota {p.mount_height_mm/1000:.2f} m"
        )

    # --- vano batteria ----------------------------------------------------
    if p.batt_bay_l > p.base_l - 2 * p.wall or p.batt_bay_w > p.base_w - 2 * p.wall:
        err.append("il vano batteria non entra nella base: rivedere base_l/base_w")
    if p.shroud_gap < 8.0:
        err.append("intercapedine < 8 mm: il camino non tira, lo schermo solare non funziona")

    # --- tenuta -----------------------------------------------------------
    if p.seal_groove_depth >= p.seal_cord_d:
        err.append("gola piu' profonda del cordone: la guarnizione non schiaccia e non tiene")
    if p.seal_groove_w <= p.seal_cord_d:
        err.append("gola piu' stretta del cordone: il cordone non ha dove espandersi")

    if err:
        raise ParamError("parametri non validi:\n  - " + "\n  - ".join(err))


def budget_table(p: Params) -> list[tuple[str, str, str]]:
    """Ripartizione del budget di errore di D-06, ricavata dai parametri.

    Non e' una simulazione e non sostituisce la misura di fase 2: e' la
    contabilita' di cosa il CAD puo' garantire e cosa resta da misurare.
    """
    return [
        ("risoluzione microstep all'uscita", f"{p.deg_per_ustep:.4f}°",
         "garantito dal rapporto e dal driver"),
        ("accuratezza microstep all'uscita", f"±{p.ustep_accuracy_out_deg:.3f}°",
         "stima di catalogo, DA MISURARE (§10)"),
        ("gioco cinghia (budget)", f"{p.backlash_budget_deg:.2f}°",
         f"= {p.belt_slack_budget_mm:.3f} mm di gioco cinghia, DA MISURARE"),
        ("scostamento assi pan/tilt", f"{p.axes_offset_error_deg:.3f}°",
         f"garantito se offset <= {p.axes_offset_max_mm} mm"),
        ("ripetibilita' finecorsa", "DA MISURARE",
         "criterio: arresto entro 1 step su 20 attivazioni"),
        ("deriva termica ASA a 50 °C", "DA MISURARE",
         "criterio: <= 0,5° dopo 2 h"),
        ("cedevolezza sotto reazione getto", "DA MISURARE",
         f"carico ipotizzato {p.jet_reaction_n} N a {p.jet_reaction_arm} mm — dato atteso da payload-fluidics"),
    ]
