// Функция для получения CSRF-токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Функция для обработки лайков
function toggleLike(element) {
    const itemId = element.getAttribute('data-item-id'); // Получаем ID публикации

    // Делаем POST-запрос
    fetch(`/liked-publication/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Добавляем CSRF-токен
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Обновляем интерфейс в зависимости от ответа
            if (data.liked) {
                element.src = '/static/images/heart.png'; // Меняем картинку на заполненное сердечко
            } else {
                element.src = '/static/images/love.png'; // Меняем картинку на пустое сердечко
            }
        } else {
            console.error('Ошибка:', data.error);
        }
    })
    .catch(error => {
        console.error('Ошибка запроса:', error);
    });
}
// Функция для обработки подписки и отписки
function toggleFollow(button) {
    const userId = button.getAttribute('data-user-id');  // Получаем ID пользователя

    // Выполняем AJAX-запрос
    fetch(`/follow-unfollow/${userId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Указываем тип данных
            'X-CSRFToken': getCookie('csrftoken'),  // Добавляем CSRF-токен
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Обновляем интерфейс в зависимости от действия
            if (data.action === 'followed') {
                // Если подписались, меняем текст на "Отписаться" и стиль кнопки
                button.textContent = 'Отписаться';
                button.classList.remove('btn-primary');
                button.classList.add('btn-danger');
                button.onclick = () => toggleFollow(button); // Переводим на отписку
            } else {
                // Если отписались, меняем текст на "Подписаться" и стиль кнопки
                button.textContent = 'Подписаться';
                button.classList.remove('btn-danger');
                button.classList.add('btn-primary');
                button.onclick = () => toggleFollow(button); // Переводим на подписку
            }
        } else {
            console.error('Ошибка:', data.error);
        }
    })
    .catch(error => {
        console.error('Ошибка запроса:', error);
    });
}


document.addEventListener("DOMContentLoaded", () => {
    const viewButtons = document.querySelectorAll(".view-comments-btn");

    viewButtons.forEach(button => {
        button.addEventListener("click", () => {
            const commentsContainer = button.nextElementSibling;
            const isVisible = button.getAttribute("data-comments-visible") === "true";

            if (isVisible) {
                commentsContainer.style.display = "none";
                button.setAttribute("data-comments-visible", "false");
                button.textContent = "View all 2 comments";
            } else {
                commentsContainer.style.display = "block";
                button.setAttribute("data-comments-visible", "true");
                button.textContent = "Hide comments";
            }
        });
    });
});



let debounceTimeout;

document.getElementById("searchInput").addEventListener("input", function () {
    const query = this.value.trim();

    if (debounceTimeout) clearTimeout(debounceTimeout);

    debounceTimeout = setTimeout(() => {
        if (query.length > 1) { // Отправляем запрос только если длина строки больше 2 символов
            fetch(`/search/?query=${encodeURIComponent(query)}`)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Ошибка сервера");
                    }
                    return response.json();
                })
                .then((data) => {
                    updateResults(data.users || []);
                })
                .catch((error) => {
                    console.error("Ошибка запроса:", error);
                });
        } else {
            updateResults([]); // Очистить результаты при пустом запросе
        }
    }, 300); // Задержка в 300 мс
});

// Функция для обновления результатов
function updateResults(users) {
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = ""; // Очистить старые результаты

    if (users.length === 0) {
        resultsContainer.innerHTML = "<p>No users found</p>";
        return;
    }

    users.forEach((user) => {
        const userCard = document.createElement("div");
        userCard.className = "user-card";
        userCard.innerHTML = `
            <div class="cart">
             <a href="/profile/${user.username}">
                <div>
                    <div class="img">
                        <img src="${user.avatar}" alt="${user.username}">
                    </div>
                    <div class="info">
                       <p class="name">${user.first_name}</p>
                        <p class="second_name">${user.username}</p>
                    </div>
                </div>
                </a>
            </div>
        `;
        resultsContainer.appendChild(userCard);
    });
}
