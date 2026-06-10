import json
import http.server
from http.cookies import SimpleCookie
from urllib.parse import urlparse
from pathlib import Path

from aigen_html.services.ollama import ai_request
from aigen_html.services.jwt import create_jwt, verify_jwt
from aigen_html import utils
from aigen_html.config import JWT_SECRET, JWT_ALGORITHM, SERVER_PORT, USER_DATA_PATH, STATIC_DIR, OLLAMA_DEFAULT_MODEL

user = { "name":"test", "password":"test", "id":0, "email":"test@test.de" }

try:
    with open(USER_DATA_PATH, 'r', encoding='utf-8') as file:
        user = json.loads(file.read())
except:
    print("users.json not found")

_chat_sessions = {}

SYSTEM_PROMPT = """
Generate a HTML page based on the user request or adapt the allready existing page.
Use modern css styling using tailwind classes.
!!! ONLY responde with HTML code !!!
"""

def ai_generate_html(prompt, old_html, session_id=None):
    if session_id and session_id in _chat_sessions:
        history = _chat_sessions[session_id]
        history[1] = {"role": "system", "content": f"current HTML code:\n{old_html}"}
    else:
        history = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"current HTML code:\n{old_html}"},
        ]

    history.append({"role": "user", "content": prompt})

    response = ai_request(messages=history, model=OLLAMA_DEFAULT_MODEL)
    content = response["message"]["content"]

    if session_id:
        history.append({"role": "assistant", "content": content})
        _chat_sessions[session_id] = history

    removed_thinking_part = utils.remove_think_tags(content)
    html = utils.extract_html_code(removed_thinking_part)
    if html == "" or html == None:
        html = removed_thinking_part

    return html

class MyRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_Auth(self):
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            cookie = SimpleCookie()
            cookie.load(cookie_header)

            if 'token' in cookie:
                token_value = cookie['token'].value
                print(f"Token-Cookie: {token_value}")

                print("validierung")
                valid = verify_jwt(token_value, JWT_SECRET)
                print(valid)

                if not valid:
                    self.send_response(302)
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Location', "/login")
                    self.end_headers()
                    self.wfile.write(b'Unauthorized: Token   invalid\n')
                return valid

            else:
                print("Kein 'token'-Cookie gefunden.")
        else:
            print("Kein Cookie-Header im Request.")

        if (
            'Authorization' not in self.headers
        ):
            self.send_response(302)
            self.send_header('WWW-Authenticate', 'Bearer realm="Access to the protected resource"')
            self.send_header('Content-type', 'text/plain')
            self.send_header('Location', "/login")
            self.end_headers()
            self.wfile.write(b'Unauthorized: Token missing or invalid\n')
            return False

        return True

    def do_POST(self):
        print("POST")

        try:
            post_data = self.rfile.read(int(self.headers['Content-Length']))
        except:
            self.send_response(500)
            message = "Internal Server Error: empty post data"
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(message.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))

        if self.path == '/login':
            print("login")
            data = utils.simple_parse_qs(post_data)
            print(data)

            email = data["email"]
            password = data["password"]
            loggedIn = ( user["email"] == email and user["password"] == password )
            if not loggedIn:
                print("Login fehlgeschlagen!")
                self.send_response(401)
                message = "Unauthorized: Invalid credentials"
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(message.encode('utf-8'))))
                self.end_headers()
                self.wfile.write(message.encode('utf-8'))
                return

            print("Login erfolgreich!")

            token = create_jwt( user["id"], JWT_SECRET )
            wants_json = "application/json" in self.headers.get("Accept", "")
            if wants_json:
                body = json.dumps({"success": True, "token": token})
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Set-Cookie", f"token={token}; HttpOnly; Path=/")
                self.end_headers()
                self.wfile.write(body.encode("utf-8"))
            else:
                self.send_response(302)
                self.send_header("Content-Type", "text/html")
                self.send_header("Authorization", f"Bearer {token}")
                self.send_header("Set-Cookie", f"token={token}; HttpOnly; Path=/")
                self.send_header("Location", "/")
                self.end_headers()
                self.wfile.write(b"Login erfolgreich. Token wurde im Header gesendet.")
            return

        if not self.do_Auth():
            return

        if self.path == '/create_html':
            data = json.loads(post_data.decode('utf-8'))
            prompt = data["prompt"]
            old_html = data.get("html", "")
            cookie_header = self.headers.get('Cookie', '')
            session_id = None
            if cookie_header:
                cookie = SimpleCookie()
                cookie.load(cookie_header)
                if 'token' in cookie:
                    session_id = cookie['token'].value
            html = ai_generate_html(prompt, old_html, session_id=session_id)
            obj_str = json.dumps({"html": html})
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(obj_str.encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()
            return

    def do_GET(self):
        parsed_url = urlparse(self.path)
        parsed_path = parsed_url.path

        if(parsed_path == "/login"):
            print("login")
            with open(STATIC_DIR / "pages" / "login.html", 'r', encoding='utf-8') as file:
                page = file.read()

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            self.wfile.write(page.encode('utf-8'))
            return

        if not self.do_Auth():
            return

        if parsed_path == "/":
            with open(STATIC_DIR / "pages" / "index.html", 'r', encoding='utf-8') as file:
                page = file.read()

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            self.wfile.write(page.encode('utf-8'))
            return


def run(server_class=http.server.HTTPServer, handler_class=MyRequestHandler, port=SERVER_PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
