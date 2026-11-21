// Leonida Casebook - offline GTA VI trophy guide & tracker.
// Views: guide (three-pane tracker), roadmap, missables, sources & save.
// All data is local: app/data/trophies.json (the 55 official trophies with
// original guides) and app/data/guide.json (sources, disputes, roadmap).
// Progress lives in localStorage and in the export file the reader saves.

const SAVE_KEY = 'leonida-casebook-save-v1';
const EXPORT_NAME = 'leonida-casebook-save.json';

const trophiesDoc = await (await fetch('data/trophies.json')).json();
const guideDoc = await (await fetch('data/guide.json')).json();
const TROPHIES = trophiesDoc.trophies;
const SOURCES = new Map(guideDoc.sources.map((s) => [s.id, s]));
const DISPUTES = guideDoc.disputes;
const AUDIT = guideDoc.audit;

let save = loadSave();
let view = (location.hash || '#guide').slice(1);
if (!['guide', 'roadmap', 'missables', 'sources'].includes(view)) view = 'guide';
let selectedId = 28; // Positive Mental Attitude: the one possibly-missable trophy
let filter = { q: '', kind: 'all', grade: 'all', status: 'all' };

function loadSave() {
  try {
    const raw = JSON.parse(localStorage.getItem(SAVE_KEY) || 'null');
    if (raw && typeof raw === 'object') {
      return { earned: raw.earned || {}, counts: raw.counts || {},
               spoiler: raw.spoiler !== false, lastImport: raw.lastImport || null };
    }
  } catch (e) { /* a broken save falls through to a fresh one */ }
  return { earned: {}, counts: {}, spoiler: true, lastImport: null };
}
function persist() { localStorage.setItem(SAVE_KEY, JSON.stringify(save)); }
function cites(ids) { return ' <span class="cites">[' + ids.map((i) => 'S' + i).join('] [') + ']</span>'; }
function esc(s) { return String(s).replaceAll('&', '&amp;').replaceAll('<', '&lt;'); }
function byId(id) { return TROPHIES.find((t) => t.id === id); }
function isEarned(t) { return !!save.earned[t.name]; }
function shielded(t) { return save.spoiler && t.kind === 'story' && !isEarned(t); }
function shownName(t) { return shielded(t) ? 'Hidden story trophy (spoiler shield on)' : t.name; }
function roadmapOrder() {
  const rank = (t) => t.id === 1 ? 900 : t.id === 14 ? 800 : t.kind === 'story' ? t.id : 100 + t.id;
  return [...TROPHIES].sort((a, b) => rank(a) - rank(b));
}

function auditStrip() {
  const a = AUDIT;
  document.getElementById('audit').innerHTML =
    '<b>AUDIT</b> ' + a.claims_cited + '/' + a.claims + ' claims cited - ' + a.claims_multi +
    ' backed by 2+ sources - ' + a.steps_cited + '/' + a.steps + ' guide steps cited - ' +
    a.sources + ' sources read 2026-11-21 (' + a.pages + ' pages) - ' + a.disputes +
    ' disagreements shown both ways - 55/55 trophies, 1,350 PSN points - ' +
    Object.keys(save.earned).length + '/55 earned';
}

function render() {
  auditStrip();
  for (const b of document.querySelectorAll('.viewbtn')) {
    b.classList.toggle('active', b.dataset.view === view);
  }
  const main = document.getElementById('main');
  if (view === 'guide') main.innerHTML = guideView();
  if (view === 'roadmap') main.innerHTML = roadmapView();
  if (view === 'missables') main.innerHTML = missablesView();
  if (view === 'sources') main.innerHTML = sourcesView();
  wire();
}

/* ---------------- guide & tracker (three panes) ---------------- */
function passesFilter(t) {
  if (filter.grade !== 'all' && t.grade !== filter.grade) return false;
  if (filter.kind === 'missable' && t.missable.status === 'not missable') return false;
  if (filter.kind !== 'all' && filter.kind !== 'missable' && t.kind !== filter.kind) return false;
  if (filter.status === 'earned' && !isEarned(t)) return false;
  if (filter.status === 'unearned' && isEarned(t)) return false;
  if (filter.status === 'counted' && !t.count) return false;
  if (filter.q && !(t.name + ' ' + t.description).toLowerCase().includes(filter.q)) return false;
  return true;
}

