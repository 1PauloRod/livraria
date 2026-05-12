export function saveToken(token){
    localStorage.setItem("token", token);
}

export function getToken(){
    return localStorage.getItem("token");
}

export function requiredeAuth(){

    const token = getToken();

    if (!token){
        window.location.href = "login.html";
    }

}

export function logout(){
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

export function redirectHome(){
    const token = getToken();

    if (token){
        window.location.href = "home.html";
    }
}