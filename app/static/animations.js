document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.post-card');
    
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Add a subtle floating animation to all buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.classList.add('float');
    });

    // Add a pulsing animation to the logo
    const logo = document.querySelector('h1');
    if (logo) {
        logo.classList.add('pulse');
    }
});