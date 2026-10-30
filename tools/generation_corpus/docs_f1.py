"""Famille 1 : pompes centrifuges (MD-Pompes CP-50 et CM-80)."""
from ref import *
from common import cover, doc, FIG

D1 = "documents/famille_1"
GP = "techniciens_pompes ; responsables"
REV = "Amr"


def codes_rows():
    return [[c, l, s, v, r, a] for c, l, s, v, r, a in sorted(CODES_POMPES)]


# ------------------------------------------------------------------ Manuel CP-50
def manuel_cp50():
    c = CP50
    meta = dict(id="manuel_pompe_cp50", dossier=D1, titre="Manuel d'utilisation et de maintenance – pompe centrifuge MD-Pompes CP-50",
                famille="pompes", equipement_id="POMPE-A-01 ; POMPE-A-02", type_document="manuel", version="v2.1 (2025-03)",
                format="pdf_texte", prompt="P03", verifie_par=REV, groupe_acces=GP, usage_test="normal",
                remarques="Document de référence pompes ; voyant orange H2 décrit p.8, codes p.9 ; couple 35 N·m p.11 (cohérent avec proc v2)")
    pages = [
        cover("Pompe centrifuge MD-Pompes CP-50", "Manuel d'utilisation et de maintenance", [
            ["Modèle", "CP-50 (monocellulaire, aspiration axiale)"], ["Équipements du site", "POMPE-A-01, POMPE-A-02 (station SP1)"],
            ["Version du manuel", "v2.1 – mars 2025 (remplace v2.0 de 2023)"], ["Langue", "Français"],
            ["Référence document", "MDP-CP50-MAN-FR"]], extra=[("space", 0.5), ("h2", "Sommaire"),
            ("table", ["Chapitre", "Page"], [["1. Consignes de sécurité", "2"], ["2. Description et caractéristiques", "3"],
             ["3. Courbes de performance", "4"], ["4. Vue éclatée et nomenclature", "5"], ["5. Installation et alignement", "6"],
             ["6. Mise en service", "7"], ["7. Panneau de commande et voyants", "8"], ["8. Codes d'alarme", "9"],
             ["9. Maintenance préventive et lubrification", "10"], ["10. Garniture mécanique et couples de serrage", "11"],
             ["11. Diagnostic des pannes et pièces de rechange", "12"]], [4, 1], None, None)]),
        [("h1", "1. Consignes de sécurité"),
         ("p", "Toute intervention sur la pompe doit être réalisée par un technicien habilité, après consignation électrique et "
               "hydraulique de l'équipement (voir fiche de sécurité « Consignation des pompes »). Le non-respect de ces consignes "
               "peut entraîner des blessures graves."),
         ("box", "danger", "Ne jamais intervenir sur une pompe en marche ou simplement arrêtée depuis l'armoire : l'arrêt par le bouton S2 "
                           "ne constitue pas une consignation. Cadenasser le disjoncteur Q1 et fermer les vannes d'aspiration et de refoulement."),
         ("h2", "1.1 Risques identifiés"),
         ("ul", ["Risque électrique : moteur 400 V triphasé, intensité nominale " + c["intensite"] + ".",
                 "Risque de projection : fluide sous pression jusqu'à " + c["pression_max"] + ", température jusqu'à " + c["temp_fluide_max"] + ".",
                 "Risque mécanique : arbre et accouplement en rotation à " + c["vitesse"] + " ; le protège-accouplement doit être en place avant tout démarrage.",
                 "Risque de brûlure : les paliers peuvent dépasser 80 °C en fonctionnement (voir code P-21).",
                 "Risque de manutention : masse de l'ensemble pompe + moteur " + c["masse"] + " ; utiliser les anneaux de levage prévus."]),
         ("h2", "1.2 Équipements de protection individuelle"),
         ("p", "Chaussures de sécurité, gants anti-coupure, lunettes de protection. Gants thermiques pour toute intervention à moins "
               "de 30 minutes après l'arrêt. Protection auditive si la pompe fonctionne à proximité (niveau sonore ≈ 78 dB(A) à 1 m)."),
         ("h2", "1.3 Usage prévu"),
         ("p", "La CP-50 est destinée au pompage d'eau claire ou faiblement chargée (particules &lt; 2 mm), de pH 6 à 9. "
               "Tout autre fluide nécessite l'accord du constructeur. La pompe ne doit jamais fonctionner à sec, ni vanne de refoulement "
               "fermée pendant plus de 2 minutes.")],
        [("h1", "2. Description et caractéristiques"),
         ("p", "La CP-50 est une pompe centrifuge monocellulaire à aspiration axiale et refoulement radial vers le haut, accouplée à un "
               "moteur asynchrone par accouplement élastique. Le palier est lubrifié à l'huile (bain d'huile avec voyant de niveau)."),
         ("table", ["Caractéristique", "Valeur"], [
             ["Débit nominal", c["debit"]], ["Hauteur manométrique (HMT) nominale", c["hmt"]], ["Vitesse de rotation", c["vitesse"]],
             ["Puissance moteur", c["puissance"]], ["Alimentation", c["tension"]], ["Intensité nominale (In)", c["intensite"]],
             ["Pression maximale de service", c["pression_max"]], ["Température maximale du fluide", c["temp_fluide_max"]],
             ["NPSH requis au point nominal", c["npsh"]], ["Étanchéité d'arbre", c["garniture"]],
             ["Roulement côté accouplement", c["roulement_ca"]], ["Roulement côté pompe", c["roulement_cm"]],
             ["Lubrification palier", c["huile"] + ", " + c["volume_huile"]], ["Masse groupe complet", c["masse"]]],
          [1.3, 1.7], "Tableau 2.1 – Caractéristiques techniques de la CP-50", "tableau_2_1"),
         ("h2", "2.1 Plaque signalétique"),
         ("p", "La plaque signalétique est rivetée sur la lanterne, côté opposé au moteur. Elle indique le modèle, le numéro de série "
               "(format CP50-AA-NNNN, AA = année), le débit et la HMT nominaux. Le numéro de série est nécessaire pour toute commande de "
               "pièces et pour identifier l'équipement dans la GMAO (POMPE-A-01 = CP50-21-0457, POMPE-A-02 = CP50-21-0458).")],
        [("h1", "3. Courbes de performance"),
         ("p", "La figure 3.1 présente la hauteur manométrique, le rendement et le NPSH requis en fonction du débit, à 2900 tr/min. "
               "Le point de fonctionnement doit rester entre 60 % et 110 % du débit nominal (30 à 55 m³/h)."),
         ("fig", FIG + "courbe_cp50.png", 14.5, "Figure 3.1 – Courbes caractéristiques HMT, rendement et NPSH requis", "figure_3_1"),
         ("h2", "3.1 Risque de cavitation"),
         ("p", "Si le NPSH disponible de l'installation devient inférieur au NPSH requis augmenté d'une marge de 0,5 m, la pompe "
               "cavite : bruit de « graviers », chute de débit, vibrations et érosion de la roue. La pression d'aspiration est surveillée "
               "par l'automate ; en dessous de 0,3 bar pendant 10 s, le code P-41 est affiché (voir chapitre 8)."),
         ("box", "warn", "Un fonctionnement prolongé en cavitation détruit la roue et la garniture en quelques semaines.")],
        [("h1", "4. Vue éclatée et nomenclature"),
         ("fig", FIG + "vue_eclatee_cp50.png", 16, "Figure 4.1 – Vue éclatée simplifiée de la CP-50 (repères 1 à 10)", "figure_4_1"),
         ("table", ["Repère", "Désignation", "Référence pièce", "Remarque"], [
             ["1", "Corps volute", "CP50-101", "Fonte EN-GJL-250"], ["2", "Roue fermée Ø 210", "CP50-102", "Équilibrage G6.3"],
             ["3", "Écrou de roue M16", "CP50-103", "Couple 60 N·m, frein-filet"], ["4", "Garniture mécanique Ø 35", "GM-35-CP", "Voir chapitre 10"],
             ["5", "Couvercle de garniture", "CP50-105", "4 vis M10, couple 35 N·m"], ["6", "Lanterne / palier", "CP50-106", "Bain d'huile 0,4 L"],
             ["7", "Roulement côté accouplement", "6307 C3", "Remplacer par paire"], ["8", "Roulement côté pompe", "6306 C3", "Remplacer par paire"],
             ["9", "Accouplement élastique", "AE-42", "Élément élastique à contrôler tous les 6 mois"], ["10", "Moteur 7,5 kW", "MOT-75-2P", "IE3, 2 pôles"]],
          [0.6, 2, 1.3, 2.4], "Tableau 4.1 – Nomenclature des pièces principales", "tableau_4_1")],
        [("h1", "5. Installation et alignement"),
         ("p", "La pompe est livrée alignée en usine, mais l'alignement doit être contrôlé après fixation du socle, après raccordement des "
               "tuyauteries et après toute intervention sur le moteur ou les roulements. Un défaut d'alignement est la première cause "
               "d'usure prématurée des roulements et de vibrations (code P-50)."),
         ("fig", FIG + "alignement.png", 14, "Figure 5.1 – Contrôle de l'alignement au comparateur", "figure_5_1"),
         ("h2", "5.1 Tolérances"),
         ("table", ["Contrôle", "Tolérance", "Correction"], [
             ["Défaut radial (parallèle)", "≤ 0,05 mm", "Cales sous les pattes moteur"], ["Défaut angulaire", "≤ 0,05 mm / 100 mm", "Cales avant / arrière"],
             ["Jeu entre demi-accouplements", "3 ± 0,5 mm", "Déplacement axial du moteur"]], [2, 1.4, 2], "Tableau 5.1 – Tolérances d'alignement", "tableau_5_1"),
         ("p", "La procédure détaillée est décrite dans le document « Procédure d'alignement moteur-pompe ». Les tuyauteries ne doivent "
               "exercer aucun effort sur les brides de la pompe : elles sont supportées indépendamment.")],
        [("h1", "6. Mise en service"),
         ("ol", ["Vérifier que la consignation est levée et que le protège-accouplement est en place.",
                 "Vérifier le niveau d'huile du palier : il doit se situer au milieu du voyant de niveau.",
                 "Ouvrir complètement la vanne d'aspiration ; laisser la vanne de refoulement fermée.",
                 "Amorcer : ouvrir le purgeur du corps jusqu'à écoulement d'eau sans bulles d'air, puis le refermer.",
                 "Contrôler le sens de rotation par une brève impulsion (flèche sur la lanterne : sens horaire vu côté moteur).",
                 "Démarrer la pompe (bouton S1), puis ouvrir progressivement la vanne de refoulement dans les 2 minutes.",
                 "Relever la pression de refoulement, l'intensité (≤ 14,5 A) et la température palier après 30 minutes."]),
         ("box", "warn", "Ne jamais démarrer la pompe sans amorçage : la garniture mécanique est détruite en moins d'une minute à sec."),
         ("h2", "6.1 Valeurs normales en fonctionnement"),
         ("table", ["Grandeur", "Valeur normale", "Seuil d'alarme"], [
             ["Température palier", "45 à 70 °C", "80 °C (P-21) / 95 °C (P-22)"], ["Vibrations (vitesse RMS)", "&lt; 4,5 mm/s", "7,1 mm/s (P-50) / 11 mm/s (P-51)"],
             ["Pression d'aspiration", "0,6 à 1,5 bar", "&lt; 0,3 bar (P-41)"], ["Intensité moteur", "12 à 14,5 A", "&gt; 1,15 × In (P-10)"]],
          [1.6, 1.4, 2], "Tableau 6.1 – Valeurs de fonctionnement normales", "tableau_6_1")],
        [("h1", "7. Panneau de commande et voyants"),
         ("p", "L'armoire AP-SP1 regroupe la commande des deux pompes de la station. Chaque pompe dispose de quatre voyants et d'un "
               "afficheur qui indique le code d'alarme actif et la mesure associée."),
         ("fig", FIG + "panel_pompes.png", 12, "Figure 7.1 – Face avant de l'armoire : exemple d'affichage avec préalarme P-21 (H2 orange fixe)", "figure_7_1"),
         ("table", ["Voyant", "Couleur", "État", "Signification"], [[v, c_, m, s] for v, c_, m, s in VOYANTS_POMPES],
          [0.7, 0.9, 0.9, 4], "Tableau 7.1 – Signification des voyants", "tableau_7_1"),
         ("box", "info", "Le voyant orange H2 <b>fixe</b> signale une préalarme (la pompe continue de tourner) : lire le code sur l'afficheur. "
                         "H2 <b>clignotant</b> signale une maintenance due ou une fuite de garniture.")],
        [("h1", "8. Codes d'alarme"),
         ("p", "Les codes P-1x concernent le moteur, P-2x les paliers, P-30 la maintenance, P-4x l'hydraulique, P-5x les vibrations et P-60 "
               "l'étanchéité. Après correction de la cause, acquitter avec le bouton S3."),
         ("table", ["Code", "Libellé", "Condition", "Voyant", "Réaction", "Action recommandée"], codes_rows(),
          [0.6, 1.4, 1.4, 1.0, 0.7, 2.6], "Tableau 8.1 – Codes d'alarme de l'armoire pompes", "tableau_8_1")],
        [("h1", "9. Maintenance préventive et lubrification"),
         ("table", ["Périodicité", "Opération", "Référence"], [
             ["Hebdomadaire", "Contrôle visuel fuites, bruit, niveau d'huile palier", "Checklist d'inspection"],
             ["Mensuelle", "Relevé vibrations, température palier, intensité", "Checklist d'inspection"],
             ["2000 h (code P-30)", "Vidange huile palier, contrôle garniture, contrôle accouplement", "Procédure de vidange v2"],
             ["8000 h ou 2 ans", "Remplacement roulements 6307 C3 / 6306 C3", "Procédure roulements"],
             ["Selon état", "Remplacement garniture mécanique (fuite &gt; 10 gouttes/min)", "Procédure garniture"],
             ["Après intervention", "Contrôle alignement", "Procédure alignement"]], [1.2, 3, 1.6], "Tableau 9.1 – Plan de maintenance préventive", "tableau_9_1"),
         ("h2", "9.1 Lubrification du palier"),
         ("p", "Huile : " + c["huile"] + ". Volume : " + c["volume_huile"] + ". Le niveau se lit sur le voyant latéral, pompe arrêtée. "
               "Une huile noircie ou laiteuse (présence d'eau) impose une vidange immédiate et la recherche de la cause (garniture ou joint de "
               "palier). Ne jamais mélanger des huiles de marques ou de viscosités différentes."),
         ("h2", "9.2 Remise à zéro du compteur"),
         ("p", "Après l'entretien 2000 h, maintenir S3 appuyé 5 s jusqu'à l'affichage « CPT 0000 h ». Le voyant H2 cesse de clignoter.")],
        [("h1", "10. Garniture mécanique et couples de serrage"),
         ("fig", FIG + "coupe_garniture.png", 12.5, "Figure 10.1 – Coupe de la garniture mécanique simple Ø 35", "figure_10_1"),
         ("p", "Une légère humidité (quelques gouttes par heure) est normale au rodage. Au-delà de 10 gouttes par minute, le détecteur LS-102 "
               "déclenche le code P-60 et la garniture doit être remplacée. Ne jamais toucher les faces de frottement avec les doigts."),
         ("table", ["Assemblage", "Dimension", "Couple de serrage"], [
             ["Vis du couvercle de garniture", "M10 (×4)", "<b>35 N·m</b> (serrage en croix)"], ["Écrou de roue", "M16", "60 N·m + frein-filet"],
             ["Vis corps / lanterne", "M12 (×8)", "70 N·m"], ["Bouchon de vidange palier", "G 1/4", "25 N·m"], ["Boulons de socle", "M16", "120 N·m"]],
          [2, 1.2, 1.8], "Tableau 10.1 – Couples de serrage (valeurs v2.1, remplacent toute valeur antérieure)", "tableau_10_1"),
         ("box", "warn", "Depuis la version 2.0 du manuel (2023), le couple des vis du couvercle de garniture est de 35 N·m. Les anciennes "
                         "procédures indiquant 25 N·m sont obsolètes.")],
        [("h1", "11. Diagnostic des pannes et pièces de rechange"),
         ("table", ["Symptôme", "Causes probables", "Code associé"], [
             ["Débit insuffisant", "Vanne partiellement fermée, roue usée, sens de rotation inversé, air à l'aspiration", "P-41 possible"],
             ["Bruit de graviers", "Cavitation : NPSH disponible insuffisant, crépine colmatée", "P-41"],
             ["Palier chaud", "Manque d'huile, huile dégradée, roulement usé, défaut d'alignement", "P-21 / P-22"],
             ["Vibrations", "Désalignement, socle desserré, roue déséquilibrée, roulement usé", "P-50 / P-51"],
             ["Fuite à l'arbre", "Garniture usée, fonctionnement à sec, montage incorrect", "P-60"],
             ["Disjonction moteur", "Blocage roue, surcharge, défaut d'isolement", "P-10 / P-11"]], [1.3, 3.2, 1], "Tableau 11.1 – Aide au diagnostic", "tableau_11_1"),
         ("h2", "11.1 Pièces de rechange recommandées"),
         ("table", ["Référence", "Désignation", "Quantité conseillée en stock"], [
             ["GM-35-CP", "Garniture mécanique Ø 35", "2"], ["6307 C3 / 6306 C3", "Jeu de roulements", "1"], ["AE-42-E", "Élément élastique d'accouplement", "2"],
             ["JT-CP50", "Pochette de joints", "2"], ["MD-Lub P68", "Huile palier, bidon 2 L", "1"]], [1.4, 2.4, 1.6], "Tableau 11.2 – Pièces de rechange", "tableau_11_2")],
    ]
    return doc(meta, "MD-Pompes – Manuel CP-50", pages)


