import { getMe } from "../api/auth.js"

export function saveTokens(access, refresh){
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
}

export function getAccessToken(){
    return localStorage.getItem("access");
}

export function getRefreshToken(){
    return localStorage.getItem("refresh");
}

export function requiredeAuth(){

    const token = getAccessToken();

    if (!token){
        window.location.href = "login.html";
    }

}

export function requireAdmin(){

    const user = getUser();

    if (!user){
        window.location.href = "login.html";
        return;
    }

    if (!user.bibliotecario){
        window.location.href = "home.html";
    }
}

export function requireUser(){

    const user = getUser();

    if (!user){
        window.location.href = "login.html";
        return;
    }

    if (user.bibliotecario){
        window.location.href = "admin.html";
    }
}

export function getUser(){

    const user = localStorage.getItem("user");

    if (!user) return null;

    return JSON.parse(user);
}

export function logout(){
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");

    window.location.href = "login.html";
}

export function redirectHome(){
    const token = getAccessToken();

    if (token){
        const user = getUser();
        if (user.bibliotecario){
            window.location.href = "admin.html";
        }else{
            window.location.href = "home.html";
        }
    }
}

