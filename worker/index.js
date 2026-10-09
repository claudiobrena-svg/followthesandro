// Worker del sito su Cloudflare.
// - Le pagine e i file del sito li serve Cloudflare direttamente (static assets).
// - Qui gestiamo solo il login GitHub del pannello /admin (Decap CMS):
//     /api/auth      -> manda a GitHub per autorizzare
//     /api/callback  -> riceve il codice da GitHub e passa il token al pannello
// Servono due "secret" nel progetto Cloudflare: GITHUB_CLIENT_ID e GITHUB_CLIENT_SECRET
// (dalla GitHub OAuth App con callback https://<indirizzo-del-sito>/api/callback).

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/auth") return auth(url, env);
    if (url.pathname === "/api/callback") return callback(request, url, env);
    return env.ASSETS.fetch(request);
  },
};

function auth(url, env) {
  if (!env.GITHUB_CLIENT_ID) return new Response("GITHUB_CLIENT_ID mancante nelle impostazioni del Worker", { status: 500 });
  const state = crypto.randomUUID();
  const github = new URL("https://github.com/login/oauth/authorize");
  github.searchParams.set("client_id", env.GITHUB_CLIENT_ID);
  github.searchParams.set("redirect_uri", `${url.origin}/api/callback`);
  github.searchParams.set("scope", url.searchParams.get("scope") || "repo,user");
  github.searchParams.set("state", state);
  return new Response(null, {
    status: 302,
    headers: {
      Location: github.toString(),
      "Set-Cookie": `oauth_state=${state}; Path=/api; HttpOnly; Secure; SameSite=Lax; Max-Age=600`,
    },
  });
}

async function callback(request, url, env) {
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const cookie = (request.headers.get("Cookie") || "").match(/oauth_state=([^;]+)/);
  if (!code || !state || !cookie || cookie[1] !== state) return pagina("error", { message: "Richiesta non valida, riprova." });

  const risposta = await fetch("https://github.com/login/oauth/access_token", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json", "User-Agent": "followthesandro" },
    body: JSON.stringify({
      client_id: env.GITHUB_CLIENT_ID,
      client_secret: env.GITHUB_CLIENT_SECRET,
      code,
      redirect_uri: `${url.origin}/api/callback`,
    }),
  });
  const dati = await risposta.json().catch(() => ({}));
  if (!dati.access_token) return pagina("error", { message: dati.error_description || "GitHub non ha dato l'autorizzazione." });
  return pagina("success", { token: dati.access_token, provider: "github" });
}

// Pagina che chiude la finestrella di login e passa il risultato al pannello (protocollo di Decap CMS)
function pagina(esito, contenuto) {
  const messaggio = `authorization:github:${esito}:${JSON.stringify(contenuto)}`;
  const html = `<!doctype html><html><body><script>
(function () {
  var msg = ${JSON.stringify(messaggio)};
  function ricevi(e) {
    if (e.origin !== location.origin) return;
    window.opener.postMessage(msg, e.origin);
    window.removeEventListener("message", ricevi, false);
  }
  window.addEventListener("message", ricevi, false);
  window.opener.postMessage("authorizing:github", location.origin);
})();
</script></body></html>`;
  return new Response(html, {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Set-Cookie": "oauth_state=; Path=/api; HttpOnly; Secure; SameSite=Lax; Max-Age=0",
      "Cache-Control": "no-store",
    },
  });
}
