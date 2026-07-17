import { requiredeAuth, logout, requireAdmin } from "../utils/auth.js";
import { getBooks, 
    getRentedAllBooks, 
    rentBooks, 
    getRentedBooks, 
    removeBook, 
    updateBook, 
    getFromOpenLibraryAPI,
    importBook,
    returnBook } from "../api/books.js";
import { getAllUsers, removeUser } from "../api/auth.js";

requiredeAuth();
requireAdmin();

let currentPage = 1;
let totalPages = 1;

let allUsers = []; 
let allRentedBooks = [];
let booksOptions = [];
let currentView = 'books';

const logoutBtn = document.getElementById("logout");
const container = document.getElementById("books");
const rentsBtn = document.getElementById("rentsBtn");
const btnUsers = document.getElementById("btnUsers");
const btnBooks = document.getElementById("btnBooks");
const btnSearch = document.getElementById("search");
const addBook = document.getElementById("btnAddBook");
const btnSearchBook = document.getElementById("btnSearchBook");
const btnPrev = document.getElementById("prev-page");
const btnNext = document.getElementById("next-page");
const pageInfo = document.getElementById("page-info");


function updatePagination(data){

    pageInfo.textContent = `Página ${currentPage} de ${totalPages}`;

    btnPrev.disabled = !data.previous;
    btnNext.disabled = !data.next;
}

async function fetchBooks(page=1){
    try{
        currentView = 'books';
        btnNext.hidden = false;
        btnPrev.hidden = false;
        pageInfo.hidden = false;
        btnSearchBook.hidden = true;
        currentPage = page;
        const response = await getBooks(page, btnSearch.value.trim());
        totalPages = Math.ceil(response.count / 50);
        renderBooks(response.results);
        updatePagination(response);
    }catch(err){
        console.error("Erro ao buscar livros: ", err);
    }
}

async function fetchSearchAddBook(){
    try{
        currentView = 'addBook';
        btnNext.hidden = true;
        btnPrev.hidden = true;
        pageInfo.hidden = true;
        btnSearchBook.hidden = false;
        booksOptions = [];
        renderAddBooks(booksOptions);
    }catch(err){
        console.error("Erro ao buscar livro: ", err);
    }
}

async function searchBooks(){
    const termo = btnSearch.value.trim();

    if (!termo) return; 

    try{
        booksOptions = await getFromOpenLibraryAPI(termo); 
    
    renderAddBooks(booksOptions);
    } catch(err){
        console.error(err);
    }
}

async function fetchUsers(){
    try{
        currentView = 'users'; 
        btnNext.hidden = true;
        btnPrev.hidden = true;
        pageInfo.hidden = true;
        btnSearchBook.hidden = true;
        allUsers = await getAllUsers();
    }catch(err){
        console.error("Erro ao buscar usuário: ", err);
    }
}

async function fetchAllRentedBooks(page=1){
    try{
        currentView = 'rents';
        btnNext.hidden = false;
        btnPrev.hidden = false;
        pageInfo.hidden = false;
        btnSearchBook.hidden = true;
        currentPage = page;
        const response = await getRentedAllBooks(page, btnSearch.value.trim());
        console.log(response.results);
        totalPages = Math.ceil(response.count / 50);
        renderAllReservedBooks(response.results);
        updatePagination(response); 
    }catch(err){
        console.error("Erro ao buscar empréstimos: ", err);
    }
}

async function fetchAllUsers(page=1){
    try{
        currentView = 'users';
        btnNext.hidden = false;
        btnPrev.hidden = false;
        pageInfo.hidden = false;
        btnSearchBook.hidden = true;
        currentPage = page;
        const response = await getAllUsers(page, btnSearch.value.trim());
        totalPages = Math.ceil(response.count / 50);
        renderUsers(response.results);
        updatePagination(response);
    }catch(err){
        console.error("Erro ao buscar usuários: ", err); 
    }
}

async function removeBookOnClick(book_id){
    try{
        await removeBook(book_id);
        await fetchBooks(currentPage);
        alert("Livro removido com sucesso."); 
    } catch(err){
        alert(err.message);
        console.error(err);
    }
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

    const publisherInput = document.createElement("input"); 
    publisherInput.value = book.editora;

    const obraIdInput = document.createElement("input");
    obraIdInput.value = book.obra_id;

    const totalInput = document.createElement("input");
    totalInput.type = "number"; 
    totalInput.value = book.estoque;

    const saveBtn = document.createElement("button");
    saveBtn.textContent = "Salvar"; 

    const cancelBtn = document.createElement("button");
    cancelBtn.textContent = "Cancelar";

    saveBtn.addEventListener("click", async () => {

        try{
            await updateBook(book.id, {
                titulo: titleInput.value,
                autor: authorInput.value,
                ano: yearInput.value, 
                editora: publisherInput.value, 
                obra_id: obraIdInput.value, 
                quantidade: totalInput.value

            });

            await fetchBooks(currentPage);

        }catch(err){
          
        }

    });

    cancelBtn.addEventListener("click", () => {
        fetchBooks(currentPage);
    });

    div.appendChild(titleInput);
    div.appendChild(authorInput);
    div.appendChild(yearInput);
    div.appendChild(publisherInput);
    div.appendChild(obraIdInput);
    div.appendChild(totalInput);
    
    const actions = document.createElement("div");
    actions.classList.add("actions");

    actions.appendChild(saveBtn);
    actions.appendChild(cancelBtn);

    div.appendChild(actions);
}

