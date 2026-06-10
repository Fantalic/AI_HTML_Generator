export async function generateHtml(prompt, oldHtml) {
  const response = await fetch("/create_html", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, html: oldHtml }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return extractHtmlBlock(data.html);
}

export async function login(email, password) {
  const body = new URLSearchParams({ email, password });
  const response = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    redirect: "manual",
    body,
  });

  return response;
}

function extractHtmlBlock(input) {
  const regex = /```html\s*([\s\S]*?)```/g;
  const matches = [];
  let match;

  while ((match = regex.exec(input)) !== null) {
    matches.push(match[1].trim());
  }

  if (matches.length === 0) {
    return input;
  }

  return matches;
}