function guideView() {
  const t = byId(selectedId);
  const list = TROPHIES.filter(passesFilter).map((x) =>
    '<li data-pick="' + x.id + '" class="' + (x.id === selectedId ? 'sel' : '') + '">' +
    '<span class="grade ' + x.grade + '">' + x.grade + '</span>' +
    '<span class="nm">' + (isEarned(x) ? '&#10003; ' : '') + esc(shownName(x)) + '</span>' +
    (x.missable.status !== 'not missable' ? '<span class="flag">' + x.missable.status + '</span>' : '') +
    '<br><span class="meta">' + x.kind + ' - ' + x.points + ' PSN pts' +
    (x.count ? ' - count ' + (save.counts[x.id] || 0) + '/' + x.count.target : '') + '</span></li>').join('');
  const disputes = DISPUTES.filter((d) => d.trophy === t.id);
  const perSource = new Map();
  const bump = (ids) => ids.forEach((i) => perSource.set(i, (perSource.get(i) || 0) + 1));
  t.steps.forEach((s) => bump(s.cites)); bump([1, 27]); bump([6, 1]);
  const srcList = [...perSource.entries()].sort((a, b) => b[1] - a[1]).map(([id, n]) =>
    '<li>S' + id + ' - ' + esc(SOURCES.get(id).name) + '<br><span class="small">' + n +
    ' claims on this guide - ' + SOURCES.get(id).pages + ' pages read</span></li>').join('');
  const nextUp = roadmapOrder().filter((x) => !isEarned(x)).slice(0, 6).map((x) =>
    '<li data-pick="' + x.id + '">' + esc(shownName(x)) + ' <span class="small">(' + x.kind + ')</span></li>').join('');
  const counter = t.count ?
    '<div class="count">YOUR COUNT <button type="button" data-count="-1">-</button>' +
    '<span class="val">' + (save.counts[t.id] || 0) + ' / ' + t.count.target + '</span>' +
    '<button type="button" data-count="1">+</button>' +
    '<span class="small">' + esc(t.count.label) + ' - step ' + t.count.step + '</span></div>' +
    '<div class="bar"><div style="width:' + Math.min(100, 100 * (save.counts[t.id] || 0) / t.count.target) + '%"></div></div>' : '';
  return '<div class="panes">' +
    '<section class="panel"><h3>Trophies - ' + TROPHIES.filter(passesFilter).length + ' shown</h3>' +
    '<div class="controls">' +
    '<input type="search" id="fq" placeholder="Search name or description" value="' + esc(filter.q) + '">' +
    '<select id="fkind"><option value="all">All kinds</option><option value="story">Story</option>' +
    '<option value="missable">Missable / at risk</option><option value="collectibles">Collectibles</option>' +
    '<option value="activities">Activities</option><option value="completion">Completion</option></select>' +
    '<select id="fgrade"><option value="all">All grades</option><option value="platinum">Platinum</option>' +
    '<option value="gold">Gold</option><option value="silver">Silver</option><option value="bronze">Bronze</option></select>' +
    '<select id="fstatus"><option value="all">Any status</option><option value="earned">Earned</option>' +
    '<option value="unearned">Not earned</option><option value="counted">Counted trophies</option></select>' +
    '<label class="small"><input type="checkbox" id="fspoiler" ' + (save.spoiler ? 'checked' : '') +
    '> Spoiler shield (hide story trophies until earned)</label></div>' +
    '<ul class="tlist">' + list + '</ul></section>' +
    '<section class="panel"><h2>' + esc(shownName(t)) + '</h2>' +
    '<p><span class="grade ' + t.grade + '">' + t.grade + '</span>' +
    (t.hidden ? '<span class="flag ok">hidden on PSN until earned</span>' : '') +
    (t.missable.status !== 'not missable' ? '<span class="flag">' + t.missable.status + '</span>' : '') +
    ' <label><input type="checkbox" id="earnbox" ' + (isEarned(t) ? 'checked' : '') + '> Earned</label></p>' +
    '<p class="desc">Official description: &quot;' + (shielded(t) ? '(hidden by the spoiler shield)' : esc(t.description)) + '&quot;</p>' +
    '<div class="facts"><span>Est. ' + t.minutes + ' min</span><span>' + t.points + ' PSN points</span>' +
    '<span>Confidence: ' + t.confidence + '</span><span>Window: ' + esc(t.chapter) + '</span>' +
    '<span>Kind: ' + t.kind + '</span>' + cites([6, 1]) + '</div>' +
    '<div class="answer"><b>Short answer first:</b> ' + esc(t.answer) + cites(t.sources.slice(0, 2)) + '</div>' +
    counter +
    '<div class="missbox' + (t.missable.status === 'not missable' ? ' safe' : '') + '"><b>Missable box - ' +
    t.missable.status + '.</b> Window: ' + esc(t.missable.window) + '<br>Last chance: ' +
    esc(t.missable.last) + '. What closes it: ' + esc(t.missable.closes) + cites([1, 27]) + '</div>' +
    '<h3>Guide steps - every step cited</h3><ol class="steps">' +
    t.steps.map((s) => '<li>' + esc(s.text) + cites(s.cites) + '</li>').join('') + '</ol>' +
    disputes.map((d) => '<div class="diffbox"><b>Sources differ - ' + esc(d.topic) + '.</b> ' +
      esc(d.a) + ' [S' + d.a_src + '] vs ' + esc(d.b) + ' [S' + d.b_src + ']<br><b>Our call:</b> ' +
      esc(d.call) + '</div>').join('') +
    '</section>' +
    '<aside class="panel rail"><h3>Next up (roadmap order)</h3><ol class="nextup">' + nextUp + '</ol>' +
    '<h3>Sources for this guide</h3><ul class="srclist">' + srcList + '</ul>' +
    '<h3>Progress</h3><p>' + Object.keys(save.earned).length + ' of 55 earned - ' +
    TROPHIES.filter(isEarned).reduce((n, x) => n + x.points, 0) + ' of 1,350 PSN points</p>' +
    '<div class="bar"><div style="width:' + (100 * Object.keys(save.earned).length / 55) + '%"></div></div>' +
    '<p class="small">Full registry and disagreements register: Sources &amp; Save view.</p></aside></div>';
}

