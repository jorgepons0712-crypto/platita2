#!/usr/bin/env python3
"""Genera 'Anotar en Platita.shortcut': agarra el texto del correo y se lo pasa a la app."""
import plistlib, uuid, sys

URL_APP = "https://jorgepons0712-crypto.github.io/platita2/#correo="
OBJ = "￼"                                  # marcador de variable

def uid(): return str(uuid.uuid4()).upper()
u_texto, u_url, u_final = uid(), uid(), uid()

def ref(output_uuid, nombre):
    return {"Value": {"Type": "ActionOutput", "OutputUUID": output_uuid, "OutputName": nombre},
            "WFSerializationType": "WFTextTokenAttachment"}

acciones = [
    # 1 · sacar el texto del correo que llega (o de lo que se comparta)
    {"WFWorkflowActionIdentifier": "is.workflow.actions.detect.text",
     "WFWorkflowActionParameters": {
        "UUID": u_texto,
        "WFInput": {"Value": {"Type": "ExtensionInput"},
                    "WFSerializationType": "WFTextTokenAttachment"}}},

    # 2 · codificarlo para que quepa en una dirección web
    {"WFWorkflowActionIdentifier": "is.workflow.actions.urlencode",
     "WFWorkflowActionParameters": {
        "UUID": u_url,
        "WFEncodeMode": "Encode",
        "WFInput": ref(u_texto, "Texto")}},

    # 3 · pegarlo detrás de la dirección de Platita
    {"WFWorkflowActionIdentifier": "is.workflow.actions.gettext",
     "WFWorkflowActionParameters": {
        "UUID": u_final,
        "WFTextActionText": {
            "Value": {"string": URL_APP + OBJ,
                      "attachmentsByRange": {
                          "{%d, 1}" % len(URL_APP): {
                              "Type": "ActionOutput", "OutputUUID": u_url,
                              "OutputName": "Texto codificado en URL"}}},
            "WFSerializationType": "WFTextTokenString"}}},

    # 4 · abrir Platita con el movimiento listo para categorizar
    {"WFWorkflowActionIdentifier": "is.workflow.actions.openurl",
     "WFWorkflowActionParameters": {"WFInput": ref(u_final, "Texto")}},
]

atajo = {
    "WFWorkflowClientVersion": "2605.0.5",
    "WFWorkflowMinimumClientVersion": 900,
    "WFWorkflowMinimumClientVersionString": "900",
    "WFWorkflowHasOutputFallback": False,
    "WFWorkflowHasShortcutInputVariables": True,
    "WFWorkflowIcon": {"WFWorkflowIconGlyphNumber": 59511,
                       "WFWorkflowIconStartColor": 4274264319},
    "WFWorkflowImportQuestions": [],
    "WFWorkflowInputContentItemClasses": [
        "WFAppStoreAppContentItem", "WFArticleContentItem", "WFContactContentItem",
        "WFDateContentItem", "WFEmailAddressContentItem", "WFGenericFileContentItem",
        "WFImageContentItem", "WFLocationContentItem", "WFPDFContentItem",
        "WFPhoneNumberContentItem", "WFRichTextContentItem",
        "WFSafariWebPageContentItem", "WFStringContentItem", "WFURLContentItem"],
    "WFWorkflowOutputContentItemClasses": [],
    "WFQuickActionSurfaces": [],
    "WFWorkflowTypes": ["ActionExtension"],      # para que salga en Compartir
    "WFWorkflowActions": acciones,
}

with open(sys.argv[1], "wb") as f:
    plistlib.dump(atajo, f)
print("generado:", sys.argv[1])
