# FORAIN
Repository de codes pour le projet CartaData Forain

## Contexte:
Les premier tests de transcription (Tests transcriptions, dont les performances sont explicitées) ont été réalisés sur les documents textuels du répertoire "ALLEMAGNE", utilisé pour une phase de **tests préliminaires** visant à choisir le modèle de transcription à employer. Ce répertoire est assez représentatif de l'ensemble du corpus textuel : il contient des textes faciles à déchiffrer, où l'écriture est claire et la mise en page simple, ainsi que des documents plus difficiles à déchiffrer, à la mise en page complexe (une carte postale en particulier).

Nous avons réalisé un benchmark d'OCR par modèles de langue ainsi que par OCR plus traditionnel. Nos recherches suggèrent que la méthode la plus performante est le passage par LLM, en particulier par GPT mini ou Claude Sonnet. À partir de ces métriques et d'une évaluation qualitative, nous avons retenu **GPT mini** pour réaliser la tâche de transcription en phase d'« industrialisation ».

Pour cette phase d'industrialisation, 44 documents différents des premiers étudiés ont été sélectionnés, issus de catégories diverses et aux particularités différentes, afin d'observer un éventail de comportements du modèle selon les types de documents.

Une fois ces 44 documents transcrits, nous avons fait générer une courte description de chaque transcription par différents modèles. Le modèle **GPT Mini** a de nouveau été retenu pour cette tâche, à l'issue d'une évaluation qualitative et d'avis croisés entre LLMs : il s'est montré le plus exact, obtient généralement les deuxièmes meilleurs résultats, et — à la différence de sa variante avec le prompt 1, meilleure sur les métriques — il introduit systématiquement le sujet global du document de façon concise en début de description.

Ce GitHub contient:
* Le code pour la génération de transcriptions par appel API (industrialisable) sur des LLMs, 
* Des exemples de transcriptions pour des modèles variés,
* Une étude de performance de différents modèles pour les tâches de transcription et description,
* Des transcriptions et descriptions de 44 documents issus du fonds

## Structure du dépôt

```
FORAIN/
├── Tests transcriptions/                  # Phase de benchmark : comparaison de 13 méthodes sur 4 documents
│   ├── GOLD STANDARD/                     # Transcription de référence, réalisée manuellement
│   ├── Qwen/
│   ├── Mistral small/
│   ├── Mistral medium/
│   ├── Mistral large/
│   ├── GPT mini/
│   ├── GPT 4.1/
│   ├── GPT chat/
│   ├── Claude Sonnet/
│   ├── Claude Opus/
│   ├── Claude chat/
│   ├── TrOCR Surya/
│   ├── Kraken/
│   └── easyOCR/
│       └── {id_image}.txt                 # une transcription par document testé et par modèle
│
├── Transcriptions - 44 éléments/
│   ├── transcriptions/
│   │   └── {catégorie}/{id_image}.txt     # transcriptions des 44 documents, générées via Claude Sonnet 4.6
│   ├── image/
│   │   └── {catégorie}/{id_image}.*       # images sources correspondant à chaque transcription
│   ├── OCR_industrialisation.ipynb        # notebook d'appel API pour générer les transcriptions en masse
│   └── RecuperationFichiersATranscrire.ipynb  # notebook Colab pour récupérer les fichiers à transcrire depuis Google Drive
│
├── descriptions/
│   ├── Mistral small/
│   ├── Mistral medium/
│   ├── Mistral large/
│   ├── GPT mini/
│   ├── GPT 4.1/
│   ├── GPT chat/
│   ├── Claude Sonnet/
│   ├── Claude Opus/
│   │   └── {catégorie}/{id_image}.txt     # courte description générée pour chaque transcription
│   ├── GPT Mini prompt 1/                 # descriptions GPT mini obtenues avec un prompt alternatif
│   └── Résumés.ipynb                      # notebook utilisé pour générer les descriptions
│
├── LOGs/                                  # avis croisés de GPT mini et Claude Sonnet sur la qualité des descriptions
│   ├── evaluations_GPTMini.json
│   └── evaluations_ClaudeSonnet.json
│
├── script.py                              # calcul des métriques CER/WER des transcriptions vs. GOLD STANDARD
├── creationDataFrame.py                   # construction du DataFrame transcriptions + descriptions
├── table_transcriptions_descriptions.csv  # DataFrame résultant, sur les 44 transcriptions déjà réalisées
└── README.md
```

