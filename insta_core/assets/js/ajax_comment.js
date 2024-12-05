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
