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
**mistralai/mistral-small-3.2-24b-instruct:** 
* Fonctionne pour textes faciles à lire
* Ne fonctionne pas pour cartes postales et documents plus difficiles (fonctionne bien sur FO-A-1640, ne fonctionne pas sur FO-A-1637_2)

**Claude Chat:** Fonctionne parfaitement pour tout. Le layout est compris et le texte aussi. 

**TrOCR:** Des tests que j'en ai fait, c'est très mauvais. C'est bien dommage, parce que ce n'est pas payant.

Tous les modèles Mistral (Mistral Small, Mistral Medium, Mistral Large) et GPT (Dernier modèle) testés ne fonctionnent pas pour la transcription d'écritures difficiles à déchiffrer. 

**Transkribus:** À tester, vraisemblablement très bon, mais impossible de faire fonctionner la webapp. Ce serait pertinent d'essayer, il y a une option gratuite et c'est sous format webapp donc un benchmark est accessible. Seule l'industrialisation peut être un peu plus compliquée à mettre en place, mais il semble qu'ils aient un système de traitement permettant l'industrialisation directement par la webapp. 

## Pré-Conclusion:
Il serait pertinent de réaliser un pré-tri des documents en fonction de la facilité de déchiffrage de l'écriture. Un document facile à déchiffrer peut être transcrit par un Mistral Small, qui est très peu cher. Pour les autres, il faudra utiliser Claude, qui est assez cher.  
Il serait vraiment pertinent de donner sa chance à Transkribus, qui ne m'a pas donné ma chance de le faire fonctionner pour le moment.