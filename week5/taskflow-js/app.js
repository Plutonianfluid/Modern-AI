const STORAGE_KEY = "week5-study-task-board";

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
const filterButtons = document.querySelectorAll(".filter");

let tasks = loadTasks();
let activeFilter = "all";

function loadTasks() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return [
      {
        id: crypto.randomUUID(),
        title: "Finish Week 5 writeup",
        category: "Writing",
        priority: "High",
        notes: "Add app descriptions, stack notes, and reflection.",
        done: false,
        createdAt: new Date().toISOString(),
      },
    ];
  }

  try {
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

function saveTasks() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
}

function visibleTasks() {
  if (activeFilter === "open") {
    return tasks.filter((task) => !task.done);
  }
  if (activeFilter === "done") {
    return tasks.filter((task) => task.done);
  }
  return tasks;
}

function render() {
  totalCount.textContent = tasks.length;
  openCount.textContent = tasks.filter((task) => !task.done).length;

  const list = visibleTasks();
  if (list.length === 0) {
    taskList.innerHTML = `<div class="empty">No tasks match this view.</div>`;
    return;
  }

  taskList.innerHTML = list
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
  return value
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

function validateTitle(title) {
  if (title.length < 3) {
    return "Task title must be at least 3 characters.";
  }
  if (title.length > 80) {
    return "Task title must be 80 characters or fewer.";
  }
  return "";
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const title = titleInput.value.trim();
  const validationError = validateTitle(title);

  if (validationError) {
    errorEl.textContent = validationError;
    titleInput.focus();
    return;
  }

  const existingId = taskIdInput.value;
  const payload = {
    title,
    category: categoryInput.value,
    priority: priorityInput.value,
    notes: notesInput.value.trim(),
  };

  if (existingId) {
    tasks = tasks.map((task) => (task.id === existingId ? { ...task, ...payload } : task));
  } else {
    tasks = [
      {
        id: crypto.randomUUID(),
        done: false,
        createdAt: new Date().toISOString(),
        ...payload,
      },
      ...tasks,
    ];
  }

  saveTasks();
  resetForm();
  render();
});

taskList.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) {
    return;
  }

  const id = button.dataset.id;
  const action = button.dataset.action;
  const task = tasks.find((item) => item.id === id);

  if (action === "toggle") {
    tasks = tasks.map((item) => (item.id === id ? { ...item, done: !item.done } : item));
  }

  if (action === "edit" && task) {
    taskIdInput.value = task.id;
    titleInput.value = task.title;
    categoryInput.value = task.category;
    priorityInput.value = task.priority;
    notesInput.value = task.notes;
    saveButton.textContent = "Save changes";
    cancelButton.hidden = false;
    titleInput.focus();
  }

  if (action === "delete") {
    tasks = tasks.filter((item) => item.id !== id);
  }

  saveTasks();
  render();
});

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    activeFilter = button.dataset.filter;
    filterButtons.forEach((item) => item.classList.toggle("active", item === button));
    render();
  });
});

cancelButton.addEventListener("click", resetForm);

render();
