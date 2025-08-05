# Log Collector

## Overview  
Log Collector is a Python-based tool designed to connect to multiple remote servers via SSH, run diagnostic commands, gather system logs and data, generate human-readable reports in text and HTML format, and package the results into a ZIP archive for easy storage and review.

It supports Linux and Windows servers (with modular diagnostics), and can operate either on a single server or multiple servers defined in a JSON list.

---

## Features

- SSH connection to remote servers  
- Runs OS-specific diagnostics
- Saves individual diagnostic logs as text files  
- Generates combined text and HTML reports  
- Packages results into ZIP archives  
- Can detect virtualization status (Linux)  
- Runs on Python 3.8+  

---

## Requirements

Install dependencies with:

```bash
python -m pip install paramiko reportlab  

## How to run
- Download the repo and create your own json server list
```bash
python main.py --server-list server_list.json
