import json
import http.server
from urllib.parse import urlparse 
from ollama_api import ai_request
import utils

def ai_generate_html(prompt, old_html):

    messages = [
        {
            "role": "system",
            "content":
                """
                Generate a HTML page based on the user request or adapt the allready existing page.
                Use modern css styling using tailwind classes.
                !!! ONLY responde with HTML code !!!
                """
        },
        {
            "role": "system",
            "content":
                f"""
                current HTML code: \n
                {old_html}
                """
        },
        {   "role": "user", "content": prompt   },
    ]

    response = ai_request(messages=messages, model="deepseek-r1:8b")

    content = response["message"]["content"]
    removed_thinking_part = utils.remove_think_tags(content)
    html = utils.extract_html_code(removed_thinking_part)
    if html == "" or html == None:
        html = removed_thinking_part

    return html



class MyRequestHandler(http.server.BaseHTTPRequestHandler):
# class MyRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        if self.path == '/create_html':
            data = json.loads(post_data.decode('utf-8'))
            prompt = data["prompt"]
            old_html = data["html"]
            html = ai_generate_html(prompt, old_html)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            obj_str = json.dumps({"html": html})
            self.wfile.write(obj_str.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            return

    def do_GET(self):

        parsed_url = urlparse(self.path)
        parsed_path = parsed_url.path

        # PAGES:
        if parsed_path == "/":
            with open('pages/index.html', 'r', encoding='utf-8') as file:
                page = file.read()

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            self.wfile.write(page.encode('utf-8'))


def run(server_class=http.server.HTTPServer, handler_class=MyRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()