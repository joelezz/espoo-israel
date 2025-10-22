// Simple working JavaScript for Espoo-Israel website

// Language Toggle Functionality
let currentLanguage = 'fi';

function toggleLanguage() {
    console.log('Toggle language called, current:', currentLanguage);
    currentLanguage = currentLanguage === 'fi' ? 'en' : 'fi';
    console.log('New language:', currentLanguage);
    updateLanguage();
    updateLanguageButton();
    localStorage.setItem('preferredLanguage', currentLanguage);
}

function updateLanguage() {
    console.log('Updating language to:', currentLanguage);
    const elements = document.querySelectorAll('[data-fi][data-en]');
    console.log('Found elements with language data:', elements.length);
    
    elements.forEach(element => {
        if (currentLanguage === 'fi') {
            element.textContent = element.getAttribute('data-fi');
        } else {
            element.textContent = element.getAttribute('data-en');
        }
    });
    
    // Update select field options
    const joinSelect = document.querySelector('select[name="join"]');
    if (joinSelect) {
        const options = joinSelect.querySelectorAll('option');
        options.forEach(option => {
            if (option.value === 'kyllä') {
                option.textContent = currentLanguage === 'fi' ? 'Kyllä' : 'Yes';
            } else if (option.value === 'ei') {
                option.textContent = currentLanguage === 'fi' ? 'Ei' : 'No';
            }
        });
    }
}

function updateLanguageButton() {
    const langToggle = document.getElementById('langToggle');
    if (!langToggle) {
        console.error('Language toggle button not found!');
        return;
    }
    
    const flagIcon = langToggle.querySelector('.flag-icon');
    if (!flagIcon) {
        console.error('Flag icon not found!');
        return;
    }
    
    if (currentLanguage === 'fi') {
        flagIcon.textContent = '🇫🇮';
        langToggle.setAttribute('title', 'Switch to English');
    } else {
        flagIcon.textContent = '🇺🇸';
        langToggle.setAttribute('title', 'Vaihda suomeksi');
    }
    console.log('Language button updated to:', flagIcon.textContent);
}

// Movie Popup Functions
function showMoviePopup() {
    setTimeout(() => {
        const popup = document.getElementById('moviePopup');
        if (popup) {
            console.log('Showing popup automatically');
            popup.classList.add('show');
            document.body.style.overflow = 'hidden';
        } else {
            console.error('Movie popup element not found!');
        }
    }, 2000);
}

function closeMoviePopup() {
    const popup = document.getElementById('moviePopup');
    if (popup) {
        popup.classList.remove('show');
        document.body.style.overflow = 'auto';
        const today = new Date().toDateString();
        localStorage.setItem('moviePopupShown', today);
    }
}

function showMoviePopupManual() {
    const popup = document.getElementById('moviePopup');
    if (popup) {
        popup.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

// Hero Video Management
function initHeroVideo() {
    const heroVideo = document.querySelector('.hero-video');
    const heroFallback = document.querySelector('.hero-fallback-bg');
    
    if (heroVideo) {
        console.log('Hero video found, initializing...');
        
        heroVideo.style.display = 'block';
        heroVideo.style.opacity = '1';
        
        setTimeout(() => {
            heroVideo.play().then(() => {
                console.log('Video started playing');
                if (heroVideo) heroVideo.style.opacity = '1';
                if (heroFallback) heroFallback.style.opacity = '0';
            }).catch(error => {
                console.log('Video autoplay failed:', error);
                if (heroFallback) heroFallback.style.opacity = '1';
            });
        }, 500);
        
        heroVideo.addEventListener('loadeddata', function() {
            console.log('Video loaded successfully');
            heroVideo.play().catch(error => {
                console.log('Play failed on loadeddata:', error);
            });
        });
        
        heroVideo.addEventListener('error', function() {
            console.log('Video error, showing fallback');
            if (heroFallback) heroFallback.style.opacity = '1';
        });
        
        document.addEventListener('click', function() {
            if (heroVideo.paused) {
                heroVideo.play().then(() => {
                    console.log('Video playing after user interaction');
                }).catch(e => {
                    console.log('Play failed even after interaction');
                });
            }
        }, { once: true });
        
        heroVideo.load();
    } else {
        console.log('No video element found, using fallback');
        if (heroFallback) heroFallback.style.opacity = '1';
    }
}

// Make functions globally available
window.toggleLanguage = toggleLanguage;
window.closeMoviePopup = closeMoviePopup;
window.showMoviePopupManual = showMoviePopupManual;

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing...');
    
    // Initialize language
    const savedLanguage = localStorage.getItem('preferredLanguage');
    if (savedLanguage) {
        currentLanguage = savedLanguage;
    }
    
    setTimeout(() => {
        updateLanguage();
        updateLanguageButton();
        
        // Add language toggle event listener
        const langToggle = document.getElementById('langToggle');
        if (langToggle) {
            langToggle.addEventListener('click', function(e) {
                e.preventDefault();
                toggleLanguage();
            });
            console.log('Language toggle event listener added');
        }
    }, 100);
    
    // Initialize hero video
    initHeroVideo();
    
    // Initialize popup
    showMoviePopup();
    
    // Popup event listeners
    const moviePopup = document.getElementById('moviePopup');
    if (moviePopup) {
        moviePopup.addEventListener('click', function(e) {
            if (e.target === moviePopup) {
                closeMoviePopup();
            }
        });
    }
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const popup = document.getElementById('moviePopup');
            if (popup && popup.classList.contains('show')) {
                closeMoviePopup();
            }
        }
    });
    
    console.log('All initialization complete');
});

console.log('Script loaded successfully');