# ------------------------------------------------------------------ Manuel CM-80
def manuel_cm80():
    c = CM80
    meta = dict(id="manuel_pompe_cm80", dossier=D1, titre="Manuel d'utilisation – pompe multicellulaire MD-Pompes CM-80",
                famille="pompes", equipement_id="POMPE-B-01", type_document="manuel", version="v1.3 (2024-06)", format="pdf_texte",
                prompt="P04", verifie_par=REV, groupe_acces=GP, usage_test="normal",
                remarques="Même armoire et mêmes codes P-xx que la CP-50 ; lubrification à la graisse (pas d'huile)")
    pages = [
        cover("Pompe multicellulaire MD-Pompes CM-80", "Manuel d'utilisation et d'entretien", [
            ["Modèle", "CM-80, horizontale, 5 étages"], ["Équipement du site", "POMPE-B-01 (surpression eau process)"],
            ["Version", "v1.3 – juin 2024"], ["Référence", "MDP-CM80-MAN-FR"]],
            extra=[("space", 0.4), ("h2", "Sommaire"), ("table", ["Chapitre", "Page"], [["1. Sécurité", "2"], ["2. Caractéristiques", "3"],
                   ["3. Description et coupe", "4"], ["4. Mise en service", "5"], ["5. Voyants et alarmes", "6"], ["6. Entretien et graissage", "7"],
                   ["7. Diagnostic", "8"]], [4, 1], None, None)]),
        [("h1", "1. Sécurité"),
         ("p", "Les consignes de la fiche « Consignation des pompes » s'appliquent. La CM-80 fonctionne à des pressions élevées (jusqu'à "
               + c["pression_max"] + ") : avant toute ouverture, vérifier l'absence de pression résiduelle au manomètre de refoulement."),
         ("box", "danger", "Fluide jusqu'à 120 °C : risque de brûlure grave. Attendre le refroidissement sous 50 °C avant toute intervention."),
         ("ul", ["Consigner électriquement le départ moteur et cadenasser.", "Fermer et condamner les vannes d'aspiration et de refoulement.",
                 "Purger la pompe par le bouchon de vidange inférieur.", "Porter gants thermiques et visière."])],
        [("h1", "2. Caractéristiques"),
         ("table", ["Caractéristique", "Valeur"], [["Débit nominal", c["debit"]], ["HMT nominale", c["hmt"]], ["Nombre d'étages", c["etages"]],
             ["Vitesse", c["vitesse"]], ["Puissance moteur", c["puissance"]], ["Intensité nominale", c["intensite"]], ["Pression maximale", c["pression_max"]],
             ["Température maximale fluide", c["temp_fluide_max"]], ["Roulements", c["roulement"]], ["Lubrification", c["huile"]], ["Masse", c["masse"]]],
          [1.3, 1.7], "Tableau 2.1 – Caractéristiques techniques CM-80", "tableau_2_1"),
         ("p", "Numéro de série de POMPE-B-01 : CM80-22-0112. La CM-80 utilise la même armoire de commande et le même jeu de codes "
               "d'alarme P-xx que les pompes CP-50.")],
        [("h1", "3. Description et coupe"),
         ("fig", FIG + "coupe_cm80.png", 15.5, "Figure 3.1 – Coupe simplifiée de la CM-80 : 5 roues montées en série", "figure_3_1"),
         ("p", "Le fluide traverse successivement les cinq étages ; chaque étage ajoute environ 17 m de hauteur. La poussée axiale "
               "résultante est reprise par une butée à billes à contact oblique 7309 BEP côté accouplement."),
         ("p", "L'étanchéité est assurée par deux garnitures mécaniques (aspiration et refoulement) de type cartouche, interchangeables.")],
        [("h1", "4. Mise en service"),
         ("ol", ["Remplir complètement la pompe et la tuyauterie d'aspiration ; purger l'air par les bouchons supérieurs de chaque étage.",
                 "Vérifier la libre rotation de l'arbre à la main.",
                 "Démarrer vanne de refoulement entrouverte (environ 1/4).",
                 "Ouvrir progressivement jusqu'au point de fonctionnement ; ne jamais fonctionner vanne fermée plus de 1 minute.",
                 "Contrôler pression d'aspiration (≥ 0,5 bar recommandé) et intensité (≤ 27 A)."]),
         ("box", "warn", "Le débit minimal continu est de 6 m³/h. En dessous, l'échauffement du fluide dans la pompe peut provoquer une vaporisation.")],
        [("h1", "5. Voyants et alarmes"),
         ("p", "La CM-80 est raccordée à l'armoire de commande standard MD-Pompes. Les voyants H1 à H4 ont la même signification que pour la "
               "CP-50 : H2 orange fixe = préalarme avec code affiché, H2 orange clignotant = maintenance due ou fuite garniture."),
         ("table", ["Code", "Libellé", "Condition", "Voyant"], [[a, b, s, v] for a, b, s, v, _, _ in sorted(CODES_POMPES)],
          [0.7, 2.2, 2.2, 1.2], "Tableau 5.1 – Rappel des codes d'alarme", "tableau_5_1"),
         ("p", "Particularité CM-80 : le seuil de préalarme vibrations P-50 est également de 7,1 mm/s ; sur cette pompe, un desserrage des "
               "boulons de socle est la cause la plus fréquente.")],
        [("h1", "6. Entretien et graissage"),
         ("table", ["Périodicité", "Opération"], [["2000 h (P-30)", "Graissage des deux paliers : 15 g de MD-Grease EP2 par palier"],
             ["Mensuelle", "Contrôle vibrations, fuites aux garnitures, pression d'aspiration"], ["Trimestrielle", "Nettoyage de la crépine d'aspiration"],
             ["16 000 h", "Remplacement des roulements"]], [1, 3], "Tableau 6.1 – Entretien périodique CM-80", "tableau_6_1"),
         ("box", "warn", "Un excès de graisse provoque un échauffement du palier (code P-21). Respecter la quantité de 15 g par palier."),
         ("p", "Contrairement à la CP-50, la CM-80 ne comporte pas de bain d'huile : aucune vidange de palier n'est à réaliser.")],
        [("h1", "7. Diagnostic"),
         ("table", ["Symptôme", "Cause probable", "Remède"], [
             ["Pression de refoulement faible", "Air dans la pompe, étage usé", "Purger, contrôler les jeux d'étage"],
             ["P-41 pression aspiration basse", "Crépine colmatée, vanne fermée", "Nettoyer la crépine (voir historique)"],
             ["P-50 vibrations", "Socle desserré, désalignement", "Resserrer à 120 N·m, contrôler alignement"],
             ["P-21 palier chaud", "Excès ou manque de graisse", "Ajuster la quantité de graisse"]], [1.6, 1.8, 2], "Tableau 7.1 – Diagnostic CM-80", "tableau_7_1")],
    ]
    return doc(meta, "MD-Pompes – Manuel CM-80", pages)


