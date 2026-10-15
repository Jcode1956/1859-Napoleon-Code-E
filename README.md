# Code E: the 1859 telegraph code of Napoleon III and Empress Eugénie

Data and checker for the decipherment of "code E". This is the private numeric code used in the telegrams between Napoleon III, on campaign in Italy, and Empress Eugénie, regent in Paris, in June 1859.

Source: Bibliothèque nationale de France, NAF 11355, [Gallica](https://gallica.bnf.fr/ark:/12148/btv1b52517729k)

Anonymous, with the help of GPT 6 Astra and a little bit of help from Opus 5.5.

## Result

| | |
|---|---|
| Telegrams | 12 (f3–f35, 1–25 June 1859) |
| Coded text tokens | 447 (header groups excluded) |
| Read | 422 (94.4%) |
| Unread | 25 tokens, 22 distinct groups |
| Key | 232 groups: 68 confirmed, 149 probable, 15 tentative |
| Alphabetical-order violations | 0 |

## Files

| File | Contents |
|---|---|
| `transcription.txt` | Hand transcription of every code-E telegram from the Gallica images (format documented at the top) |
| `key.tsv` | Recovered key: group, reading, confidence tier |
| `check.py` | Applies the key, checks alphabetical order, reports coverage (Python 3, standard library only) |
| `expected_output.txt` | What `check.py` prints |

## Run it

```
python3 check.py
```

Compare the output with `expected_output.txt`. To test a change, edit `key.tsv` and re-run. Any reading that breaks alphabetical order is reported as a violation.

## How the code works

**One-part, alphabetical.** Group numbers rise with the alphabetical order of the plaintext: à 30, de 323, la 702, le 708, que 1040, vous 1385. The book has about 1,450 entries. This ordering is the main check: every reading must sort between its neighbours.

**Syllabary.** Letters and syllables are filed among the words. Names and missing words are spelled from these pieces:

- O-G-LI-O (Oglio)
- MIN-CI-O (Mincio)
- CAS-TI-GL-I-ON (Castiglione)
- MA-GEN-TA (Magenta)
- CO-T-TE (de Cotte)

`check.py` prints these pieces separately, so `DE CO T TE` reads "de Cotte".

**ʒ groups.** These are written `z` in the files.

- 10ʒ and 26ʒ are full stops.
- 329ʒ, 980ʒ, 1047ʒ and 1102ʒ stand for proper names: autrichien, Piémont, Rome, Sardaigne. They do not fit the main order, and are inferred to be a separate list of names.

**Groups below 30.** These are digits and signs. They lie outside the word list, so order cannot test them.

**Headers.** The groups listed in `hdr=` open a telegram and are not text.

## Confidence tiers

| Tier | Criterion |
|---|---|
| confirmed | Fits order and sense in two or more independent contexts, or lies in the externally confirmed passage |
| probable | Fits order and sense in one context |
| tentative | Plausible but weakly constrained |

## External confirmation

Telegram f29 (Montechiaro, 23 June) ends with this sentence, decoded with the name only partly read:

> De Cotte était de service hier ; il se portait très bien, il a couché à ma porte, et à minuit, au moment où on lui apportait une dépêche, il est mort subitement.

Bazancourt independently records the sudden death of General de Cotte, the Emperor's aide-de-camp, at about midnight while reading newly arrived dispatches, at Montechiaro on 23 June 1859. The source is *La campagne d'Italie de 1859* (Paris: Amyot, 1860), [archive.org](https://archive.org/details/lacampagnedital01unkngoog). Bazancourt does not quote the telegram.

## Unread groups

85, 162ʒ, 163, 204, 225, 228, 274, 296, 442, 543, 565, 633, 666, 735, 824, 865, 1046, 1142, 1197, 1203, 1216, 1250

Notes on some of them:

- **1216** sits in DI-C-TA-[1216]-RE, which should be *dictature*. That needs *tu*, which would be group 1316, so 1216 is probably a one-digit slip in the manuscript.
- **228** is probably a slip for 248 (*co*), giving "de Cotte".

## Prior publication

We found no earlier decipherment. We checked the following:

- DECODE
- Cryptiana
- the 1870–77 Tuileries papers
- Bazancourt (1860)
- the 1862 official history
- web searches

The Archives nationales (400 AP) were not consulted. Corrections and earlier decodes are welcome.

## Licence

CC0 1.0: public domain dedication. Use freely.
