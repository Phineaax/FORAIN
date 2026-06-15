# FORAIN
Repository de codes pour le projet CartaData Forain

## Contexte:
Les tests résumés ici ont été réalisés sur les documents textuels du répertoire "ALLEMAGNE", qui est assez représentatif de l'ensemble du corpus textuel. Il contient des textes faciles à déchiffrer, où l'écriture est claire et où la mise en page est simple. Il contient également des documents plus difficiles à déchiffrer, où la mise en page est complexe également (cartes postales, notamment).  
Nous avons réalisé un benchmark d'OCR par modèles de langue ainsi que par OCR plus traditionnel. Nos recherches suggèrent que la méthode la plus performante est le passage par LLM, en particulier par Claude.  
Ce GitHub contient:
* Le code pour la génération de transcriptions par appel API (industrialisable) sur des LLMs, 
* Des exemples de transcriptions pour Mistral et Claude
* Le prompt utilisé

## Résumé des modèles utilisés par API et performances:
**Modèles Mistral** 
* Fonctionnent plutôt bien pour textes faciles à lire
* Ne fonctionnent pas pour cartes postales et documents plus difficiles (fonctionne bien sur FO-A-1640, ne fonctionne pas sur FO-A-1637_2)

**Claude Chat:** Fonctionne parfaitement pour tout. Le layout est compris et le texte aussi. 
**Claude API:** Fonctionne moins bien que Claude Chat, parce que Claude Chat contient des instructions supplémentaires dans son prompt, qui améliorent la qualité des résultats (voir https://platform.claude.com/docs/en/release-notes/system-prompts). Nous avons construit un deuxième prompt pour Claude Sonnet de façon à améliorer les performances en API. Celui-ci permet de gagner 3 points de performances. Cela reste insuffisant. Il faudrait travailler plus en profondeur sur le prompt, ou accepter d'intégrer le prompt system officiel, qui est très long et coûte donc plus en tokens d'entrée.

**TrOCR:** Des tests que j'en ai fait, c'est très mauvais. C'est dommage, parce que ce n'est pas payant.

Tous les modèles Mistral (Mistral Small, Mistral Medium, Mistral Large) et GPT (Dernier modèle) testés ne fonctionnent pas pour la transcription d'écritures difficiles à déchiffrer. 

**Transkribus:** À tester, vraisemblablement très bon, mais impossible de faire fonctionner la webapp. Ce serait pertinent d'essayer, il y a une option gratuite et c'est sous format webapp donc un benchmark est accessible. Seule l'industrialisation peut être un peu plus compliquée à mettre en place, mais il semble qu'ils aient un système de traitement permettant l'industrialisation directement par la webapp. 

## Pré-Conclusion:
Il pourrait être intéressant de réaliser un pré-tri des documents en fonction de la facilité de déchiffrage de l'écriture. Un document facile à déchiffrer peut être transcrit par un Mistral Small, qui est très peu cher. Pour les autres, il faudra utiliser Claude, qui est assez cher.  
Il serait vraiment pertinent de donner sa chance à Transkribus, qui ne m'a pas donné ma chance de le faire fonctionner pour le moment.


## Performances:
Les performances montrent ici que Claude Chat est de loin de le plus performant. Ses CER (character error rate) et WER (word error rate) sont les plus bas. 
Les autres modèles se valent plus ou moins, Claude Opus étant le moins mauvais et ChatGPT étant le pire. 


### Version sans system prompt (system prompt = user prompt)
| Model                    | Sample      |         CER |         WER |
| ------------------------ | ----------- | ----------: | ----------: |
| Claude Chat (Sonnet 4.6) | FO-A-1638_1 |       5.61% |      22.64% |
| Claude Chat (Sonnet 4.6) | FO-A-1640   |       7.44% |      29.03% |
| Claude Chat (Sonnet 4.6) | FO-A-1642   |      26.50% |      48.41% |
| Claude Chat (Sonnet 4.6) | FO-A-1647_2 |      16.53% |      71.88% |
| Claude Chat (Sonnet 4.6) | **AVERAGE** |  **14.02%** |  **42.99%** |
| ------------------------ | ----------- | ----------: | ----------: |
| Claude Opus              | FO-A-1638_1 |      22.15% |      52.83% |
| Claude Opus              | FO-A-1640   |      18.91% |      41.94% |
| Claude Opus              | FO-A-1642   |      32.94% |      44.44% |
| Claude Opus              | FO-A-1647_2 |      69.49% |      93.75% |
| Claude Opus              | **AVERAGE** |  **35.88%** |  **58.24%** |
| ------------------------ | ----------- | ----------: | ----------: |
| Claude Sonnet 4.6 (nouveau prompt)| FO-A-1638_1 |       33.23% |      57.55% |
| Claude Sonnet 4.6 (nouveau prompt)| FO-A-1640   |       19.84% |      44.09% |
| Claude Sonnet 4.6 (nouveau prompt)| FO-A-1642   |      27.79% |      39.68% |
| Claude Sonnet 4.6 (nouveau prompt)| FO-A-1647_2 |      78.39% |      140.62% |
| Claude Sonnet 4.6 (nouveau prompt)| **AVERAGE** |  **39.81%** |  **70.49%** |
| ------------------------ | ----------- | ----------: | ----------: |
| Claude Sonnet            | FO-A-1638_1 |      21.55% |      51.89% |
| Claude Sonnet            | FO-A-1640   |      18.60% |      43.01% |
| Claude Sonnet            | FO-A-1642   |      31.65% |      43.65% |
| Claude Sonnet            | FO-A-1647_2 |      97.03% |     156.25% |
| Claude Sonnet            | **AVERAGE** |  **42.21%** |  **73.70%** |
| ------------------------ | ----------- | ----------: | ----------: |
| GPT 5 Mini               | FO-A-1638_1 |      26.71% |      53.77% |
| GPT 5 Mini               | FO-A-1640   |      19.69% |      43.01% |
| GPT 5 Mini               | FO-A-1642   |      32.94% |      44.44% |
| GPT 5 Mini               | FO-A-1647_2 |      86.44% |     140.62% |
| GPT 5 Mini               | **AVERAGE** |  **41.44%** |  **70.46%** |
| ------------------------ | ----------- | ----------: | ----------: |
| GPT Chat                 | FO-A-1638_1 |     102.73% |      50.00% |
| GPT Chat                 | FO-A-1640   |      87.60% |      49.46% |
| GPT Chat                 | FO-A-1642   |      57.19% |      53.17% |
| GPT Chat                 | FO-A-1647_2 |     239.83% |     109.38% |
| GPT Chat                 | **AVERAGE** | **121.84%** |  **65.50%** |
| ------------------------ | ----------- | ----------: | ----------: |
| GPT_4.1                  | FO-A-1638_1 |      21.55% |      51.89% |
| GPT_4.1                  | FO-A-1640   |      18.29% |      41.94% |
| GPT_4.1                  | FO-A-1642   |      33.05% |      44.44% |
| GPT_4.1                  | FO-A-1647_2 |      64.41% |      90.62% |
| GPT_4.1                  | **AVERAGE** |  **34.32%** |  **57.22%** |
| ------------------------ | ----------- | ----------: | ----------: |
| Mistral Large            | FO-A-1638_1 |      25.34% |      51.89% |
| Mistral Large            | FO-A-1640   |      18.60% |      37.63% |
| Mistral Large            | FO-A-1642   |      33.05% |      44.44% |
| Mistral Large            | FO-A-1647_2 |      82.20% |      93.75% |
| Mistral Large            | **AVERAGE** |  **39.80%** |  **56.93%** |
| ------------------------ | ----------- | ----------: | ----------: |
| Mistral Medium           | FO-A-1638_1 |      21.09% |      47.17% |
| Mistral Medium           | FO-A-1640   |      18.14% |      43.01% |
| Mistral Medium           | FO-A-1642   |      32.94% |      44.44% |
| Mistral Medium           | FO-A-1647_2 |      84.75% |     146.88% |
| Mistral Medium           | **AVERAGE** |  **39.23%** |  **70.38%** |
| ------------------------ | ----------- | ----------: | ----------: |
| Mistral Small            | FO-A-1638_1 |      24.73% |      51.89% |
| Mistral Small            | FO-A-1640   |      18.60% |      43.01% |
| Mistral Small            | FO-A-1642   |      33.26% |      44.44% |
| Mistral Small            | FO-A-1647_2 |     111.86% |     168.75% |
| Mistral Small            | **AVERAGE** |  **47.12%** |  **77.02%** |
| ------------------------ | ----------- | ----------: | ----------: |
| OLD                      | FO-A-1638_1 |      24.43% |      51.89% |
| OLD                      | FO-A-1640   |      19.69% |      46.24% |
| OLD                      | FO-A-1647_2 |     120.34% |     212.50% |
| OLD                      | **AVERAGE** |  **54.82%** | **103.54%** |
| ------------------------ | ----------- | ----------: | ----------: |
| Qwen                     | FO-A-1638_1 |      21.09% |      49.06% |
| Qwen                     | FO-A-1640   |      15.81% |      39.78% |
| Qwen                     | FO-A-1642   |      32.94% |      44.44% |
| Qwen                     | FO-A-1647_2 |      72.03% |     106.25% |
| Qwen                     | **AVERAGE** |  **35.47%** |  **59.88%** |
| ------------------------ | ----------- | ----------: | ----------: |



## 
