#!/usr/bin/env python3
"""
Hero-video toiminnallisuuden testaus v2 branchissa
"""

import requests
from bs4 import BeautifulSoup
import re

def test_hero_video_implementation():
    """Testaa hero-videon täydellinen toteutus"""
    print("🎬 HERO VIDEO IMPLEMENTATION TEST - V2")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    # 1. Testaa HTML-rakenne
    print("\n📄 HTML STRUCTURE TEST:")
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tarkista hero-osio
    hero_section = soup.find('section', id='hero')
    if hero_section:
        print("   ✅ Hero section found")
        
        # Tarkista video-container
        video_container = hero_section.find('div', class_='hero-video-container')
        if video_container:
            print("   ✅ Hero video container found")
            
            # Tarkista video-elementti
            video = video_container.find('video', class_='hero-video')
            if video:
                print("   ✅ Hero video element found")
                
                # Tarkista video-attribuutit
                attributes = ['autoplay', 'muted', 'loop', 'playsinline', 'preload']
                for attr in attributes:
                    if video.has_attr(attr):
                        print(f"   ✅ Video attribute: {attr}")
                    else:
                        print(f"   ❌ Missing attribute: {attr}")
                        
                # Tarkista source
                source = video.find('source')
                if source and source.get('src') == '/static/videos/hero-video.mp4':
                    print("   ✅ Video source correct: hero-video.mp4")
                else:
                    print("   ❌ Video source incorrect or missing")
            else:
                print("   ❌ Hero video element not found")
                
            # Tarkista fallback
            fallback = video_container.find('div', class_='hero-fallback-bg')
            if fallback:
                print("   ✅ Fallback background found")
            else:
                print("   ❌ Fallback background missing")
                
            # Tarkista overlay
            overlay = video_container.find('div', class_='hero-video-overlay')
            if overlay:
                print("   ✅ Video overlay found")
            else:
                print("   ❌ Video overlay missing")
        else:
            print("   ❌ Hero video container not found")
    else:
        print("   ❌ Hero section not found")
    
    # 2. Testaa CSS-tyylit
    print("\n🎨 CSS STYLES TEST:")
    css_response = requests.get(base_url + "/static/style.css")
    css_content = css_response.text
    
    css_classes = [
        '.hero-video-container',
        '.hero-video',
        '.hero-fallback-bg', 
        '.hero-video-overlay',
        '.hero-content'
    ]
    
    for css_class in css_classes:
        if css_class in css_content:
            print(f"   ✅ CSS class found: {css_class}")
        else:
            print(f"   ❌ CSS class missing: {css_class}")
    
    # Tarkista z-index arvot
    z_index_patterns = [
        (r'\.hero-video-container[^}]*z-index:\s*1', 'hero-video-container z-index: 1'),
        (r'\.hero-video[^}]*z-index:\s*2', 'hero-video z-index: 2'),
        (r'\.hero-fallback-bg[^}]*z-index:\s*1', 'hero-fallback-bg z-index: 1'),
        (r'\.hero-video-overlay[^}]*z-index:\s*3', 'hero-video-overlay z-index: 3'),
        (r'\.hero-content[^}]*z-index:\s*10', 'hero-content z-index: 10')
    ]
    
    print("\n📐 Z-INDEX LAYERING TEST:")
    for pattern, description in z_index_patterns:
        if re.search(pattern, css_content, re.DOTALL):
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - incorrect or missing")
    
    # 3. Testaa JavaScript-funktiot
    print("\n📜 JAVASCRIPT FUNCTIONS TEST:")
    js_response = requests.get(base_url + "/static/script.js")
    js_content = js_response.text
    
    js_functions = [
        'initHeroVideo',
        'querySelector(\'.hero-video\')',
        'querySelector(\'.hero-fallback-bg\')',
        'heroVideo.play()',
        'addEventListener(\'loadeddata\'',
        'addEventListener(\'error\''
    ]
    
    for func in js_functions:
        if func in js_content:
            print(f"   ✅ JS function/call found: {func}")
        else:
            print(f"   ❌ JS function/call missing: {func}")
    
    # 4. Testaa videon saavutettavuus
    print("\n🎥 VIDEO ACCESSIBILITY TEST:")
    try:
        video_response = requests.head(base_url + "/static/videos/hero-video.mp4")
        if video_response.status_code == 200:
            content_length = video_response.headers.get('content-length', 'Unknown')
            content_type = video_response.headers.get('content-type', 'Unknown')
            print(f"   ✅ Video accessible: {video_response.status_code}")
            print(f"   📊 Video size: {content_length} bytes")
            print(f"   📋 Content type: {content_type}")
            
            # Testaa partial content (video streaming)
            headers = {'Range': 'bytes=0-1023'}
            partial_response = requests.get(base_url + "/static/videos/hero-video.mp4", headers=headers)
            if partial_response.status_code == 206:
                print("   ✅ Video streaming (partial content) works")
            else:
                print(f"   ⚠️  Video streaming status: {partial_response.status_code}")
        else:
            print(f"   ❌ Video not accessible: {video_response.status_code}")
    except Exception as e:
        print(f"   ❌ Video accessibility error: {e}")
    
    # 5. Yhteenveto
    print("\n" + "=" * 50)
    print("🎯 HERO VIDEO IMPLEMENTATION SUMMARY:")
    print("   Expected behavior:")
    print("   • Video loads automatically in background")
    print("   • Autoplay starts when possible")
    print("   • Fallback image shows if video fails")
    print("   • Proper layering: video behind content")
    print("   • Responsive design for mobile")
    
    print("\n🧪 MANUAL TEST STEPS:")
    print("   1. Open http://127.0.0.1:5000")
    print("   2. Check hero section background")
    print("   3. Video should play automatically")
    print("   4. Text should be readable over video")
    print("   5. Check browser console for video logs")
    
    print("\n📱 MOBILE TEST:")
    print("   • Video should work on mobile devices")
    print("   • Fallback image on very small screens")
    print("   • Performance optimized")

if __name__ == "__main__":
    test_hero_video_implementation()