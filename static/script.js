document.addEventListener("DOMContentLoaded", () => {
    // Flash fade out
    document.querySelectorAll(".flash").forEach(f => {
        setTimeout(() => { f.style.transition = "opacity 1s"; f.style.opacity = "0"; }, 3000);
    });

    // Toggle password
    document.querySelectorAll(".toggle-password").forEach(btn => {
        btn.addEventListener("click", () => {
            const input = document.querySelector(`#${btn.dataset.target}`);
            input.type = input.type === "password" ? "text" : "password";
        });
    });

    // AJAX add task
    const taskForm = document.querySelector("#task-form");
    if(taskForm){
        taskForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const formData = new FormData(taskForm);
            fetch("/dashboard", { method:"POST", body: formData })
            .then(resp => resp.text())
            .then(() => { location.reload(); });
        });
    }

    // AJAX Delete task
    document.querySelectorAll(".delete-task").forEach(btn => {
        btn.addEventListener("click", () => {
            const row = btn.closest("tr");
            const taskId = row.dataset.taskId;
            fetch(`/delete_task/${taskId}`, { method:"POST" })
            .then(resp => resp.text())
            .then(() => { location.reload(); });
        });
    });

    // AJAX Edit task (simple prompt)
    document.querySelectorAll(".edit-task").forEach(btn => {
        btn.addEventListener("click", () => {
            const row = btn.closest("tr");
            const taskId = row.dataset.taskId;
            const title = prompt("Edit task title:", row.children[0].innerText);
            if(title){
                fetch(`/edit_task/${taskId}`, {
                    method:"POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ title: title })
                }).then(resp => resp.text())
                .then(() => { location.reload(); });
            }
        });
    });
});
