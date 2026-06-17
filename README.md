# FORAIN
Repository de codes pour le projet CartaData Forain

## Contexte:
Les tests résumés ici ont été réalisés sur les documents textuels du répertoire "ALLEMAGNE", qui est assez représentatif de l'ensemble du corpus textuel. Il contient des textes faciles à déchiffrer, où l'écriture est claire et où la mise en page est simple. Il contient également des documents plus difficiles à déchiffrer, où la mise en page est complexe également (une carte postale en particulier).  
Nous avons réalisé un benchmark d'OCR par modèles de langue ainsi que par OCR plus traditionnel. Nos recherches suggèrent que la méthode la plus performante est le passage par LLM, en particulier par GPT mini ou Claude Sonnet. 
Ce GitHub contient:
* Le code pour la génération de transcriptions par appel API (industrialisable) sur des LLMs, 
* Des exemples de transcriptions pour Mistral et Claude
* Le prompt utilisé

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
