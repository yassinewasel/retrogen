function filterProducts(category) {
    const products = document.querySelectorAll('.product-card');
    products.forEach(product => {
        if (category === 'all' || product.dataset.category === category) {
            product.style.display = 'block';
        } else {
            product.style.display = 'none';
        }
    });

    const buttons = document.querySelectorAll('.category-btn');
    buttons.forEach(button => {
        if (button.innerText.toLowerCase().includes(category) || (category === 'all' && button.innerText.toLowerCase().includes('tous nos produits'))) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });
}

function searchProducts() {
    const input = document.getElementById('search-input').value.trim().toLowerCase();
    const productCards = document.querySelectorAll('.product-card');

    productCards.forEach(card => {
        const productName = card.querySelector('h3').textContent.trim().toLowerCase();
        card.style.display = productName.includes(input) ? 'block' : 'none';
    });
}

const scrollToTopBtn = document.getElementById('scrollToTopBtn');

window.onscroll = function() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        scrollToTopBtn.classList.add('show');
    } else {
        scrollToTopBtn.classList.remove('show');
    }
};

scrollToTopBtn.addEventListener('click', function() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});