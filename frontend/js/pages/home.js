import { requiredeAuth, logout, redirectHome, requireUser } from "../utils/auth.js";
import { getBooks, rentBooks, getRentedBooks } from "../api/books.js";

requiredeAuth();
requireUser();

const title = document.querySelector("h1");
const user = JSON.parse(localStorage.getItem("user"));
title.textContent = `Olá, ${user.name}`
   

let allBooks = [];
let allRentedBooks = [];
let currentView = 'books';

const container = document.getElementById("books");
const searchInput = document.getElementById("search");
const logoutBtn = document.getElementById("logout");
const renderRentBooksBtn = document.getElementById("rent-books");
const renderMyReservedBooksBtn = document.getElementById("reserved-books");

async function fetchBooks() {
    try{
        currentView = 'books';
        allBooks = await getBooks();
        renderBooks(allBooks);
        console.log(allBooks);
    }catch(err){
        console.error("Erro ao buscar livros: ", err);
    }
}

async function fetchMyRentedBooks(){
    try{
        currentView = 'rented';
        allRentedBooks = await getRentedBooks();
        console.log(allRentedBooks.data_devolucao);
        renderMyReservedBooks(allRentedBooks);
    }catch(err){
        console.error("Erro ao buscar empréstimos: ", err);
    }
}

function rentBookOnClick(book_id){
    rentBooks(book_id);
    fetchBooks();
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
            const btn = document.createElement("button");
            btn.textContent = "Alugar";
            btn.addEventListener("click", () => {
                rentBookOnClick(book.id);
            });

            div.appendChild(p);
            div.appendChild(btn);

        } else {
            const span = document.createElement("span");
            span.textContent = "Indisponível";

            div.appendChild(p);
            div.appendChild(span);
        }

        container.appendChild(div);
    });
}

function renderMyReservedBooks(rentedBooks){
    container.innerHTML = "";

    rentedBooks.forEach((rentedBook) => {
        const div = document.createElement("div");
        div.classList.add("rented-item");

        const p = document.createElement("p");
        const date_rent = new Date(rentedBook.data_emprestimo);
        let text = `${rentedBook.livro.autor} - ${rentedBook.livro.titulo} (${rentedBook.livro.ano}) - ${date_rent.toLocaleString("pt-BR")} - `;

        const statusSpan = document.createElement("span");
        statusSpan.classList.add("rented-status");

        if (!rentedBook.data_devolucao){
            div.classList.add("rented-active"); 
            statusSpan.textContent = "Ativo";
            statusSpan.classList.add("status-active");
        } else {
            const date_return = new Date(rentedBook.data_devolucao);
            statusSpan.textContent = date_return.toLocaleString("pt-BR");
            statusSpan.classList.add("status-returned");
        }

        p.textContent = text;
        p.appendChild(statusSpan);

        div.appendChild(p);
        container.appendChild(div);
    }); 
}

function renderHome(){
    container.innerHTML = "";

    fetchBooks();

    renderRentBooksBtn.addEventListener("click", ()=> {
       fetchBooks();
    }); 

    renderMyReservedBooksBtn.addEventListener("click", () => {
        fetchMyRentedBooks();
    }); 
}

searchInput.addEventListener("input", (e)=>{
    const termo = e.target.value.toLowerCase();
    
    if (currentView === 'books'){
        const filters = allBooks.filter((livro) => 
        livro.titulo.toLowerCase().includes(termo) || 
        livro.autor.toLowerCase().includes(termo));

        renderBooks(filters);

    }else if (currentView === 'rented'){
       const filters = allRentedBooks.filter((rentedBook) => 
            rentedBook.livro.titulo.toLowerCase().includes(termo) ||
            rentedBook.livro.autor.toLowerCase().includes(termo)
        );

        renderMyReservedBooks(filters);
    }
});

logoutBtn.addEventListener("click", (e)=>{
    logout();
})


//fetchBooks();
renderHome();

