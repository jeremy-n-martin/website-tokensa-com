const $status = document.getElementById('status');
const $form = document.getElementById('form');
const $out = document.getElementById('out');
const $loader = document.getElementById('loader');
const $submitBtn = $form?.querySelector('button[type="submit"]');

// Détection et configuration de l'URL de l'API (remote ou locale)
const API_BASE = (() => {
  const params = new URLSearchParams(location.search);
  const override = params.get('server');
  const saved = localStorage.getItem('tokensa_api_base');
  const candidate = override || saved;
  if (candidate) {
    try {
      const u = new URL(candidate);
      // Normalise: retire les / finaux
      const norm = `${u.origin}${u.pathname}`.replace(/\/+$/, '');
      // Persiste si fourni via query
      if (override) localStorage.setItem('tokensa_api_base', norm);
      return norm;
    } catch {}
  }
  // Prod: domaine principal -> API publique
  if (location.hostname === 'tokensa.com' || location.hostname === 'www.tokensa.com') {
    return 'https://api.tokensa.com';
  }
  // Dev local par défaut
  return 'http://127.0.0.1:3327';
})();

async function detect() {
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 500);
    const r = await fetch(`${API_BASE}/api/health`, { signal: ctrl.signal });
    clearTimeout(t);
    if (r.ok) {
      $status.innerHTML = `API Tokensa détectée ✅ — <a href="${API_BASE}/api/health" target="_blank" rel="noopener">${API_BASE}</a>`;
      return true;
    }
  } catch {}
  $status.innerHTML =
    'API Tokensa non détectée ❌<br>' +
    `URL actuelle: <code>${API_BASE}</code><br>` +
    'Vérifiez le domaine/API puis cliquez sur <button id="retry">Réessayer</button><br>' +
    'Astuce: ajoutez <code>?server=https://api.tokensa.com</code> à l’URL de cette page pour forcer une autre API.';
  document.getElementById('retry')?.addEventListener('click', detect);
  return false;
}

$form.addEventListener('submit', async (e) => {
  e.preventDefault();
  $out.textContent = '';
  const fd = new FormData($form);
  const data = Object.fromEntries(fd.entries());
  const tags = fd.getAll('tags').map(String).filter(Boolean);

  // Validation minimale côté client pour éviter un 400 (et un blocage CORS)
  if (!tags.length) {
    $out.textContent = 'Veuillez sélectionner au moins un item.';
    return;
  }

  try {
    // Affiche le loader et désactive le bouton pendant l'appel
    $loader?.classList.add('is-visible');
    if ($submitBtn) $submitBtn.disabled = true;

    const r = await fetch(`${API_BASE}/api/generate`, {
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
  } finally {
    // Cache le loader et réactive le bouton quoi qu'il arrive
    $loader?.classList.remove('is-visible');
    if ($submitBtn) $submitBtn.disabled = false;
  }
});

detect();
