import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Slack Webhook URL (실제 webhook URL로 교체하세요)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# GitHub API 설정
GITHUB_TOKEN = os.getenv("PR_GITHUB_TOKEN")
GITHUB_API_BASE = "https://api.github.com"

def get_repositories(owner, repo_type="all"):
    """
    type에 따라 사용자나 organization의
    type에 맞는 모든 repository 목록을 가져옵니다.
    
    Args:
        owner (str): 사용자명 또는 organization 이름
        repo_type (str): repository 타입 ("all"(default), "private", "public")
    
    Returns:
        list: repository 목록
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"{GITHUB_API_BASE}/user/repos"
    params = {
        "type": repo_type,
        "per_page": 100,
        "sort": "created",
        "direction": "desc"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        repositories = response.json()
        return repositories
        
    except requests.exceptions.RequestException as e:
        print(f"Repository list fetching failed: {e}")
        return []

def get_pull_requests(owner, repo, state="open"):
    """
    GitHub repository에서 pull request 목록을 가져옵니다.
    
    Args:
        owner (str): repository 소유자 (username 또는 organization)
        repo (str): repository 이름
        state (str): PR 상태 ("open"(default), "closed", "all")
    
    Returns:
        list: pull request 목록
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls"
    params = {
        "state": state,
        "per_page": 100,  # max number of pull requests to fetch at once
        "sort": "updated",
        "direction": "desc"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        # check HTTP response status code and raise exception if there is an error
        response.raise_for_status()
        
        pull_requests = response.json()
        return pull_requests
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {e}")
        return []

def get_all_pull_requests(owner, state="open", repo_type="private"):
    """
    특정 사용자나 organization의 모든 repository에서 pull request를 가져옵니다.
    
    Args:
        owner (str): 사용자명 또는 organization 이름
        state (str): PR 상태 ("open"(default), "closed", "all")
        repo_type (str): repository 타입 ("all", "private"(default), "public")
    
    Returns:
        dict: repository별 pull request 목록
        없으면 패스 있으면 레포이름에 레포지토리로 레포정보랑 풀리퀘스트로 풀리퀘스트 정보 전달
        { 레포이름 : { "repository": 레포정보, "pull_requests": 풀리퀘스트정보 } , ...}
    """
    print(f"'{owner}'의 {repo_type} repository들을 검색 중...")
    
    # 모든 repository 가져오기
    repositories = get_repositories(owner, repo_type)
    
    if not repositories:
        print(f"'{owner}'의 repository를 찾을 수 없습니다.")
        return {}
    
    print(f"총 {len(repositories)}개의 repository를 찾았습니다.")
    
    all_pull_requests = {}
    
    for repo in repositories:
        repo_name = repo["name"]
        # repo_private = repo["private"]
        
        # # private repository만 처리 (repo_type이 "private"인 경우)
        # if repo_type == "private" and not repo_private:
        #     continue
            
        # # if repo_private ture print private, else print public
        # print(f"  - {repo_name} ({'private' if repo_private else 'public'})")
        
        # 해당 repository의 pull request 가져오기
        pull_requests = get_pull_requests(owner, repo_name, state)
        
        if pull_requests:
            all_pull_requests[repo_name] = {
                "repository": repo,
                "pull_requests": pull_requests
            }
            print(f"    → {len(pull_requests)}개의 PR 발견")
        else:
            print(f"    → PR 없음")
    return all_pull_requests

def format_pull_request(pr):
    """
    Pull request 정보를 보기 좋게 포맷팅합니다.
    """
    return {
        "number": pr["number"],
        "body": pr["body"],
        "title": pr["title"],
        "state": pr["state"],
        "author": pr["user"]["login"],
        "created_at": pr["created_at"],
        "updated_at": pr["updated_at"],
        "url": pr["html_url"],
        "draft": pr["draft"],
        "mergeable": pr.get("mergeable"),
        "labels": [label["name"] for label in pr["labels"]]
    }

def make_pull_requests_msg(all_pull_requests):
    """
    모든 repository의 pull request를 출력합니다.
    """
    if not all_pull_requests:
        print("어떤 repository에서도 pull request를 찾을 수 없습니다.")
        return

    msg = "*모든 PR 목록:*\n"
    for repo_name, data in all_pull_requests.items():
        repository = data["repository"]
        pull_requests = data["pull_requests"]

        msg += f"📁 Repository: {repo_name}\n"
        msg += f"   URL: {repository['html_url']}\n"
        msg += f"   설명: {repository.get('description', '설명 없음')}\n"
        msg += f"   PR 개수: {len(pull_requests)}\n"
        msg += f"{'='*50}\n"
        for pr in pull_requests:
            formatted_pr = format_pull_request(pr)
            msg += f"  #{formatted_pr['number']} - {formatted_pr['title']}\n"
            msg += f"    작성자: {formatted_pr['author']}\n"
            msg += f"    본문: {formatted_pr['body']}\n"
            msg += f"    생성일: {formatted_pr['created_at']}\n"
            msg += f"    URL: {formatted_pr['url']}\n"
            msg += f"{'='*50}\n"
    return msg

# def print_all_pull_requests(all_pull_requests):
    """
    모든 repository의 pull request를 출력합니다.
    """
    if not all_pull_requests:
        print("어떤 repository에서도 pull request를 찾을 수 없습니다.")
        return
    
    total_prs = sum(len(data["pull_requests"]) for data in all_pull_requests.values())
    print(f"\n{'='*60}")
    print(f"총 {len(all_pull_requests)}개 repository에서 {total_prs}개의 Pull Request를 찾았습니다!")
    print(f"{'='*60}\n")

    
    for repo_name, data in all_pull_requests.items():
        repository = data["repository"]
        pull_requests = data["pull_requests"]
        
        print(f"📁 Repository: {repo_name}")
        print(f"   URL: {repository['html_url']}")
        print(f"   설명: {repository.get('description', '설명 없음')}")
        print(f"   PR 개수: {len(pull_requests)}")
        print("-" * 50)
        
        for pr in pull_requests:
            formatted_pr = format_pull_request(pr)
            
            print(f"  #{formatted_pr['number']} - {formatted_pr['title']}")
            print(f"    작성자: {formatted_pr['author']}")
            print(f"    본문: {formatted_pr['body']}")
            print(f"    상태: {formatted_pr['state']}")
            print(f"    생성일: {formatted_pr['created_at']}")
            print(f"    업데이트: {formatted_pr['updated_at']}")
            print(f"    URL: {formatted_pr['url']}")
            
            if formatted_pr['labels']:
                print(f"    라벨: {', '.join(formatted_pr['labels'])}")
            
            if formatted_pr['draft']:
                print("    [DRAFT]")
            
            print()


def send_slack_message(message, channel="#general", username="Bot", icon_emoji=":robot_face:"):
    """
    Send message using Slack webhook.
    
    Args:
        message (str): message to send
        channel (str): channel name (e.g. "#general", "@username")
        username (str): bot name
        icon_emoji (str): bot icon emoji
    """
    payload = {
        "text": message,
        "channel": channel,
        "username": username,
        "icon_emoji": icon_emoji
    }
    if SLACK_WEBHOOK_URL is None:
        print("SLACK_WEBHOOK_URL need to be set.")
        return False
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print(f"Message sent successfully: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Message sending failed: {e}")
        return False


def main():
    """
    메인 함수
    """
    # 여기에 실제 사용자/organization 정보를 입력하세요
    owner = "samdasoo2l"  # 사용자명 또는 organization 이름
    
    print(f"GitHub Owner: {owner}")
    print("=" * 50)
    
    # 모든 private repository에서 open PR 가져오기
    print("\n[모든 Private Repository의 Open Pull Requests]")
    all_open_prs = get_all_pull_requests(owner, state="open", repo_type="private")
    msg = make_pull_requests_msg(all_open_prs)
    send_slack_message(msg, "#general")
    
    # 모든 private repository에서 closed PR 가져오기 (최근 것들)
    # print("\n[모든 Private Repository의 Recent Closed Pull Requests]")
    # all_closed_prs = get_all_pull_requests(owner, state="closed", repo_type="private")
    
    # # 각 repository에서 최근 5개씩만 표시
    # for repo_name, data in all_closed_prs.items():
    #     data["pull_requests"] = data["pull_requests"][:5]
    
    # print_all_pull_requests(all_closed_prs)

if __name__ == "__main__":
    main()