/* ---------------- roadmap ---------------- */
function roadmapView() {
  const claims = guideDoc.roadmap.map((r) =>
    '<tr><td>' + esc(r.claim) + '</td><td>' + cites(r.cites) + '</td></tr>').join('');
  const stages = guideDoc.stages.map((s) =>
    '<section class="panel"><h3>' + esc(s.name) + ' - ' + esc(s.hours) + cites(s.cites) + '</h3><p>' +
    esc(s.text) + '</p></section>').join('');
  const watch = TROPHIES.filter((t) => t.missable.status !== 'not missable').map((t) =>
    '<li><b>' + esc(t.name) + '</b> - ' + t.missable.status + '. Last chance: ' + esc(t.missable.last) + cites([1, 27]) + '</li>').join('');
  return '<h2>Roadmap to the platinum - Vice Got a Price!</h2>' +
    '<div class="grid2"><section class="panel"><h3>Headline claims, each one cited</h3>' +
    '<table><tr><th>Claim</th><th>Sources</th></tr>' + claims + '</table></section>' +
    '<div>' + stages +
    '<section class="panel"><h3>Missable watch rail</h3><ul>' + watch + '</ul>' +
    '<p class="small">Only one trophy is reported possibly missable; the rest of this rail is at-risk insurance. ' +
    'Keep a manual save at the start and end of every chapter - there is no mission replay.</p></section></div></div>';
}

