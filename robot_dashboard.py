#!/usr/bin/env python3
"""
🤖 ROBOT APPROVAL DASHBOARD - Operation Golden Harvest
Web-baseret dashboard til at styre robot tasks og approvals
"""

import os
import json
import sqlite3
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from smart_robot_framework import SmartRobotFramework

app = Flask(__name__)
robot_framework = None

# HTML Templates
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🤖 Robot Dashboard - Operation Golden Harvest</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: 'Consolas', monospace; 
            background: #1a1a1a; 
            color: #00ff00; 
            margin: 0; 
            padding: 20px;
        }
        .header { 
            text-align: center; 
            border-bottom: 2px solid #00ff00; 
            padding-bottom: 20px; 
            margin-bottom: 30px;
        }
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }
        .stat-box { 
            background: #2a2a2a; 
            padding: 20px; 
            border: 1px solid #00ff00; 
            border-radius: 8px;
        }
        .stat-value { 
            font-size: 2em; 
            font-weight: bold; 
            color: #00ff00;
        }
        .task-card { 
            background: #2a2a2a; 
            margin: 10px 0; 
            padding: 20px; 
            border-left: 4px solid #ffaa00; 
            border-radius: 4px;
        }
        .task-card.approved { border-left-color: #00ff00; }
        .task-card.denied { border-left-color: #ff0000; }
        .btn { 
            padding: 8px 16px; 
            margin: 5px; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer; 
            font-weight: bold;
        }
        .btn-approve { background: #00aa00; color: white; }
        .btn-deny { background: #aa0000; color: white; }
        .btn-execute { background: #0066aa; color: white; }
        .section { 
            margin: 30px 0; 
            padding: 20px; 
            background: #2a2a2a; 
            border-radius: 8px;
        }
        .json-display { 
            background: #1a1a1a; 
            padding: 10px; 
            border-radius: 4px; 
            overflow-x: auto; 
            font-size: 0.9em;
        }
        .status-online { color: #00ff00; }
        .status-offline { color: #ff0000; }
        .refresh-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }
    </style>
    <script>
        function refreshPage() {
            location.reload();
        }
        
        function approveTask(taskId) {
            const notes = prompt('Approval notes (optional):');
            fetch('/approve_task', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({task_id: taskId, notes: notes || ''})
            }).then(() => refreshPage());
        }
        
        function denyTask(taskId) {
            const reason = prompt('Denial reason:');
            if (reason) {
                fetch('/deny_task', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({task_id: taskId, reason: reason})
                }).then(() => refreshPage());
            }
        }
        
        // Auto-refresh every 30 seconds
        setTimeout(refreshPage, 30000);
    </script>
</head>
<body>
    <button class="btn btn-execute refresh-btn" onclick="refreshPage()">🔄 REFRESH</button>
    
    <div class="header">
        <h1>🤖 ROBOT CONTROL DASHBOARD</h1>
        <h2>Operation Golden Harvest - AI Automation</h2>
        <p>Session: {{ status.session_id }} | 
        Status: <span class="status-{{ 'online' if status.running else 'offline' }}">
            {{ 'ONLINE' if status.running else 'OFFLINE' }}
        </span></p>
    </div>

    <div class="stats-grid">
        <div class="stat-box">
            <div>📊 Intelligence Records</div>
            <div class="stat-value">{{ status.intelligence_records }}</div>
        </div>
        <div class="stat-box">
            <div>⚡ Executed Tasks</div>
            <div class="stat-value">{{ status.executed_tasks }}</div>
        </div>
        <div class="stat-box">
            <div>🔄 Pending Approvals</div>
            <div class="stat-value">{{ pending_count }}</div>
        </div>
        <div class="stat-box">
            <div>🎯 Total Tasks</div>
            <div class="stat-value">{{ total_tasks }}</div>
        </div>
    </div>

    <div class="section">
        <h3>🚨 PENDING APPROVALS (SEMI-AUTO TASKS)</h3>
        {% if pending_approvals %}
            {% for task in pending_approvals %}
            <div class="task-card">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <div style="flex: 1;">
                        <h4>🎯 {{ task.task_id }} ({{ task.task_type }})</h4>
                        <p><strong>Created:</strong> {{ task.created_at }}</p>
                        <div class="json-display">
                            <strong>Target Info:</strong><br>
                            {{ task.target_info | tojson(indent=2) }}
                        </div>
                        <div class="json-display">
                            <strong>Payload Data:</strong><br>
                            {{ task.payload_data | tojson(indent=2) }}
                        </div>
                    </div>
                    <div style="margin-left: 20px;">
                        <button class="btn btn-approve" onclick="approveTask('{{ task.task_id }}')">
                            ✅ APPROVE
                        </button><br>
                        <button class="btn btn-deny" onclick="denyTask('{{ task.task_id }}')">
                            ❌ DENY
                        </button>
                    </div>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <p>🎉 No tasks pending approval</p>
        {% endif %}
    </div>

    <div class="section">
        <h3>📋 ALL ROBOT TASKS</h3>
        <div style="max-height: 400px; overflow-y: auto;">
            {% for task in all_tasks %}
            <div class="task-card {% if task.approved %}approved{% elif task.approved == false %}denied{% endif %}">
                <h4>{{ task.task_id }} - {{ task.task_type }} ({{ task.approval_level }})</h4>
                <p><strong>Status:</strong> 
                    {% if task.executed %}✅ EXECUTED{% elif task.approved %}✅ APPROVED{% elif task.approved == false %}❌ DENIED{% else %}⏳ PENDING{% endif %}
                </p>
                <p><strong>Created:</strong> {{ task.created_at }}</p>
                {% if task.result %}
                <div class="json-display">
                    <strong>Result:</strong><br>
                    {{ task.result | tojson(indent=2) }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="section">
        <h3>📊 SYSTEM STATUS</h3>
        <div class="json-display">
            {{ status | tojson(indent=2) }}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard page"""
    global robot_framework
    
    if not robot_framework:
        return "❌ Robot Framework not initialized", 500
    
    # Get system status
    status = robot_framework.get_system_status()
    
    # Get pending approvals
    pending_approvals = robot_framework.get_pending_approvals()
    
    # Get all tasks
    conn = sqlite3.connect(robot_framework.database_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT task_id, task_type, approval_level, target_info, payload_data, 
               created_at, approved, executed, result
        FROM robot_tasks 
        ORDER BY created_at DESC
    """)
    
    all_tasks = []
    for row in cursor.fetchall():
        all_tasks.append({
            'task_id': row[0],
            'task_type': row[1], 
            'approval_level': row[2],
            'target_info': json.loads(row[3]),
            'payload_data': json.loads(row[4]),
            'created_at': row[5],
            'approved': row[6] if row[6] is not None else None,
            'executed': bool(row[7]),
            'result': json.loads(row[8]) if row[8] else None
        })
    
    conn.close()
    
    return render_template_string(DASHBOARD_HTML, 
                                status=status,
                                pending_approvals=pending_approvals,
                                pending_count=len(pending_approvals),
                                total_tasks=len(all_tasks),
                                all_tasks=all_tasks)

@app.route('/approve_task', methods=['POST'])
def approve_task():
    """Approve a SEMI-AUTO task"""
    global robot_framework
    
    data = request.json
    task_id = data.get('task_id')
    notes = data.get('notes', '')
    
    if robot_framework:
        robot_framework.approve_task(task_id, notes)
        return jsonify({'status': 'approved'})
    
    return jsonify({'error': 'Robot framework not available'}), 500

@app.route('/deny_task', methods=['POST'])  
def deny_task():
    """Deny a SEMI-AUTO task"""
    global robot_framework
    
    data = request.json
    task_id = data.get('task_id')
    reason = data.get('reason', '')
    
    if robot_framework:
        robot_framework.deny_task(task_id, reason)
        return jsonify({'status': 'denied'})
    
    return jsonify({'error': 'Robot framework not available'}), 500

@app.route('/status')
def status():
    """Get system status as JSON"""
    global robot_framework
    
    if robot_framework:
        return jsonify(robot_framework.get_system_status())
    
    return jsonify({'error': 'Robot framework not available'}), 500

def start_dashboard(robot_instance, port=8080):
    """Start the dashboard with robot framework instance"""
    global robot_framework
    robot_framework = robot_instance
    
    print(f"🌐 Starting Robot Dashboard on http://localhost:{port}")
    print("🎯 Admin interface ready for Operation Golden Harvest")
    
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    # Test mode - start dashboard without robot framework
    print("🤖 Starting Dashboard in Test Mode")
    app.run(host='0.0.0.0', port=8080, debug=True)