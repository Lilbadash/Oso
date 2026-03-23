async function addTask() {
    const input = document.getElementById("task-input");
    const title = input.value.trim();
    if (!title) return;

    const res = await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
    });
    const task = await res.json();

    const li = document.createElement("li");
    li.dataset.id = task.id;
    li.innerHTML = `<span>${task.title}</span><button onclick="toggleTask(${task.id})">Done</button>`;
    document.getElementById("task-list").appendChild(li);

    input.value = "";
}

async function toggleTask(id) {
    const res = await fetch(`/api/tasks/${id}`, { method: "PUT" });
    const task = await res.json();

    const li = document.querySelector(`li[data-id="${id}"]`);
    li.classList.toggle("done", task.done);
    li.querySelector("button").textContent = task.done ? "Undo" : "Done";
}
