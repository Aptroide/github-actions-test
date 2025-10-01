import os
import sys
import json
import urllib.request
import urllib.error


def send_teams_notification(webhook_url, message):
    """
    Envía un mensaje simple a Microsoft Teams

    Args:
        webhook_url (str): URL del webhook de Teams
        message (str): Mensaje a enviar

    Returns:
        bool: True si se envió correctamente, False en caso contrario
    """
    if not webhook_url:
        print("❌ Error: TEAMS_WEBHOOK_URL no está configurado", file=sys.stderr)
        return False

    # Crear el payload simple para Teams
    payload = {
        "text": message
    }

    try:
        # Convertir a JSON
        data = json.dumps(payload).encode('utf-8')

        # Crear la petición
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )

        # Enviar la petición
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print("✅ Mensaje enviado correctamente a Teams")
                return True
            else:
                print(f"⚠️  Respuesta inesperada: {response.status}", file=sys.stderr)
                return False

    except urllib.error.URLError as e:
        print(f"❌ Error al enviar mensaje a Teams: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}", file=sys.stderr)
        return False


def main():
    # Obtener el webhook URL desde variable de entorno
    webhook_url = os.getenv('TEAMS_WEBHOOK_URL')

    # Obtener información del workflow
    run_number = os.getenv('GITHUB_RUN_NUMBER', 'N/A')
    repository = os.getenv('GITHUB_REPOSITORY', 'N/A')
    actor = os.getenv('GITHUB_ACTOR', 'N/A')

    # Crear mensaje simple
    message = f"✅ Workflow completado - Run #{run_number}\n📦 Repositorio: {repository}\n👤 Actor: {actor}"

    # Enviar notificación
    success = send_teams_notification(webhook_url, message)

    # Salir con código apropiado
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
