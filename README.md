# 🎙️ agent-vocal-rdv — Agent Vocal IA pour la Prise de RDV

Un agent vocal IA qui répond au téléphone à ta place, comprend le besoin du client et réserve automatiquement un rendez-vous dans ton agenda.

**Flux :** Appel entrant → Agent VAPI (GPT-4o + ElevenLabs) → Google Calendar + Airtable → Dashboard de pilotage

---

## ⚡ Démarrage rapide

### Importer dans VS Code

```bash
git clone https://github.com/mechapizzai-lab/agent-vocal-starter.git
cd agent-vocal-starter
code .
```

### Importer dans Antigravity

```bash
git clone https://github.com/mechapizzai-lab/agent-vocal-starter.git
```

Ouvre ensuite le dossier `agent-vocal-starter` depuis Antigravity.

---

## Concept clé

Plutôt que de manquer des appels ou de passer du temps à qualifier chaque prospect, l'agent vocal prend en charge toute la conversation : il pose les bonnes questions, vérifie tes disponibilités en temps réel et pose le RDV directement dans ton calendrier — sans que tu n'aies à décrocher.

---

## Ce que fait l'agent

- ✅ Répond aux appels entrants 24h/24 en français
- ✅ Pose 2-3 questions pour comprendre le besoin du client
- ✅ Épelle et confirme l'email lettre par lettre pour éviter les erreurs
- ✅ Consulte ton Google Calendar pour proposer des créneaux libres
- ✅ Crée l'événement et envoie l'invitation par email au client
- ✅ Enregistre le contact et le besoin dans Airtable
- ✅ Synchronise les annulations entre Calendar et Airtable

---

## Dashboard de pilotage

Un dashboard web intégré accessible depuis n'importe quel navigateur :

- ✅ Vue de tous les RDV avec statuts (Confirmé / Terminé / Annulé)
- ✅ Stats en temps réel (total, taux de confirmation)
- ✅ Gestion des plages de disponibilité par jour et par horaire
- ✅ Annulation depuis le dashboard → suppression automatique dans Calendar
- ✅ Protégé par mot de passe, persistant entre les sessions

---

## Stack

| Brique | Rôle |
|---|---|
| **VAPI** | Agent vocal + numéro de téléphone |
| **GPT-4o** | Cerveau de la conversation |
| **Deepgram** | Transcription vocale (STT) |
| **ElevenLabs** | Synthèse vocale naturelle (TTS) |
| **Google Calendar** | Disponibilités + réservation |
| **Airtable** | Base de données des RDV |
| **FastAPI** | Serveur webhook |
| **Railway** | Hébergement cloud |

---

## Cas d'usage & monétisation

- Installer l'agent pour ton propre business (coaching, consulting, agence...)
- Proposer le service clé en main à des PME locales (médecins, artisans, coachs)
- Créer une offre d'agence autour de l'agent vocal IA
- Revendre le projet en marque blanche à tes propres clients

---

## Contenu de ce dépôt

```
agent-vocal-starter/
├── main.py                  # App FastAPI
├── dashboard.py             # Dashboard web + API
├── templates/               # Interface HTML/CSS/JS du dashboard
├── models.py                # Modèles Pydantic
├── services/                # Services locaux, remplaçables par Airtable/Calendar
├── tests/                   # Tests pytest
├── .interface-design/       # Direction UI/UX du produit
├── Dockerfile               # Déploiement Dokploy
├── .env.example             # Variables d'environnement
├── Skill.md                 # Skill Claude Code utilisé pendant le cours
└── README.md                # Ce fichier
```

Le projet démarre maintenant par un dashboard FastAPI local, prêt à être branché ensuite à Airtable, Google Calendar et VAPI.

---

## Développement local

Crée un fichier `.env` à partir de `.env.example`, puis installe les dépendances :

```bash
py -3.11 -m pip install -r requirements.txt
```

Lance les tests :

```bash
py -3.11 -m pytest -v
```

Démarre l'application :

```bash
py -3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Ouvre ensuite :

- `http://localhost:8000/`
- `http://localhost:8000/dashboard`

Le mot de passe par défaut est `change-me`.

---

## Déploiement Dokploy

Dans Dokploy, crée une application Docker/Git qui build ce dossier avec le `Dockerfile`.

Si Dokploy utilise Nixpacks/buildpack au lieu du Dockerfile, le projet fournit aussi :

- `Procfile`
- `nixpacks.toml`

Configuration minimale :