## Méthode prompting:
Les prompts system et user ont été écrits en fonction de la tâche puis augmentés avec Claude Sonnet pour améliorer leur pertinence. 

### Performances HTR LLMs
CER: Character error rate (=le taux de caractères faux dans le document transcrit)  
WER: Word error rate (=le taux de mots faux dans le document transcrit)  
Un score plus bas est meilleur, donc. Les deux meilleurs modèles sont Claude Sonnet et GPT Mini. Claude étant beaucoup plus cher, GPT mini semble être une meilleure option.  
Il faudrait tester Transkribus, qui devrait être plutôt bon sur la tâche. Je n'ai pas réussi à le faire fonctionner, le site étant toujours en maintenance, mais il est facile d'utilisation et _a priori_ performant.

| Model                    | Sample      |         CER |         WER |
| ------------------------ | ----------- | ----------: | ----------: |
| Claude Opus 4.8          | FO-A-1638_1 |       8.50% |      39.62% |
| Claude Opus 4.8          | FO-A-1640   |      14.73% |      44.09% |
| Claude Opus 4.8          | FO-A-1642   |      28.65% |      50.00% |
| Claude Opus 4.8          | FO-A-1647_2 |      21.61% |      68.75% |
| Claude Opus 4.8          | **AVERAGE** |  **18.37%** |  **50.61%** |
| ------------------------ | ----------- | ----------- | ----------- |
| Claude Sonnet 4.6        | FO-A-1638_1 |       8.95% |      36.79% |
| Claude Sonnet 4.6        | FO-A-1640   |      24.50% |      51.61% |
| Claude Sonnet 4.6        | FO-A-1642   |      21.57% |      46.03% |
| Claude Sonnet 4.6        | FO-A-1647_2 |      16.95% |      68.75% |
| Claude Sonnet 4.6        | **AVERAGE** |  **17.99%** |  **50.80%** |
| ------------------------ | ----------- | ----------- | ----------- |
| GPT 4.1                  | FO-A-1638_1 |      28.53% |      58.49% |
| GPT 4.1                  | FO-A-1640   |      26.05% |      49.46% |
| GPT 4.1                  | FO-A-1642   |      35.41% |      33.33% |
| GPT 4.1                  | FO-A-1647_2 |      38.14% |      81.25% |
| GPT 4.1                  | **AVERAGE** |  **32.03%** |  **55.63%** |
| ------------------------ | ----------- | ----------- | ----------- |
| GPT Chat                 | FO-A-1638_1 |     102.73% |      50.00% |
| GPT Chat                 | FO-A-1640   |      87.60% |      49.46% |
| GPT Chat                 | FO-A-1642   |      57.19% |      53.17% |
| GPT Chat                 | FO-A-1647_2 |     239.83% |     109.38% |
| GPT Chat                 | **AVERAGE** | **121.84%** |  **65.50%** |
| ------------------------ | ----------- | ----------- | ----------- |
| GPT Mini                 | FO-A-1638_1 |      16.39% |      46.23% |
| GPT Mini                 | FO-A-1640   |       9.15% |      47.31% |
| GPT Mini                 | FO-A-1642   |      24.03% |      62.70% |
| GPT Mini                 | FO-A-1647_2 |      21.61% |      50.00% |
| GPT Mini                 | **AVERAGE** |  **17.80%** |  **51.56%** |
| ------------------------ | ----------- | ----------- | ----------- |
| Mistral Large            | FO-A-1638_1 |      34.90% |      60.38% |
| Mistral Large            | FO-A-1640   |      26.51% |      50.54% |
| Mistral Large            | FO-A-1642   |      32.30% |      43.65% |
| Mistral Large            | FO-A-1647_2 |      96.19% |     118.75% |
| Mistral Large            | **AVERAGE** |  **47.47%** |  **68.33%** |
| ------------------------ | ----------- | ----------- | ----------- |
| Mistral Medium           | FO-A-1638_1 |      20.18% |      48.11% |
| Mistral Medium           | FO-A-1640   |      27.75% |      54.84% |
| Mistral Medium           | FO-A-1642   |      35.09% |      54.76% |
| Mistral Medium           | FO-A-1647_2 |      67.80% |     100.00% |
| Mistral Medium           | **AVERAGE** |  **37.70%** |  **64.43%** |
| ------------------------ | ----------- | ----------- | ----------- |
| Mistral Small            | FO-A-1638_1 |      46.89% |      77.36% |
| Mistral Small            | FO-A-1640   |      25.43% |      61.29% |
| Mistral Small            | FO-A-1642   |       9.23% |      42.06% |
| Mistral Small            | FO-A-1647_2 |      82.63% |     100.00% |
| Mistral Small            | **AVERAGE** |  **41.04%** |  **70.18%** |
| ------------------------ | ----------- | ----------- | ----------- |
| Qwen 3.7                 | FO-A-1647_2 |      33.47% |      84.38% |
| Qwen 3.7                 | **AVERAGE** |  **33.47%** |  **84.38%** |

