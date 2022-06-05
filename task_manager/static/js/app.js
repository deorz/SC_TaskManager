if (document.getElementById('signIn')) {

    document.getElementById('signIn').addEventListener('click', async () => {
        const login = document.getElementById('inputLogin').value
        const password = document.getElementById('inputPassword').value

        if (login && password) {
            const response = await fetch('http://localhost:8000/api/v1/users/login/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    username: login,
                    password: password
                })

            });
            if (response.ok) {
                sessionStorage.setItem('username', login)
                sessionStorage.setItem('password', password)
                window.location.href = 'http://localhost:63342/SC_TaskManager/task_manager/templates/index.html'
            }
            else {
                const alertMessage = await response.json()
                alert(`${alertMessage['error']}`)
            }
        }
    });
}

if (sessionStorage.getItem('username') && sessionStorage.getItem('password')) {
    const registerOrLogin = document.getElementById('registerOrLogin');
    registerOrLogin.innerHTML = `
        <span class="mt-3 me-2">Пользователь: ${sessionStorage.getItem('username')}</span>
        <a onclick="logOut()" class="btn btn-outline-light me-2">Выйти</a>
    `
}

function logOut() {
    sessionStorage.removeItem('username')
    sessionStorage.removeItem('password')
    document.location.reload()
}

if (document.getElementById('signUp')) {

    document.getElementById('signUp').addEventListener('click', async () => {
        const first_name = document.getElementById('inputFirstName').value
        const last_name = document.getElementById('inputLastName').value
        const email = document.getElementById('inputEmail').value
        const login = document.getElementById('inputLogin').value
        const password = document.getElementById('inputPassword').value

        if (first_name && last_name && email && login && password) {
            const response = await fetch('http://localhost:8000/api/v1/users/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    first_name,
                    last_name,
                    email,
                    username: login,
                    password
                })
            });
            if (response.ok) {
                window.location.href = 'http://localhost:63342/SC_TaskManager/task_manager/templates/index.html'
            }
            else {
                const alertMessage = await response.json()
                alert(`${alertMessage['error']}`)
            }
        }
    });
}


