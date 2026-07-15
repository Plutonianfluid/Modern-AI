const PAGE_SIZE = 5;
const state = { notesPage: 1, actionsPage: 1 };

async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  return res.status === 204 ? null : res.json();
}

function button(label, onClick) {
  const element = document.createElement('button');
  element.textContent = label;
  element.onclick = onClick;
  return element;
}

async function loadNotes() {
  const params = new URLSearchParams({
    q: document.getElementById('note-search').value,
    sort: document.getElementById('note-sort').value,
    page: state.notesPage,
    page_size: PAGE_SIZE,
  });
  const data = await fetchJSON(`/notes/search?${params}`);
  const list = document.getElementById('notes');
  list.innerHTML = '';
  for (const note of data.items) list.appendChild(renderNote(note));
  document.getElementById('note-count').textContent = `${data.total} result(s)`;
  document.getElementById('notes-page').textContent = `Page ${data.page}`;
  document.getElementById('notes-prev').disabled = data.page === 1;
  document.getElementById('notes-next').disabled = data.page * PAGE_SIZE >= data.total;
}

function renderNote(note) {
  const li = document.createElement('li');
  const text = document.createElement('span');
  text.textContent = `${note.title}: ${note.content}`;
  li.append(text);
  li.append(button('Edit', async () => {
    const title = prompt('Title', note.title);
    if (title === null) return;
    const content = prompt('Content', note.content);
    if (content === null) return;
    const old = { title: note.title, content: note.content };
    text.textContent = `${title}: ${content}`;
    try {
      await fetchJSON(`/notes/${note.id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ title, content }) });
    } catch (error) {
      text.textContent = `${old.title}: ${old.content}`;
      alert(`Update failed: ${error.message}`);
    }
  }));
  li.append(button('Delete', async () => {
    const next = li.nextSibling;
    li.remove();
    try {
      await fetchJSON(`/notes/${note.id}`, { method: 'DELETE' });
      await loadNotes();
    } catch (error) {
      document.getElementById('notes').insertBefore(li, next);
      alert(`Delete failed: ${error.message}`);
    }
  }));
  return li;
}

async function loadActions() {
  const params = new URLSearchParams({ page: state.actionsPage, page_size: PAGE_SIZE });
  const completed = document.getElementById('action-filter').value;
  if (completed) params.set('completed', completed);
  const data = await fetchJSON(`/action-items/?${params}`);
  const list = document.getElementById('actions');
  list.innerHTML = '';
  for (const item of data.items) {
    const li = document.createElement('li');
    if (!item.completed) {
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox'; checkbox.dataset.itemId = item.id; li.append(checkbox);
    }
    li.append(`${item.description} [${item.completed ? 'done' : 'open'}]`);
    if (!item.completed) li.append(button('Complete', async () => {
      await fetchJSON(`/action-items/${item.id}/complete`, { method: 'PUT' }); loadActions();
    }));
    list.appendChild(li);
  }
  document.getElementById('action-count').textContent = `${data.total} item(s)`;
  document.getElementById('actions-page').textContent = `Page ${data.page}`;
  document.getElementById('actions-prev').disabled = data.page === 1;
  document.getElementById('actions-next').disabled = data.page * PAGE_SIZE >= data.total;
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const body = { title: document.getElementById('note-title').value, content: document.getElementById('note-content').value };
    await fetchJSON('/notes/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    event.target.reset(); state.notesPage = 1; loadNotes();
  });
  document.getElementById('action-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const body = { description: document.getElementById('action-desc').value };
    await fetchJSON('/action-items/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    event.target.reset(); state.actionsPage = 1; loadActions();
  });
  document.getElementById('note-search').oninput = () => { state.notesPage = 1; loadNotes(); };
  document.getElementById('note-sort').onchange = () => { state.notesPage = 1; loadNotes(); };
  document.getElementById('action-filter').onchange = () => { state.actionsPage = 1; loadActions(); };
  document.getElementById('notes-prev').onclick = () => { state.notesPage--; loadNotes(); };
  document.getElementById('notes-next').onclick = () => { state.notesPage++; loadNotes(); };
  document.getElementById('actions-prev').onclick = () => { state.actionsPage--; loadActions(); };
  document.getElementById('actions-next').onclick = () => { state.actionsPage++; loadActions(); };
  document.getElementById('bulk-complete').onclick = async () => {
    const ids = [...document.querySelectorAll('[data-item-id]:checked')].map((box) => Number(box.dataset.itemId));
    if (!ids.length) return;
    await fetchJSON('/action-items/bulk-complete', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ids }) });
    loadActions();
  };
  loadNotes(); loadActions();
});
