document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const closeMenuBtn = document.querySelector('.close-menu-btn');
    const mobileMenuOverlay = document.querySelector('.mobile-menu-overlay');

    if(mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenuOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    }

    if(closeMenuBtn) {
        closeMenuBtn.addEventListener('click', () => {
            mobileMenuOverlay.classList.remove('active');
            document.body.style.overflow = 'auto';
        });
    }

    // Flash messages close
    const closeFlashBtns = document.querySelectorAll('.close-flash');
    closeFlashBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.target.parentElement.style.opacity = '0';
            setTimeout(() => {
                e.target.parentElement.remove();
            }, 300);
        });
    });

    // Auto-remove flash messages after 5 seconds
    setTimeout(() => {
        const flashes = document.querySelectorAll('.flash-alert');
        flashes.forEach(flash => {
            flash.style.opacity = '0';
            setTimeout(() => {
                flash.remove();
            }, 300);
        });
    }, 5000);

    // Theme toggle
    const themeToggleBtn = document.querySelector('.theme-toggle');
    if (themeToggleBtn) {
        const themeIcon = themeToggleBtn.querySelector('i');
        const currentTheme = document.documentElement.getAttribute('data-theme');
        
        if (currentTheme === 'light') {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        }
        
        themeToggleBtn.addEventListener('click', () => {
            let _currentTheme = document.documentElement.getAttribute('data-theme');
            let _newTheme = _currentTheme === 'light' ? 'dark' : 'light';
            
            document.documentElement.setAttribute('data-theme', _newTheme);
            localStorage.setItem('theme', _newTheme);
            
            if (_newTheme === 'light') {
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
            } else {
                themeIcon.classList.remove('fa-sun');
                themeIcon.classList.add('fa-moon');
            }
        });
    }
});
