const $status = document.getElementById('status');
const $form = document.getElementById('form');
const $out = document.getElementById('out');

async function detect() {
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 500);
    const r = await fetch('http://127.0.0.1:3327/api/health', { signal: ctrl.signal });
    clearTimeout(t);
    if (r.ok) {
      $status.textContent = 'Serveur local détecté ✅';
      return true;
    }
  } catch {}
  $status.innerHTML =
    'Serveur local non détecté ❌<br>' +
    'Installez et lancez <strong>tokensa-local-server</strong> puis cliquez sur <button id="retry">Réessayer</button>';
  document.getElementById('retry')?.addEventListener('click', detect);
  return false;
}

$form.addEventListener('submit', async (e) => {
  e.preventDefault();
  $out.textContent = '';
  const data = Object.fromEntries(new FormData($form).entries());
  const tags = (Array.isArray(data.tags) ? data.tags : [data.tags]).filter(Boolean);

  // Validation minimale côté client pour éviter un 400 (et un blocage CORS)
  if (!tags.length) {
    $out.textContent = 'Veuillez sélectionner au moins un domaine (ex.: Dyslexie).';
    return;
  }

  try {
    const r = await fetch('http://127.0.0.1:3327/api/generate', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-tokensa': 'v1' },
      body: JSON.stringify({ age: Number(data.age), tags }),
    });

    if (!r.ok) {
      const txt = await r.text().catch(() => '');
      throw new Error(`Requête échouée (${r.status}) ${r.statusText}${txt ? ` — ${txt}` : ''}`);
    }
    const json = await r.json();
    $out.textContent = json?.text ?? '(réponse vide)';
  } catch (err) {
    // Cas typique d’erreur fetch (ex.: CORS bloqué, serveur indisponible)
    $out.textContent =
      'Erreur lors de la génération. Vérifiez que le serveur local tourne et que votre navigateur autorise l’accès au réseau local.\n' +
      (err instanceof Error ? err.message : String(err));
  }
});

detect();
