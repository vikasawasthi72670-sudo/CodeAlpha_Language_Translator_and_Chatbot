#!/usr/bin/env python3
"""
Push code to GitHub - Simple & Clean
Uses GitHub API (no git CLI required)
"""
import requests
import base64
import sys
from pathlib import Path

def push_to_github(token):
    """Push all files to GitHub using API"""
    
    GITHUB_USER = "vikasawasthi72670-sudo"
    GITHUB_REPO = "CodeAlpha_Language_Translator_and_Chatbot"
    API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    def get_file_sha(path):
        try:
            resp = requests.get(f"{API_URL}/contents/{path}", headers=headers, timeout=5)
            return resp.json().get("sha") if resp.status_code == 200 else None
        except:
            return None
    
    def upload_file(local_path, github_path):
        try:
            with open(local_path, 'rb') as f:
                content = base64.b64encode(f.read()).decode()
            
            sha = get_file_sha(github_path)
            data = {
                "message": f"Update {github_path}",
                "content": content,
            }
            if sha:
                data["sha"] = sha
            
            resp = requests.put(
                f"{API_URL}/contents/{github_path}",
                headers=headers,
                json=data,
                timeout=10
            )
            return resp.status_code in [200, 201]
        except:
            return False
    
    files = [
        ("app.py", "app.py"),
        ("faqs.json", "faqs.json"),
        ("requirements.txt", "requirements.txt"),
        ("README.md", "README.md"),
        (".gitignore", ".gitignore"),
    ]
    
    print("\n" + "=" * 60)
    print("Pushing to GitHub...")
    print("=" * 60 + "\n")
    
    success = 0
    for local_path, github_path in files:
        if Path(local_path).exists():
            print(f"  {github_path}...", end=" ")
            if upload_file(local_path, github_path):
                print("✓")
                success += 1
            else:
                print("✗")
        else:
            print(f"  {local_path} not found")
    
    print("\n" + "=" * 60)
    if success == len(files):
        print(f"✓ ALL FILES PUSHED! ({success}/{len(files)})")
        print("\nView your repository:")
        print(f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}\n")
        return True
    else:
        print(f"⚠ Partial push ({success}/{len(files)})")
        print("Check your token and repository access\n")
        return False

if __name__ == "__main__":
    token = input("Paste your GitHub token and press Enter: ").strip()
    
    if not token or len(token) < 20:
        print("✗ Invalid token")
        sys.exit(1)
    
    success = push_to_github(token)
    sys.exit(0 if success else 1)
