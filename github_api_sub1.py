import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_BASE = "https://api.github.com"

def get_my_private_repositories():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"{GITHUB_API_BASE}/user/repos"
    params = {
        "type": "private",
        "per_page": 100,
        "sort": "updated",
        "direction": "desc"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        repositories = response.json()
        private_repos = [repo for repo in repositories if repo["private"]]
        print(f"Private repositories: {len(private_repos)}개")
        for repo in private_repos:
            print(f"- {repo['name']} | {repo['html_url']}")
        return private_repos
    except requests.exceptions.RequestException as e:
        print(f"Repository 목록 가져오기 중 오류 발생: {e}")
        return []

if __name__ == "__main__":
    get_my_private_repositories()
