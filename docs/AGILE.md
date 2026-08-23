# Metodo di lavoro

Modalità agile, adattata a un progetto hardware con una squadra di agenti e una
persona sola che fa tutto il lavoro fisico.

---

## 1. Lo sprint è il gate, non la settimana

L'adattamento principale. Uno sprint a durata fissa su un progetto hardware
produce sprint finti: si chiude il venerdì con il pezzo ancora in stampa e si
dichiara «fatto all'80%», che in meccanica non significa niente.

Qui il traguardo di sprint è il **gate di una fase**, e il gate si chiude quando
il criterio di FATTO è **misurato**. `RMS ≤1,0° su 20 cicli a 5 m` passa o non
passa: non esiste l'80%.

La **cadenza** resta quotidiana — standup e aggiornamento del sinottico — ma non
è la cadenza a decidere quando una cosa è finita.

## 2. Definition of Done

Già scritta, e più severa di qualunque DoD: **il criterio di FATTO nel file di
ogni agente**. Non si rinegozia a fine sprint. Un elemento entra in *Fatto* solo
con il numero misurato e il protocollo registrato.

Fra *In corso* e *Fatto* c'è **In verifica**: il lavoro è consegnato ma il numero
non è ancora stato misurato. È la colonna più importante della board, perché è
dove un progetto hardware si illude di aver finito.

## 3. Le colonne

| Colonna | Significato |
|---|---|
| **Backlog** | Ha una dipendenza non soddisfatta. Non si può iniziare. |
| **Pronto** | Nessuna dipendenza aperta. Si può attivare oggi. |
| **In corso** | Un agente o lo sponsor ci sta lavorando ora. |
| **In verifica** | Consegnato, criterio di FATTO non ancora misurato. |
| **Fatto** | Criterio misurato e superato, con protocollo registrato. |

## 4. Lo standup

Ogni agente attivato riporta tre cose, nella forma classica:

1. **Cosa ho consegnato**
2. **Cosa faccio adesso**
3. **Cosa mi blocca — e chi lo può sbloccare**

Il terzo punto è l'unico che conta davvero. Con una squadra di agenti i blocchi
non sono di coordinamento fra persone: sono quasi sempre **acquisti da fare,
decisioni dello sponsor, o misure che nessuno può eseguire**. Lo standup serve a
farli emergere tutti insieme, ogni giorno, invece che uno alla volta.

Lo standup è **automatico**: si compila dai report degli agenti e finisce sul
sinottico. Non è una riunione.

## 5. Chi è chi

| Ruolo agile | Qui |
|---|---|
| Product Owner | **Sponsor** (la persona): priorità, budget, decisioni di §10 |
| Tech Lead | **chief-engineer**: architettura, confini, accettazione delle misure |
| Team | I nove agenti specialisti |
| *Scrum Master* | **Nessuno.** Non c'è nulla da facilitare: i blocchi sono visibili all'istante. |

## 6. Cosa NON facciamo, e perché

- **Story point e velocity** — stimare in punti il lavoro di un agente non
  predice niente di utile: il vincolo non è la capacità produttiva, sono acquisti
  e calendario.
- **Retrospettive come riunione** — la funzione ce l'ha già il giornale
  (`journal/`), che registra errori e «da rifare diversamente» il giorno stesso.
  Dalla D-16 la *funzione* retrospettiva ha un proprietario, `retrospective`, che
  però non convoca nulla: legge report, giornale e libro mastro e ne ricava la
  sintesi serale e le proposte di emendamento ai mandati. Resta escluso il rito,
  non il miglioramento continuo.
- **Sprint planning come cerimonia** — la priorità la decide la scadenza, ed è
  visibile sulla board.

## 7. La regola di priorità

Gli elementi si ordinano **per scadenza, non per importanza**. È la stessa
correzione applicata agli acquisti nel libro mastro: l'anemometro è più
importante del microfono, ma il microfono scade e l'anemometro no.

Un elemento con una scadenza esterna batte sempre un elemento più importante ma
rinviabile.
