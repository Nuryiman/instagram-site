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

document.querySelector('.comment-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Предотвращаем обычную отправку формы

    const form = event.target;
    const itemId = form.getAttribute('data-item-id');  // Получаем ID публикации
    const commentText = form.querySelector('.comment-input').value;  // Получаем текст комментария

    // Делаем POST-запрос
    fetch(`/add-comment/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Указываем тип данных
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ comment: commentText })  // Передаем комментарий в теле запроса
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Создаем новый элемент для комментария
            const newComment = document.createElement('p');
            newComment.innerHTML = `<a class="bold" href="#">${data.comment.user}</a> ${data.comment.text}`;

            // Добавляем новый комментарий в начало списка
            const commentsContainer = document.querySelector(`#comments-container-${itemId}`);
            commentsContainer.insertBefore(newComment, commentsContainer.firstChild); // Добавляем в начало

            // Очистить поле ввода
            form.querySelector('.comment-input').value = '';
        } else {
            console.error('Ошибка:', data.error);
        }
    })
    .catch(error => console.error('Ошибка запроса:', error));
});
