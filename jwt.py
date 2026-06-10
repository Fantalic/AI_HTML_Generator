# # Token Autentisierung
# JWT steht für JSON Web Token. Es handelt sich dabei um einen offenen Standard (RFC 7519), der eine kompakte und selbstenthaltende Methode definiert, um sicher Informationen zwischen Parteien als JSON-Objekt zu übertragen. Diese Informationen können durch eine digitale Signatur verifiziert und somit auf ihre Integrität und Authentizität geprüft werden.
# Ein JWT besteht aus drei Teilen:
# Header: Enthält Metadaten wie den Signaturalgorithmus (z. B. HS256) und den Typ (JWT).
# Payload: Enthält die eigentlichen Daten oder Claims, z. B. Benutzeridentität, Rollen oder Ablaufzeit.
# Signatur: Sichert die Integrität des Tokens und bestätigt, dass es vom Aussteller stammt.

import json
import base64
import hmac
import hashlib
from time import time

TOKEN_EXPIRE_SECONDS = 5*60 # 5 minutes


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def base64url_decode(input_str: str) -> bytes:
    rem = len(input_str) % 4
    if rem > 0:
        input_str += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input_str)

def create_jwt(user_id:int, secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}

    payload=   {
        "sub": str(user_id),
        "iat": int(time()),
        "exp": int(time()) + TOKEN_EXPIRE_SECONDS  # Ablauf in 5 Minuten
    }

    # JSON serialisieren
    # Standardmäßig würde json.dumps() z.B. ', ' (Komma + Leerzeichen) und ': ' (Doppelpunkt + Leerzeichen) als Trennzeichen verwenden.
    header_json = json.dumps(header, separators=(',', ':')).encode('utf-8')
    payload_json = json.dumps(payload, separators=(',', ':')).encode('utf-8')

    # Base64Url kodieren
    header_b64 = base64url_encode(header_json)
    payload_b64 = base64url_encode(payload_json)

    # Signatur vorbereiten
    signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    signature = hmac.new(secret.encode('utf-8'), signing_input, hashlib.sha256).digest()
    signature_b64 = base64url_encode(signature)

    # JWT zusammensetzen
    jwt_token = f"{header_b64}.{payload_b64}.{signature_b64}"
    return jwt_token

def verify_jwt(token: str, secret: str) -> dict | None:
    try:
        header_b64, payload_b64, signature_b64 = token.split('.')

        signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')

        signature = base64url_decode(signature_b64 )

        expected_signature = hmac.new(secret.encode('utf-8'), signing_input, hashlib.sha256).digest()

        if not hmac.compare_digest(signature, expected_signature):
            print("Ungültige Signatur")
            return None

        payload_json = base64url_decode(payload_b64)
        payload = json.loads(payload_json)

        if "exp" in payload and time() > payload["exp"]:
            print("Token abgelaufen")
            return None

        return payload
    except Exception as e:
        print(f"Fehler bei der Verifikation: {e}")
        return None


if __name__ == "__main__":
    # Beispiel: Token erstellen und prüfen
    secret_key = "mein_geheimer_schluessel"
    payload_data = {
        "sub": "1234567890",
        "name": "Max Mustermann",
        "iat": int(time()),
        "exp": int(time()) + 600  # Ablauf in 10 Minuten
    }

    token = create_jwt(payload_data, secret_key)
    print("JWT:", token)

    verified_payload = verify_jwt(token, secret_key)
    print("Payload nach Verifikation:", verified_payload)
