"""Référentiel unique du corpus MaintiDoc (source de vérité).
Tous les documents, schémas, photos et historiques sont générés à partir de ces données,
ce qui garantit la cohérence des identifiants, codes d'alarme et valeurs entre documents.
Site, marques (MD-Pompes, MD-Air), personnes et interventions : entièrement fictifs.
"""

SITE = "Site industriel fictif « Usine-École Démo »"
MENTION = "Document synthétique – usage pédagogique MaintiDoc (EMSI 2026) – marques et données fictives"

# ---------------------------------------------------------------- Équipements
EQUIPEMENTS = {
    "POMPE-A-01": dict(famille="pompes", modele="CP-50", marque="MD-Pompes", serie="CP50-21-0457",
                       annee=2021, lieu="Station de pompage SP1 – ligne eau de refroidissement"),
    "POMPE-A-02": dict(famille="pompes", modele="CP-50", marque="MD-Pompes", serie="CP50-21-0458",
                       annee=2021, lieu="Station de pompage SP1 – pompe de secours (redondance)"),
    "POMPE-B-01": dict(famille="pompes", modele="CM-80", marque="MD-Pompes", serie="CM80-22-0112",
                       annee=2022, lieu="Bâtiment chaufferie – surpression eau process"),
    "COMP-A-01": dict(famille="compresseurs", modele="VS-37", marque="MD-Air", serie="VS37-20-1093",
                      annee=2020, lieu="Local compresseurs LC1 – réseau air 7 bar"),
    "COMP-A-02": dict(famille="compresseurs", modele="VS-37", marque="MD-Air", serie="VS37-20-1094",
                      annee=2020, lieu="Local compresseurs LC1 – secours / appoint"),
    "COMP-B-02": dict(famille="compresseurs", modele="PS-11", marque="MD-Air", serie="PS11-19-0331",
                      annee=2019, lieu="Atelier mécanique – poste de soufflage"),
}

# ---------------------------------------------------------------- Caractéristiques
CP50 = dict(debit="50 m³/h", hmt="32 m", vitesse="2900 tr/min", puissance="7,5 kW", tension="400 V triphasé 50 Hz",
            intensite="14,5 A", pression_max="10 bar", temp_fluide_max="90 °C", garniture="garniture mécanique simple Ø 35 mm",
            roulement_ca="6307 C3", roulement_cm="6306 C3", huile="huile minérale ISO VG 68 (MD-Lub P68)",
            volume_huile="0,4 L", masse="118 kg", npsh="3,2 m")
CM80 = dict(debit="30 m³/h", hmt="85 m", vitesse="2900 tr/min", puissance="15 kW", tension="400 V triphasé 50 Hz",
            intensite="27 A", etages="5 étages", pression_max="16 bar", temp_fluide_max="120 °C",
            roulement="7309 BEP (butée) + 6309 C3", huile="graisse lithium EP2 (MD-Grease EP2)", masse="245 kg")
VS37 = dict(puissance="37 kW", pression_service="7,5 bar", pression_max="8,5 bar", debit="6,2 m³/min",
            tension="400 V triphasé 50 Hz", intensite="66 A", huile="huile synthétique MD-Lub S46 (ISO VG 46)",
            volume_huile="16 L", temp_ref_normale="75 à 95 °C", niveau_sonore="69 dB(A)", masse="780 kg")
PS11 = dict(puissance="11 kW", pression_max="10 bar", debit="1,4 m³/min", reservoir="500 L",
            tension="400 V triphasé 50 Hz", intensite="21 A", huile="huile minérale MD-Lub C100 (ISO VG 100)",
            volume_huile="2,5 L", cylindres="2 cylindres en V, 2 étages", masse="310 kg")