if (window.location.href === 'http://localhost:63342/SC_TaskManager/task_manager/templates/tasks.html' ||
    window.location.href === 'http://localhost:63342/SC_TaskManager/task_manager/templates/tasks.html#') {

    window.addEventListener('DOMContentLoaded', getTasks)

    async function getTasks() {
        const response = await fetch('http://localhost:8000/api/v1/status/', {
            method: 'GET',
            headers: {
                "Authorization": `Basic ${btoa(`${sessionStorage.getItem('username')}:${sessionStorage.getItem('password')}`)}`
            }
        });
        const tasks = await response.json()
        tasks.forEach(task => representTasks(task))
    }

    function representTasks({task, status}) {
        const tasks_rows = document.getElementById('tasks');
        tasks_rows.insertAdjacentHTML('beforeend', `
        <th scope="row">
            <a onclick="fillTaskForm(${task['id']})" class="btn btn-link" data-bs-toggle="modal"
                data-bs-target="#exampleModal1">
                    ${task['id']}
            </a>
        </th>
            <td>${task['path']}</td>
            <td>${task['params']}</td>
            <td>${task['num_threads']}</td>
            <td>${task['priority']}</td>
            <td>${status}</td>
            <td><button onclick="executeTask(${task['id']})" id="execute_${task['id']}" class="btn btn-outline-primary">Запустить</button></td>
            <td><button onclick="pauseTask(${task['id']})" id="pause_${task['id']}" class="btn btn-outline-primary">Приостановить</button></td>
            <td><button onclick="deleteTask(${task['id']})" id="delete_${task['id']}" class="btn btn-outline-primary">Удалить</button></td>
        `);
    }

    async function fillTaskForm(task_id) {
        const response = await fetch(`http://localhost:8000/api/v1/tasks/${task_id}`, {
            method: 'GET',
            headers: {
                "Authorization": `Basic ${btoa(`${sessionStorage.getItem('username')}:${sessionStorage.getItem('password')}`)}`
            }
        });
        const result = await response.json()

        const task_form = document.getElementById('exampleModal1');
        task_form.innerHTML = `
            <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel1">Редактирование задачи</h5>
                    <button type="button" class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="pathField" class="col-form-label">
                            Уникальный идентификатор задачи
                        </label>
                        <input type="text" class="form-control"
                               id="inputTaskId" value="${result['id']}" disabled readonly>
                    </div>
                    <div class="mb-3">
                        <label for="pathField" class="col-form-label">
                            Путь файла
                        </label>
                        <input type="text" class="form-control"
                               id="inputFilePath1" value="${result['path']}">
                    </div>
                    <div class="mb-3">
                        <label for="paramsField" class="col-form-label">
                            Параметры командной строки
                        </label>
                        <input type="text" class="form-control"
                               id="inputParams1" value="${result['params']}">
                    </div>
                    <div class="mb-3">
                        <label for="numThreadsField" class="col-form-label">
                            Количество потоков
                        </label>
                        <input type="number" class="form-control"
                               id="inputNumThreads1" value="${result['num_threads']}">
                    </div>
                    <div class="mb-3">
                        <label for="priorityField" class="col-form-label">
                            Приоритет
                        </label>
                        <input type="number" class="form-control"
                               id="inputPriority1" max="100" value="${result['priority']}">
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary"
                            data-bs-dismiss="modal">Закрыть
                    </button>
                    <button onclick="updateTask()" type="button" id="updateTask"
                            class="btn btn-primary">
                        Изменить
                    </button>
                    </div>`

    }

    async function updateTask() {
        const id = document.getElementById('inputTaskId').value
        const path = document.getElementById('inputFilePath1').value
        const params = document.getElementById('inputParams1').value
        const num_threads = document.getElementById('inputNumThreads1').value
        const priority = document.getElementById('inputPriority1').value

        const response = await fetch(`http://localhost:8000/api/v1/tasks/${id}/`, {
            method: 'PATCH',
            headers: {
                "Authorization": `Basic ${btoa(`${sessionStorage.getItem('username')}:${sessionStorage.getItem('password')}`)}`,
                "Content-Type": 'application/json'
            },
            body: JSON.stringify({
                path,
                params,
                num_threads,
                priority
            })
        });
        if (response.ok) {
            window.location.reload()

        } else {
            const alertMessage = await response.json()
            if (alertMessage['path']) {
                alert(`${alertMessage['path']}`)
            }
            else if (alertMessage['params']) {
                alert(`${alertMessage['params']}`)
            }
            else if (alertMessage['num_threads']) {
                alert(`${alertMessage['num_threads']}`)
            }
            else if (alertMessage['priority']) {
                alert(`${alertMessage['priority']}`)
            }

        }

    }

    async function executeTask(task_id) {
        const response = await fetch(`http://localhost:8000/api/v1/tasks/${task_id}/execute/`, {
            method: 'POST',
            headers: {
                "Authorization": `Basic ${btoa(`${sessionStorage.getItem('username')}:${sessionStorage.getItem('password')}`)}`
            }
        });
        if (response.ok) {
            window.location.reload()
        }
        else {
            const alertMessage = await response.json()
            alert(`${alertMessage['error']}`)
        }

    }

    async function pauseTask(task_id) {
        const response = await fetch(`http://localhost:8000/api/v1/tasks/${task_id}/pause/`, {
            method: 'POST',
            headers: {
                "Authorization": `Basic ${btoa(`${sessionStorage.getItem('username')}:${sessionStorage.getItem('password')}`)}`
            }
        });
        if (response.ok) {
            window.location.reload()
        }
        else {
            const alertMessage = await response.json()
            alert(`${alertMessage['error']}`)
        }

    }

    async function deleteTask(task_id) {
        const response = await fetch(`http://localhost:8000/api/v1/tasks/${task_id}/delete/`, {
            method: 'POST',
            headers: {
                "Authorization": `Basic ${btoa(`${sessionStorage.getItem('username')}:${sessionStorage.getItem('password')}`)}`
            }
        });
        if (response.ok) {
            window.location.reload()
        }
        else {
            const alertMessage = await response.json()
            alert(`${alertMessage['error']}`)
        }

    }

    if (document.getElementById('createTask')) {

        document.getElementById('createTask').addEventListener('click', async () => {
            const path = document.getElementById('inputFilePath').value
            const params = document.getElementById('inputParams').value
            const num_threads = document.getElementById('inputNumThreads').value
            const priority = document.getElementById('inputPriority').value

            if (params && num_threads && priority) {
                const response = await fetch('http://localhost:8000/api/v1/tasks/', {
                    method: 'POST',
                    headers: {
                        "Authorization": `Basic ${btoa(`${sessionStorage.getItem('username')}:${sessionStorage.getItem('password')}`)}`,
                        "Content-Type": 'application/json'
                    },
                    body: JSON.stringify({
                        path,
                        params,
                        num_threads,
                        priority
                    })
                });
                if (response.ok) {
                    window.location.reload()
                } else {
                    alert(response.json())
                }

            }
        });

    }
}

if (window.location.href === 'http://localhost:63342/SC_TaskManager/task_manager/templates/queue.html' ||
    window.location.href === 'http://localhost:63342/SC_TaskManager/task_manager/templates/queue.html#') {

    window.addEventListener('DOMContentLoaded', getOrder)

    async function getOrder() {
        const response = await fetch('http://localhost:8000/api/v1/order/', {
            method: 'GET',
            headers: {
                "Authorization": `Basic ${btoa(`${sessionStorage.getItem('username')}:${sessionStorage.getItem('password')}`)}`
            }
        });
        const order = await response.json()
        order.forEach(order_object => representOrder(order_object))
    }

    function representOrder({task, order_number}) {
        const order_rows = document.getElementById('order');
        order_rows.insertAdjacentHTML('beforeend', `
        <th scope="row">${task['id']}</th>
            <td>${task['path']}</td>
            <td>${task['params']}</td>
            <td>${task['num_threads']}</td>
            <td>${task['priority']}</td>
            <td>${order_number}</td>
        `);
    }

}




