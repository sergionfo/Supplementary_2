# Supplementary material – version 18

Deep Learning for Seismic Phase Picking: A Systematic Mapping Study (Moro & Oliveira).

## Data (data/)
- record_identifiers_827.csv – DOI, WoS UT or Scopus link and inclusion status of all retrieved records (raw exports are not redistributed because of database licences).
- Sentinel_set.csv – sentinel studies (SeisBench is ineligible under EC5 and excluded from the recall test: 14/16 retrieved, 14/14 included).
- excluded_audit.csv – random sample (seed 1) of 40 of the 270 excluded records with the audit decision (2 likely false exclusions).
- sensitivity_wos.csv – eligible and out-of-scope records of the search-sensitivity query.
- WoS2026_screening.csv – screening of the preliminary 2026 update (searched 1 November 2026).
- audit_197.json, author_variants.csv – number audit and author-name variants (788 -> 762 distinct authors when merged).
- boundary_sensitivity.json – the 18 boundary cases and indicators with and without them.
- lexical_validation.csv – validation sample of the lexical coding (30 records, seed 1).

## Search-sensitivity query (Web of Science Core Collection, 1–3 November 2026)
Arrival and onset terms ("P-wave arrival", "S-wave arrival", "arrival-time picking", "phase onset", "seismic arrival", first arrival) and the model names PhaseNet and EQTransformer, combined with the AI terms of Table 3, NOT the original phrases of Table 4.
EXACT STRING: [authors: copy from the Web of Science search history before archiving]

## Regional Azores search (Web of Science Core Collection, all years, 1–3 November 2026)
Azores / Açores and island names combined with seismic and machine-learning terms; 15 records.
EXACT STRING AND RECORD LIST: [authors: export from the Web of Science search history before archiving]

## Seeds
Louvain: 3 (themes), 1 (keyword co-occurrence), 2 (co-authorship). Permutation test (B = 20,000, p = (b+1)/(B+1)), excluded-record audit sample and lexical validation sample: NumPy default_rng(1).

## Software
Python 3.13, pandas 3.0, NumPy 2.5, SciPy 1.18, networkx 3.7, matplotlib 3.11, pyreadr 0.5; Bibliometrix (R) for the Biblioshiny outputs.

## Checksums
SHA-256 of every file in checksums.txt.
