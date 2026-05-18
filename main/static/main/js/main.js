// Плавная прокрутка к якорям
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
                const offset = -50;
                
                window.scrollTo({
                    top: elementPosition - offset,
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Валидация формы (без fetch!)
$(document).ready(function() {
    $('#form').validate({
        rules: {
            name: { required: true, minlength: 2 },
            surname: { required: true, minlength: 2 },
            email: { required: true, email: true },
            number: { required: true, minlength: 10 },
            ticket_type: { required: true }
        },
        messages: {
            name: { required: "Введите имя", minlength: "Минимум 2 символа" },
            surname: { required: "Введите фамилию", minlength: "Минимум 2 символа" },
            email: { required: "Введите email", email: "Неверный формат" },
            number: { required: "Введите телефон", minlength: "Минимум 10 цифр" },
            ticket_type: { required: "Выберите тип билета" }
        },
        submitHandler: function(form) {
            $('#submit').prop('disabled', true).text('Отправка...');
            form.submit();
            return true;
        }
    });
});