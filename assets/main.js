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

  const r = await fetch('http://127.0.0.1:3327/api/generate', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-tokensa': 'v1' },
    body: JSON.stringify({ age: Number(data.age), tags }),
  });

  const reader = r.body.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    $out.textContent += decoder.decode(value);
  }
});

detect();
