import { BASE_URL, getAuthHeaders } from "../api/config.js"

export async function registerRequest(data){
    const response = await fetch(`${BASE_URL}/accounts/register/`, 
        {
            method: "POST", 
            headers: {
                "Content-Type": "application/json", 
            }, 
            body: JSON.stringify(data),
        }
    );

    if (!response.ok) throw new Error("Erro no cadastro");

    return response.json();
}

export async function loginRequest(data){
    const response = await fetch(`${BASE_URL}/accounts/login/`, 
        {
            method: "POST", 
            headers: {
                "Content-Type": "application/json"
            }, 
            body: JSON.stringify(data)
        }
    );

    if (!response.ok) throw new Error("Erro no login");

    return response.json();
}


export async function getMe(){

    const response = await fetch(`${BASE_URL}/accounts/me/`, {
        headers: getAuthHeaders()
    });

    if (!response.ok){
        throw new Error("Erro ao buscar usuário");
    }
    return await response.json();
}

export async function getAllUsers(page=1, termo=""){

    const response = await fetch(`${BASE_URL}/accounts/listar/?page=${page}&q=${encodeURIComponent(termo)}`, 
        {
            method: "GET", 
            headers: getAuthHeaders()
        }
    );

    if (!response.ok) throw new Error("Erro ao buscar usuário");

    return await response.json();
}

export async function removeUser(user_id){

    const response = await fetch(`${BASE_URL}/accounts/deletar/${user_id}/`, 
        {
            method: "DELETE", 
            headers: getAuthHeaders(), 
            body: JSON.stringify({user_id: user_id})
        }
    ); 

    console.log(response);
    if (!response.ok){
        alert("Não foi possivel remover usuario ");
    };

    return response;
}
