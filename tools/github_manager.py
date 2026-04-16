#!/usr/bin/env python3
"""
GitHub Repository Manager
Nutzt PyGithub für API-Zugriff
Erstellt von: Truthseeker v6.4
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from github import Github, GithubException

def load_github_token():
    """Lädt GitHub Token aus Config"""
    env_path = Path(__file__).parent.parent / "config" / "github.env"
    if env_path.exists():
        load_dotenv(env_path)
    
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Fehler: GITHUB_TOKEN nicht gefunden!")
        sys.exit(1)
    return token

def connect_github():
    """Stellt Verbindung zu GitHub her"""
    token = load_github_token()
    g = Github(token)
    
    try:
        user = g.get_user()
        print(f"✅ Verbunden als: {user.login}")
        print(f"   Name: {user.name or 'N/A'}")
        print(f"   Public Repos: {user.public_repos}")
        return g, user
    except GithubException as e:
        print(f"❌ Verbindungsfehler: {e}")
        sys.exit(1)

def list_repositories(user, limit=20):
    """Listet Repositories des Users"""
    print(f"\n📁 Repositories (max {limit}):")
    print("-" * 60)
    
    repos = user.get_repos(sort="updated", direction="desc")
    count = 0
    
    for repo in repos:
        if count >= limit:
            break
        
        visibility = "🔒" if repo.private else "🌐"
        lang = repo.language or "N/A"
        updated = repo.updated_at.strftime("%Y-%m-%d") if repo.updated_at else "N/A"
        
        print(f"{visibility} {repo.full_name}")
        print(f"   Lang: {lang} | Updated: {updated}")
        print(f"   {repo.description or 'Keine Beschreibung'}")
        print()
        count += 1
    
    return repos

def get_repo_details(g, repo_name):
    """Holt Details zu einem spezifischen Repo"""
    try:
        repo = g.get_repo(repo_name)
        print(f"\n📊 {repo.full_name}")
        print("=" * 60)
        print(f"Beschreibung: {repo.description or 'N/A'}")
        print(f"Sprache: {repo.language or 'N/A'}")
        print(f"Stars: {repo.stargazers_count} | Forks: {repo.forks_count}")
        print(f"Issues: {repo.open_issues_count} | Watchers: {repo.watchers_count}")
        print(f"Default Branch: {repo.default_branch}")
        print(f"Letzter Push: {repo.pushed_at}")
        print(f"Erstellt: {repo.created_at}")
        
        # Get topics
        topics = repo.get_topics()
        if topics:
            print(f"Topics: {', '.join(topics)}")
        
        return repo
        
    except GithubException as e:
        print(f"❌ Fehler beim Laden von {repo_name}: {e}")
        return None

def main():
    """CLI Interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GitHub Repository Manager")
    parser.add_argument("--list", "-l", action="store_true", help="Liste alle Repos")
    parser.add_argument("--repo", "-r", help="Zeige Details zu einem Repo (owner/name)")
    parser.add_argument("--limit", "-n", type=int, default=20, help="Limit für Liste")
    
    args = parser.parse_args()
    
    g, user = connect_github()
    
    if args.repo:
        get_repo_details(g, args.repo)
    else:
        list_repositories(user, args.limit)

if __name__ == "__main__":
    main()