# Valeurs critiques volontairement contradictoires entre versions
COUPLE_COUVERCLE_GARNITURE = {"v1": "25 N·m", "v2": "35 N·m"}   # proc_vidange_cp50_v1 / v2 ; manuel = v2
VIDANGE_VS37 = {"v1": dict(intervalle="2000 h", huile="huile minérale MD-Lub C46", volume="18 L"),
                "v2": dict(intervalle="4000 h", huile="huile synthétique MD-Lub S46", volume="16 L")}

# ---------------------------------------------------------------- Voyants
# Panneau armoire pompes (identique pour CP-50 et CM-80)
VOYANTS_POMPES = [
    ("H1", "vert", "fixe", "Pompe en marche"),
    ("H2", "orange", "fixe", "Préalarme : voir code affiché (température palier, vibrations, aspiration)"),
    ("H2", "orange", "clignotant", "Maintenance préventive due ou fuite garniture détectée"),
    ("H3", "rouge", "fixe", "Défaut avec arrêt de la pompe"),
    ("H4", "bleu", "fixe", "Manque d'eau / niveau bas bâche"),
]
# Contrôleur compresseur VS-37 : même couleur orange, signification différente (cas ambigu volontaire)
VOYANTS_VS37 = [
    ("L1", "vert", "fixe", "Compresseur en charge"),
    ("L1", "vert", "clignotant", "Compresseur à vide / attente redémarrage automatique"),
    ("L2", "orange", "fixe", "Préalarme : voir code affiché (température refoulement, purgeur)"),
    ("L2", "orange", "clignotant", "Entretien requis (filtres, vidange)"),
    ("L3", "rouge", "fixe", "Arrêt sur défaut – acquittement requis"),
]
VOYANTS_PS11 = [
    ("V1", "vert", "fixe", "Sous tension / moteur en marche"),
    ("V2", "orange", "fixe", "Température culasse élevée"),
    ("V3", "rouge", "fixe", "Arrêt sécurité (thermique moteur ou pression)"),
]

