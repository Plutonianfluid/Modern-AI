const form = document.querySelector("#task-form");
const taskIdInput = document.querySelector("#task-id");
const titleInput = document.querySelector("#title");
const categoryInput = document.querySelector("#category");
const priorityInput = document.querySelector("#priority");
const notesInput = document.querySelector("#notes");
const errorEl = document.querySelector("#form-error");
const saveButton = document.querySelector("#save-button");
const cancelButton = document.querySelector("#cancel-button");
const taskList = document.querySelector("#task-list");
const totalCount = document.querySelector("#total-count");
const openCount = document.querySelector("#open-count");

let tasks = [];

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || "Something went wrong.");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

async function loadTasks() {
  try {
    tasks = await api("/api/tasks");
    render();
  } catch (error) {
    taskList.innerHTML = `<div class="empty">${escapeHtml(error.message)}</div>`;
  }
}

function render() {
  totalCount.textContent = tasks.length;
  openCount.textContent = tasks.filter((task) => !task.done).length;

  if (tasks.length === 0) {
    taskList.innerHTML = `<div class="empty">No tasks yet.</div>`;
    return;
  }

  taskList.innerHTML = tasks
    .map(
      (task) => `
        <article class="task-card ${task.done ? "done" : ""}">
          <div class="card-head">
            <h2>${escapeHtml(task.title)}</h2>
            <span class="badge">${task.done ? "Done" : "Open"}</span>
          </div>
          <div class="badges">
            <span class="badge">${escapeHtml(task.category)}</span>
            <span class="badge ${task.priority.toLowerCase()}">${escapeHtml(task.priority)}</span>
          </div>
          <p>${task.notes ? escapeHtml(task.notes) : "No notes yet."}</p>
          <div class="card-actions">
            <button type="button" class="secondary" data-action="toggle" data-id="${task.id}">
              ${task.done ? "Reopen" : "Complete"}
            </button>
            <button type="button" class="secondary" data-action="edit" data-id="${task.id}">Edit</button>
            <button type="button" class="danger" data-action="delete" data-id="${task.id}">Delete</button>
          </div>
        </article>
      `,
    )
    .join("");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function resetForm() {
  form.reset();
  taskIdInput.value = "";
  errorEl.textContent = "";
  saveButton.textContent = "Add task";
  cancelButton.hidden = true;
}

function payloadFromForm(done = false) {
  return {
    title: titleInput.value.trim(),
    category: categoryInput.value,
    priority: priorityInput.value,
    notes: notesInput.value.trim(),
    done,
  };
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorEl.textContent = "";

  const existingId = taskIdInput.value;
  const existing = tasks.find((task) => String(task.id) === existingId);
  const payload = payloadFromForm(existing ? existing.done : false);

  if (payload.title.length < 3) {
    errorEl.textContent = "Task title must be at least 3 characters.";
    titleInput.focus();
    return;
  }

  try {
    if (existingId) {
      await api(`/api/tasks/${existingId}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
    } else {
      await api("/api/tasks", {
        method: "POST",
        body: JSON.stringify(payload),
      });
    }
    resetForm();
    await loadTasks();
  } catch (error) {
    errorEl.textContent = error.message;
  }
});

taskList.addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) {
    return;
  }

  const id = button.dataset.id;
  const task = tasks.find((item) => String(item.id) === id);
  if (!task) {
    return;
  }

  if (button.dataset.action === "edit") {
    taskIdInput.value = task.id;
    titleInput.value = task.title;
    categoryInput.value = task.category;
    priorityInput.value = task.priority;
    notesInput.value = task.notes;
    saveButton.textContent = "Save changes";
    cancelButton.hidden = false;
    titleInput.focus();
    return;
  }

  try {
    if (button.dataset.action === "toggle") {
      await api(`/api/tasks/${id}`, {
        method: "PUT",
        body: JSON.stringify({ ...task, done: !task.done }),
      });
    }

    if (button.dataset.action === "delete") {
      await api(`/api/tasks/${id}`, { method: "DELETE" });
    }

    await loadTasks();
  } catch (error) {
    errorEl.textContent = error.message;
  }
});

cancelButton.addEventListener("click", resetForm);
loadTasks();
