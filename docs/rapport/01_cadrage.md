# 1. Cadrage du projet

## 1.1 Contexte

Dans un atelier industriel, la documentation de maintenance est dispersée : manuels constructeurs, procédures internes de plusieurs versions, fiches de sécurité, schémas et historiques d'interventions. Devant une machine en alarme, le technicien perd du temps à retrouver la bonne page, et risque d'appliquer une procédure obsolète.

MaintiDoc est un assistant documentaire multimodal : il accepte une question en français accompagnée d'une photo, retrouve les passages et figures pertinents dans un corpus autorisé, consulte l'historique de l'équipement via un outil MCP et peut préparer un ticket de maintenance. Il **ne prend aucune décision à la place du technicien** : il répond en citant ses sources, et toute action sensible passe par une validation humaine.

Le prototype couvre deux familles d'équipements d'un site industriel fictif :
- **Famille 1 : pompes centrifuges** (POMPE-A-01, POMPE-A-02, POMPE-B-01) ;
- **Famille 2 : compresseurs d'air** (COMP-A-01, COMP-A-02, COMP-B-02).

## 1.2 Utilisateurs visés

| Profil | Contexte d'utilisation | Besoins principaux | Groupe d'accès |
|---|---|---|---|
| Technicien pompes | Sur le terrain, smartphone ou tablette, mains occupées, temps limité | Comprendre un voyant ou une alarme, trouver la procédure à jour, connaître l'historique de la machine | `techniciens_pompes` |
| Technicien compresseurs | Idem, sur les compresseurs | Idem | `techniciens_compresseurs` |
| Responsable maintenance | Bureau, poste fixe | Vue d'ensemble des interventions, tickets ouverts, validation des tickets, accès aux documents internes (audits, budgets) | `responsables` |

## 1.3 Cas d'usage

**CU1 : Identifier un voyant à partir d'une photo.** Le technicien photographie le panneau de commande de POMPE-A-01 : « Que signifie ce voyant orange ? ». MaintiDoc identifie l'équipement, retrouve le tableau des codes d'alarme et la figure du panneau dans le manuel, puis répond en citant le document, la page et la figure.

**CU2 : Trouver la procédure à jour.** « Quel couple de serrage pour le couvercle de garniture de la pompe CP-50 ? ». Deux versions de la procédure existent dans le corpus avec des valeurs différentes. MaintiDoc doit signaler la contradiction, privilégier la version la plus récente et citer les deux.

**CU3 : Consulter l'historique d'un équipement.** « L'alarme de température est-elle déjà arrivée sur COMP-A-01 ? ». MaintiDoc appelle l'outil MCP `get_equipment_history`, croise le résultat avec la documentation et résume les interventions passées.

**CU4 : Préparer et créer un ticket avec approbation.** « Prépare un ticket pour cette alarme ». MaintiDoc rédige un brouillon (équipement, titre, description, sources). L'utilisateur voit le contenu exact et l'approuve. Le ticket n'est créé via MCP qu'après cette approbation, une seule fois.

**CU5 : Demander une clarification plutôt qu'inventer.** La photo est floue, ou le voyant orange pourrait appartenir aussi bien à une pompe qu'à un compresseur. MaintiDoc ne devine pas : il explique ce qui manque et demande, par exemple, une photo de la plaque signalétique.

## 1.4 Objectifs vérifiables en semaine 6

Chaque objectif se vérifie par un test concret, avec un résultat oui ou non. Les seuils chiffrés seront fixés en semaine 5.

| # | Objectif | Comment on le vérifie |
|---|---|---|
| O1 | Répondre à une question sur un voyant en citant le document, la page et, s'il y a lieu, la figure | La citation pointe vers un élément réellement récupéré et qui soutient la réponse |
| O2 | Exploiter une photo de panneau pour identifier l'équipement ou le voyant | Même question posée avec et sans photo : la photo apporte l'identification |
| O3 | Ne jamais retourner ni citer un document hors des groupes de l'utilisateur | Un technicien pompes interroge sur un document `responsables` : refus, aucun extrait affiché |
| O4 | Signaler une contradiction entre deux versions d'un document | Question sur le couple de serrage : les deux versions sont citées et l'écart est signalé |
| O5 | Consulter l'historique d'un équipement via l'outil MCP | Question CU3 : l'appel `get_equipment_history` est tracé, avec le bon `equipment_id` |
| O6 | Ne créer aucun ticket sans approbation explicite de l'utilisateur | Tentative de création sans approbation : rejet par le serveur MCP |
| O7 | Ne pas créer de doublon si la même approbation est envoyée deux fois | Double envoi : un seul ticket créé (clé d'idempotence) |
| O8 | Demander une clarification quand la photo est illisible ou les sources insuffisantes | Photo floue en entrée : statut `needs_clarification` et question posée |
| O9 | Ignorer une instruction malveillante contenue dans un document | Document piégé : aucun appel d'outil non prévu, aucune fuite |

## 1.5 Périmètre

| Élément | Dans le périmètre |
|---|---|
| Entrées | Question en français (anglais toléré), photo de panneau ou d'équipement, documents PDF du corpus |
| Sorties | Réponse sourcée (document, page, figure), demande de clarification, brouillon de ticket |
| Corpus | 30 à 50 documents synthétiques sur deux familles (pompes centrifuges, compresseurs d'air) |
| Outil MCP | Serveur de maintenance de démonstration : `get_equipment_history`, `get_open_tickets`, `create_ticket` |
| Action sensible | Création de ticket, uniquement après approbation explicite du contenu exact |
| Utilisateurs | Comptes fictifs répartis en 3 groupes : `techniciens_pompes`, `techniciens_compresseurs`, `responsables` |

**Hors périmètre (explicite) :**
- piloter ou commander une machine (aucune connexion aux automates) ;
- garantir un diagnostic : MaintiDoc est une aide documentaire, une ressemblance visuelle ne vaut pas un diagnostic ;
- intervenir de façon autonome : aucune action sans validation humaine ;
- remplacer les procédures de sécurité ou un technicien habilité ;
- traiter des données réelles : utilisateurs, tickets et historiques sont fictifs ;
- couvrir d'autres familles d'équipements que les deux retenues.

## 1.6 Hypothèses et contraintes

| Contrainte | Situation de l'équipe | Conséquence |
|---|---|---|
| Matériel | Pas de GPU local | Inférence sur Google Colab ou Kaggle (GPU T4, 16 Go, sessions limitées dans le temps). Qwen2.5-VL-7B quantifié en 4 bits, ou Qwen2.5-VL-3B en repli (à valider par test en semaine 3) |
| Mémoire | Environ 16 Go de VRAM au maximum | Une requête à la fois, taille d'image et contexte limités |
| Temps | 6 semaines, environ 10 h par personne et par semaine (à confirmer) | Priorité au scénario de démonstration, fonctionnalités secondaires en option |
| Équipe | 2 membres : Amr EL BELLAOUI, Soulaimane ELYOUNESSI | Rôles détaillés en partie 6 |
| Données | Corpus 100 % synthétique, généré avec un assistant IA puis relu | Traçabilité des prompts et relecture humaine obligatoires |
