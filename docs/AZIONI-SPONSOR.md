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
A-17|DECIDERE: accettare per iscritto il rischio di ribaltamento dell'Unità B, oppure rinunciare al montante da 120 cm|Congelamento del telaio, fase 1|-|Con la geometria migliore raggiungibile bastano 530-900 g di spinta laterale in cima per rovesciare il robot: un gatto, un bambino, la coda di un cane. Verificato con calcolo indipendente. Non esiste una terza via: o si accetta il rischio residuo o si abbassa il montante. Deciderlo dopo il CAD significa rifare il telaio.|aperta
A-18|Rilievo dell'abitazione: luce netta delle porte, altezza soglie, pavimenti, scale, specchi e vetrate, arredi fra 150 e 1200 mm, due posizioni candidate per il dock|Pianificabilità della fase 7|-|Senza, i criteri «60 m² con chiusura d'anello ≤10 cm» e «0 cadute in 2 h» non sono nemmeno pianificabili: gli specchi e le vetrate sono la causa nota di fallimento del LIDAR. Gemello del rilievo del balcone (A-14).|aperta
A-16|Generare una password per app Google e impostare R2S_SMTP_USER e R2S_SMTP_PASS|Recapito del rapporto mattutino senza dipendere da Mail.app|-|Se Mail.app torna offline i rapporti si accodano in silenzio. Con SMTP diretto il canale non dipende più da un'applicazione che deve restare aperta e online.|aperta
A-11|Lanciare /cost e comunicare il consumo del giorno|Chiusura del libro mastro|-|Senza, la contabilità dei token resta parziale e le stime non si calibrano mai.|aperta
A-12|L'Unità A si alimenta da una presa esistente o serve un circuito nuovo?|Gate installazione Unità A|-|Se serve un circuito nuovo NON è fai-da-te: D.M. 37/2008 impone impresa abilitata e dichiarazione di conformità. Scoprirlo dopo significa rifare l'impianto.|aperta
A-13|Verificare se c'è un differenziale da 30 mA sul circuito del balcone|Gate installazione Unità A|-|Alimentazione di rete in esterno senza differenziale adeguato è il rischio elettrico principale del progetto.|aperta
A-14|Sopralluogo fotografico dal balcone: cosa entra davvero nel campo visivo|Gate installazione Unità A, privacy|-|Non è determinabile a tavolino ed è la differenza fra eccezione domestica e art. 615-bis c.p. La maschera di privacy deve essere ottica, non software.|aperta
A-15|Regolamento condominiale + notizia preventiva all'amministratore (art. 1122 c.c.)|Gate installazione Unità A|-|È dovuta per legge. Ometterla espone a rimozione dell'impianto anche se tutto il resto è conforme.|aperta
```