# ------------------------------------------------------------------ Codes d'alarme
def codes_alarme_pompes():
    meta = dict(id="codes_alarme_pompes", dossier=D1, titre="Tableau des codes d'alarme et voyants – armoire pompes AP-SP1",
                famille="pompes", equipement_id="POMPE-A-01 ; POMPE-A-02 ; POMPE-B-01", type_document="codes_alarme", version="v3.0 (2025-05)",
                format="pdf_texte", prompt="P05", verifie_par=REV, groupe_acces=GP, usage_test="ambigu",
                remarques="Voyant orange fixe H2 : même couleur que L2 compresseur VS-37 mais sens différent (test d'ambiguïté)")
    pages = [
        [("h1", "Codes d'alarme et voyants – armoire pompes AP-SP1"),
         ("p", "Fiche à afficher dans le local de la station SP1 et le bâtiment chaufferie. Elle s'applique aux pompes POMPE-A-01, POMPE-A-02 "
               "(CP-50) et POMPE-B-01 (CM-80). Version 3.0 – mai 2025."),
         ("table", ["Voyant", "Couleur", "État", "Signification"], [[v, c_, m, s] for v, c_, m, s in VOYANTS_POMPES],
          [0.7, 0.9, 0.9, 4], "Tableau 1 – Voyants de l'armoire pompes", "tableau_1"),
         ("fig", FIG + "panel_pompes.png", 10.5, "Figure 1 – Disposition des voyants H1 à H4 et de l'afficheur", "figure_1"),
         ("box", "warn", "Ne pas confondre avec le contrôleur des compresseurs VS-37, dont le voyant orange L2 a une signification différente.")],
        [("h1", "Liste des codes"),
         ("table", ["Code", "Libellé", "Condition", "Voyant", "Réaction", "Action"], codes_rows(),
          [0.6, 1.4, 1.4, 1.0, 0.7, 2.6], "Tableau 2 – Codes d'alarme P-xx", "tableau_2")],
        [("h1", "Conduite à tenir"),
         ("ol", ["Lire le code sur l'afficheur avant tout acquittement (le code disparaît après S3).",
                 "Noter le code, la mesure affichée et l'heure dans le cahier de quart.",
                 "Si voyant rouge H3 : ne pas redémarrer avant d'avoir identifié la cause.",
                 "Si voyant orange H2 fixe : la pompe continue de fonctionner ; planifier un contrôle dans la journée.",
                 "Si deux préalarmes successives du même code en moins de 30 jours : créer un ticket de maintenance corrective.",
                 "Pour POMPE-A-01 et POMPE-A-02, basculer sur la pompe de secours si une intervention est nécessaire."]),
         ("h2", "Hiérarchie des alarmes"),
         ("p", "Rouge (arrêt) &gt; bleu (arrêt sur manque d'eau) &gt; orange fixe (préalarme) &gt; orange clignotant (information maintenance). "
               "Si plusieurs codes sont actifs, l'afficheur fait défiler les codes toutes les 3 secondes, du plus grave au moins grave.")],
    ]
    return doc(meta, "Armoire pompes AP-SP1 – Codes d'alarme", pages)


