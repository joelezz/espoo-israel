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

// Mobile-First Hero Video Management
function initHeroVideo() {
    const heroVideo = document.querySelector('.hero-video');
    const heroFallback = document.querySelector('.hero-fallback-bg');
    
    // Check if we're on mobile
    const isMobile = window.innerWidth <= 768;
    const isVerySmall = window.innerWidth <= 320;
    
    console.log(`Initializing hero video - Mobile: ${isMobile}, Very small: ${isVerySmall}`);

    if (heroVideo && !isVerySmall) {
        console.log('Hero video found, initializing...');

        // Mobile-first: different loading strategy
        if (isMobile) {
            // On mobile: be more conservative with autoplay
            heroVideo.preload = 'metadata';
            console.log('Mobile detected: using conservative video loading');
        } else {
            // On desktop: full preload
            heroVideo.preload = 'auto';
            console.log('Desktop detected: using full video preload');
        }

        heroVideo.style.display = 'block';

        // Try to play video with mobile-friendly approach
        const attemptPlay = () => {
            heroVideo.play().then(() => {
                console.log('Video started playing successfully');
                if (heroVideo) heroVideo.style.opacity = '1';
                if (heroFallback) heroFallback.style.opacity = '0';
            }).catch(error => {
                console.log('Video autoplay failed:', error.message);
                // On mobile, this is expected - show fallback
                if (heroFallback) heroFallback.style.opacity = '1';
                if (heroVideo) heroVideo.style.opacity = '0';
            });
        };

        // Different timing for mobile vs desktop
        const playDelay = isMobile ? 1000 : 500;
        setTimeout(attemptPlay, playDelay);

        heroVideo.addEventListener('loadeddata', function () {
            console.log('Video loaded successfully');
            if (!isMobile) {
                // Only auto-retry on desktop
                heroVideo.play().catch(error => {
                    console.log('Play failed on loadeddata:', error.message);
                });
            }
        });

        heroVideo.addEventListener('error', function (e) {
            console.log('Video error, showing fallback:', e.message || 'Unknown error');
            if (heroFallback) heroFallback.style.opacity = '1';
            if (heroVideo) heroVideo.style.opacity = '0';
        });

        // User interaction handler - works on both mobile and desktop
        document.addEventListener('click', function () {
            if (heroVideo.paused) {
                heroVideo.play().then(() => {
                    console.log('Video playing after user interaction');
                    if (heroVideo) heroVideo.style.opacity = '1';
                    if (heroFallback) heroFallback.style.opacity = '0';
                }).catch(e => {
                    console.log('Play failed even after interaction:', e.message);
                });
            }
        }, { once: true });

        // Load video
        heroVideo.load();
        
    } else {
        console.log(isVerySmall ? 'Very small screen: using fallback only' : 'No video element found, using fallback');
        if (heroFallback) {
            heroFallback.style.opacity = '1';
            heroFallback.style.zIndex = '2';
        }
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        const newIsMobile = window.innerWidth <= 768;
        const newIsVerySmall = window.innerWidth <= 320;
        
        if (newIsVerySmall && heroVideo) {
            // Disable video on very small screens
            heroVideo.style.display = 'none';
            if (heroFallback) heroFallback.style.opacity = '1';
        } else if (!newIsVerySmall && heroVideo) {
            heroVideo.style.display = 'block';
        }
    });
}

// Make functions globally available
window.toggleLanguage = toggleLanguage;
window.closeMoviePopup = closeMoviePopup;
window.showMoviePopupManual = showMoviePopupManual;

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
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
            langToggle.addEventListener('click', function (e) {
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
        moviePopup.addEventListener('click', function (e) {
            if (e.target === moviePopup) {
                closeMoviePopup();
            }
        });
    }

    document.addEventListener('keydown', function (e) {
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