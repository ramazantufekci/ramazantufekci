import os
import requests
from datetime import datetime
import pytz
from github import Github
import json

# GitHub token'ı al
github_token = os.getenv('GITHUB_TOKEN')
g = Github(github_token)

# Kullanıcı bilgilerini al
user = g.get_user()
username = user.login

def get_recent_activity():
    # Son aktiviteleri al
    events_url = f"https://api.github.com/users/{username}/events/public"
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(events_url, headers=headers)
    events = response.json()[:5]  # Son 5 aktivite
    
    activity_list = []
    for event in events:
        repo_name = event['repo']['name']
        event_type = event['type'].replace('Event', '')
        created_at = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        
        activity_list.append(f"- [{repo_name}](https://github.com/{repo_name}) - {event_type}")
    
    return '\n'.join(activity_list)

def get_stats():
    # GitHub istatistiklerini al
    user = g.get_user()
    public_repos = user.public_repos
    followers = user.followers
    
    return public_repos, followers

def generate_readme():
    # İstatistikleri al
    public_repos, followers = get_stats()
    
    # Son aktiviteleri al
    recent_activity = get_recent_activity()
    
    # README template
    readme_content = f'''<div align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDJ1OWMwNmR2MWh1OXFlZnUyNWxieDdzNWNxbW5uMWt0OG1jbDN3dCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qgQUggAC3Pfv687qPC/giphy.gif" width="300" alt="tech"/>
  
  # 👨‍💻 Ramazan TÜFEKÇİ
  
  <p align="center">
    <strong>System Administrator & Network Security Associate</strong>
    <br>
    <small>13 Yıllık Sistem Yönetimi | 7+ Yıl Ağ Güvenliği Deneyimi</small>
  </p>
</div>

## 🚀 Uzmanlık Alanlarım

- 🛡️ Sistem Yönetimi ve Ağ Güvenliği
- 🌐 Network Altyapı Çözümleri
- 🔒 Siber Güvenlik Danışmanlığı
- 💻 Sunucu Yönetimi ve Optimizasyonu

## 📊 GitHub İstatistiklerim

- 📚 Toplam Repository: {public_repos}
- 👥 Takipçi Sayısı: {followers}

## 🔥 Son Aktivitelerim

{recent_activity}

## 🛠️ Teknoloji Stack'im

<div align="center">
  
  ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
  ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
  ![Fortinet](https://img.shields.io/badge/Fortinet-EE3124?style=for-the-badge&logo=fortinet&logoColor=white)
  ![Networking](https://img.shields.io/badge/Networking-00979D?style=for-the-badge&logo=cisco&logoColor=white)
  
</div>

## 🤝 İletişim

<div align="center">
  
[![Website](https://img.shields.io/badge/Website-ramazantufekci.com-blue?style=for-the-badge&logo=google-chrome)](https://www.ramazantufekci.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-ramazan--tufekci-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/ramazan-tufekci)
[![YouTube](https://img.shields.io/badge/YouTube-ramazan--tufekci-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/@ramazan-tufekci)
[![Facebook](https://img.shields.io/badge/Facebook-ramazantufekciblog-blue?style=for-the-badge&logo=facebook)](https://www.facebook.com/ramazantufekciblog)

</div>

<div align="center">
  
  ![Profil Ziyaretçi Sayısı](https://profile-counter.glitch.me/ramazantufekci/count.svg)
  
</div>

---

<div align="center">
  <i>Son güncelleme: {datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC</i>
</div>
'''
    
    # README.md dosyasını güncelle
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == "__main__":
    generate_readme()
