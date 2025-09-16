#!/usr/bin/env python3
"""
Update All Webhook URLs - Operation Golden Harvest
Replace old Discord webhook with new Spidey Bot webhook
"""

import os
import glob

class WebhookUpdater:
    def __init__(self):
        self.old_webhook = "https://discord.com/api/webhooks/1417442947686731856/1UGJsXCLBqIZmb2shm4CjxJhAzZtObsbKtbStAmPg5jKtvbVt9WqRfRkNZ6ymjuiDS95"
        self.new_webhook = "https://discord.com/api/webhooks/1417442947686731856/1UGJsXCLBqIZmb2shm4CjxJhAzZtObsbKtbStAmPg5jKtvbVt9WqRfRkNZ6ymjuiDS95"
        
    def update_file(self, filepath):
        """Update webhook URL in a single file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if self.old_webhook in content:
                updated_content = content.replace(self.old_webhook, self.new_webhook)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                    
                print(f"✅ Updated: {filepath}")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Error updating {filepath}: {e}")
            return False
    
    def update_all_files(self):
        """Update webhook URLs in all project files"""
        print("🔄 UPDATING WEBHOOK URLs - Operation Golden Harvest")
        print("=" * 60)
        
        # File patterns to check
        patterns = [
            "*.py",
            "*.html",
            "*.js", 
            "*.ps1",
            "*.bat",
            "obfuscated/*.py"
        ]
        
        updated_files = []
        
        for pattern in patterns:
            files = glob.glob(pattern, recursive=True)
            for filepath in files:
                if self.update_file(filepath):
                    updated_files.append(filepath)
        
        print(f"\n🎯 WEBHOOK UPDATE COMPLETE!")
        print(f"Updated {len(updated_files)} files:")
        for file in updated_files:
            print(f"  • {file}")
            
        return updated_files

if __name__ == "__main__":
    updater = WebhookUpdater()
    updated_files = updater.update_all_files()
    
    print(f"\n🕷️ NEW WEBHOOK ACTIVE:")
    print(f"Spidey Bot: ...1417442947686731856/...")
    print(f"\n🚀 Ready for live beacon tracking!")