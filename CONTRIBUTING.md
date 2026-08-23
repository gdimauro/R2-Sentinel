# Contribuire

## Prima di tutto

Leggi [SAFETY.md](SAFETY.md). Definisce vincoli non negoziabili di questo
progetto. Contributi che li violano non verranno accettati, per quanto ben
scritti.

## Decision Log

`docs/PROJECT.md` §3 contiene il Decision Log. Ogni scelta tecnica va
registrata lì **con la motivazione**, non solo con l'esito.

Formato: `| D-NN | Decisione | Perché, e cosa è stato scartato | Data |`

Una PR che cambia un'architettura senza aggiornare il Decision Log è
incompleta. Il valore di questo repository è nel "perché", non nel "cosa".

## CAD

- I sorgenti sono **CadQuery parametrici** in `cad/src/`. Sono testo, quindi
  diffabili e revisionabili in PR. Modifica quelli, non gli export.
- Gli export in `cad/export/` sono generati, tracciati con Git LFS.
- Ogni pezzo espone i parametri `clearance` e spessore parete per generare sia
  la variante FDM sia quella SLS (vedi PROJECT.md §7.3).

## Privacy

Non committare mai mappe SLAM, riprese di interni, o file di configurazione con
credenziali. Il `.gitignore` li blocca, ma **verifica il diff prima di ogni
commit**: da Git la history non si cancella davvero.

Se ti accorgi di aver committato materiale privato, non limitarti a
rimuoverlo con un commit successivo: apri una issue e valutiamo un rewrite
della history.

## Issue

Usa i template. Per problemi di sicurezza, label `safety`, o contatto privato
se la divulgazione pubblica può creare rischio.