# ------------------------------------------------------------------ Procédures vidange (contradictoires)
def proc_vidange(ver):
    v1 = ver == "v1"
    couple = COUPLE_COUVERCLE_GARNITURE[ver]
    meta = dict(id=f"proc_vidange_cp50_{ver}", dossier=D1,
                titre=f"Procédure de vidange palier et contrôle garniture – pompe CP-50 ({ver})", famille="pompes",
                equipement_id="POMPE-A-01 ; POMPE-A-02", type_document="procedure",
                version="v1 (2023-06)" if v1 else "v2 (2025-02)", format="pdf_scanne" if v1 else "pdf_texte",
                prompt="P06", verifie_par=REV, groupe_acces="techniciens_pompes ; responsables", usage_test="contradictoire",
                remarques=("Version obsolète scannée ; couple couvercle garniture 25 N·m, contredit proc_vidange_cp50_v2 (35 N·m)" if v1 else
                           "Version en vigueur ; couple 35 N·m, contredit proc_vidange_cp50_v1 (25 N·m) ; cohérente avec le manuel p.11"))
    pages = [
        [("h1", f"PROCÉDURE PM-CP50-02 – Vidange palier et contrôle garniture ({ver})"),
         ("table", ["Rubrique", "Valeur"], [["Équipements", "POMPE-A-01, POMPE-A-02 (CP-50)"], ["Déclencheur", "Code P-30 (2000 h) ou huile dégradée"],
             ["Durée estimée", "1 h 30"], ["Habilitation", "Mécanicien niveau 1 + consignation"], ["Date d'application", "juin 2023" if v1 else "février 2025"],
             ["Statut", "Remplacée par v2 (02/2025)" if v1 else "En vigueur – annule et remplace v1 (06/2023)"]], [1, 2.2], None, None),
         ("h2", "Matériel"),
         ("ul", ["Huile " + CP50["huile"] + ", " + CP50["volume_huile"], "Bac de récupération 2 L, chiffons", "Clé dynamométrique 10–60 N·m",
                 "Joint de bouchon de vidange neuf", "Lampe, miroir d'inspection"]),
         ("h2", "1. Préparation"),
         ("ol", ["Basculer la production sur la pompe de secours.", "Consigner la pompe (fiche FS-P-01) : Q1 cadenassé, vannes fermées.",
                 "Attendre que la température du palier soit inférieure à 40 °C."])],
        [("h2", "2. Vidange du palier"),
         ("ol", ["Placer le bac sous le bouchon de vidange du palier.", "Déposer le bouchon de remplissage puis le bouchon de vidange.",
                 "Laisser s'écouler complètement (environ 10 minutes). Observer l'huile : couleur, présence d'eau ou de particules.",
                 "Remonter le bouchon de vidange avec un joint neuf, couple 25 N·m.",
                 "Remplir avec 0,4 L d'huile ISO VG 68 jusqu'au milieu du voyant de niveau."]),
         ("fig", FIG + "coupe_garniture.png", 10, "Schéma 1 – Repérage de la garniture et du couvercle (rep. D)", "schema_1"),
         ("h2", "3. Contrôle de la garniture"),
         ("ol", ["Déposer le protège-accouplement.", "Inspecter la zone de la garniture : traces de fuite, cristaux, dépôts.",
                 "Contrôler le serrage des 4 vis du couvercle de garniture (rep. D) à la clé dynamométrique : <b>" + couple + "</b>, en croix.",
                 "Remonter le protège-accouplement."])],
        [("h2", "4. Remise en service"),
         ("ol", ["Déconsigner selon FS-P-01.", "Amorcer et démarrer la pompe (manuel CP-50, chapitre 6).",
                 "Vérifier l'absence de fuite après 15 minutes de fonctionnement.",
                 "Remettre le compteur d'heures à zéro (S3 appuyé 5 s).", "Renseigner l'intervention dans la GMAO (code P-30)."]),
         ("h2", "5. Critères d'acceptation"),
         ("table", ["Contrôle", "Critère"], [["Fuite garniture", "&lt; 10 gouttes / min"], ["Température palier après 30 min", "&lt; 70 °C"],
                                            ["Couple vis couvercle", couple]], [2, 2], None, None)] +
        ([("box", "warn", "Version 1 – juin 2023. Document archivé (copie papier scannée).")] if v1 else
         [("box", "info", "Modification v2 : le couple de serrage des vis du couvercle de garniture passe de 25 N·m à 35 N·m suite à la mise à jour "
                          "du manuel constructeur (v2.0). Des desserrages avaient été constatés avec l'ancienne valeur.")]),
    ]
    return doc(meta, f"PM-CP50-02 – Vidange palier CP-50 ({ver})", pages)


# ------------------------------------------------------------------ Autres procédures
def proc_amorcage():
    meta = dict(id="proc_amorcage_demarrage_pompes", dossier=D1, titre="Procédure d'amorçage et de démarrage des pompes de la station SP1",
                famille="pompes", equipement_id="POMPE-A-01 ; POMPE-A-02", type_document="procedure", version="v2 (2024-09)",
                format="pdf_texte", prompt="P07", verifie_par=REV, groupe_acces=GP, usage_test="normal", remarques="Réamorçage après code P-40")
    pages = [
        [("h1", "PROCÉDURE PE-SP1-01 – Amorçage et démarrage"),
         ("p", "Applicable après une vidange, une intervention sur la pompe ou un arrêt sur manque d'eau (code P-40, voyant bleu H4)."),
         ("fig", FIG + "pid_station.png", 15, "Figure 1 – Station SP1 : bâche T-101, vannes V-101 / V-111, clapets, capteur PT-103", "figure_1"),
         ("h2", "1. Vérifications préalables"),
         ("ul", ["Niveau de la bâche T-101 au-dessus du niveau bas LSL-101 (voyant H4 éteint).", "Vanne d'aspiration (V-101 ou V-111) ouverte.",
                 "Niveau d'huile palier correct.", "Protège-accouplement en place."])],
        [("h2", "2. Amorçage"),
         ("ol", ["Ouvrir le purgeur situé au sommet du corps de pompe.", "Laisser l'eau s'écouler jusqu'à disparition complète des bulles d'air.",
                 "Faire tourner l'arbre à la main de quelques tours pour chasser l'air piégé dans la roue.", "Refermer le purgeur."]),
         ("h2", "3. Démarrage"),
         ("ol", ["Vanne de refoulement fermée, démarrer par S1.", "Vérifier la montée en pression sur le manomètre PI (environ 3,9 bar à débit nul).",
                 "Ouvrir progressivement la vanne de refoulement en moins de 2 minutes.", "Contrôler l'intensité (≤ 14,5 A)."]),
         ("box", "warn", "Si la pression ne monte pas dans les 10 secondes, arrêter immédiatement : la pompe n'est pas amorcée.")],
        [("h2", "4. Après un arrêt sur manque d'eau (P-40)"),
         ("p", "Identifier la cause de la baisse de niveau (vanne d'appoint, flotteur, consommation anormale) avant tout redémarrage. "
               "Après rétablissement du niveau, refaire l'amorçage complet : l'aspiration a pu se désamorcer."),
         ("h2", "5. Basculement pompe principale / secours"),
         ("ol", ["Démarrer la pompe de secours selon les étapes 2 et 3.", "Une fois la pression stabilisée, arrêter la pompe principale.",
                 "Fermer la vanne d'aspiration de la pompe arrêtée si une intervention est prévue."])],
    ]
    return doc(meta, "PE-SP1-01 – Amorçage et démarrage", pages)


