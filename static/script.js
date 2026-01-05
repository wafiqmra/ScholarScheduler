document.addEventListener("DOMContentLoaded", () => {
    // Enhanced Flash fade out
    document.querySelectorAll(".flash").forEach(f => {
        setTimeout(() => { 
            f.style.transition = "opacity 0.5s ease, transform 0.5s ease";
            f.style.opacity = "0";
            f.style.transform = "translateY(-10px)";
            setTimeout(() => f.remove(), 500);
        }, 4000);
    });

    // Toggle password with better UX
    document.querySelectorAll(".toggle-password").forEach(btn => {
        btn.addEventListener("click", () => {
            const input = document.querySelector(`#${btn.dataset.target}`);
            const isPassword = input.type === "password";
            input.type = isPassword ? "text" : "password";
            btn.innerHTML = isPassword ? 
                '<i class="fas fa-eye-slash"></i>' : 
                '<i class="fas fa-eye"></i>';
        });
    });

    // AJAX add task with loading state
    const taskForm = document.querySelector("#task-form");
    if(taskForm){
        taskForm.addEventListener("submit", (e) => {
            e.preventDefault();
            
            const submitBtn = taskForm.querySelector("button[type='submit']");
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
            submitBtn.disabled = true;
            
            const formData = new FormData(taskForm);
            
            fetch("/dashboard", { 
                method: "POST", 
                body: formData 
            })
            .then(resp => {
                if (resp.ok) {
                    return resp.text();
                }
                throw new Error('Network response was not ok');
            })
            .then(() => {
                // Show success animation
                submitBtn.innerHTML = '<i class="fas fa-check"></i> Added!';
                submitBtn.style.background = "linear-gradient(135deg, #10b981, #059669)";
                
                setTimeout(() => {
                    location.reload();
                }, 500);
            })
            .catch(error => {
                console.error('Error:', error);
                submitBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
                submitBtn.style.background = "linear-gradient(135deg, #ef4444, #dc2626)";
                
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                    submitBtn.style.background = "linear-gradient(135deg, #3b82f6, #14b8a6)";
                }, 2000);
            });
        });
    }

    // AJAX Delete task with confirmation
    document.querySelectorAll(".delete-task").forEach(btn => {
        btn.addEventListener("click", () => {
            if (!confirm("Are you sure you want to delete this task?")) {
                return;
            }
            
            const row = btn.closest("tr");
            const taskId = row.dataset.taskId;
            
            // Add loading state to button
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            btn.disabled = true;
            
            fetch(`/delete_task/${taskId}`, { 
                method: "POST" 
            })
            .then(resp => {
                if (resp.ok) {
                    // Add fade out animation
                    row.style.transition = "opacity 0.3s ease, transform 0.3s ease";
                    row.style.opacity = "0";
                    row.style.transform = "translateX(-20px)";
                    
                    setTimeout(() => {
                        location.reload();
                    }, 300);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                btn.innerHTML = '<i class="fas fa-trash"></i>';
                btn.disabled = false;
                alert("Failed to delete task. Please try again.");
            });
        });
    });

    // AJAX Edit task with modal-like UI
    document.querySelectorAll(".edit-task").forEach(btn => {
        btn.addEventListener("click", () => {
            const row = btn.closest("tr");
            const taskId = row.dataset.taskId;
            const currentTitle = row.children[0].innerText;
            
            // Create modal overlay
            const modal = document.createElement("div");
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000;
                backdrop-filter: blur(4px);
                animation: fadeIn 0.2s ease;
            `;
            
            // Create modal content
            const modalContent = document.createElement("div");
            modalContent.style.cssText = `
                background: var(--notion-card);
                padding: 2rem;
                border-radius: 12px;
                min-width: 400px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                animation: slideUp 0.3s ease;
            `;
            
            modalContent.innerHTML = `
                <h3 style="margin-top: 0; color: var(--notion-text);">Edit Task</h3>
                <input type="text" id="edit-task-input" value="${currentTitle}" style="width: 100%; padding: 0.8rem; margin-bottom: 1.5rem; border: 1px solid var(--notion-border); border-radius: 8px; font-family: 'Poppins', sans-serif;">
                <div style="display: flex; gap: 1rem; justify-content: flex-end;">
                    <button id="cancel-edit" style="padding: 0.8rem 1.5rem; background: var(--notion-border); border: none; border-radius: 8px; cursor: pointer; font-family: 'Poppins', sans-serif;">Cancel</button>
                    <button id="save-edit" style="padding: 0.8rem 1.5rem; background: linear-gradient(135deg, #3b82f6, #14b8a6); color: white; border: none; border-radius: 8px; cursor: pointer; font-family: 'Poppins', sans-serif;">Save Changes</button>
                </div>
            `;
            
            modal.appendChild(modalContent);
            document.body.appendChild(modal);
            
            // Focus on input
            document.getElementById("edit-task-input").focus();
            
            // Event listeners for modal buttons
            document.getElementById("cancel-edit").addEventListener("click", () => {
                modal.style.opacity = "0";
                setTimeout(() => document.body.removeChild(modal), 200);
            });
            
            document.getElementById("save-edit").addEventListener("click", () => {
                const newTitle = document.getElementById("edit-task-input").value.trim();
                if (!newTitle) {
                    alert("Task title cannot be empty");
                    return;
                }
                
                const saveBtn = document.getElementById("save-edit");
                const originalText = saveBtn.innerHTML;
                saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
                saveBtn.disabled = true;
                
                fetch(`/edit_task/${taskId}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ title: newTitle })
                })
                .then(resp => resp.text())
                .then(() => {
                    saveBtn.innerHTML = '<i class="fas fa-check"></i> Saved!';
                    saveBtn.style.background = "linear-gradient(135deg, #10b981, #059669)";
                    setTimeout(() => {
                        location.reload();
                    }, 500);
                })
                .catch(error => {
                    console.error('Error:', error);
                    saveBtn.innerHTML = originalText;
                    saveBtn.disabled = false;
                    saveBtn.style.background = "linear-gradient(135deg, #3b82f6, #14b8a6)";
                    alert("Failed to save changes. Please try again.");
                });
            });
            
            // Close modal on ESC key
            document.addEventListener("keydown", function escHandler(e) {
                if (e.key === "Escape") {
                    modal.style.opacity = "0";
                    setTimeout(() => {
                        document.body.removeChild(modal);
                        document.removeEventListener("keydown", escHandler);
                    }, 200);
                }
            });
            
            // Close modal on background click
            modal.addEventListener("click", (e) => {
                if (e.target === modal) {
                    modal.style.opacity = "0";
                    setTimeout(() => document.body.removeChild(modal), 200);
                }
            });
        });
    });

    // Add animation to task rows on load
    document.querySelectorAll("tr[data-task-id]").forEach((row, index) => {
        row.style.animation = `fadeIn 0.3s ease ${index * 0.05}s both`;
    });
    
    // Stress box hover effect
    document.querySelectorAll(".stress-box").forEach(box => {
        box.addEventListener("mouseenter", () => {
            box.style.transform = "scale(1.02)";
        });
        box.addEventListener("mouseleave", () => {
            box.style.transform = "scale(1)";
        });
    });
    
    // Course selection handling
    const courseSelect = document.getElementById('course-select');
    const newCourseFields = document.getElementById('new-course-fields');
    
    if (courseSelect && newCourseFields) {
        courseSelect.addEventListener('change', function() {
            if (this.value === 'new') {
                newCourseFields.style.display = 'grid';
                // Clear existing course selection
                document.querySelector('select[name="course_id"]').required = false;
                document.querySelector('input[name="new_course"]').required = true;
            } else {
                newCourseFields.style.display = 'none';
                document.querySelector('select[name="course_id"]').required = true;
                document.querySelector('input[name="new_course"]').required = false;
            }
        });
    }
    
    // Add CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);
});