const registerButton = document.getElementById('register');
const logoutButton = document.getElementById('logout');
const loginButton = document.getElementById('login');


if (loginButton) {
    loginButton.onclick = async function (e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        const res = await axios.post("/api/auth/sign-in", { password, email });
        localStorage.setItem('auth', res.data.token);
        localStorage.setItem('name', res.data.name);
        window.location = "/";
    }
}

if (registerButton) {
    const signUpForm = jQuery("#sign-up-form")
    
    registerButton.onclick = async function (e) {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const repeatPassword = document.getElementById('repeatPassword').value;
        const firstName = document.getElementById('firstName').value;
        const lastName = document.getElementById('lastName').value;
        const form = document.getElementById('sign-up-form')

        form.reportValidity()

        if (signUpForm.valid()) {
            await axios.post("/api/auth/sign-up", { firstName, lastName, password, email, repeatPassword });
            window.location = "/login.html";
        }
    }
}

if (logoutButton) {
    logoutButton.onclick = function () {
        localStorage.removeItem('auth');
    }
}