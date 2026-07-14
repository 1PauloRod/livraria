import { requiredeAuth, logout, redirectHome, requireUser } from "../utils/auth.js";
import { getBooks, rentBooks, getRentedBooks } from "../api/books.js";

requiredeAuth();
requireUser();

const title = document.querySelector("h1");
const user = JSON.parse(localStorage.getItem("user"));
title.textContent = `Olá, ${user.name}`

let currentPage = 1;
let totalPages = 1;

let allBooks = [];
let allRentedBooks = [];
let currentView = 'books';

const container = document.getElementById("books");
const searchInput = document.getElementById("search");
const logoutBtn = document.getElementById("logout");
const renderRentBooksBtn = document.getElementById("rent-books");
const renderMyReservedBooksBtn = document.getElementById("reserved-books");
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
        currentPage = page;
        const response = await getBooks(page, searchInput.value.trim());
        totalPages = Math.ceil(response.count / 50);
        renderBooks(response.results);
        updatePagination(response);
    }catch(err){
        console.error("Erro ao buscar livros: ", err);
    }
}

async function fetchMyRentedBooks(){
    try{
        currentView = 'rented';
        btnNext.hidden = false;
        btnPrev.hidden = false;
        pageInfo.hidden = false;
        allRentedBooks = await getRentedBooks();
        console.log(allRentedBooks.data_devolucao);
        renderMyReservedBooks(allRentedBooks);
    }catch(err){
        console.error("Erro ao buscar empréstimos: ", err);
    }
}

function rentBookOnClick(book_id){
    rentBooks(book_id);
    fetchBooks(1);
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

        const btn = document.createElement("button");

        if (book.usuario_possui) {

            btn.textContent = "Alugado";
            btn.disabled = true;
            btn.classList.add("btn-disabled");

        } else if (book.estoque === 0) {

            btn.textContent = "Indisponível";
            btn.disabled = true;
            btn.classList.add("btn-disabled");

        } else {

            btn.textContent = "Alugar";

            btn.addEventListener("click", () => {
                rentBookOnClick(book.id);
            });
        }

        div.appendChild(p);
        div.appendChild(btn);

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

    fetchBooks(1);

    renderRentBooksBtn.addEventListener("click", ()=> {
       fetchBooks(1);
    }); 

    renderMyReservedBooksBtn.addEventListener("click", () => {
        fetchMyRentedBooks();
    }); 

    btnNext.addEventListener("click", () => {

    if(currentPage < totalPages){
        fetchBooks(currentPage + 1);
    }

    });

    btnPrev.addEventListener("click", () => {

    if(currentPage > 1){
        fetchBooks(currentPage - 1);
    }

    });
}

searchInput.addEventListener("input", (e)=>{
    
    if (currentView === 'books'){
        fetchBooks(1);

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