# ---------------------------------------------------------------- Codes d'alarme
# (code, libellé, seuil/condition, voyant, réaction automatique, action recommandée)
CODES_POMPES = [
    ("P-10", "Surintensité moteur", "I > 1,15 × In pendant 5 s", "H3 rouge", "Arrêt",
     "Vérifier blocage de la roue, tension d'alimentation, état du moteur (isolement)."),
    ("P-11", "Défaut thermique moteur (sonde PTC)", "Sonde PTC déclenchée", "H3 rouge", "Arrêt",
     "Laisser refroidir, vérifier ventilation moteur et charge. Contrôler la sonde."),
    ("P-21", "Température palier élevée (préalarme)", "T palier ≥ 80 °C", "H2 orange fixe", "Aucune",
     "Contrôler niveau d'huile palier, état des roulements (procédure roulements), alignement."),
    ("P-22", "Température palier très élevée", "T palier ≥ 95 °C", "H3 rouge", "Arrêt",
     "Ne pas redémarrer. Contrôler lubrification et roulements avant remise en service."),
    ("P-30", "Maintenance préventive due", "Compteur ≥ 2000 h depuis dernier entretien", "H2 orange clignotant", "Aucune",
     "Réaliser l'entretien 2000 h (vidange palier, contrôle garniture). Remettre le compteur à zéro."),
    ("P-41", "Pression d'aspiration basse", "P aspiration < 0,3 bar pendant 10 s", "H2 orange fixe", "Aucune",
     "Risque de cavitation. Vérifier vanne d'aspiration, crépine, niveau bâche."),
    ("P-40", "Manque d'eau", "Niveau bâche < niveau bas (LSL-101)", "H4 bleu", "Arrêt",
     "Vérifier l'alimentation de la bâche. Réamorcer si nécessaire (procédure démarrage)."),
    ("P-50", "Vibrations élevées (préalarme)", "Vitesse vibratoire ≥ 7,1 mm/s RMS", "H2 orange fixe", "Aucune",
     "Contrôler alignement, fixation du socle, roulements. Planifier une analyse vibratoire."),
    ("P-51", "Vibrations très élevées", "Vitesse vibratoire ≥ 11 mm/s RMS", "H3 rouge", "Arrêt",
     "Ne pas redémarrer avant contrôle de l'alignement et des roulements."),
    ("P-60", "Fuite garniture mécanique", "Détecteur de fuite LS-102 actif", "H2 orange clignotant", "Aucune",
     "Contrôler la garniture. Remplacer si fuite > 10 gouttes/min (procédure garniture)."),
]
CODES_VS37 = [
    ("A-10", "Surintensité moteur principal", "I > 1,1 × In", "L3 rouge", "Arrêt",
     "Vérifier tension, serrage des bornes, état du moteur et de l'élément de compression."),
    ("A-12", "Température de refoulement élevée (préalarme)", "T refoulement ≥ 100 °C", "L2 orange fixe", "Aucune",
     "Nettoyer le radiateur, vérifier ventilation du local (≤ 40 °C) et niveau d'huile."),
    ("A-13", "Température de refoulement excessive", "T refoulement ≥ 110 °C", "L3 rouge", "Arrêt",
     "Laisser refroidir. Contrôler huile, thermostat de régulation et radiateur avant redémarrage."),
    ("A-20", "Pression de refoulement haute", "P ≥ 8,5 bar", "L3 rouge", "Arrêt",
     "Vérifier le capteur de pression et l'électrovanne de mise à vide."),
    ("A-22", "Ordre des phases incorrect", "Détection au démarrage", "L3 rouge", "Démarrage bloqué",
     "Intervention électricien habilité : inverser deux phases à l'alimentation."),
    ("A-31", "Filtre à air colmaté", "Δp filtre ≥ 50 mbar", "L2 orange clignotant", "Aucune",
     "Remplacer la cartouche filtre à air (procédure filtres)."),
    ("A-32", "Séparateur d'huile colmaté", "Δp séparateur ≥ 1 bar", "L2 orange clignotant", "Aucune",
     "Remplacer le séparateur air/huile (procédure filtres)."),
    ("A-35", "Entretien périodique dû", "Compteur ≥ 4000 h", "L2 orange clignotant", "Aucune",
     "Réaliser la vidange et le remplacement des filtres (procédure vidange v2)."),
    ("A-40", "Défaut purgeur de condensats", "Pas de décharge détectée depuis 30 min", "L2 orange fixe", "Aucune",
     "Contrôler le purgeur électronique et la ligne de purge (procédure purge)."),
]
CODES_PS11 = [
    ("B-10", "Défaut thermique moteur", "Relais thermique déclenché", "V3 rouge", "Arrêt",
     "Vérifier courroies, charge et ventilation. Réarmer après refroidissement."),
    ("B-12", "Température culasse élevée", "T culasse ≥ 180 °C", "V2 orange", "Aucune",
     "Vérifier propreté des ailettes, sens de rotation du ventilateur, taux de marche."),
    ("B-20", "Pression réservoir haute", "P ≥ 10 bar (pressostat de sécurité)", "V3 rouge", "Arrêt",
     "Vérifier le pressostat de régulation et la soupape de sûreté (tarée à 11 bar)."),
    ("B-35", "Vidange huile due", "Compteur ≥ 500 h", "aucun (afficheur)", "Aucune",
     "Vidanger le carter (2,5 L MD-Lub C100)."),
]

