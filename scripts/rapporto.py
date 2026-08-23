#!/usr/bin/env python3
"""Rapporto giornaliero R2-Sentinel — genera e invia via Mail.app."""
import io, os, re, subprocess, sys
from datetime import date, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = "giudimauro@gmail.com"
# Finestra stagionale zanzare: servono ~25 notti di calendario per 20 utili.
FINE_STAGIONE = date(2026, 9, 30)
NOTTI_NECESSARIE = 25

def sh(*a):
    try:
        return subprocess.run(a, cwd=ROOT, capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        return ""

def azioni():
    p = os.path.join(ROOT, "docs", "AZIONI-SPONSOR.md")
    if not os.path.exists(p): return []
    out = []
    for ln in io.open(p, encoding="utf-8"):
        ln = ln.strip()
        if not re.match(r"^A-\d+\|", ln): continue
        f = ln.split("|")
        if len(f) < 6: continue
        out.append(dict(id=f[0], azione=f[1], blocca=f[2], scadenza=f[3],
                        conseguenza=f[4], stato=f[5]))
    return out

def giorni_a(s):
    try: return (datetime.strptime(s, "%Y-%m-%d").date() - date.today()).days
    except Exception: return None

def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def costruisci():
    oggi = date.today()
    ap = [a for a in azioni() if a["stato"] == "aperta"]
    urgenti = sorted([a for a in ap if a["scadenza"] != "-"], key=lambda a: a["scadenza"])
    altre = [a for a in ap if a["scadenza"] == "-"]

    # finestra stagionale
    residui = (FINE_STAGIONE - oggi).days
    margine = residui - NOTTI_NECESSARIE
    if margine > 0:
        stagione = (f"<b>{margine} giorni</b> di margine prima che diventi impossibile. "
                    f"Servono ~{NOTTI_NECESSARIE} notti di calendario per {20} utili, "
                    f"e la stagione chiude il {FINE_STAGIONE.strftime('%d/%m')}: "
                    f"l'ultimo giorno utile per <b>iniziare</b> è il "
                    f"<b>{(FINE_STAGIONE.toordinal()-NOTTI_NECESSARIE) and datetime.fromordinal(FINE_STAGIONE.toordinal()-NOTTI_NECESSARIE).strftime('%d/%m/%Y')}</b>.")
        col = "#B4302B" if margine < 14 else "#B8631A"
    else:
        stagione = ("<b>Finestra chiusa.</b> Non è più possibile raccogliere 20 notti "
                    "utili entro la stagione: la fase 5 slitta all'anno prossimo.")
        col = "#B4302B"

    commit = sh("git", "log", "--oneline", "--since=midnight") or "(nessun commit oggi)"
    branch = sh("git", "branch", "--show-current")
    ncommit = len([l for l in commit.split("\n") if l.strip() and not l.startswith("(")])

    h = []
    h.append(f"""<div style="font-family:-apple-system,Segoe UI,sans-serif;max-width:680px;color:#151C25;line-height:1.55">
<div style="border-left:3px solid #B8631A;padding-left:14px;margin-bottom:22px">
<div style="font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#78879A">Rapporto giornaliero</div>
<h1 style="margin:4px 0 2px;font-size:26px">R2-Sentinel</h1>
<div style="color:#4A5765;font-size:13px">{oggi.strftime('%d %B %Y')} · branch <code>{esc(branch)}</code> · {ncommit} commit oggi</div>
</div>""")

    h.append(f"""<div style="background:#F8E3E1;border:1px solid {col};border-radius:3px;padding:14px 16px;margin-bottom:22px">
<div style="font-weight:600;color:{col};margin-bottom:5px">⏳ Finestra stagionale zanzare</div>
<div style="font-size:14px">{stagione}</div></div>""")

    h.append("<h2 style='font-size:16px;margin:26px 0 10px;text-transform:uppercase;letter-spacing:.04em'>Cosa devi fare tu</h2>")
    h.append("<div style='font-size:13px;color:#4A5765;margin-bottom:12px'>Sono le cose che nessun agente può fare al posto tuo. Ordinate per scadenza.</div>")

    if not ap:
        h.append("<p style='color:#1F7A50'>Nessuna azione aperta. </p>")

    for a in urgenti + altre:
        g = giorni_a(a["scadenza"]) if a["scadenza"] != "-" else None
        if g is not None:
            badge = (f"<span style='background:#B4302B;color:#fff;padding:2px 7px;border-radius:2px;"
                     f"font-size:11px;font-weight:600'>SCADE FRA {g} GIORNI</span>") if g >= 0 else \
                    "<span style='background:#B4302B;color:#fff;padding:2px 7px;border-radius:2px;font-size:11px;font-weight:600'>SCADUTA</span>"
        else:
            badge = "<span style='background:#EEF1F4;color:#4A5765;padding:2px 7px;border-radius:2px;font-size:11px'>senza scadenza</span>"
        h.append(f"""<div style="border:1px solid #D2DAE2;border-radius:3px;padding:13px 15px;margin-bottom:9px">
<div style="display:block;margin-bottom:6px"><code style="font-size:11px;color:#78879A">{a['id']}</code> {badge}</div>
<div style="font-weight:600;font-size:14px;margin-bottom:5px">{esc(a['azione'])}</div>
<div style="font-size:12.5px;color:#4A5765"><b>Blocca:</b> {esc(a['blocca'])}</div>
<div style="font-size:12.5px;color:#B4302B;margin-top:4px"><b>Se ritardi:</b> {esc(a['conseguenza'])}</div>
</div>""")

    h.append(f"""<h2 style='font-size:16px;margin:26px 0 10px;text-transform:uppercase;letter-spacing:.04em'>Lavoro di ieri</h2>
<pre style="background:#F3F6F8;border:1px solid #E2E8EE;border-radius:3px;padding:12px;font-size:12px;overflow-x:auto;white-space:pre-wrap">{esc(commit)}</pre>""")

    h.append("""<div style="margin-top:26px;padding-top:14px;border-top:1px solid #D2DAE2;font-size:12px;color:#78879A">
Sinottico locale: <a href="http://127.0.0.1:8787/plancia.html">127.0.0.1:8787/plancia.html</a> ·
Repository: <a href="https://github.com/gdimauro/R2-Sentinel">github.com/gdimauro/R2-Sentinel</a><br>
Tutti gli acquisti vanno fatti <b>con fattura</b>. Comunica gli estremi e li registro nel libro mastro.
</div></div>""")
    return "".join(h)

def invia_smtp(html, oggetto, allegati=None):
    """Invio diretto via SMTP. Non dipende da Mail.app, che può restare
    offline con i messaggi fermi in coda senza segnalare nulla.

    Credenziali da variabili d'ambiente (mai nel repository):
      R2S_SMTP_USER  = giudimauro@gmail.com
      R2S_SMTP_PASS  = password per app di Google (16 caratteri, non quella
                       dell'account: si genera da myaccount.google.com/apppasswords)
    """
    import smtplib, ssl
    from email.message import EmailMessage
    user = os.environ.get("R2S_SMTP_USER")
    pw = os.environ.get("R2S_SMTP_PASS")
    if not (user and pw):
        return False, "credenziali SMTP assenti (R2S_SMTP_USER / R2S_SMTP_PASS)"
    m = EmailMessage()
    m["Subject"] = oggetto
    m["From"] = user
    m["To"] = DEST
    m.set_content("Rapporto R2-Sentinel in formato HTML.")
    m.add_alternative(html, subtype="html")
    for a in (allegati or []):
        if not os.path.isfile(a):
            continue
        with open(a, "rb") as f:
            m.add_attachment(f.read(), maintype="text", subtype="html",
                             filename=os.path.basename(a))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465,
                              context=ssl.create_default_context(), timeout=30) as srv:
            srv.login(user, pw)
            srv.send_message(m)
        return True, "smtp"
    except Exception as exc:
        return False, "SMTP: " + repr(exc)[:200]


