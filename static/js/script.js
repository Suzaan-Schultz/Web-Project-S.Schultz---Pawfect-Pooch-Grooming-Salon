// Wait for the DOM to fully load before running scripts
document.addEventListener("DOMContentLoaded", () => {

    // Lightbox modal added to make images more visually appealing
    const galleryImages = document.querySelectorAll(".gallery-img");
    const lightbox = document.getElementById("lightbox");
    const lightboxImg = document.getElementById("lightboxImg");
    const closeBtn = document.getElementById("closeBtn");

    if (galleryImages.length && lightbox && lightboxImg && closeBtn) {
        galleryImages.forEach(img => {
            // Enlarge the image when clicked on
            img.addEventListener("click", () => {
                lightbox.classList.add("show");
                lightboxImg.src = img.src;
            });
        });
        // Close the image when the close button is clicked
        closeBtn.addEventListener("click", () => {
            lightbox.classList.remove("show");
        });
        
        // Close the image if anywhere else on the screen is clicked
        lightbox.addEventListener("click", (e) => {
            if (e.target === lightbox) {
                lightbox.classList.remove("show");
            }
        });
    }


    // Toggle between the login and register forms
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
    const showRegisterBtn = document.getElementById("show-register");
    const showLoginBtn = document.getElementById("show-login");

    if (loginForm && registerForm && showRegisterBtn && showLoginBtn) {
        // Show the registration form
        showRegisterBtn.addEventListener("click", () => {
            loginForm.style.display = "none";
            registerForm.style.display = "block";
        });

        // Show the login form
        showLoginBtn.addEventListener("click", () => {
            registerForm.style.display = "none";
            loginForm.style.display = "block";
        });
    }

    // Show edit/delete buttons if user is logged in (in session)
    const sessionUsername = "{{ session.username if 'username' in session else '' }}";
    if (sessionUsername) {
        const editDeleteDiv = document.createElement("div");
        editDeleteDiv.style.marginTop = "20px";

        // Edit button
        const editForm = document.createElement("form");
        editForm.action = "/edit_account";
        editForm.method = "GET";
        editForm.style.display = "inline-block";
        const editBtn = document.createElement("button");
        editBtn.type = "submit";
        editBtn.className = "btn edit-btn";
        editBtn.textContent = "Edit Account";
        editForm.appendChild(editBtn);
        editDeleteDiv.appendChild(editForm);

        // Delete button
        const deleteForm = document.createElement("form");
        deleteForm.action = "/delete_account";
        deleteForm.method = "POST";
        deleteForm.style.display = "inline-block";
        deleteForm.onsubmit = function() {
            return confirm("Are you sure you want to delete your account?");
        };
        const deleteBtn = document.createElement("button");
        deleteBtn.type = "submit";
        deleteBtn.className = "btn delete-btn";
        deleteBtn.textContent = "Delete Account";
        deleteForm.appendChild(deleteBtn);
        editDeleteDiv.appendChild(deleteForm);

        // Append edit or delete buttons
        loginForm.appendChild(editDeleteDiv);
    }

});
