import { loginRequest, getMe } from "../api/auth.js";
import { saveToken, redirectHome } from "../utils/auth.js"

redirectHome(); 

const form = document.getElementById("login-form");


form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try{
        const data = await loginRequest({ email, password});
        
        console.log("LOGIN RESPONSE COMPLETO:", data);
        console.log("ACCESS:", data.token);

        const token = data.token

        saveToken(token);

        const user = await getMe();

        localStorage.setItem("user", JSON.stringify(user));

        if (user.bibliotecario){
            window.location.href = "admin.html"
        }else{
            window.location.href = "home.html"
        }
        
        
    }catch(err){
        const errorMessage = document.getElementById("error-message");
        errorMessage.textContent = "Login inválido";
        console.log(err); 
    }
})