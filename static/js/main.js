/**
 * NusantaraKos - Main Client JavaScript
 * Navbar scroll, hero slideshow, scroll animations, WhatsApp booking.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ─── NAVBAR SCROLL EFFECT ──────────────────────────────────────────────
    const navbar = document.querySelector('.navbar-custom');
    if (navbar) {
        const onScroll = () => {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    // ─── HERO SLIDESHOW ────────────────────────────────────────────────────
    const slideshow = document.getElementById('heroSlideshow');
    if (slideshow) {
        const slides = slideshow.querySelectorAll('.slide-img');
        let current = 0;
        if (slides.length > 1) {
            setInterval(() => {
                slides[current].classList.remove('active');
                current = (current + 1) % slides.length;
                slides[current].classList.add('active');
            }, 4000);
        }
    }

    // ─── SCROLL ANIMATIONS ─────────────────────────────────────────────────
    const animatedEls = document.querySelectorAll('.animate-on-scroll');
    if (animatedEls.length > 0 && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

        animatedEls.forEach((el) => observer.observe(el));
    }

    // ─── COUNTER ANIMATION ─────────────────────────────────────────────────
    const counters = document.querySelectorAll('.counter');
    if (counters.length > 0 && 'IntersectionObserver' in window) {
        const countObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.getAttribute('data-target')) || 0;
                    const duration = 1500;
                    const start = performance.now();

                    function step(now) {
                        const progress = Math.min((now - start) / duration, 1);
                        const ease = 1 - Math.pow(1 - progress, 3);
                        el.textContent = Math.floor(ease * target);
                        if (progress < 1) requestAnimationFrame(step);
                        else el.textContent = target;
                    }

                    requestAnimationFrame(step);
                    countObserver.unobserve(el);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach((c) => countObserver.observe(c));
    }

    // ─── SMOOTH SCROLL FOR ANCHOR LINKS ────────────────────────────────────
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

});
