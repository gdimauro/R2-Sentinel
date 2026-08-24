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
A-06|Decidere: Unità A alimentata da rete o autonoma|Fase 1, CAD della testa|-|DECISO 2026-08-24: **autonoma a batteria**.|fatta
A-07|Decidere: da quale modulo CAD partire (raccomandato: testa pan-tilt)|Fase 1|-|DECISO 2026-08-24: **testa pan-tilt**.|fatta
A-08|Decidere: getto d'aria, nebulizzazione, o entrambi|Fase 4 e dimensionamento payload|-|Blocca payload-fluidics sul dimensionamento. L'istruttoria comparativa è in corso.|aperta
A-09|Indicare il comune dell'installazione|Chiusura del dossier normativo, gate fase 4|-|Il regolamento comunale può essere più restrittivo di quello nazionale: scoprirlo a Unità A installata significa smontarla.|aperta
A-10|Decidere quanto pacco batteria installare nell'Unità B (la domanda è cambiata con D-26: non piu' quante ore di autonomia)|Dimensionamento batteria e budget di massa del payload, fase 1|-|Con il ciclo 45/45 alimentato dal dock l'autonomia notturna non serve piu'. Resta che la batteria e' l'unica zavorra utile: 1,3 kg -> 3,0 kg abbassano il baricentro di 25 mm e alzano il carico ammesso in cima da 1,10 a 1,50 kg. Va decisa insieme al budget di massa del payload, non prima e non dopo.|aperta
A-19|Indicare in quale stanza va il dock dell'Unita' B, non dove c'e' la presa comoda|Posizione del dock, fase 7, ed efficacia di cattura|-|Conseguenza di D-26: con il ciclo 45/45 il robot cattura meta' del tempo nella stanza del dock. Il dock va dove ci sono persone di notte, altrimenti meta' delle ore di cattura sono sprecate in un corridoio. Serve pavimento duro, 1200 mm liberi davanti e 400 mm per lato.|aperta
A-17|DECIDERE: accettare per iscritto il rischio di ribaltamento dell'Unità B, oppure rinunciare al montante da 120 cm|Congelamento del telaio, fase 1|-|DECISO 2026-08-24: **rischio accettato per iscritto**, verbale VRB-2026-0009. Le tre mitigazioni di D-22/D-23 restano vincolanti: se una cade, l'accettazione decade.|fatta
A-18|Rilievo dell'abitazione: luce netta delle porte, altezza soglie, pavimenti, scale, specchi e vetrate, arredi fra 150 e 1200 mm, due posizioni candidate per il dock|Pianificabilità della fase 7|-|Senza, i criteri «60 m² con chiusura d'anello ≤10 cm» e «0 cadute in 2 h» non sono nemmeno pianificabili: gli specchi e le vetrate sono la causa nota di fallimento del LIDAR. Gemello del rilievo del balcone (A-14).|aperta
A-20|Come si ricarica l'Unità A autonoma? Pannello solare, presa di servizio o pacco estraibile|Dimensionamento del pacco e volume del carter, fase 1|-|Discende dalla scelta del 24/08. Il compressore è il carico più pesante del progetto e su un balcone al sole la LiFePO4 non si carica sopra ~45 °C: senza una strategia, il pacco si dimensiona a vuoto.|aperta
A-16|Generare una password per app Google e impostare R2S_SMTP_USER e R2S_SMTP_PASS|Recapito del rapporto mattutino senza dipendere da Mail.app|-|Se Mail.app torna offline i rapporti si accodano in silenzio. Con SMTP diretto il canale non dipende più da un'applicazione che deve restare aperta e online.|aperta
A-11|Lanciare /cost e comunicare il consumo del giorno|Chiusura del libro mastro|-|Senza, la contabilità dei token resta parziale e le stime non si calibrano mai.|aperta
A-12|L'Unità A si alimenta da una presa esistente o serve un circuito nuovo?|Gate installazione Unità A|-|Se serve un circuito nuovo NON è fai-da-te: D.M. 37/2008 impone impresa abilitata e dichiarazione di conformità. Scoprirlo dopo significa rifare l'impianto.|aperta
A-13|Verificare se c'è un differenziale da 30 mA sul circuito del balcone|Gate installazione Unità A|-|Alimentazione di rete in esterno senza differenziale adeguato è il rischio elettrico principale del progetto.|aperta
A-14|Sopralluogo fotografico dal balcone: cosa entra davvero nel campo visivo|Gate installazione Unità A, privacy|-|Non è determinabile a tavolino ed è la differenza fra eccezione domestica e art. 615-bis c.p. La maschera di privacy deve essere ottica, non software.|aperta
A-15|Regolamento condominiale + notizia preventiva all'amministratore (art. 1122 c.c.)|Gate installazione Unità A|-|È dovuta per legge. Ometterla espone a rimozione dell'impianto anche se tutto il resto è conforme.|aperta
```
