const API_URL = "http://127.0.0.1:5000/tasks";

const taskList = document.getElementById("tasks");
const form = document.getElementById("addForm");
const titleInput = document.getElementById("title");
const status = document.getElementById("status");

// Fetch tasks from backend
async function loadTasks() {
  status.textContent = "Loading...";
  try {
    const res = await fetch(API_URL);
    const data = await res.json();
    renderTasks(data);
    status.textContent = "";
  } catch (err) {
    status.textContent = "Error loading tasks.";
  }
}

// Render task list
function renderTasks(tasks) {
  taskList.innerHTML = "";
  tasks.forEach(task => {
    const li = document.createElement("li");
    li.textContent = task.title;
    if (task.completed) li.classList.add("done");

    // toggle button
    const toggleBtn = document.createElement("button");
    toggleBtn.textContent = task.completed ? "Undo" : "Done";
    toggleBtn.onclick = () => toggleTask(task.id, !task.completed);

    // delete button
    const delBtn = document.createElement("button");
    delBtn.textContent = "✖";
    delBtn.classList.add("delete-btn");
    delBtn.onclick = () => deleteTask(task.id);

    const right = document.createElement("div");
    right.appendChild(toggleBtn);
    right.appendChild(delBtn);

    li.appendChild(right);
    taskList.appendChild(li);
  });
}

// Add a new task
form.addEventListener("submit", async e => {
  e.preventDefault();
  const title = titleInput.value.trim();
  if (!title) return;
  await fetch(API_URL, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ title })
  });
  titleInput.value = "";
  loadTasks();
});

// Delete a task
async function deleteTask(id) {
  await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  loadTasks();
}

// Toggle task completion
async function toggleTask(id, completed) {
  await fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ completed })
  });
  loadTasks();
}

// initial load
loadTasks();
