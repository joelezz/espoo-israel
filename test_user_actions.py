#!/usr/bin/env python3
"""
Simuloi käyttäjän toimintoja sivustolla ja seuraa server-lokeja
"""

import requests
import time
import json
from bs4 import BeautifulSoup

class UserActionSimulator:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        # Simuloi oikea selain
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def simulate_page_load(self):
        """Simuloi sivun lataus kuten oikea selain"""
        print("🌐 Simulating page load...")
        
        # 1. Lataa HTML
        response = self.session.get(self.base_url)
        print(f"   📄 HTML loaded: {response.status_code}")
        
        # 2. Parsee HTML ja etsi staattiset resurssit
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. Lataa CSS
        css_links = soup.find_all('link', rel='stylesheet')
        for link in css_links:
            href = link.get('href')
            if href and href.startswith('/static/'):
                css_response = self.session.get(self.base_url + href)
                print(f"   🎨 CSS loaded: {href} ({css_response.status_code})")
        
        # 4. Lataa JavaScript
        js_scripts = soup.find_all('script', src=True)
        for script in js_scripts:
            src = script.get('src')
            if src and src.startswith('/static/'):
                js_response = self.session.get(self.base_url + src)
                print(f"   📜 JS loaded: {src} ({js_response.status_code})")
        
        # 5. Lataa kuvat
        images = soup.find_all('img', src=True)
        for img in images[:3]:  # Vain muutama ensimmäinen
            src = img.get('src')
            if src and src.startswith('/static/'):
                img_response = self.session.get(self.base_url + src)
                print(f"   🖼️  Image loaded: {src} ({img_response.status_code})")
        
        # 6. Lataa video (simuloi autoplay)
        video = soup.find('video')
        if video:
            sources = video.find_all('source')
            for source in sources:
                src = source.get('src')
                if src:
                    # Simuloi video lataus (HEAD request ensin, sitten partial content)
                    video_head = self.session.head(self.base_url + src)
                    print(f"   🎬 Video HEAD: {src} ({video_head.status_code})")
                    
                    # Simuloi partial content request (kuten video player tekisi)
                    headers = {'Range': 'bytes=0-1023'}
                    video_partial = self.session.get(self.base_url + src, headers=headers)
                    print(f"   🎬 Video partial: {src} ({video_partial.status_code})")
                    break
        
        print("   ✅ Page load simulation complete")
        return response
        
    def simulate_language_toggle(self):
        """Simuloi kielenvaihtoa (ei voi testata JavaScriptiä, mutta testaa että elementit ovat paikallaan)"""
        print("\n🌍 Simulating language toggle...")
        
        response = self.session.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tarkista että kielenvaihtopainike löytyy
        lang_toggle = soup.find('button', id='langToggle')
        if lang_toggle:
            print("   ✅ Language toggle button found")
            flag_icon = lang_toggle.find(class_='flag-icon')
            if flag_icon:
                print(f"   🏴 Flag icon: {flag_icon.get_text()}")
        
        # Tarkista kielenvaihtoa varten tarvittavat data-attribuutit
        lang_elements = soup.find_all(attrs={"data-fi": True, "data-en": True})
        print(f"   📝 Found {len(lang_elements)} elements with language data")
        
        # Näytä muutama esimerkki
        for i, elem in enumerate(lang_elements[:3]):
            fi_text = elem.get('data-fi', '')[:30]
            en_text = elem.get('data-en', '')[:30]
            print(f"   🔄 Element {i+1}: FI='{fi_text}...' EN='{en_text}...'")
            
    def simulate_popup_interaction(self):
        """Simuloi popup-vuorovaikutusta"""
        print("\n🎬 Simulating popup interaction...")
        
        response = self.session.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tarkista popup-elementti
        popup = soup.find('div', id='moviePopup')
        if popup:
            print("   ✅ Movie popup element found")
            
            # Tarkista popup-sisältö
            popup_header = popup.find(class_='popup-header')
            if popup_header:
                title = popup_header.find('h2')
                if title:
                    print(f"   🎭 Popup title: {title.get_text()}")
            
            # Tarkista Stripe-painike
            stripe_button = popup.find('stripe-buy-button')
            if stripe_button:
                print("   💳 Stripe buy button found")
                
            # Tarkista sulkemispainike
            close_button = popup.find(class_='popup-close')
            if close_button:
                print("   ❌ Close button found")
        else:
            print("   ❌ Movie popup not found")
            
    def simulate_form_interaction(self):
        """Simuloi lomakkeen täyttöä"""
        print("\n📝 Simulating form interaction...")
        
        response = self.session.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        form = soup.find('form')
        if form:
            print("   ✅ Contact form found")
            
            # Tarkista lomakkeen kentät
            fields = [
                ('name', 'Nimi'),
                ('email', 'Sähköposti'),
                ('phone', 'Puhelin'),
                ('address', 'Osoite'),
                ('message', 'Viesti')
            ]
            
            for field_name, field_label in fields:
                field = form.find(attrs={'name': field_name})
                if field:
                    print(f"   📋 Field found: {field_label} ({field_name})")
                else:
                    print(f"   ❌ Field missing: {field_label} ({field_name})")
            
            # Testaa lomakkeen lähetys tyhjillä arvoilla
            print("   🧪 Testing form submission with empty values...")
            
            form_data = {
                'name': '',
                'email': 'test@example.com',  # Vähintään email että nähdään validointi
                'phone': '',
                'address': '',
                'postal_code': '',
                'city': '',
                'join': 'kyllä',
                'message': '',
                'accept_policy': 'y'
            }
            
            try:
                form_response = self.session.post(self.base_url, data=form_data)
                print(f"   📤 Form submission: {form_response.status_code}")
                
                # Tarkista että palataan lomakkeeseen (validointivirheet)
                if 'form' in form_response.text.lower():
                    print("   ✅ Form validation working (returned to form)")
                else:
                    print("   ⚠️  Form validation unclear")
                    
            except Exception as e:
                print(f"   ❌ Form submission error: {e}")
        else:
            print("   ❌ Contact form not found")
            
    def simulate_navigation_clicks(self):
        """Simuloi navigoinnin klikkauksia"""
        print("\n🧭 Simulating navigation clicks...")
        
        response = self.session.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tarkista navigointi
        nav = soup.find('nav')
        if nav:
            nav_links = nav.find_all('a', class_='nav-link')
            print(f"   ✅ Found {len(nav_links)} navigation links")
            
            for link in nav_links:
                href = link.get('href', '')
                text = link.get_text().strip()
                if href.startswith('#'):
                    print(f"   🔗 Internal link: '{text}' -> {href}")
                elif href.startswith('javascript:'):
                    print(f"   📜 JavaScript link: '{text}'")
                else:
                    print(f"   🌐 External link: '{text}' -> {href}")
        
    def run_full_simulation(self):
        """Suorita täydellinen käyttäjäsimulaatio"""
        print("🤖 Starting Full User Action Simulation")
        print("=" * 60)
        
        try:
            # Simuloi sivun lataus
            self.simulate_page_load()
            
            # Odota hetki (simuloi käyttäjän lukemista)
            time.sleep(1)
            
            # Simuloi eri toimintoja
            self.simulate_language_toggle()
            self.simulate_popup_interaction()
            self.simulate_form_interaction()
            self.simulate_navigation_clicks()
            
            print("\n" + "=" * 60)
            print("✅ User simulation completed successfully!")
            print("📊 Check server logs for detailed request information")
            
        except Exception as e:
            print(f"\n❌ Simulation failed: {e}")

if __name__ == "__main__":
    simulator = UserActionSimulator()
    simulator.run_full_simulation()