```env
DASHBOARD_PASSWORD=un-mot-de-passe-solide
VAPI_PRIVATE_KEY=ta-cle-privee-vapi
VAPI_PUBLIC_KEY=ta-cle-publique-vapi
WEBHOOK_URL=https://ton-domaine.com/webhook
COMPANY_DESCRIPTION=Entreprise qui reçoit des demandes de rendez-vous par téléphone.
AGENT_FIRST_MESSAGE=Bonjour, je suis l'assistant de rendez-vous. Comment puis-je vous aider ?
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
VAPI_MODEL_PROVIDER=deepseek
VAPI_MODEL_NAME=deepseek-v4-flash
AIRTABLE_API_KEY=ton-token-airtable
AIRTABLE_BASE_ID=appxxxxxxxxxxxxxx
AIRTABLE_APPOINTMENTS_TABLE=Rendez-vous
AIRTABLE_CONFIG_TABLE=Config
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
GOOGLE_CALENDAR_ID=primary
GOOGLE_CALENDAR_TIMEZONE=Africa/Douala
COMPANY_NAME=KamTech
```

Expose le port `8000`. Le conteneur lance automatiquement :

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Webhook VAPI

Le serveur expose maintenant :

```text
POST /webhook
```

### Créer l'assistant VAPI

Après déploiement Dokploy, renseigne `WEBHOOK_URL` avec ton URL publique terminée par `/webhook`, puis lance :

```bash
py -3.11 setup_vapi.py
```

Le script crée un assistant avec :

- modèle configurable via `VAPI_MODEL_PROVIDER` et `VAPI_MODEL_NAME`
- par défaut : `deepseek` / `deepseek-v4-flash`
- transcription Deepgram `nova-2` en français
- voix ElevenLabs `eleven_multilingual_v2`
- tools `verifier_disponibilites` et `reserver_creneau`

Tools supportés :

- `verifier_disponibilites`
- `reserver_creneau`

Format attendu par VAPI :

```json
{
  "message": {
    "type": "tool-calls",
    "toolCallList": [
      {
        "id": "tc-xxx",
        "function": {
          "name": "verifier_disponibilites",
          "arguments": "{\"jours\": 7}"
        }
      }
    ]
  }
}
```

Le webhook retourne :

```json
{
  "results": [
    {
      "toolCallId": "tc-xxx",
      "result": "Créneaux disponibles..."
    }
  ]
}
```

---

## Airtable

Si `AIRTABLE_API_KEY` et `AIRTABLE_BASE_ID` sont configurés, le dashboard et le webhook utilisent Airtable. Sinon, l'application reste en mode local.

Table `Rendez-vous` :

| Champ | Type recommandé |
|---|---|
| Prenom | Single line text |
| Nom | Single line text |
| Email | Email |
| Date RDV | Single line text |
| Besoin | Long text |
| Statut | Single select: `Confirme`, `Annule`, `Termine` |
| Cree le | Single line text |
| Call ID | Single line text |
| Calendar Event ID | Single line text |

Table `Config` :

| Champ | Type recommandé |
|---|---|
| Cle | Single line text |
| Valeur | Long text |

La configuration des disponibilités est stockée dans `Config` avec :

```text
Cle = availability_windows
Valeur = JSON des plages de disponibilités
```

---

## Google Calendar

Si `GOOGLE_SERVICE_ACCOUNT_JSON` est configuré, `reserver_creneau` crée aussi un événement Google Calendar avant d'enregistrer le RDV.

Variables :

```env
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
GOOGLE_CALENDAR_ID=primary
GOOGLE_CALENDAR_TIMEZONE=Africa/Douala
COMPANY_NAME=KamTech
```

Étapes :

1. Créer un service account dans Google Cloud.
2. Activer Google Calendar API.
3. Créer une clé JSON pour le service account.
4. Coller le contenu JSON complet dans `GOOGLE_SERVICE_ACCOUNT_JSON`.
5. Partager le calendrier cible avec l'email du service account.
6. Mettre l'identifiant du calendrier dans `GOOGLE_CALENDAR_ID`.

Effets :

- Réservation VAPI → création événement Calendar + RDV sauvegardé.
- Annulation dashboard d'un RDV avec `Calendar Event ID` → suppression de l'événement Calendar.

---

## Membres Skool

Tu es membre payant de la communauté MechaPizzAI ? Tu as accès au **projet complet clé en main** dans la section ressources :

- Code source intégral prêt à déployer
- Version marque blanche pour tes clients
- Dashboard inclus
- Il ne reste qu'à remplir tes clés API

👉 [Rejoindre la communauté MechaPizzAI sur Skool](https://www.skool.com/mechapizzai/about)