function renderBooks(books) {
    container.innerHTML = "";

    books.forEach((book) => {

        const div = document.createElement("div");
        div.classList.add("book-item");

        if (book.estoque === 0) {
            div.classList.add("book-unavailable");
        }

        const p = document.createElement("p");
        p.textContent = `${book.autor} - ${book.titulo} (${book.ano})`;

        const actions = document.createElement("div");
        actions.classList.add("book-actions");

        // Botão Editar (sempre aparece)
        const btnUpdate = document.createElement("button");
        btnUpdate.textContent = "Editar";

        btnUpdate.addEventListener("click", () => {
            console.log(book);
            renderEditBook(div, book);
        });

        // Botão Excluir
        const btnRemove = document.createElement("button");
        btnRemove.textContent = "Excluir";
        btnRemove.classList.add("btn-delete");

        btnRemove.addEventListener("click", () => {
            removeBookOnClick(book.id);
        });

        actions.appendChild(btnRemove);
        actions.appendChild(btnUpdate);

        div.appendChild(p);

        if (book.estoque === 0) {
            const span = document.createElement("span");
            span.textContent = "Indisponível";
            div.appendChild(span);
        }

        div.appendChild(actions);

        container.appendChild(div);
    });
}

async function removeUserOnClick(user_id){
    await removeUser(user_id);
    await fetchAllUsers();
}

function renderAddBooks(books){
    container.innerHTML = "";

    books.forEach((book) => {
        const div = document.createElement("div");
        div.classList.add("book-item");

        const p = document.createElement("p");
        p.textContent = `${book.autores} - ${book.titulo} (${book.ano})`;

        const btnAdd = document.createElement("button");
        btnAdd.textContent = "Adicionar";
        btnAdd.classList.add("btn-save");

        btnAdd.addEventListener("click", async () => {
            try {
                const response = await importBook(book);

                console.log(book); 

                if (response.created) {
                    alert("Livro adicionado com sucesso!");
       
                } else {
                alert("Esse livro já existe.");
            }
            } catch (err) {
                console.error(err);
                alert("Erro ao adicionar livro.");
            }
        });

        // Container dos botoes
        const actions = document.createElement("div");
        actions.classList.add("book-actions");

        actions.appendChild(btnAdd);

        div.appendChild(p);
        div.appendChild(actions);

        container.appendChild(div);
    });
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
    await fetchAllRentedBooks(1);
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
    fetchBooks(currentPage);
    
    btnBooks.addEventListener("click", () => {
        fetchBooks(currentPage);
    });

    btnAddBook.addEventListener("click", () => {
        fetchSearchAddBook();
    });

    btnSearchBook.addEventListener("click", searchBooks);

    btnUsers.addEventListener("click", () => {
        fetchAllUsers();
    });

    rentsBtn.addEventListener("click", () => {
        fetchAllRentedBooks(1);
    });

    btnNext.addEventListener("click", () => {

    if (currentView === 'books'){
        if(currentPage < totalPages){
            fetchBooks(currentPage + 1);
        }
    }else if (currentView === 'users'){
        if(currentPage < totalPages){
            fetchAllUsers(currentPage + 1);
        }
    }else if (currentView === 'rents'){
        if(currentPage < totalPages){
            fetchAllRentedBooks(currentPage + 1);
        }
    }
    });

    btnPrev.addEventListener("click", () => {

    if (currentView === 'books'){
        if(currentPage > 1){
        fetchBooks(currentPage - 1);
        }
    }else if (currentView === 'users'){
        if(currentPage > 1){
            fetchAllUsers(currentPage - 1);
        }
    }else if (currentView === 'rents'){
        if(currentPage > 1){
            fetchAllRentedBooks(currentPage - 1);
        }
    }
    });
}

logoutBtn.addEventListener('click', (e)=>{
    logout();
});


btnSearch.addEventListener("input", (e) => {

    if (currentView === 'books'){

        fetchBooks(1); 
    }

    else if (currentView === 'addBook'){
        const filter = booksOptions.filter((book) => 
        book.titulo.toLowerCase().includes(termo))
        renderAddBooks(filter);
    }

    else if (currentView === 'users'){
        fetchAllUsers(1);
    }

    else if (currentView === 'rents'){
        fetchAllRentedBooks(1);
    }

})

renderHome();