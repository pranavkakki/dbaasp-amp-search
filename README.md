# dbaasp-amp-search
Search the DBAASP database for antimicrobial peptide sequences by target organism. Streamlit app, live REST API, FASTA export.

# DBAASP AMP Search

Find antimicrobial peptide sequences active against a given organism.

Enter a target organism and get every AMP sequence in [DBAASP](https://dbaasp.org)
tested against it, downloadable as plain text or FASTA. Queries run against the
live DBAASP REST API, so results reflect the current database rather than a
stale export.

**[Open the app →](YOUR-STREAMLIT-URL-HERE)**

## Usage

Type an organism name. Matching is by substring, so `Escherichia coli` returns
sequences tested against every *E. coli* strain in the database
(`ATCC 25922`, `UB1005`, and so on), while `Escherichia coli ATCC 25922` narrows
to that one strain.

Some organisms to start with:

| Organism | Approx. sequences |
|---|---|
| `Escherichia coli` | ~2,000 |
| `Staphylococcus aureus` | ~2,000 |
| `Candida albicans` | several hundred |
| `Pasteurella multocida` | under 100 |

## Reading the sequences

DBAASP notation, not standard FASTA:

- **Lowercase letters** are D-amino acids (`kwkikwpvkwfkml`)
- **`X`** marks a modified or unusual residue with no single-letter code

Long runs of near-identical sequences are normal — they're synthetic analog
series from structure–activity studies, one entry per residue substitution.

## Running locally

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
pip install -r requirements.txt
streamlit run app.py
```

## How it works

A single `GET https://dbaasp.org/peptides` with `targetSpecies.value` set to the
organism, paged 200 at a time via `limit`/`offset` until `totalCount` is reached.
Multi-peptide records carry their chains in a nested `monomers` array, so those
are flattened out; sequences are then deduplicated and sorted. Full API spec:
`https://dbaasp.org/v3/api-docs`.

Results are cached per organism for the session, so repeat searches return
instantly. Restart the app to force a fresh fetch.

## Data source

All data comes from DBAASP and is subject to their
[terms and conditions](https://dbaasp.org/terms-and-conditions). If you use this
in published work, cite:

> Pirtskhalava M, Amstrong AA, Grigolava M, Chubinidze M, Alimbarashvili E,
> Vishnepolsky B, Gabrielian A, Rosenthal A, Hurt DE, Tartakovsky M.
> DBAASP v3: database of antimicrobial/cytotoxic activity and structure of
> peptides as a resource for development of new therapeutics.
> *Nucleic Acids Research*, 2021, 49(D1): D288–D297.
> https://doi.org/10.1093/nar/gkaa991
