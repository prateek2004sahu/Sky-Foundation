// ================= CAPTCHA =================
const captchas = {
    login: "",
};

// Generate random captcha
function generateCaptcha(type) {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let captcha = "";

    for (let i = 0; i < 5; i++) {
        captcha += chars.charAt(Math.floor(Math.random() * chars.length));
    }

    captchas[type] = captcha;

    const captchaElement = document.getElementById(type + "Captcha");
    if (captchaElement) {
        captchaElement.innerText = captcha;
    }
}

// ================= LOAD AFTER DOM =================
document.addEventListener("DOMContentLoaded", function () {

    // Load captcha
    generateCaptcha("login");

    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", async function (e) {
            e.preventDefault(); // stop refresh

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            const captchaInput = document.getElementById("loginCaptchaInput").value;

            // ✅ CAPTCHA VALIDATION (case-insensitive)
            if (captchaInput.toUpperCase() !== captchas["login"]) {
                alert("Invalid Captcha!");
                generateCaptcha("login");
                return;
            }

            try {
                const response = await fetch("/api/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    alert("Login successful!");

                    // ✅ Switch UI
                    document.getElementById("login").style.display = "none";
                    document.getElementById("dashboard").style.display = "block";

                    // ✅ Reset form
                    loginForm.reset();

                } else {
                    alert(data.message || "Login failed");
                    generateCaptcha("login");
                }

            } catch (error) {
                console.error(error);
                alert("Server error");
            }
        });
    }
});


// ================= LOGOUT =================
async function logout() {
    try {
        await fetch("/api/logout", {
            method: "POST"
        });

        // Switch back to login
        document.getElementById("dashboard").style.display = "none";
        document.getElementById("login").style.display = "block";

        generateCaptcha("login");

    } catch (error) {
        console.error(error);
        alert("Logout failed");
    }
}