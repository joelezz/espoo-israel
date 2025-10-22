#!/usr/bin/env python3
"""
Yksityiskohtainen diagnostiikka JavaScript-toiminnallisuudelle
"""

import requests
import re
from bs4 import BeautifulSoup

class DiagnosticTester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def analyze_javascript_functions(self):
        """Analysoi JavaScript-funktioiden määrittelyt"""
        print("🔍 JAVASCRIPT FUNCTION ANALYSIS")
        print("=" * 50)
        
        response = self.session.get(self.base_url + "/static/script.js")
        js_content = response.text
        
        # Etsi funktioiden määrittelyt
        function_patterns = [
            (r'function\s+(\w+)\s*\(', 'Function declarations'),
            (r'(\w+)\s*=\s*function', 'Function expressions'),
            (r'window\.(\w+)\s*=', 'Window assignments'),
            (r'addEventListener\s*\(\s*[\'"](\w+)[\'"]', 'Event listeners')
        ]
        
        for pattern, description in function_patterns:
            matches = re.findall(pattern, js_content)
            print(f"\n📋 {description}:")
            for match in matches:
                print(f"   • {match}")
                
        # Tarkista kriittiset funktiot
        critical_functions = [
            'toggleLanguage',
            'updateLanguage', 
            'updateLanguageButton',
            'showMoviePopup',
            'closeMoviePopup',
            'initHeroVideo'
        ]
        
        print(f"\n🎯 CRITICAL FUNCTIONS CHECK:")
        for func in critical_functions:
            if f"function {func}" in js_content or f"{func} =" in js_content:
                print(f"   ✅ {func} - FOUND")
            else:
                print(f"   ❌ {func} - MISSING")
                
        # Tarkista DOMContentLoaded
        if "DOMContentLoaded" in js_content:
            print(f"   ✅ DOMContentLoaded - FOUND")
        else:
            print(f"   ❌ DOMContentLoaded - MISSING")
            
        # Tarkista console.log viestit
        console_logs = re.findall(r'console\.log\([\'"]([^\'"]+)[\'"]', js_content)
        print(f"\n📝 CONSOLE LOG MESSAGES:")
        for log in console_logs:
            print(f"   • {log}")
            
    def analyze_html_structure(self):
        """Analysoi HTML-rakenteen JavaScript-yhteensopivuus"""
        print("\n🏗️  HTML STRUCTURE ANALYSIS")
        print("=" * 50)
        
        response = self.session.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tarkista tärkeät ID:t
        important_ids = [
            'langToggle',
            'moviePopup', 
            'hero'
        ]
        
        print("🆔 IMPORTANT IDs:")
        for element_id in important_ids:
            element = soup.find(attrs={'id': element_id})
            if element:
                print(f"   ✅ #{element_id} - FOUND ({element.name})")
            else:
                print(f"   ❌ #{element_id} - MISSING")
                
        # Tarkista onclick-attribuutit
        onclick_elements = soup.find_all(attrs={'onclick': True})
        print(f"\n👆 ONCLICK HANDLERS:")
        for elem in onclick_elements:
            onclick = elem.get('onclick', '')
            tag_info = f"{elem.name}"
            if elem.get('id'):
                tag_info += f"#{elem.get('id')}"
            if elem.get('class'):
                tag_info += f".{'.'.join(elem.get('class'))}"
            print(f"   • {tag_info}: {onclick}")
            
        # Tarkista data-attribuutit kielenvaihtoa varten
        lang_elements = soup.find_all(attrs={"data-fi": True, "data-en": True})
        print(f"\n🌍 LANGUAGE DATA ATTRIBUTES:")
        print(f"   📊 Total elements: {len(lang_elements)}")
        
        # Ryhmittele elementtien mukaan
        element_types = {}
        for elem in lang_elements:
            tag = elem.name
            element_types[tag] = element_types.get(tag, 0) + 1
            
        for tag, count in element_types.items():
            print(f"   • {tag}: {count} elements")
            
    def analyze_css_javascript_integration(self):
        """Analysoi CSS:n ja JavaScriptin integraatio"""
        print("\n🎨 CSS-JAVASCRIPT INTEGRATION")
        print("=" * 50)
        
        # Hae CSS
        css_response = self.session.get(self.base_url + "/static/style.css")
        css_content = css_response.text
        
        # Hae JavaScript
        js_response = self.session.get(self.base_url + "/static/script.js")
        js_content = js_response.text
        
        # Etsi CSS-luokkia joita JavaScript käyttää
        js_classes = re.findall(r'[\'"]([a-zA-Z-]+)[\'"]', js_content)
        css_classes = re.findall(r'\.([a-zA-Z-]+)', css_content)
        
        # Tarkista että JavaScript:ssä käytetyt luokat löytyvät CSS:stä
        print("🔗 JAVASCRIPT-CSS CLASS MATCHING:")
        
        important_js_classes = [
            'show', 'animate-in', 'movie-popup-overlay', 
            'hero-video', 'flag-icon', 'lang-btn'
        ]
        
        for js_class in important_js_classes:
            if js_class in js_content:
                if js_class in css_content or f".{js_class}" in css_content:
                    print(f"   ✅ .{js_class} - Used in JS, defined in CSS")
                else:
                    print(f"   ⚠️  .{js_class} - Used in JS, NOT in CSS")
            else:
                print(f"   ℹ️  .{js_class} - Not used in JS")
                
    def analyze_video_implementation(self):
        """Analysoi videon toteutus"""
        print("\n🎬 VIDEO IMPLEMENTATION ANALYSIS")
        print("=" * 50)
        
        response = self.session.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tarkista video-elementti
        video = soup.find('video')
        if video:
            print("✅ VIDEO ELEMENT FOUND:")
            
            # Tarkista video-attribuutit
            attributes = ['autoplay', 'muted', 'loop', 'playsinline', 'preload']
            for attr in attributes:
                if video.has_attr(attr):
                    print(f"   ✅ {attr}: {video.get(attr, 'true')}")
                else:
                    print(f"   ❌ {attr}: missing")
                    
            # Tarkista source-elementit
            sources = video.find_all('source')
            print(f"\n📁 VIDEO SOURCES ({len(sources)}):")
            for source in sources:
                src = source.get('src', '')
                type_attr = source.get('type', '')
                print(f"   • {src} ({type_attr})")
                
                # Testaa videon saavutettavuus
                if src:
                    try:
                        video_response = self.session.head(self.base_url + src)
                        size = video_response.headers.get('content-length', 'Unknown')
                        print(f"     Status: {video_response.status_code}, Size: {size} bytes")
                    except Exception as e:
                        print(f"     Error: {e}")
        else:
            print("❌ VIDEO ELEMENT NOT FOUND")
            
        # Tarkista video-CSS
        css_response = self.session.get(self.base_url + "/static/style.css")
        css_content = css_response.text
        
        video_css_classes = [
            'hero-video', 'hero-video-container', 
            'hero-fallback-bg', 'hero-video-overlay'
        ]
        
        print(f"\n🎨 VIDEO CSS CLASSES:")
        for css_class in video_css_classes:
            if f".{css_class}" in css_content:
                print(f"   ✅ .{css_class} - defined")
            else:
                print(f"   ❌ .{css_class} - missing")
                
    def run_full_diagnostics(self):
        """Suorita täydellinen diagnostiikka"""
        print("🔬 COMPREHENSIVE DIAGNOSTICS")
        print("=" * 60)
        
        self.analyze_javascript_functions()
        self.analyze_html_structure()
        self.analyze_css_javascript_integration()
        self.analyze_video_implementation()
        
        print("\n" + "=" * 60)
        print("✅ DIAGNOSTICS COMPLETED")
        print("📋 Review the analysis above for any issues")

if __name__ == "__main__":
    diagnostics = DiagnosticTester()
    diagnostics.run_full_diagnostics()