## Performances HTR traditionnel
Les modèles d'HTR traditionnels ne fonctionnent pas très bien dans l'ensemble. Le meilleur est Kraken, avec un CER de 40%, ce qui est supérieur à celui de la plupart des modèles LLMs étudiés. Un entraînement supplémentaire pourrait améliorer les performances mais cela représente un travail conséquent.

| Model                    | Sample      |         CER |         WER |
| ------------------------ | ----------- | ----------: | ----------: |
| EasyOCR                  | FO-A-1638_1 |      80.58% |     103.77% |
| EasyOCR                  | FO-A-1640   |      60.62% |     102.15% |
| EasyOCR                  | FO-A-1642   |      22.64% |      74.60% |
| EasyOCR                  | FO-A-1647_2 |      80.51% |     128.12% |
| EasyOCR                  | **AVERAGE** |  **61.09%** | **102.16%** |
| ------------------------ | ----------- | ----------- | ----------- |
| Kraken ManuMcFrenchV3    | FO-A-1638_1 |      24.89% |      62.26% |
| Kraken ManuMcFrenchV3    | FO-A-1640   |      34.11% |      70.97% |
| Kraken ManuMcFrenchV3    | FO-A-1642   |      30.90% |      65.87% |
| Kraken ManuMcFrenchV3    | FO-A-1647_2 |      72.46% |     100.00% |
| Kraken ManuMcFrenchV3    | **AVERAGE** |  **40.59%** |  **74.78%** |
| ------------------------ | ----------- | ----------- | ----------- |
| TrOCR + Surya            | FO-A-1638_1 |      81.79% |     125.47% |
| TrOCR + Surya            | FO-A-1640   |      56.12% |      83.87% |
| TrOCR + Surya            | FO-A-1642   |      26.07% |      46.03% |
| TrOCR + Surya            | FO-A-1647_2 |     119.92% |     190.62% |
| TrOCR + Surya            | **AVERAGE** |  **70.98%** | **111.50%** |

## Pipeline de traitement

1. **Choix des images à traiter** – Parcours des documents du drive
2. **Récupération des images** — `RecuperationFichiersATranscrire.ipynb` enregistre dans un dossier alternatif les fichiers à transcrire depuis Google Drive, de façon à télécharger en local ledit fichier ensuite.
3. **Transcription** — `OCR_industrialisation.ipynb` appelle l'API du LLM choisi (Claude Sonnet pour les 44 documents) et enregistre le résultat dans `Transcriptions - 44 éléments/transcriptions/{catégorie}/{id_image}.txt`.
4. **Description** — `Résumés.ipynb` génère, pour chaque transcription, une courte description par modèle (dossiers `descriptions/{modèle}/`).
5. **Évaluation des descriptions** — les fichiers JSON du dossier `LOGs/` consignent l'avis de GPT mini et de Claude Sonnet sur la qualité des descriptions produites.
6. **Calcul des métriques** — `script.py` compare chaque transcription à la `GOLD STANDARD` et calcule le CER et le WER.
7. **Consolidation** — `creationDataFrame.py` regroupe transcriptions et descriptions dans `table_transcriptions_descriptions.csv`.

## Limites et perspectives

* Transkribus n'a pas pu être testé (site en maintenance au moment du benchmark) ; il faudrait l'évaluer car il est réputé performant et simple d'utilisation sur ce type de tâche.
* Le benchmark de transcription repose sur seulement 4 documents ; les conclusions restent à confirmer sur un échantillon plus large du corpus. D'un point de vue qualitatif, les transcriptions sont bonnes mais il y a quelques hallucinations pour certains documents difficiles sur les 44 supplémentaires.
* Un entraînement supplémentaire des modèles d'HTR traditionnels (Kraken notamment) pourrait améliorer leurs performances, au prix d'un travail de mise en œuvre conséquent.