def proc_alignement():
    meta = dict(id="proc_alignement_accouplement", dossier=D1, titre="Procédure d'alignement moteur-pompe au comparateur",
                famille="pompes", equipement_id="POMPE-A-01 ; POMPE-A-02 ; POMPE-B-01", type_document="procedure", version="v1.1 (2024-01)",
                format="pdf_texte", prompt="P07", verifie_par=REV, groupe_acces=GP, usage_test="normal", remarques="")
    pages = [
        [("h1", "PROCÉDURE PM-POM-05 – Alignement moteur-pompe"),
         ("p", "À réaliser après remplacement de roulements, intervention sur le moteur, ou en cas de vibrations élevées (code P-50)."),
         ("fig", FIG + "alignement.png", 14.5, "Figure 1 – Montage des comparateurs radial (R) et axial (A)", "figure_1"),
         ("h2", "Outillage"), ("ul", ["2 comparateurs à cadran 1/100 mm avec supports magnétiques", "Jeu de cales pelables inox", "Clé dynamométrique"])],
        [("h2", "Mode opératoire"),
         ("ol", ["Consigner la pompe et déposer le protège-accouplement.", "Fixer les supports sur le demi-accouplement côté moteur.",
                 "Positionner le comparateur radial sur la jante et l'axial sur la face du demi-accouplement pompe ; mettre à zéro à 12 h.",
                 "Faire tourner les deux arbres ensemble et relever les valeurs à 3 h, 6 h et 9 h.",
                 "Calculer les corrections verticales (cales) puis horizontales (déplacement latéral du moteur).",
                 "Resserrer les pattes moteur au couple et refaire une série de mesures."]),
         ("table", ["Contrôle", "Tolérance"], [["Radial", "≤ 0,05 mm"], ["Angulaire", "≤ 0,05 mm / 100 mm"], ["Jeu axial accouplement", "3 ± 0,5 mm"]],
          [2, 2], "Tableau 1 – Tolérances (identiques au manuel CP-50, tableau 5.1)", "tableau_1"),
         ("p", "Consigner les valeurs finales dans la GMAO (exemple : « réalignement 0,04 mm »).")],
        [("h2", "Erreurs fréquentes"),
         ("ul", ["Oublier de contrôler le « pied boiteux » : une patte qui ne porte pas fausse toutes les mesures (tolérance 0,05 mm).",
                 "Aligner à froid une pompe véhiculant de l'eau chaude sans tenir compte de la dilatation (CM-80 : prévoir + 0,10 mm côté pompe).",
                 "Serrer les boulons de socle sans clé dynamométrique (120 N·m pour M16)."]),
         ("box", "info", "Un alignement correct réduit fortement l'usure des roulements et les préalarmes P-21 et P-50.")],
    ]
    return doc(meta, "PM-POM-05 – Alignement", pages)


def proc_roulements():
    meta = dict(id="proc_remplacement_roulements_cp50", dossier=D1, titre="Procédure de remplacement des roulements – pompe CP-50",
                famille="pompes", equipement_id="POMPE-A-01 ; POMPE-A-02", type_document="procedure", version="v1 (2024-04)", format="pdf_texte",
                prompt="P07", verifie_par=REV, groupe_acces=GP, usage_test="normal", remarques="Utilisée lors de INT-2026-0098 (POMPE-A-01)")
    pages = [
        [("h1", "PROCÉDURE PM-CP50-04 – Remplacement des roulements"),
         ("table", ["Rubrique", "Valeur"], [["Équipements", "POMPE-A-01, POMPE-A-02"], ["Déclencheurs", "P-21 répétées, P-22, bruit, 8000 h"],
             ["Pièces", "Roulements 6307 C3 (côté accouplement) et 6306 C3 (côté pompe), joints à lèvre"], ["Durée", "4 à 5 h"]], [1, 2.4], None, None),
         ("fig", FIG + "vue_eclatee_cp50.png", 15, "Figure 1 – Repères 6, 7 et 8 : lanterne-palier et roulements", "figure_1"),
         ("h2", "1. Dépose"),
         ("ol", ["Consigner (FS-P-01), vidanger le palier (procédure PM-CP50-02).", "Déposer le moteur et le demi-accouplement (extracteur).",
                 "Déposer l'ensemble rotatif côté arrière (conception « back pull-out » : le corps reste sur la tuyauterie)."])],
        [("ol", ["Déposer la roue (écrou M16, filetage à droite) et la garniture mécanique.", "Extraire l'arbre du palier, puis les roulements à la presse.",
                 "Nettoyer le logement, contrôler l'arbre (portées : tolérance k5)."]),
         ("h2", "2. Montage"),
         ("ol", ["Chauffer les roulements neufs à 90 °C maximum au chauffe-roulement à induction (jamais à la flamme).",
                 "Monter les roulements en butée sur l'épaulement de l'arbre ; laisser refroidir.", "Remonter joints à lèvre neufs, arbre, garniture neuve.",
                 "Remonter la roue (60 N·m + frein-filet) et le couvercle de garniture (35 N·m).", "Remonter l'ensemble, refaire le plein d'huile (0,4 L)."])],
        [("h2", "3. Contrôles finaux"),
         ("ol", ["Réaliser l'alignement (PM-POM-05).", "Amorcer, démarrer, surveiller la température palier pendant 2 h : elle peut atteindre 75 °C "
                 "pendant le rodage puis doit redescendre sous 70 °C.", "Mesurer les vibrations : &lt; 4,5 mm/s."]),
         ("box", "warn", "Toujours remplacer les deux roulements ensemble, ainsi que la garniture mécanique démontée."),
         ("h2", "4. Traçabilité"), ("p", "Indiquer dans la GMAO les références et numéros de lot des roulements montés.")],
        [("h2", "Annexe – Signes d'usure des roulements"),
         ("table", ["Constat", "Cause probable"], [["Écaillage piste extérieure", "Fatigue normale, surcharge"], ["Traces de corrosion", "Eau dans l'huile (garniture)"],
             ["Coloration bleue", "Échauffement : manque d'huile"], ["Marques régulières (brinelling)", "Vibrations à l'arrêt, mauvais montage"]],
          [2, 2], "Tableau A.1 – Diagnostic visuel", "tableau_a_1")],
    ]
    return doc(meta, "PM-CP50-04 – Roulements CP-50", pages)


