#!/usr/bin/env python3
"""
Testaa kielenvaihtotoiminnon korjaus
"""

import requests
from bs4 import BeautifulSoup

def test_language_button_fix():
    """Testaa että kielenvaihtopainike on korjattu"""
    print("🔧 Testing Language Button Fix")
    print("=" * 40)
    
    response = requests.get("http://127.0.0.1:5000")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tarkista kielenvaihtopainike
    lang_button = soup.find('button', id='langToggle')
    
    if lang_button:
        print("✅ Language button found")
        
        # Tarkista että onclick-attribuutti on poistettu
        onclick = lang_button.get('onclick')
        if onclick:
            print(f"❌ onclick attribute still present: {onclick}")
            print("   This will cause double event firing!")
        else:
            print("✅ onclick attribute removed - good!")
            
        # Tarkista että ID on oikein
        button_id = lang_button.get('id')
        if button_id == 'langToggle':
            print("✅ Button ID correct: langToggle")
        else:
            print(f"❌ Button ID wrong: {button_id}")
            
        # Tarkista flag icon
        flag_icon = lang_button.find(class_='flag-icon')
        if flag_icon:
            flag_text = flag_icon.get_text()
            print(f"✅ Flag icon found: {flag_text}")
        else:
            print("❌ Flag icon not found")
            
    else:
        print("❌ Language button not found!")
        
    print("\n📋 Expected behavior:")
    print("   • One click should trigger toggleLanguage() only once")
    print("   • Console should show single set of messages per click")
    print("   • Language should change: fi ↔ en")
    
    print("\n🧪 Test in browser:")
    print("   1. Open http://127.0.0.1:5000")
    print("   2. Open DevTools Console (F12)")
    print("   3. Click the flag button once")
    print("   4. Should see only ONE set of toggle messages")

if __name__ == "__main__":
    test_language_button_fix()