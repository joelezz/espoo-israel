#!/usr/bin/env python3
"""
End-to-End testaus Espoo-Israel sivustolle
Testaa kaikki toiminnot ja raportoi tulokset
"""

import requests
import time
import json
from bs4 import BeautifulSoup
import re

class E2ETest:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        
    def log(self, test_name, status, message=""):
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.results.append(result)
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {message}")
        
    def test_server_running(self):
        """Testaa että serveri on käynnissä"""
        try:
            response = self.session.get(self.base_url, timeout=5)
            if response.status_code == 200:
                self.log("Server Running", "PASS", f"Status: {response.status_code}")
                return True
            else:
                self.log("Server Running", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log("Server Running", "FAIL", f"Error: {str(e)}")
            return False
            
    def test_html_structure(self):
        """Testaa HTML-rakenteen oikeellisuus"""
        try:
            response = self.session.get(self.base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Testaa että tärkeät elementit löytyvät
            tests = [
                ("Hero section", soup.find('section', id='hero')),
                ("Navigation", soup.find('nav', class_='navbar')),
                ("Language toggle", soup.find('button', id='langToggle')),
                ("Movie popup", soup.find('div', id='moviePopup')),
                ("Hero video", soup.find('video', class_='hero-video')),
                ("Contact form", soup.find('form')),
            ]
            
            for test_name, element in tests:
                if element:
                    self.log(f"HTML: {test_name}", "PASS", "Element found")
                else:
                    self.log(f"HTML: {test_name}", "FAIL", "Element not found")
                    
        except Exception as e:
            self.log("HTML Structure", "FAIL", f"Error: {str(e)}")
            
    def test_static_files(self):
        """Testaa että staattiset tiedostot latautuvat"""
        static_files = [
            "/static/style.css",
            "/static/script.js", 
            "/static/videos/hero-video.mp4",
            "/static/images/logo.webp",
            "/static/images/hero.jpg"
        ]
        
        for file_path in static_files:
            try:
                response = self.session.get(self.base_url + file_path, timeout=10)
                if response.status_code in [200, 206]:  # 206 for video partial content
                    self.log(f"Static File: {file_path}", "PASS", f"Status: {response.status_code}")
                else:
                    self.log(f"Static File: {file_path}", "FAIL", f"Status: {response.status_code}")
            except Exception as e:
                self.log(f"Static File: {file_path}", "FAIL", f"Error: {str(e)}")
                
    def test_language_data_attributes(self):
        """Testaa että kielenvaihtoa varten tarvittavat data-attribuutit löytyvät"""
        try:
            response = self.session.get(self.base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Etsi elementtejä joissa on data-fi ja data-en attribuutit
            lang_elements = soup.find_all(attrs={"data-fi": True, "data-en": True})
            
            if len(lang_elements) > 0:
                self.log("Language Data Attributes", "PASS", f"Found {len(lang_elements)} elements")
                
                # Testaa muutamia esimerkkejä
                examples = lang_elements[:5]
                for i, elem in enumerate(examples):
                    fi_text = elem.get('data-fi', '')
                    en_text = elem.get('data-en', '')
                    if fi_text and en_text:
                        self.log(f"Language Example {i+1}", "PASS", f"FI: '{fi_text[:30]}...' EN: '{en_text[:30]}...'")
                    else:
                        self.log(f"Language Example {i+1}", "FAIL", "Missing translation")
            else:
                self.log("Language Data Attributes", "FAIL", "No language elements found")
                
        except Exception as e:
            self.log("Language Data Attributes", "FAIL", f"Error: {str(e)}")
            
    def test_form_submission(self):
        """Testaa lomakkeen lähetys (GET csrf token ensin)"""
        try:
            # Hae lomake ja CSRF token
            response = self.session.get(self.base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            form = soup.find('form')
            if not form:
                self.log("Form Submission", "FAIL", "Form not found")
                return
                
            csrf_token = soup.find('input', {'name': 'csrf_token'})
            if csrf_token:
                csrf_value = csrf_token.get('value', '')
                self.log("CSRF Token", "PASS", f"Token found: {csrf_value[:20]}...")
            else:
                self.log("CSRF Token", "WARN", "No CSRF token found")
                csrf_value = ""
            
            # Testaa lomakkeen lähetys tyhjillä arvoilla (pitäisi epäonnistua validoinnissa)
            form_data = {
                'csrf_token': csrf_value,
                'name': '',
                'email': '',
                'phone': '',
                'address': '',
                'postal_code': '',
                'city': '',
                'join': 'kyllä',
                'message': '',
                'accept_policy': 'y'
            }
            
            response = self.session.post(self.base_url, data=form_data)
            
            if response.status_code == 200:
                # Tarkista että validointivirheet näkyvät
                if 'error' in response.text.lower() or 'required' in response.text.lower():
                    self.log("Form Validation", "PASS", "Form validation working")
                else:
                    self.log("Form Validation", "WARN", "Form validation unclear")
            else:
                self.log("Form Submission", "FAIL", f"Status: {response.status_code}")
                
        except Exception as e:
            self.log("Form Submission", "FAIL", f"Error: {str(e)}")
            
    def test_javascript_loading(self):
        """Testaa JavaScript-tiedoston sisältö"""
        try:
            response = self.session.get(self.base_url + "/static/script.js")
            if response.status_code == 200:
                js_content = response.text
                
                # Testaa että tärkeät funktiot löytyvät
                functions = [
                    "toggleLanguage",
                    "updateLanguage", 
                    "showMoviePopup",
                    "closeMoviePopup",
                    "initHeroVideo"
                ]
                
                for func in functions:
                    if func in js_content:
                        self.log(f"JS Function: {func}", "PASS", "Function found")
                    else:
                        self.log(f"JS Function: {func}", "FAIL", "Function not found")
                        
                # Testaa että ei ole syntaksivirheitä (yksinkertainen testi)
                if js_content.count('{') == js_content.count('}'):
                    self.log("JS Syntax: Braces", "PASS", "Braces balanced")
                else:
                    self.log("JS Syntax: Braces", "FAIL", "Unbalanced braces")
                    
            else:
                self.log("JavaScript Loading", "FAIL", f"Status: {response.status_code}")
                
        except Exception as e:
            self.log("JavaScript Loading", "FAIL", f"Error: {str(e)}")
            
    def test_css_loading(self):
        """Testaa CSS-tiedoston sisältö"""
        try:
            response = self.session.get(self.base_url + "/static/style.css")
            if response.status_code == 200:
                css_content = response.text
                
                # Testaa että tärkeät CSS-luokat löytyvät
                css_classes = [
                    ".movie-popup-overlay",
                    ".hero-video",
                    ".language-toggle",
                    ".lang-btn",
                    ".card-premium"
                ]
                
                for css_class in css_classes:
                    if css_class in css_content:
                        self.log(f"CSS Class: {css_class}", "PASS", "Class found")
                    else:
                        self.log(f"CSS Class: {css_class}", "FAIL", "Class not found")
                        
            else:
                self.log("CSS Loading", "FAIL", f"Status: {response.status_code}")
                
        except Exception as e:
            self.log("CSS Loading", "FAIL", f"Error: {str(e)}")
            
    def test_video_accessibility(self):
        """Testaa videon saavutettavuus"""
        try:
            # Testaa video-tiedoston lataus
            response = self.session.head(self.base_url + "/static/videos/hero-video.mp4")
            
            if response.status_code in [200, 206]:
                content_length = response.headers.get('content-length', 'Unknown')
                content_type = response.headers.get('content-type', 'Unknown')
                
                self.log("Video Accessibility", "PASS", 
                        f"Size: {content_length} bytes, Type: {content_type}")
                        
                # Testaa että video on riittävän iso (ei tyhjä tiedosto)
                if content_length != 'Unknown' and int(content_length) > 1000:
                    self.log("Video Size Check", "PASS", f"Video size OK: {content_length} bytes")
                else:
                    self.log("Video Size Check", "WARN", f"Video might be too small: {content_length}")
                    
            else:
                self.log("Video Accessibility", "FAIL", f"Status: {response.status_code}")
                
        except Exception as e:
            self.log("Video Accessibility", "FAIL", f"Error: {str(e)}")
            
    def run_all_tests(self):
        """Suorita kaikki testit"""
        print("🚀 Starting End-to-End Testing for Espoo-Israel Website")
        print("=" * 60)
        
        if not self.test_server_running():
            print("❌ Server not running, aborting tests")
            return
            
        self.test_html_structure()
        self.test_static_files()
        self.test_language_data_attributes()
        self.test_javascript_loading()
        self.test_css_loading()
        self.test_video_accessibility()
        self.test_form_submission()
        
        # Yhteenveto
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = len([r for r in self.results if r['status'] == 'PASS'])
        failed = len([r for r in self.results if r['status'] == 'FAIL'])
        warnings = len([r for r in self.results if r['status'] == 'WARN'])
        
        print(f"✅ PASSED: {passed}")
        print(f"❌ FAILED: {failed}")
        print(f"⚠️  WARNINGS: {warnings}")
        print(f"📈 TOTAL: {len(self.results)}")
        
        if failed == 0:
            print("\n🎉 ALL CRITICAL TESTS PASSED!")
        else:
            print(f"\n⚠️  {failed} TESTS FAILED - CHECK DETAILS ABOVE")
            
        return self.results

if __name__ == "__main__":
    tester = E2ETest()
    results = tester.run_all_tests()