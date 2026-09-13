## Date Structure Brainstormer

### Starting Point

```json
{
  "reference": "NX-CORTEX-7",
  "family": "NEURAL",
  "label": "Interface corticale NX-7",
  "manufacturer": "NeuroLink Corp",
  "specs": {
    "bandwidth_mbps": 480,
    "power_draw_w": 2.4,
    "expected_lifespan_months": 96
  },
  "compatibility": {
    "min_age": 18,
    "incompatible_with": ["NX-CORTEX-5", "SYN-RELAY-2"]
  },
  "monitored_parameters": [
    { "code": "NEURAL_IMPEDANCE", "unit": "kOhm", "nominal_min": 8.0, "nominal_max": 14.0 },
    { "code": "SYNAPTIC_LATENCY", "unit": "ms", "nominal_min": 0.4, "nominal_max": 2.1 }
  ]
}
```
# FAMILY

| Code | Famille | Ce qu'elle couvre | Paramètres surveillés typiques |
|---|---|---|---|
| `NEURAL` | Interfaces neuronales | Interfaces corticales, relais médullaires, liaisons cerveau-machine | `NEURAL_IMPEDANCE` (kΩ), `SYNAPTIC_LATENCY` (ms), `CORTICAL_TEMP` (°C) |
| `SENSORY` | Augmentations sensorielles | Rétines synthétiques, cochlées, capteurs tactiles, spectres étendus | `SIGNAL_FIDELITY` (%), `INPUT_LATENCY` (ms), `RECEPTOR_DRIFT` |
| `MOTOR` | Augmentations motrices | Prothèses de membres, renforts articulaires, exosquelettes internes | `TORQUE_OUTPUT` (Nm), `JOINT_WEAR` (%), `ACTUATOR_TEMP` (°C) |
| `METABOLIC` | Régulateurs métaboliques | Pancréas artificiels, filtres hépatiques et rénaux, régulateurs hormonaux | `FILTRATION_RATE` (mL/min), `GLYCEMIC_VARIANCE`, `INFLAMMATORY_INDEX` |
| `CARDIO` | Assistance circulatoire | Cœurs auxiliaires, pompes d'assistance, oxygénateurs | `FLOW_RATE` (L/min), `PUMP_CYCLE_VARIANCE`, `HEMOLYSIS_INDEX` |
| `DERMAL` | Systèmes sous-cutanés | Blindage dermique, thermorégulation, réservoirs sous-cutanés | `SUBDERMAL_TEMP` (°C), `TISSUE_ADHESION`, `INFLAMMATORY_INDEX` |

**Deux paramètres transverses** à ajouter sur toutes les familles : `POWER_LEVEL` (%) et `DEVICE_TEMP` (°C). Ils servent le scénario de panne matérielle — chute brutale de charge — indépendamment du type d'implant.

**`INFLAMMATORY_INDEX` apparaît volontairement sur trois familles.** C'est lui qui, croisé avec une température, porte la règle de corrélation du rejet aigu. Sans cette redondance, la détection par corrélation n'est démontrable que sur une poignée de séries.

## TIER

| Code | Libellé | Positionnement | Durée de vie | Garantie | Suivi | Effets secondaires |
|---|---|---|---|---|---|---|
| `SALVAGE` | Reconditionné | Pièces récupérées, marché gris, traçabilité partielle | 18-30 mois | Aucune | Mensuel | 6 à 10, plusieurs fréquents |
| `STANDARD` | Série courante | Le gros du catalogue, fiabilité correcte | 48-72 mois | 24 mois | Trimestriel | 3 à 5 |
| `CLINICAL` | Grade clinique | Tolérances resserrées, biocompatibilité certifiée | 96-120 mois | 60 mois | Semestriel | 2 à 4, majoritairement rares |
| `PRIME` | Haut de gamme | Électronique redondée, autodiagnostic embarqué | 120-180 mois | 120 mois | Annuel | 1 à 3, rares |
| `MILSPEC` | Grade militaire | Durci, blindé, tolérant aux chocs, aux champs et au brouillage. Conçu pour tenir, pas pour ménager le porteur | 60-90 mois | 36 mois (usage civil exclu) | Trimestriel | 4 à 7, dont des effets fréquents liés à la contrainte imposée aux tissus |
| `PROTOTYPE` | Expérimental | Sous protocole d'essai, comportement mal caractérisé | Non caractérisée | Aucune | Hebdomadaire | 4 à 8, dont non documentés |

| Tier | `NOMINAL` | Dérive lente | Artefacts isolés | Panne matérielle | Rejet aigu | Trous capteur |
|---|---|---|---|---|---|---|
| `SALVAGE` | 15 % | 25 % | 20 % | 25 % | 10 % | 5 % |
| `STANDARD` | 40 % | 20 % | 15 % | 10 % | 10 % | 5 % |
| `CLINICAL` | 60 % | 15 % | 10 % | 5 % | 5 % | 5 % |
| `PRIME` | 75 % | 10 % | 5 % | 5 % | 3 % | 2 % |
| `MILSPEC` | 30 % | **35 %** | 5 % | 3 % | 20 % | 7 % |
| `PROTOTYPE` | 25 % | 20 % | 10 % | 10 % | 25 % | 10 % |

