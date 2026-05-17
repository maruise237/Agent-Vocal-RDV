import os
from typing import Any

import httpx


VAPI_BASE_URL = "https://api.vapi.ai"


class VapiClient:
    def __init__(
        self,
        private_key: str,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.private_key = private_key
        self.http_client = http_client or httpx.Client(timeout=30)

    def create_assistant(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.http_client.post(
            f"{VAPI_BASE_URL}/assistant",
            headers={
                "Authorization": f"Bearer {self.private_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        return response.json()


def build_system_prompt(company_name: str, company_description: str) -> str:
    return f"""
Tu es l'agent vocal de {company_name}.

Contexte entreprise :
{company_description}

Objectif :
Qualifier l'appelant, comprendre son besoin, vérifier les disponibilités, puis réserver un rendez-vous si le client confirme.

Règles obligatoires :
- Parle en français, de façon naturelle et professionnelle.
- Demande le prénom, le nom, l'email et le besoin du client.
- Fais répéter et confirmer l'email lettre par lettre avant réservation.
- Utilise uniquement les créneaux retournés par verifier_disponibilites.
- Ne réserve jamais sans confirmation explicite du client.
- Après réservation, récapitule le nom, l'email, la date et le besoin.
""".strip()


def build_assistant_payload(
    company_name: str,
    company_description: str,
    first_message: str,
    webhook_url: str,
    voice_id: str,
    model_provider: str,
    model_name: str,
) -> dict[str, Any]:
    return {
        "name": f"Agent RDV - {company_name}",
        "firstMessage": first_message,
        "serverUrl": webhook_url,
        "model": {
            "provider": model_provider,
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": build_system_prompt(company_name, company_description),
                }
            ],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "verifier_disponibilites",
                        "description": "Vérifie les disponibilités de rendez-vous configurées.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "jours": {
                                    "type": "integer",
                                    "description": "Nombre de jours à vérifier à partir d'aujourd'hui.",
                                    "default": 7,
                                }
                            },
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "reserver_creneau",
                        "description": "Réserve un rendez-vous après confirmation du client.",
                        "parameters": {
                            "type": "object",
                            "required": [
                                "prenom",
                                "nom",
                                "email",
                                "date_rdv",
                                "besoin",
                            ],
                            "properties": {
                                "prenom": {"type": "string"},
                                "nom": {"type": "string"},
                                "email": {"type": "string"},
                                "date_rdv": {
                                    "type": "string",
                                    "description": "Date au format YYYY-MM-DD HH:MM.",
                                },
                                "besoin": {"type": "string"},
                                "call_id": {"type": "string"},
                            },
                        },
                    },
                },
            ],
        },
        "voice": {
            "provider": "11labs",
            "voiceId": voice_id,
            "model": "eleven_multilingual_v2",
        },
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2",
            "language": "fr",
        },
    }


def main() -> None:
    private_key = os.environ["VAPI_PRIVATE_KEY"]
    payload = build_assistant_payload(
        company_name=os.environ.get("COMPANY_NAME", "KamTech"),
        company_description=os.environ.get(
            "COMPANY_DESCRIPTION",
            "Entreprise qui reçoit des demandes de rendez-vous par téléphone.",
        ),
        first_message=os.environ.get(
            "AGENT_FIRST_MESSAGE",
            "Bonjour, je suis l'assistant de rendez-vous. Comment puis-je vous aider ?",
        ),
        webhook_url=os.environ["WEBHOOK_URL"],
        voice_id=os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"),
        model_provider=os.environ.get("VAPI_MODEL_PROVIDER", "deepseek"),
        model_name=os.environ.get("VAPI_MODEL_NAME", "deepseek-v4-flash"),
    )

    assistant = VapiClient(private_key).create_assistant(payload)
    print(f"Assistant VAPI créé : {assistant['id']}")


if __name__ == "__main__":
    main()
