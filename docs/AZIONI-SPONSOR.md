# Azioni che solo lo sponsor può fare

Fonte dati del rapporto giornaliero. **Formato rigido**: lo script
`scripts/rapporto.py` lo legge. Una riga per azione.

Colonne: `id | azione | blocca | scadenza | conseguenza-ritardo | stato`

- `scadenza`: `AAAA-MM-GG` oppure `-` se non scade
- `stato`: `aperta` | `fatta` | `annullata`

```csv
id|azione|blocca|scadenza|conseguenza|stato
A-01|Ordinare il microfono di misura USB (UMIK-1, SoundImports, fattura B2B con P.IVA)|Prima notte di registrazione, fase 5|2026-09-05|Ogni giorno perso è un giorno di finestra stagionale. Oltre la scadenza la fase 5 slitta di 12 mesi, non di settimane.|aperta
A-02|Installare git-lfs: brew install git-lfs && git lfs install|Primo export CAD committato, fase 1|-|Senza, il primo STEP finisce in Git normale e gonfia la history in modo non reversibile senza riscrittura.|aperta
A-03|Ordinare la Bambu P2S Combo + alimentatore AMS + ugello 0,6 + piatti|Fase 0 completa, quindi tutta la catena fisica|-|Ogni settimana di ritardo sposta di una settimana ogni fase fisica. Verificare i tempi di consegna prima di ordinare.|aperta
A-04|Ordinare i filamenti del set di partenza (PLA, PETG x2, ASA, TPU 95A)|Taratura profili, fase 0|-|Arrivare con la stampante e senza materiale significa perdere i giorni di taratura.|aperta
A-05|Attivare un account Amazon Business (fattura automatica)|Tutti gli acquisti su Amazon|-|Senza, ogni ordine richiede di rincorrere la fattura a mano.|aperta
A-06|Decidere: Unità A alimentata da rete o autonoma|Fase 1, CAD della testa|-|Cambia il volume del carter e il percorso cavi: deciderlo dopo il CAD significa rifare il CAD.|aperta
A-07|Decidere: da quale modulo CAD partire (raccomandato: testa pan-tilt)|Fase 1|-|Finché non è deciso, mechatronics non può iniziare.|aperta
A-08|Decidere: getto d'aria, nebulizzazione, o entrambi|Fase 4 e dimensionamento payload|-|Blocca payload-fluidics sul dimensionamento. L'istruttoria comparativa è in corso.|aperta
A-09|Indicare il comune dell'installazione|Chiusura del dossier normativo, gate fase 4|-|Il regolamento comunale può essere più restrittivo di quello nazionale: scoprirlo a Unità A installata significa smontarla.|aperta
A-10|Decidere l'autonomia target dell'Unità B|Dimensionamento batteria, fase 7|-|Il pacco batteria determina la massa del telaio: deciderlo dopo il telaio significa rifare il telaio.|aperta
A-11|Lanciare /cost e comunicare il consumo del giorno|Chiusura del libro mastro|-|Senza, la contabilità dei token resta parziale e le stime non si calibrano mai.|aperta
```
