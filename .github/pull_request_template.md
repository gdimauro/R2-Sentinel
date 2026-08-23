## Cosa cambia

<!-- Una frase. Il "perche'" va nel Decision Log, non qui. -->

## Tipo di modifica

- [ ] Implementazione dentro un modulo esistente
- [ ] Cambio di architettura o di contratto fra ruoli -> **richiede una riga in `docs/PROJECT.md` §3**
- [ ] Tocca il payload o la sicurezza -> **richiede nota di conformita'** (file in `docs/compliance/` o etichetta `conformita-ok`)
- [ ] Solo documentazione

## Verifiche

- [ ] `make check` passa in locale
- [ ] `make test` passa in locale
- [ ] Criterio di FATTO interessato eseguito: `./scripts/fatto.sh <ruolo>` — esito incollato sotto
- [ ] Nessun peso, dataset, mappa SLAM, audio o credenziale nel diff (lo verifica anche la CI, ma guarda il diff comunque)

<details><summary>Esito di ./scripts/fatto.sh</summary>

```
incolla qui
```
</details>

## Note per il chief-engineer

<!-- Numeri falliti con la causa isolata, questioni aperte per §10, incognite.
     Un numero che non torna si riporta, non si arrotonda. -->
