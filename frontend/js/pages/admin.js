import { requiredeAuth, logout, requireAdmin } from "../utils/auth.js";
import { getBooks, 
    getRentedAllBooks, 
    rentBooks, 
    getRentedBooks, 
    removeBook, 
    updateBook, 
    returnBook } from "../api/books.js";
import { getAllUsers, removeUser } from "../api/auth.js";

requiredeAuth();
requireAdmin();

let allBooks = [];
let allUsers = []; 
let allRentedBooks = [];
let currentView = 'books';

const logoutBtn = document.getElementById("logout");
const container = document.getElementById("books");
const rentsBtn = document.getElementById("rentsBtn");
const btnUsers = document.getElementById("btnUsers");
const btnBooks = document.getElementById("btnBooks");
const btnSearch = document.getElementById("search");

async function fetchBooks(){
    
    try{
        currentView = 'books';
        allBooks = await getBooks();
        renderBooks(allBooks);
    }catch(err){
        console.error("Erro ao buscar livros: ", err);
    }
}

async function fetchUsers(){
    try{
        currentView = 'users'; 
        allUsers = await getAllUsers();
    }catch(err){
        console.error("Erro ao buscar usuário: ", err);
    }
}

async function fetchAllRentedBooks(){
    try{
        currentView = 'rents';
        allRentedBooks = await getRentedAllBooks();
        console.log(allRentedBooks.data_devolucao);
        renderAllReservedBooks(allRentedBooks);
    }catch(err){
        console.error("Erro ao buscar empréstimos: ", err);
    }
}

async function fetchAllUsers(){
    try{
        currentView = 'users';
        allUsers = await getAllUsers();
        renderUsers(allUsers);
    }catch(err){

    }
}

async function removeBookOnClick(book_id){
    await removeBook(book_id);
    await fetchBooks();
}

function renderEditBook(div, book){

    div.innerHTML = "";

    const titleInput = document.createElement("input");
    titleInput.value = book.titulo;

    const authorInput = document.createElement("input");
    authorInput.value = book.autor;

    const yearInput = document.createElement("input");
    yearInput.type = "number";
    yearInput.value = book.ano;

    const saveBtn = document.createElement("button");
    saveBtn.textContent = "Salvar";

    const cancelBtn = document.createElement("button");
    cancelBtn.textContent = "Cancelar";

    saveBtn.addEventListener("click", async () => {

        try{
            await updateBook(book.id, {
                titulo: titleInput.value,
                autor: authorInput.value,
                ano: yearInput.value
            });

            await fetchBooks();

        }catch(err){
            console.error(err);
        }

    });

    cancelBtn.addEventListener("click", () => {
        fetchBooks();
    });

    div.appendChild(titleInput);
    div.appendChild(authorInput);
    div.appendChild(yearInput);
    const actions = document.createElement("div");
    actions.classList.add("actions");

    actions.appendChild(saveBtn);
    actions.appendChild(cancelBtn);

    div.appendChild(actions);
}

function renderBooks(books){
    container.innerHTML = "";

    books.forEach((book) => {
        const div = document.createElement("div");
        div.classList.add("book-item");

        if (!book.disponivel) {
            div.classList.add("book-unavailable");
        }

        const p = document.createElement("p");
        p.textContent = `${book.autor} - ${book.titulo} (${book.ano})`;

        if (book.disponivel) {
            const btnRemove = document.createElement("button");
            const btnUpdate = document.createElement("button");
            btnRemove.textContent = "Excluir";
            btnUpdate.textContent = "Editar";
            btnRemove.addEventListener("click", () => {
                removeBookOnClick(book.id);
            });

            btnUpdate.addEventListener("click", () => {
                renderEditBook(div, book);

            });

            const actions = document.createElement("div");
            actions.classList.add("book-actions");

            btnRemove.classList.add("btn-delete");
            btnUpdate.classList.add("btn-edit");

            actions.appendChild(btnRemove);
            actions.appendChild(btnUpdate);

            div.appendChild(p);
            div.appendChild(actions);

        } else {
            const span = document.createElement("span");
            span.textContent = "Alugado";

            div.appendChild(p);
            div.appendChild(span);
        }

        container.appendChild(div);
    });
}