# ---------------------------------------------------------------- Historiques (cohérents avec le serveur MCP)
# (id, date, type, code, description, action, durée h, technicien (matricule fictif), statut)
HISTORIQUES = {
    "POMPE-A-01": [
        ("INT-2024-0187", "2024-05-14", "Corrective", "P-60", "Fuite garniture mécanique ≈ 25 gouttes/min",
         "Remplacement garniture mécanique Ø 35 (réf. GM-35-CP)", 3.5, "T-014", "Clôturée"),
        ("INT-2024-0402", "2024-11-06", "Préventive", "P-30", "Entretien 2000 h",
         "Vidange palier (0,4 L ISO VG 68), contrôle garniture, compteur remis à zéro", 1.5, "T-014", "Clôturée"),
        ("INT-2025-0311", "2025-09-22", "Corrective", "P-21", "Préalarme température palier, 84 °C relevé",
         "Appoint huile palier, roulement côté accouplement bruyant : à surveiller", 1.0, "T-022", "Clôturée"),
        ("INT-2026-0098", "2026-03-11", "Corrective", "P-21", "Nouvelle préalarme température palier, 87 °C",
         "Remplacement roulements 6307 C3 et 6306 C3, réalignement accouplement (0,04 mm)", 5.0, "T-014", "Clôturée"),
        ("INT-2026-0256", "2026-09-30", "Préventive", "P-30", "Entretien 2000 h",
         "Vidange palier, contrôle alignement, vibrations 3,2 mm/s", 1.5, "T-022", "Clôturée"),
    ],
    "POMPE-B-01": [
        ("INT-2025-0077", "2025-03-04", "Préventive", "P-30", "Entretien 2000 h",
         "Graissage roulements (MD-Grease EP2, 15 g par palier), contrôle garniture", 1.0, "T-031", "Clôturée"),
        ("INT-2025-0290", "2025-08-19", "Corrective", "P-41", "Pression aspiration basse, 0,2 bar",
         "Crépine d'aspiration colmatée : nettoyage, P aspiration revenue à 0,8 bar", 2.0, "T-031", "Clôturée"),
        ("INT-2026-0187", "2026-07-08", "Corrective", "P-50", "Vibrations 7,8 mm/s",
         "Resserrage boulons de socle, vibrations ramenées à 4,1 mm/s", 1.5, "T-022", "Clôturée"),
    ],
    "COMP-A-01": [
        ("INT-2025-0120", "2025-04-02", "Corrective", "A-31", "Filtre à air colmaté (Δp 56 mbar)",
         "Remplacement cartouche filtre à air FA-37", 0.5, "T-041", "Clôturée"),
        ("INT-2025-0388", "2025-10-15", "Préventive", "A-35", "Entretien 4000 h",
         "Vidange 16 L MD-Lub S46, filtre huile, filtre à air, séparateur", 4.0, "T-041", "Clôturée"),
        ("INT-2026-0145", "2026-06-24", "Corrective", "A-12", "Préalarme température refoulement, 102 °C",
         "Radiateur encrassé : soufflage, T revenue à 88 °C. Local à 38 °C (canicule)", 2.0, "T-047", "Clôturée"),
        ("INT-2026-0233", "2026-08-12", "Corrective", "A-12", "Nouvelle préalarme température refoulement, 104 °C",
         "Thermostat de régulation suspecté : pièce commandée", 1.0, "T-041", "En attente pièce"),
    ],
    "COMP-B-02": [
        ("INT-2025-0205", "2025-06-10", "Préventive", "B-35", "Vidange 500 h",
         "Vidange 2,5 L MD-Lub C100, contrôle tension courroies", 1.0, "T-047", "Clôturée"),
        ("INT-2026-0061", "2026-02-17", "Corrective", "B-10", "Défaut thermique moteur",
         "Courroies détendues et usées : remplacement jeu de courroies SPA", 1.5, "T-047", "Clôturée"),
    ],
}
TICKETS_OUVERTS = {
    "POMPE-A-01": [("TCK-2026-0215", "2026-10-02", "Vibrations en hausse (5,9 mm/s) – à surveiller", "Ouvert")],
    "COMP-A-01": [("TCK-2026-0230", "2026-08-12", "Remplacement thermostat de régulation (suite INT-2026-0233)", "En attente pièce")],
}

GROUPES = {
    "techniciens_pompes": "Techniciens habilités sur la famille pompes",
    "techniciens_compresseurs": "Techniciens habilités sur la famille compresseurs",
    "responsables": "Responsables maintenance (accès à tout le corpus)",
}