def proc_garniture():
    meta = dict(id="proc_remplacement_garniture_cp50", dossier=D1, titre="Procédure de remplacement de la garniture mécanique – pompe CP-50",
                famille="pompes", equipement_id="POMPE-A-01 ; POMPE-A-02", type_document="procedure", version="v2 (2025-02)", format="pdf_texte",
                prompt="P07", verifie_par=REV, groupe_acces=GP, usage_test="normal", remarques="Couple 35 N·m cohérent avec manuel v2.1 et proc_vidange v2")
    pages = [
        [("h1", "PROCÉDURE PM-CP50-03 – Remplacement de la garniture mécanique"),
         ("p", "Déclencheur : code P-60 (fuite garniture, voyant H2 orange clignotant) avec fuite constatée supérieure à 10 gouttes/min."),
         ("fig", FIG + "coupe_garniture.png", 13, "Figure 1 – Garniture mécanique Ø 35 : grain tournant (A), grain fixe (B), ressort (C), couvercle (D)", "figure_1"),
         ("h2", "Pièces"), ("ul", ["Garniture mécanique GM-35-CP", "Joint torique de couvercle", "Pochette de joints JT-CP50"])],
        [("h2", "Mode opératoire"),
         ("ol", ["Consigner (FS-P-01) et vidanger le corps de pompe.", "Déposer l'ensemble rotatif (back pull-out), puis la roue.",
                 "Déposer le couvercle de garniture (4 vis M10) et extraire le grain fixe.", "Retirer la partie tournante en desserrant les vis de blocage.",
                 "Nettoyer l'arbre, vérifier l'absence de rayure à l'emplacement des joints.",
                 "Monter la partie tournante neuve, lubrifiée à l'eau savonneuse (jamais de graisse sur les faces).",
                 "Monter le grain fixe dans le couvercle, à la main, sans toucher la face de frottement.",
                 "Serrer les 4 vis du couvercle en croix à <b>35 N·m</b>.", "Remonter la roue et l'ensemble ; amorcer avant tout démarrage."])],
        [("h2", "Essais"),
         ("ul", ["Fuite tolérée pendant le rodage (1 h) : quelques gouttes par minute.", "Après rodage : pas de fuite visible.",
                 "Si la fuite persiste au-delà de 2 h : vérifier le montage et l'état de surface de l'arbre."]),
         ("box", "danger", "Ne jamais faire fonctionner la pompe à sec, même quelques secondes, après remplacement de la garniture."),
         ("h2", "Historique des révisions"), ("table", ["Version", "Date", "Modification"], [["v1", "2022-05", "Création"],
             ["v2", "2025-02", "Couple vis de couvercle porté à 35 N·m (manuel v2.0)"]], [0.6, 0.8, 3], None, None)],
        [("h2", "Annexe – Causes de défaillance des garnitures"),
         ("table", ["Constat sur la garniture déposée", "Cause probable", "Action"], [
             ["Faces rayées radialement", "Particules dans le fluide", "Vérifier la filtration"], ["Faces brûlées / fissurées", "Marche à sec", "Vérifier amorçage, niveau bâche"],
             ["Usure irrégulière", "Désalignement, vibrations", "Contrôler alignement et roulements"], ["Joint torique gonflé", "Incompatibilité chimique", "Vérifier le fluide"]],
          [2, 1.6, 2], "Tableau A.1 – Analyse des garnitures déposées", "tableau_a_1")],
    ]
    return doc(meta, "PM-CP50-03 – Garniture CP-50", pages)


def fiche_consignation():
    meta = dict(id="fiche_securite_consignation_pompes", dossier=D1, titre="Fiche de sécurité FS-P-01 – Consignation des pompes",
                famille="pompes", equipement_id="POMPE-A-01 ; POMPE-A-02 ; POMPE-B-01", type_document="fiche_securite", version="v4 (2025-01)",
                format="pdf_texte", prompt="P08", verifie_par=REV, groupe_acces=GP, usage_test="normal", remarques="")
    pages = [
        [("h1", "FICHE DE SÉCURITÉ FS-P-01 – Consignation des pompes"),
         ("box", "danger", "Aucune intervention mécanique sans consignation complète, électrique ET hydraulique, vérifiée par l'intervenant lui-même."),
         ("h2", "1. Consignation électrique"),
         ("ol", ["Arrêter la pompe par S2.", "Ouvrir le disjoncteur Q1 du départ concerné dans l'armoire AP-SP1.",
                 "Poser le cadenas personnel et l'étiquette « Ne pas manœuvrer – intervention en cours » (nom, date).",
                 "Vérifier l'absence de tension (VAT) par une personne habilitée électriquement.", "Tenter un démarrage par S1 : la pompe ne doit pas démarrer."]),
         ("h2", "2. Consignation hydraulique"),
         ("ol", ["Fermer la vanne d'aspiration et la vanne de refoulement, les condamner (chaîne + cadenas).", "Ouvrir le purgeur et vérifier l'absence de pression.",
                 "Vidanger le corps si l'intervention l'impose ; récupérer le fluide."])],
        [("h2", "3. Déconsignation"),
         ("ol", ["Vérifier que tout le personnel est sorti de la zone et que les protections sont remontées.", "Retirer les condamnations hydrauliques, ouvrir l'aspiration.",
                 "Chaque intervenant retire son propre cadenas.", "Refermer Q1. Amorcer et redémarrer selon PE-SP1-01."]),
         ("h2", "4. EPI obligatoires"), ("table", ["Situation", "EPI"], [["Toute intervention", "Chaussures, gants, lunettes"],
             ["Fluide chaud (CM-80)", "Gants thermiques, visière"], ["Mesure électrique", "EPI électriques selon habilitation"]], [1.5, 2.5], None, None),
         ("p", "Le cadenas est personnel : il ne peut jamais être retiré par une autre personne que son propriétaire, sauf procédure exceptionnelle "
               "validée par le responsable maintenance.")],
    ]
    return doc(meta, "FS-P-01 – Consignation des pompes", pages)


def fds_huile():
    meta = dict(id="fiche_securite_huile_p68", dossier=D1, titre="Fiche de données de sécurité (simplifiée) – huile MD-Lub P68",
                famille="pompes", equipement_id="POMPE-A-01 ; POMPE-A-02", type_document="fiche_securite", version="v1 (2024-11)", format="pdf_texte",
                prompt="P08", verifie_par=REV, groupe_acces=GP, usage_test="normal", remarques="Produit fictif ; structure inspirée des 16 rubriques d'une FDS")
    pages = [
        [("h1", "FDS simplifiée – MD-Lub P68 (huile minérale ISO VG 68)"),
         ("box", "info", "Produit fictif. Cette fiche reprend la structure d'une FDS réglementaire à des fins pédagogiques uniquement."),
         ("table", ["Rubrique", "Contenu"], [
             ["1. Identification", "MD-Lub P68 – huile hydraulique et de palier, usage industriel"],
             ["2. Dangers", "Non classé dangereux. Peut provoquer une irritation cutanée en cas de contact prolongé."],
             ["3. Composition", "Huile de base minérale hautement raffinée &gt; 95 %, additifs anti-usure et anti-oxydants"],
             ["4. Premiers secours", "Peau : laver à l'eau et au savon. Yeux : rincer 15 min. Ingestion : ne pas faire vomir, consulter un médecin."],
             ["5. Incendie", "Moyens d'extinction : poudre, CO2, mousse. Ne pas utiliser de jet d'eau direct."],
             ["6. Déversement", "Contenir avec absorbant, éviter les égouts, récupérer en fût étiqueté."],
             ["7. Stockage", "Local ventilé, à l'abri de la chaleur, sur rétention, entre 0 et 40 °C."],
             ["8. Protection", "Gants nitrile, lunettes."]], [1, 3], "Tableau 1 – Rubriques 1 à 8", "tableau_1")],
        [("table", ["Rubrique", "Contenu"], [
             ["9. Propriétés", "Liquide ambré ; viscosité 68 mm²/s à 40 °C ; point d'éclair &gt; 220 °C ; densité 0,87"],
             ["10. Stabilité", "Stable. Éviter oxydants forts."], ["11. Toxicologie", "Faible toxicité aiguë."],
             ["12. Écologie", "Peu biodégradable : ne pas rejeter dans l'environnement."],
             ["13. Élimination", "Huile usagée : collecte par un éliminateur agréé (déchet dangereux 13 01 10*)."],
             ["14. Transport", "Non réglementé."], ["15. Réglementation", "Sans objet (produit fictif)."], ["16. Autres", "Version 1 – novembre 2024."]],
          [1, 3], "Tableau 2 – Rubriques 9 à 16", "tableau_2"),
         ("h2", "Consignes atelier"),
         ("ul", ["Les huiles usagées issues des vidanges de palier sont versées dans le fût « huiles usagées » du local SP1.",
                 "Ne jamais mélanger la MD-Lub P68 avec la graisse EP2 utilisée sur la CM-80.", "Absorbants usagés : benne déchets souillés."])],
        [("h2", "Pictogrammes et étiquetage"),
         ("p", "Le produit n'étant pas classé, aucun pictogramme de danger n'est requis. L'étiquette du bidon indique le nom commercial, la viscosité, "
               "le numéro de lot et la date de fabrication. Durée de conservation : 5 ans en emballage d'origine fermé."),
         ("h2", "Compatibilité"),
         ("table", ["Matériau", "Compatibilité"], [["Joints NBR", "Bonne"], ["Joints FKM (Viton)", "Bonne"], ["Joints EPDM", "Mauvaise – ne pas utiliser"]],
          [2, 2], "Tableau 3 – Compatibilité avec les élastomères", "tableau_3")],
    ]
    return doc(meta, "FDS – MD-Lub P68", pages)


