import json
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from services.agent_tools import reserver_creneau, verifier_disponibilites


router = APIRouter()


class VapiFunction(BaseModel):
    name: str
    arguments: str | dict[str, Any] = Field(default_factory=dict)


class VapiToolCall(BaseModel):
    id: str
    function: VapiFunction


class VapiMessage(BaseModel):
    type: str | None = None
    tool_call_list: list[VapiToolCall] = Field(default_factory=list, alias="toolCallList")


class VapiWebhookPayload(BaseModel):
    message: VapiMessage


def parse_tool_arguments(raw_arguments: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(raw_arguments, dict):
        return raw_arguments
    if not raw_arguments:
        return {}
    return json.loads(raw_arguments)


def dispatch_tool(name: str, arguments: dict[str, Any]) -> str:
    if name == "verifier_disponibilites":
        return verifier_disponibilites(jours=int(arguments.get("jours", 7)))

    if name == "reserver_creneau":
        return reserver_creneau(
            prenom=arguments["prenom"],
            nom=arguments["nom"],
            email=arguments["email"],
            date_rdv=arguments["date_rdv"],
            besoin=arguments["besoin"],
            call_id=arguments.get("call_id"),
        )

    return f"Outil inconnu : {name}"


@router.post("/webhook")
def vapi_webhook(payload: VapiWebhookPayload) -> dict[str, list[dict[str, str]]]:
    results = []

    for tool_call in payload.message.tool_call_list:
        try:
            arguments = parse_tool_arguments(tool_call.function.arguments)
            result = dispatch_tool(tool_call.function.name, arguments)
        except Exception as exc:
            result = f"Erreur pendant l'exécution de {tool_call.function.name} : {exc}"

        results.append({"toolCallId": tool_call.id, "result": result})

    return {"results": results}
