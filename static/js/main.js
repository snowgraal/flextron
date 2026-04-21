// Удаление прелоадера
window.addEventListener('load', function() {
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        setTimeout(() => {
            preloader.style.opacity = '0';
            setTimeout(() => preloader.remove(), 500);
        }, 1000);
    }
});

// Плавный скролл
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const headerOffset = 80;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
            window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
        }
    });
});

// Кнопки "Запросить цену"
document.querySelectorAll('.btn-order').forEach(btn => {
    btn.addEventListener('click', function() {
        const product = this.getAttribute('data-product');
        const productInput = document.getElementById('productInput');
        if (productInput && product) {
            productInput.value = product;
        }
        const orderSection = document.getElementById('order');
        if (orderSection) {
            const headerOffset = 80;
            const elementPosition = orderSection.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
            window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
        }
    });
});

// Отправка формы
document.getElementById('orderForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const submitBtn = document.getElementById('submitBtn');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Отправляем...';
    submitBtn.disabled = true;

    const formData = {
        name: this.querySelector('[name="full_name"]').value,
        phone: this.querySelector('[name="phone"]').value,
        product: this.querySelector('[name="product"]').value || 'Не указано',
        quantity: this.querySelector('[name="quantity"]').value,
        email: this.querySelector('[name="email"]').value || 'Не указан',
        comment: this.querySelector('[name="comment"]').value || 'Не указан'
    };

    try {
        const response = await fetch('/submit_lead', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (result.success) {
            const successModal = new bootstrap.Modal(document.getElementById('successModal'));
            successModal.show();
            this.reset();
        } else {
            alert(result.message);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка отправки. Пожалуйста, позвоните нам: 8 (958) 571-84-63');
    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
});

// Кнопка "Наверх"
window.addEventListener('scroll', () => {
    const scrollBtn = document.querySelector('.scroll-top');
    if (scrollBtn) {
        if (window.scrollY > 500) {
            scrollBtn.classList.add('show');
        } else {
            scrollBtn.classList.remove('show');
        }
    }
});

// Подсветка активного пункта меню
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    let current = '';
    const scrollPosition = window.scrollY + 100;

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});