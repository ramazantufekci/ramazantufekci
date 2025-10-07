from github import Github
import os
from datetime import datetime
import pytz

def get_latest_projects(gh):
    user = gh.get_user()
    repos = user.get_repos(sort='updated', direction='desc')
    projects = []
    for repo in list(repos)[:5]:  # Son 5 repo
        if not repo.fork:  # Fork olmayan repolar
            projects.append(f"- [{repo.name}]({repo.html_url}) - {repo.description or ''} (Son güncelleme: {repo.updated_at.strftime('%Y-%m-%d')})")
    return "\n".join(projects)

def get_latest_contributions(gh):
    user = gh.get_user()
    events = user.get_events()
    contributions = []
    seen = set()
    
    for event in events:
        if len(contributions) >= 5:  # Son 5 katkı
            break
            
        if event.type in ['PushEvent', 'PullRequestEvent', 'IssuesEvent']:
            repo_name = event.repo.name
            if repo_name not in seen:
                seen.add(repo_name)
                repo = gh.get_repo(repo_name)
                contributions.append(f"- [{repo.name}]({repo.html_url}) - {repo.description or ''}")
    
    return "\n".join(contributions)

def main():
    github_token = os.getenv('GITHUB_TOKEN')
    gh = Github(github_token)
    
    # README template'ini oku
    with open('README.template.md', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Projeleri güncelle
    latest_projects = get_latest_projects(gh)
    template = template.replace(
        "<!-- LATEST_PROJECTS:START -->\n<!-- LATEST_PROJECTS:END -->",
        f"<!-- LATEST_PROJECTS:START -->\n{latest_projects}\n<!-- LATEST_PROJECTS:END -->"
    )
    
    # Katkıları güncelle
    latest_contributions = get_latest_contributions(gh)
    template = template.replace(
        "<!-- LATEST_CONTRIBUTIONS:START -->\n<!-- LATEST_CONTRIBUTIONS:END -->",
        f"<!-- LATEST_CONTRIBUTIONS:START -->\n{latest_contributions}\n<!-- LATEST_CONTRIBUTIONS:END -->"
    )
    
    # Tarihi güncelle
    now = datetime.now(pytz.UTC)
    template = template.replace(
        "{{ date \"2006-01-02 15:04:05\" }}",
        now.strftime("%Y-%m-%d %H:%M:%S UTC")
    )
    
    # Yeni README'yi kaydet
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(template)

if __name__ == "__main__":
    main()
