const apiUrl = 'http://127.0.0.1:8000/todos/';

async function fetchTodos() {
    const response = await fetch(apiUrl);
    const todos = await response.json();
    renderTodos(todos);
}

function renderTodos(todos) {
    const todoList = document.getElementById('todo-list');
    todoList.innerHTML = '';
    todos.forEach(todo => {
        const todoItem = document.createElement('li');
        todoItem.className = 'list-group-item';
        todoItem.innerHTML = `
            <h5>${todo.title}</h5>
            <p>${todo.description}</p>
            <button onclick="deleteTodo(${todo.id})" class="btn btn-danger btn-sm">Delete</button>
        `;
        todoList.appendChild(todoItem);
    });
}

document.getElementById('todo-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const id = Date.now(); // Genera un ID simple basado en la marca de tiempo actual

    const newTodo = { id, title, description, completed: false };
    await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(newTodo),
    });
    fetchTodos();
});

async function deleteTodo(id) {
    await fetch(`${apiUrl}${id}`, {
        method: 'DELETE',
    });
    fetchTodos();
}

fetchTodos();