def schema_vue_eclatee():
    meta = dict(id="schema_vue_eclatee_cp50", dossier=D1, titre="Schéma – vue éclatée et nomenclature de la pompe CP-50", famille="pompes",
                equipement_id="POMPE-A-01 ; POMPE-A-02", type_document="schema", version="v2 (2025-03)", format="pdf_texte", prompt="P09",
                verifie_par=REV, groupe_acces=GP, usage_test="normal", remarques="Repères identiques au manuel (figure 4.1)")
    pages = [
        [("h1", "Vue éclatée CP-50 – planche MDP-CP50-PL01"),
         ("fig", FIG + "vue_eclatee_cp50.png", 17, "Planche 1 – Vue éclatée, repères 1 à 10", "planche_1"),
         ("table", ["Rep.", "Désignation", "Réf."], [["1", "Corps volute", "CP50-101"], ["2", "Roue fermée Ø 210", "CP50-102"], ["3", "Écrou de roue M16", "CP50-103"],
             ["4", "Garniture mécanique Ø 35", "GM-35-CP"], ["5", "Couvercle de garniture", "CP50-105"]], [0.5, 2.5, 1.2], None, None)],
        [("h1", "Détail garniture et couples"),
         ("fig", FIG + "coupe_garniture.png", 13, "Planche 2 – Détail de la garniture mécanique (rep. 4 et 5)", "planche_2"),
         ("table", ["Rep.", "Désignation", "Réf."], [["6", "Lanterne / palier", "CP50-106"], ["7", "Roulement CA", "6307 C3"], ["8", "Roulement CP", "6306 C3"],
             ["9", "Accouplement élastique", "AE-42"], ["10", "Moteur 7,5 kW", "MOT-75-2P"]], [0.5, 2.5, 1.2], None, None)],
    ]
    return doc(meta, "Planche MDP-CP50-PL01", pages)


def schema_pid():
    meta = dict(id="schema_pid_station_sp1", dossier=D1, titre="Schéma P&ID simplifié – station de pompage SP1", famille="pompes",
                equipement_id="POMPE-A-01 ; POMPE-A-02", type_document="schema", version="v1 (2023-02)", format="pdf_texte", prompt="P09",
                verifie_par=REV, groupe_acces=GP, usage_test="normal", remarques="Repères LSL-101, PT-103 utilisés par les codes P-40 et P-41")
    pages = [[("h1", "P&ID simplifié – Station SP1"),
              ("fig", FIG + "pid_station.png", 17, "Figure 1 – Bâche T-101, pompes POMPE-A-01 et POMPE-A-02, vannes, clapets et instrumentation", "figure_1"),
              ("table", ["Repère", "Désignation", "Lien alarme"], [["LSL-101", "Détecteur niveau bas bâche", "P-40"], ["PT-103", "Transmetteur pression refoulement", "—"],
                  ["PI", "Manomètres d'aspiration", "P-41 (capteur associé PT-100)"], ["V-101 / V-111", "Vannes d'aspiration", "—"], ["CL", "Clapets anti-retour", "—"]],
               [1, 2.5, 2], "Tableau 1 – Instrumentation", "tableau_1")]]
    return doc(meta, "P&ID station SP1", pages)


def schema_elec():
    meta = dict(id="schema_electrique_armoire_pompes", dossier=D1, titre="Schéma électrique simplifié – armoire AP-SP1", famille="pompes",
                equipement_id="POMPE-A-01 ; POMPE-A-02", type_document="schema", version="v2 (2024-05)", format="pdf_texte", prompt="P09",
                verifie_par=REV, groupe_acces=GP, usage_test="normal", remarques="")
    pages = [
        [("h1", "Armoire AP-SP1 – schéma de puissance et de commande"),
         ("fig", FIG + "elec_armoire_pompes.png", 17, "Folio 1 – Départs moteurs Q1/KM1/F1 et circuit de commande 24 V des voyants H1 à H4", "folio_1"),
         ("box", "danger", "Intervention réservée au personnel habilité électriquement (BR / B2V). Schéma simplifié, non contractuel.")],
        [("h1", "Folio 2 – Entrées / sorties automate"),
         ("table", ["Adresse", "Signal", "Utilisation"], [["I0.0", "Sonde PTC moteur", "P-11"], ["I0.1", "LS-102 détecteur fuite", "P-60"],
             ["I0.2", "LSL-101 niveau bas", "P-40"], ["IW64", "PT-100 pression aspiration 4-20 mA", "P-41"], ["IW66", "TT-105 température palier", "P-21 / P-22"],
             ["IW68", "VT-104 vibrations 4-20 mA", "P-50 / P-51"], ["IW70", "Transformateur de courant", "P-10"],
             ["Q0.0 – Q0.3", "Voyants H1 à H4", "—"]], [1, 2.5, 1.5], "Tableau 1 – Table des entrées / sorties", "tableau_1")],
    ]
    return doc(meta, "Schéma électrique AP-SP1", pages)


def historique(eq, prompt):
    rows = [[i, d, t, c, de, a, str(h).replace(".", ","), tec, s] for i, d, t, c, de, a, h, tec, s in HISTORIQUES[eq]]
    tk = TICKETS_OUVERTS.get(eq, [])
    e = EQUIPEMENTS[eq]
    meta = dict(id=f"historique_{eq.lower().replace('-', '_')}", dossier=D1 if e["famille"] == "pompes" else "documents/famille_2",
                titre=f"Historique des interventions – {eq} (export GMAO)", famille=e["famille"], equipement_id=eq, type_document="historique",
                version="export 2026-10-15", format="pdf_texte", prompt=prompt, verifie_par=REV if e["famille"] == "pompes" else "Soulaimane",
                groupe_acces=("techniciens_pompes" if e["famille"] == "pompes" else "techniciens_compresseurs") + " ; responsables",
                usage_test="normal", remarques="Identifiants INT-/TCK- identiques aux données du serveur MCP de démonstration")
    pages = [[("h1", f"Historique des interventions – {eq}"),
              ("table", ["Champ", "Valeur"], [["Équipement", f"{eq} – {e['marque']} {e['modele']}"], ["N° de série", e["serie"]], ["Mise en service", str(e["annee"])],
                                              ["Localisation", e["lieu"]], ["Période exportée", "2024-01-01 → 2026-10-15"]], [1, 3], None, None),
              ("table", ["N° intervention", "Date", "Type", "Code", "Constat", "Action réalisée", "h", "Tech.", "Statut"], rows,
               [1.45, 1.25, 1.1, 0.7, 1.65, 2.15, 0.6, 0.8, 0.95], "Tableau 1 – Interventions", "tableau_1")] +
             ([("h2", "Tickets ouverts"), ("table", ["Ticket", "Date", "Objet", "Statut"], [list(t) for t in tk], [1, 0.8, 3, 1], "Tableau 2 – Tickets ouverts", "tableau_2")] if tk else
              [("p", "Aucun ticket ouvert à la date de l'export.")]) +
             [("p", "Les techniciens sont identifiés par un matricule fictif (T-0xx) : aucune donnée personnelle.")]]
    return doc(meta, f"Export GMAO – {eq}", pages)


