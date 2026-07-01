#!/usr/bin/env python3
"""
Detection modules for FuzzForge.
"""

import re

class Detector:
    def __init__(self, baseline_response=None):
        self.baseline = baseline_response

    def detect_anomalies(self, results):
        anomalies = []
        if not self.baseline:
            lengths = [r['length'] for r in results if isinstance(r.get('length'), int)]
            if lengths:
                avg_length = sum(lengths) / len(lengths)
                baseline_length = avg_length * 1.5
            else:
                baseline_length = 0
        else:
            baseline_length = self.baseline.get('length', 0)

        for r in results:
            if r['status'] == 'TIMEOUT' or r['status'] == 'ERROR':
                continue
            if r.get('status') in [200, 301, 302, 303, 307, 308, 401, 403, 500, 502, 503]:
                if r['length'] > baseline_length * 2 or r['length'] < baseline_length * 0.5:
                    r['anomaly'] = 'unusual_length'
                    anomalies.append(r)
        return anomalies

    def check_sqli(self, response_text):
        sql_patterns = [
            r'SQL syntax.*MySQL', r'Warning.*mysql_', r'MySQLSyntaxErrorException',
            r'valid MySQL result', r'PostgreSQL.*ERROR', r'Warning.*\Wpg_.*',
            r'valid PostgreSQL result', r'ORA-[0-9]{5}', r'Oracle error',
            r'SQLite/JDBCDriver', r'SQLite.Exception', r'System.Data.SQLite.SQLiteException',
            r'Warning.*sqlite_.*', r'valid SQLite result', r'.*SQL Server.*Driver.*',
            r'Driver.*SQL Server.*', r'SQLServer JDBC Driver', r'com.microsoft.sqlserver',
            r'Unclosed quotation mark', r'Microsoft OLE DB Provider for ODBC Drivers'
        ]
        for pattern in sql_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                return True
        return False

    def check_xss(self, response_text, payload):
        if payload in response_text and payload not in f'&lt;{payload[1:]}&gt;':
            return True
        return False