// Initialize AOS (Animate On Scroll)
AOS.init({
  duration: 800, // Animation duration in ms
  easing: 'ease-in-out',
  once: true, // Only animate once per element
  mirror: false // Don’t animate when scrolling past
});

// Optional: Add smooth scroll to top button
const scrollToTopBtn = document.createElement('button');
scrollToTopBtn.textContent = '↑';
scrollToTopBtn.className = 'scroll-to-top';
document.body.appendChild(scrollToTopBtn);

scrollToTopBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

window.addEventListener('scroll', () => {
  scrollToTopBtn.style.display = window.scrollY > 300 ? 'block' : 'none';
});