def guide_diag():
    meta = dict(id="guide_diagnostic_pompes", dossier=D1, titre="Guide de diagnostic des pompes centrifuges (symptôme – cause – action)",
                famille="pompes", equipement_id="POMPE-A-01 ; POMPE-A-02 ; POMPE-B-01", type_document="procedure", version="v1 (2025-06)",
                format="pdf_texte", prompt="P10", verifie_par=REV, groupe_acces=GP, usage_test="normal", remarques="")
    pages = [
        [("h1", "Guide de diagnostic – pompes centrifuges"),
         ("p", "Ce guide aide le technicien à orienter son diagnostic. Il ne remplace pas les procédures et ne garantit pas la cause : plusieurs "
               "causes peuvent produire le même symptôme. Toujours confirmer par une mesure."),
         ("table", ["Symptôme", "Mesure à faire", "Causes possibles", "Action / document"], [
             ["Voyant H2 orange fixe + P-21", "Température palier, niveau huile", "Manque d'huile, roulement usé, désalignement", "Manuel CP-50 ch. 9 ; PM-CP50-04"],
             ["Voyant H2 orange fixe + P-50", "Vibrations RMS sur les 2 paliers", "Socle desserré, désalignement, balourd", "PM-POM-05"],
             ["Voyant H2 orange fixe + P-41", "Pression aspiration", "Crépine colmatée, vanne fermée, niveau bas", "PE-SP1-01"],
             ["Voyant H2 clignotant", "Code affiché", "P-30 maintenance due ou P-60 fuite", "PM-CP50-02 ou PM-CP50-03"],
             ["Voyant H3 rouge", "Code affiché, intensité", "P-10, P-11, P-22, P-51", "Ne pas redémarrer"],
             ["Voyant H4 bleu", "Niveau bâche", "Manque d'eau P-40", "PE-SP1-01 §4"]], [1.3, 1.3, 1.8, 1.6], "Tableau 1 – Diagnostic par voyant", "tableau_1")],
        [("h1", "Interprétation des vibrations"),
         ("table", ["Vitesse RMS", "Zone (ISO 10816-3, machines &lt; 15 kW)", "Décision"], [["&lt; 2,8 mm/s", "A – Bon état", "Rien à signaler"],
             ["2,8 à 4,5 mm/s", "B – Acceptable", "Surveillance normale"], ["4,5 à 7,1 mm/s", "C – Tolérable court terme", "Planifier une intervention"],
             ["&gt; 7,1 mm/s", "D – Dommages possibles", "Préalarme P-50 ; intervention rapide"]], [1.2, 2.2, 2], "Tableau 2 – Seuils de vibration utilisés", "tableau_2"),
         ("p", "Une hausse progressive (par exemple 3,2 puis 5,9 mm/s en quelques semaines) est plus significative qu'une valeur isolée : comparer "
               "avec l'historique de l'équipement.")],
        [("h1", "Bonnes pratiques"),
         ("ul", ["Toujours consulter l'historique : une préalarme récurrente (deux P-21 en six mois) signale un problème de fond.",
                 "Photographier l'afficheur avant acquittement.", "En cas de doute entre deux causes, commencer par la plus simple à vérifier (niveau d'huile).",
                 "Signaler toute anomalie dans la GMAO, même sans intervention."])],
    ]
    return doc(meta, "Guide de diagnostic pompes", pages)


def technote_cavitation():
    meta = dict(id="technote_cavitation_en", dossier=D1, titre="Technical note TN-07 – Cavitation in centrifugal pumps (English)", famille="pompes",
                equipement_id="POMPE-A-01 ; POMPE-A-02 ; POMPE-B-01", type_document="procedure", version="v1 (2024-10)", format="pdf_texte", prompt="P11",
                verifie_par=REV, groupe_acces=GP, usage_test="normal", remarques="Document en anglais (signalé) ; test de recherche multilingue")
    pages = [
        [("h1", "Technical Note TN-07 – Cavitation in centrifugal pumps"),
         ("p", "Cavitation occurs when the pressure at the impeller eye falls below the vapour pressure of the liquid. Vapour bubbles form and then "
               "collapse violently in higher-pressure zones, causing noise, vibration, loss of head and pitting of the impeller."),
         ("h2", "1. Symptoms"), ("ul", ["Crackling noise, like gravel passing through the pump.", "Fluctuating discharge pressure and motor current.",
                                       "Increased vibration (on MD-Pompes panels: code P-50 may follow code P-41).", "Pitting on impeller vanes at inspection."]),
         ("fig", FIG + "courbe_cp50.png", 13, "Figure 1 – NPSH required rises with flow rate (CP-50 example)", "figure_1")],
        [("h2", "2. Root causes and remedies"),
         ("table", ["Root cause", "Remedy"], [["Clogged suction strainer", "Clean strainer (see POMPE-B-01 history, 2025-08)"],
             ["Partially closed suction valve", "Fully open suction valve; throttle only on discharge"], ["Low tank level", "Restore level; check LSL-101"],
             ["Operation far right of the curve", "Reduce flow to ≤ 110 % of nominal"], ["Hot liquid", "Check NPSH available with actual temperature"]],
          [2, 3], "Table 1 – Causes and remedies", "table_1"),
         ("box", "info", "Rule of thumb: keep NPSH available at least 0.5 m above NPSH required.")],
    ]
    return doc(meta, "MD-Pompes – TN-07 Cavitation", pages, lang="en")


def checklist():
    meta = dict(id="checklist_inspection_pompes", dossier=D1, titre="Checklist d'inspection mensuelle – station SP1 (remplie, scannée)",
                famille="pompes", equipement_id="POMPE-A-01 ; POMPE-A-02", type_document="procedure", version="v2 (2026-09)", format="pdf_scanne",
                prompt="P12", verifie_par=REV, groupe_acces=GP, usage_test="normal", remarques="Formulaire rempli de septembre 2026, scanné ; test OCR")
    rows = [["Niveau huile palier", "OK", "OK"], ["Fuite garniture", "Aucune", "Aucune"], ["Température palier (°C)", "64", "58"],
            ["Vibrations RMS (mm/s)", "5,9 ⚠", "2,7"], ["Intensité (A)", "13,8", "—"], ["Pression aspiration (bar)", "0,9", "0,9"],
            ["Protège-accouplement", "OK", "OK"], ["Propreté / bruit", "Bruit roulement léger", "OK"]]
    pages = [
        [("h1", "CHECKLIST MENSUELLE – STATION SP1"), ("p", "Mois : septembre 2026 – Matricule contrôleur : T-022 – Date : 2026-09-29"),
         ("table", ["Point de contrôle", "POMPE-A-01", "POMPE-A-02 (secours)"], rows, [2, 1.5, 1.5], "Tableau 1 – Relevés", "tableau_1"),
         ("p", "Observations : vibrations POMPE-A-01 en hausse (3,2 → 5,9 mm/s). Ticket à ouvrir pour surveillance. Pompe A-02 essayée 15 min : RAS.")],
        [("h2", "Rappels"), ("ul", ["Valeurs de référence : manuel CP-50, tableau 6.1.", "Toute valeur hors tolérance : ticket dans la GMAO.",
                                   "Visa du chef d'équipe obligatoire."]),
         ("p", "Visa chef d'équipe : ____ (matricule T-003) – date : 2026-09-30")],
    ]
    return doc(meta, "Checklist SP1 – 09/2026", pages)


def plan_maintenance():
    meta = dict(id="plan_maintenance_pompes_2026", dossier=D1, titre="Plan de maintenance et budget pompes 2026 (interne responsables)",
                famille="pompes", equipement_id="POMPE-A-01 ; POMPE-A-02 ; POMPE-B-01", type_document="procedure", version="v1 (2026-01)",
                format="pdf_texte", prompt="P13", verifie_par=REV, groupe_acces="responsables", usage_test="normal",
                remarques="Réservé au groupe responsables : test de contrôle d'accès (un technicien ne doit pas y accéder)")
    pages = [
        [("h1", "Plan de maintenance pompes 2026 – document interne"),
         ("box", "warn", "Diffusion restreinte : responsables maintenance uniquement (données budgétaires)."),
         ("table", ["Équipement", "Opération planifiée", "Trimestre", "Budget (MAD, fictif)"], [
             ["POMPE-A-01", "Remplacement roulements (fait en mars)", "T1", "6 800"], ["POMPE-A-01", "Analyse vibratoire externe", "T4", "3 500"],
             ["POMPE-A-02", "Remplacement garniture préventif", "T2", "4 200"], ["POMPE-B-01", "Révision complète 16 000 h", "T3", "18 500"],
             ["Station SP1", "Remplacement capteur PT-103", "T2", "2 900"]], [1.2, 2.6, 0.8, 1.2], "Tableau 1 – Plan et budget 2026", "tableau_1"),
         ("p", "Budget total pompes 2026 : 35 900 MAD (fictif). Écart à fin septembre : +4 % (pièces).")],
        [("h2", "Indicateurs 2025"), ("table", ["Indicateur", "POMPE-A-01", "POMPE-B-01"], [["Disponibilité", "98,7 %", "99,2 %"], ["MTBF (h)", "2 900", "4 100"],
            ["Interventions correctives", "2", "2"]], [2, 1.5, 1.5], "Tableau 2 – Indicateurs", "tableau_2"),
         ("p", "Décision : la récurrence des préalarmes P-21 sur POMPE-A-01 justifie une analyse vibratoire externe en T4.")],
    ]
    return doc(meta, "Plan maintenance pompes 2026 – INTERNE", pages)


def all_docs():
    return [manuel_cp50(), manuel_cm80(), codes_alarme_pompes(), proc_vidange("v1"), proc_vidange("v2"), proc_amorcage(), proc_alignement(),
            proc_roulements(), proc_garniture(), fiche_consignation(), fds_huile(), schema_vue_eclatee(), schema_pid(), schema_elec(),
            historique("POMPE-A-01", "P14"), historique("POMPE-B-01", "P14"), guide_diag(), technote_cavitation(), checklist(), plan_maintenance()]