async function removeUserOnClick(user_id){
    await removeUser(user_id);
    await fetchAllUsers();
}

function renderUsers(users){
    container.innerHTML = "";

    users.forEach((user) => {

        const div = document.createElement("div");
        div.classList.add("rented-item");

        const p = document.createElement("p");

        let text = `${user.name} ${user.last_name} - ${user.email}`;

        const btnRemoveUser = document.createElement("button");
        btnRemoveUser.textContent = "Excluir";
        btnRemoveUser.addEventListener("click", () => {
            removeUserOnClick(user.id); 
        })

        const statusSpan = document.createElement("span");
        statusSpan.classList.add("rented-status");

        p.textContent = text;
        p.appendChild(statusSpan);

        const actions = document.createElement("div");
        actions.classList.add("actions");

        btnRemoveUser.classList.add("btn-delete");

        actions.appendChild(btnRemoveUser);

        div.appendChild(p);
        div.appendChild(actions);
        container.appendChild(div);
    }); 
}

async function returnBookOnClick(rent_id){
    await returnBook(rent_id);
    await fetchAllRentedBooks();
}

function renderAllReservedBooks(rentedBooks){
    container.innerHTML = "";

    rentedBooks.forEach((rentedBook) => {

        const div = document.createElement("div");
        div.classList.add("rented-item");

        const p = document.createElement("p");

        const data = new Date(rentedBook.data_emprestimo);

        let text = `${rentedBook.user.email} - ${rentedBook.livro.autor} - ${rentedBook.livro.titulo} (${rentedBook.livro.ano}) - ${data.toLocaleString("pt-BR")} - `;

        const statusSpan = document.createElement("span");
        statusSpan.classList.add("rented-status");

        p.textContent = text;

        if (!rentedBook.data_devolucao){

            statusSpan.textContent = "Ativo";
            statusSpan.classList.add("status-active");

            const btnReturnBook = document.createElement("button");

            btnReturnBook.textContent = "Devolver";

            btnReturnBook.classList.add("btn-save");

            btnReturnBook.addEventListener("click", () => {
                returnBookOnClick(rentedBook.id);
            });

            const actions = document.createElement("div");
            actions.classList.add("actions");

            actions.appendChild(btnReturnBook);

            p.appendChild(statusSpan);

            div.appendChild(p);
            div.appendChild(actions);

        } else {

            statusSpan.textContent = "Devolvido";
            statusSpan.classList.add("status-returned");

            p.appendChild(statusSpan);

            div.appendChild(p);
        }

        container.appendChild(div);
    }); 
}


function renderHome(){
    container.innerHTML = "";
    fetchBooks();
    
    btnBooks.addEventListener("click", () => {
        fetchBooks();
    });

    btnUsers.addEventListener("click", () => {
        fetchAllUsers();
    });

    rentsBtn.addEventListener("click", () => {
        fetchAllRentedBooks();
    });
}

logoutBtn.addEventListener('click', (e)=>{
    logout();
});


btnSearch.addEventListener("input", (e) => {
    const termo = e.target.value.toLowerCase();

    if (currentView === 'books'){
        const filter = allBooks.filter((book) => 
        book.titulo.toLowerCase().includes(termo) ||
        book.autor.toLowerCase().includes(termo))

        renderBooks(filter);
    }

    else if (currentView === 'users'){
        const filter = allUsers.filter((user) => 
        user.email.toLowerCase().includes(termo) || 
        user.name.toLowerCase().includes(termo)  ||
        user.last_name.toLowerCase().includes(termo) ) 

        renderUsers(filter); 
    }

    else if (currentView === 'rents'){
        const filter = allRentedBooks.filter((rent) => 
        rent.user.email.toLowerCase().includes(termo))
        
        renderAllReservedBooks(filter);
    }

})

renderHome();