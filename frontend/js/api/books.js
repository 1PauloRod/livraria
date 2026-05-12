import { BASE_URL } from "../api/config.js"
import { getAuthHeaders } from "../api/config.js"

export async function getBooks(termo=""){

    const response = await fetch(`${BASE_URL}/livro/listar/?q=${encodeURIComponent(termo)}`, 
        {
            method: "GET",
            headers: getAuthHeaders(), 
        }
    )

    if (!response.ok){
        throw new Error("Erro ao buscar livros");
    }

    return response.json();
}

export async function getRentedBooks(termo=""){
    const response = await fetch(`${BASE_URL}/emprestimo/listar/?q=${encodeURIComponent(termo)}`, 
        {  
            method: "GET",
            headers: getAuthHeaders(),
        }
    )
    if (!response.ok) throw Error("Erro ao buscar empréstimos.");

    return response.json();
}

export async function getRentedAllBooks(termo=""){
    const response = await fetch(`${BASE_URL}/emprestimo/listar/todos/?q=${encodeURIComponent(termo)}`, 
        {
            method: "GET", 
            headers: getAuthHeaders()
        })

        if (!response.ok) throw Error("Erro ao buscar todos empréstimos");

        return response.json();
}

export async function rentBooks(book_id){

    const response = await fetch(`${BASE_URL}/emprestimo/alugar/${book_id}/`, 
        {
        method: "POST",
        headers: getAuthHeaders(), 
        body: JSON.stringify({livro_id: book_id})
    });

}

export async function removeBook(book_id){

    const response = await fetch(`${BASE_URL}/livro/deletar/${book_id}/`, 
    {
        method: "DELETE", 
        headers: getAuthHeaders(),
        body: JSON.stringify({livro_id: book_id}) 

    });

    if (!response.ok) {
        throw new Error("Erro ao remover livro");
    }

    return response;
}

export async function updateBook(book_id, data){

    const response = await fetch(`${BASE_URL}/livro/atualizar/${book_id}/`, 
         {
        method: "POST", 
        headers: getAuthHeaders(), 
        body: JSON.stringify(data) 

    });
    
    if (!response.ok) throw new Error("Erro ao atualizar livro");
    

    return response.json();
}

export async function returnBook(rent_id){

    const response = await fetch(`${BASE_URL}/emprestimo/devolver/${rent_id}/`, 
        {
            method: "POST", 
            headers: getAuthHeaders(), 
            body: JSON.stringify({emprestimo_id: rent_id})
        }
    );

    if (!response.ok) throw Error("Não foi possível devolver o livro");

    return response.json();
}