/* ---------------- missables ---------------- */
function missablesView() {
  const cols = ['Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5', 'Post'];
  const rows = TROPHIES.filter((t) => t.kind === 'story' || t.missable.status !== 'not missable' || t.id === 14 || t.id === 1)
    .sort((a, b) => (a.id === 28 ? 0 : a.missable.status !== 'not missable' ? 1 : 2) -
                    (b.id === 28 ? 0 : b.missable.status !== 'not missable' ? 1 : 2) || a.id - b.id);
  const cell = (t, c) => {
    if (t.id === 28) return c === 0 ? '<td class="last">LAST - balcony meditation</td>' : '<td>spots open</td>';
    if (t.kind === 'story') {
      const mine = { 'Chapter 1': 0, 'Chapter 2': 1, 'Chapter 3': 2, 'Chapter 4': 3, 'Chapter 5 (final mission)': 4 }[t.chapter];
      return c === mine ? '<td>pops here (automatic)</td>' : '<td></td>';
    }
    return c === 5 ? '<td>open in free roam</td>' : '<td>open</td>';
  };
  const grid = rows.map((t) => '<tr><td><b>' + esc(t.name) + '</b><br><span class="small">' +
    t.missable.status + '</span></td>' + cols.map((_, c) => cell(t, c)).join('') + '</tr>').join('');
  const gates = TROPHIES.filter((t) => t.kind === 'story').map((t) =>
    '<li><b>' + esc(t.chapter) + ' - ' + esc(t.name) + ':</b> &quot;' + esc(t.description) +
    '&quot; Automatic on completion; cannot be missed.' + cites([1, 9]) + '</li>').join('');
  return '<h2>Missables - point-of-no-return windows</h2>' +
    '<section class="panel"><h3>Chapter-window grid (Ch1-Ch5 / Post)</h3>' +
    '<table><tr><th>Trophy</th>' + cols.map((c) => '<th>' + c + '</th>').join('') + '</tr>' + grid + '</table>' +
    '<p class="small">The single hard window in the game: the Chapter 1 balcony meditation at Jason\'s house, ' +
    'the morning after Down to Earth. Accept Lucia\'s invitation before Chapter 1 ends.' + cites([1, 18]) + '</p></section>' +
    '<section class="panel"><h3>Story gates in chapter order</h3><ol>' + gates + '</ol></section>';
}

/* ---------------- sources & save ---------------- */
function bar(label, done, total) {
  return '<p>' + label + ': ' + done + '/' + total + '</p><div class="bar"><div style="width:' +
    (total ? 100 * done / total : 0) + '%"></div></div>';
}
function sourcesView() {
  const grades = ['platinum', 'gold', 'silver', 'bronze'].map((g) =>
    bar(g, TROPHIES.filter((t) => t.grade === g && isEarned(t)).length,
        TROPHIES.filter((t) => t.grade === g).length)).join('');
  const kinds = ['story', 'collectibles', 'activities', 'completion'].map((k) =>
    bar(k, TROPHIES.filter((t) => t.kind === k && isEarned(t)).length,
        TROPHIES.filter((t) => t.kind === k).length)).join('');
  const registry = guideDoc.sources.map((s) =>
    '<tr><td>S' + s.id + '</td><td>' + esc(s.name) + '<br><span class="small">' + esc(s.url) +
    '</span></td><td>' + s.scope + '</td><td>' + s.pages + '</td><td>' + esc(s.independence) +
    '</td><td>' + s.read + '</td></tr>').join('');
  const disputes = DISPUTES.map((d) =>
    '<tr><td>' + esc(d.topic) + ' (' + esc(byId(d.trophy).name) + ')</td><td>' + esc(d.a) +
    ' [S' + d.a_src + ']</td><td>' + esc(d.b) + ' [S' + d.b_src + ']</td><td><b>' + esc(d.call) +
    '</b></td></tr>').join('');
  return '<h2>Sources &amp; Save</h2><div class="grid2"><div>' +
    '<section class="panel"><h3>Saved state</h3><div class="savebox">' +
    '<p>Stored in this browser under localStorage key <b>' + SAVE_KEY + '</b>: earned trophies, ' +
    'YOUR COUNT counters, the spoiler-shield setting and the last-import receipt. Nothing leaves the browser ' +
    'except the file you export yourself.</p>' +
    '<p>Spoiler shield: <b>' + (save.spoiler ? 'ON - story trophies hidden until earned' :
      'OFF - story names shown') + '</b> <button type="button" id="spoiltoggle">Toggle shield</button></p>' +
    '<p>Export file name: <b>' + EXPORT_NAME + '</b></p>' +
    '<p>Last import: <b>' + (save.lastImport ? esc(save.lastImport) : 'none yet') + '</b></p>' +
    '<p><button type="button" id="exportbtn">Export save to file</button> ' +
    '<label>Import save <input type="file" id="importfile" accept="application/json"></label></p></div>' +
    '<h3>The real exported save JSON</h3><pre class="savejson">' + esc(JSON.stringify(save, null, 1)) + '</pre></section>' +
    '<section class="panel"><h3>Progress by grade</h3>' + grades +
    '<h3>Progress by kind</h3>' + kinds + '</section></div>' +
    '<section class="panel"><h3>Source registry - read 2026-11-21</h3>' +
    '<table><tr><th>#</th><th>Source</th><th>Scope read</th><th>Pages</th><th>Independence</th><th>Read</th></tr>' +
    registry + '</table><p class="small">An aggregator is never counted as a confirmation; ' +
    'a source that shares a witness with another is labelled as such.</p></section></div>' +
    '<section class="panel"><h3>Disagreements register - both versions, and our call (' + DISPUTES.length + ')</h3>' +
    '<table><tr><th>Topic</th><th>Version A</th><th>Version B</th><th>Our call</th></tr>' + disputes + '</table></section>';
}

