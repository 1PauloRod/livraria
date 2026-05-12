import { registerRequest } from "../api/auth.js"
import { redirectHome } from "../utils/auth.js";

redirectHome();

const form = document.getElementById("register-form");


form.addEventListener("submit", async(e) => {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const last_name = document.getElementById("last-name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const password2 = document.getElementById("password2").value;

    try{
        const data = await registerRequest({ name, last_name, email, 
                                            password, password2
                                            })
        window.location.href = "../html/login.html";
    } catch(err){
        alert("Cadastro inválido");
        console.error(err);
    }
}); 