def invia_mailapp(html, oggetto):
    """Ripiego. ATTENZIONE: se Mail.app è offline il messaggio resta in coda
    senza errore — l'invio risulta riuscito ma la mail non parte."""
    import tempfile
    fd, path = tempfile.mkstemp(suffix=".html")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(html)
    scpt = """
    set htmlFile to POSIX file "%s"
    set htmlText to (read htmlFile as «class utf8»)
    tell application "Mail"
      set nm to make new outgoing message with properties {visible:false}
      set subject of nm to "%s"
      set html content of nm to htmlText
      tell nm to make new to recipient at end of to recipients with properties {address:"%s"}
      send nm
    end tell""" % (path, oggetto.replace('"', "'"), DEST)
    r = subprocess.run(["osascript", "-e", scpt], capture_output=True, text=True)
    try: os.unlink(path)
    except Exception: pass
    if r.returncode != 0:
        return False, (r.stderr or "").strip()
    # Verifica reale: se resta in coda, NON è partita.
    #
    # ATTENZIONE — questo controllo va fatto CON ATTESA. La prima versione
    # leggeva la coda subito dopo `send` e dichiarava fallimento per messaggi
    # che sarebbero partiti un istante dopo: lo stesso errore, rovesciato, del
    # valore di ritorno che dichiarava successo senza verificare l'effetto
    # (lezione L-03 del 2026-08-23). Uno stato transitorio non è un esito.
    import time as _t
    scadenza = _t.time() + 20
    n = 1
    while _t.time() < scadenza:
        q = subprocess.run(
            ["osascript", "-e",
             'tell application "Mail" to return count of (every message of outbox)'],
            capture_output=True, text=True)
        try:
            n = int((q.stdout or "0").strip())
        except ValueError:
            n = 0
        if n == 0:
            return True, "mail.app"
        _t.sleep(2)
    return False, (f"messaggio fermo in coda dopo 20 s: {n} in «In uscita». "
                   "Mail.app è offline — Casella > Attiva tutti gli account")


def invia(html, oggetto, allegati=None):
    ok, info = invia_smtp(html, oggetto, allegati)
    if ok:
        return True, info
    ok2, info2 = invia_mailapp(html, oggetto)
    return ok2, (info2 if ok2 else f"{info} | {info2}")

if __name__ == "__main__":
    html = costruisci()
    ogg = f"R2-Sentinel · rapporto del {date.today().strftime('%d/%m/%Y')}"
    if "--dry" in sys.argv:
        print(html[:1500]); sys.exit(0)
    ok, err = invia(html, ogg)
    print("inviata a " + DEST if ok else "ERRORE: " + err)