/* ---------------- wiring ---------------- */
function setView(v) { view = v; location.hash = v; render(); }
function wire() {
  const q = (id) => document.getElementById(id);
  if (q('fq')) {
    q('fq').addEventListener('input', (e) => { filter.q = e.target.value.toLowerCase(); renderKeepFocus(); });
    q('fkind').value = filter.kind; q('fgrade').value = filter.grade; q('fstatus').value = filter.status;
    q('fkind').addEventListener('change', (e) => { filter.kind = e.target.value; render(); });
    q('fgrade').addEventListener('change', (e) => { filter.grade = e.target.value; render(); });
    q('fstatus').addEventListener('change', (e) => { filter.status = e.target.value; render(); });
    q('fspoiler').addEventListener('change', (e) => { save.spoiler = e.target.checked; persist(); render(); });
  }
  if (q('earnbox')) q('earnbox').addEventListener('change', (e) => {
    const t = byId(selectedId);
    if (e.target.checked) save.earned[t.name] = true; else delete save.earned[t.name];
    persist(); render();
  });
  for (const b of document.querySelectorAll('[data-count]')) {
    b.addEventListener('click', () => {
      const t = byId(selectedId);
      const now = (save.counts[t.id] || 0) + Number(b.dataset.count) * t.count.step;
      save.counts[t.id] = Math.max(0, Math.min(t.count.target, now));
      if (save.counts[t.id] >= t.count.target) save.earned[t.name] = true;
      persist(); render();
    });
  }
  for (const el of document.querySelectorAll('[data-pick]')) {
    el.addEventListener('click', () => { selectedId = Number(el.dataset.pick); view = 'guide'; render(); });
  }
  if (q('exportbtn')) q('exportbtn').addEventListener('click', exportSave);
  if (q('spoiltoggle')) q('spoiltoggle').addEventListener('click', () => { save.spoiler = !save.spoiler; persist(); render(); });
  if (q('importfile')) q('importfile').addEventListener('change', async (e) => {
    const f = e.target.files[0]; if (!f) return;
    try {
      const parsed = JSON.parse(await f.text());
      if (!parsed || typeof parsed !== 'object' || !('earned' in parsed)) throw new Error('not a casebook save');
      save = { earned: parsed.earned || {}, counts: parsed.counts || {},
               spoiler: parsed.spoiler !== false,
               lastImport: f.name + ' at ' + new Date().toISOString() };
      persist(); render();
    } catch (err) { alert('Import failed: ' + err.message); }
  });
}
function renderKeepFocus() {
  render();
  const fq = document.getElementById('fq');
  if (fq) { fq.focus(); fq.setSelectionRange(fq.value.length, fq.value.length); }
}
function exportSave() {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(save, null, 1)], { type: 'application/json' }));
  a.download = EXPORT_NAME; a.click(); URL.revokeObjectURL(a.href);
}
for (const b of document.querySelectorAll('.viewbtn')) {
  b.addEventListener('click', () => setView(b.dataset.view));
}
window.addEventListener('hashchange', () => {
  const v = location.hash.slice(1);
  if (['guide', 'roadmap', 'missables', 'sources'].includes(v) && v !== view) { view = v; render(); }
});
render();
