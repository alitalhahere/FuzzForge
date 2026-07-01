#!/usr/bin/env python3
"""
Report generation for FuzzForge.
"""

import json
import os
from datetime import datetime

def generate_json_report(results, filename='reports/fuzz_report.json'):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"[+] JSON report saved to {filename}")

def generate_html_report(results, filename='reports/fuzz_report.html'):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>FuzzForge Report</title>
    <style>
        body {{ font-family: monospace; background: #0a0e1a; color: #00ffcc; padding: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #00ffcc; padding: 8px; text-align: left; }}
        th {{ background: #1a2a3a; color: #fff; }}
        .status-200 {{ color: #00ff00; }}
        .status-301 {{ color: #ffaa00; }}
        .status-403 {{ color: #ff6600; }}
        .status-500 {{ color: #ff0000; }}
    </style>
</head>
<body>
    <h1>🔨 FuzzForge Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Total interesting findings: {len(results)}</p>
    <table>
        <tr><th>#</th><th>URL</th><th>Status</th><th>Length</th></tr>
"""
    for i, r in enumerate(results, 1):
        status = str(r.get('status', 'N/A'))
        status_class = ''
        if status == '200':
            status_class = 'status-200'
        elif status in ['301', '302', '307']:
            status_class = 'status-301'
        elif status == '403':
            status_class = 'status-403'
        elif status.startswith('5'):
            status_class = 'status-500'

        html += f"""        <tr>
            <td>{i}</td>
            <td>{r.get('url', 'N/A')}</td>
            <td class="{status_class}">{status}</td>
            <td>{r.get('length', 'N/A')}</td>
        </tr>
"""
    html += """    </table>
</body>
</html>"""
    with open(filename, 'w') as f:
        f.write(html)
    print(f"[+] HTML report saved to {filename}")