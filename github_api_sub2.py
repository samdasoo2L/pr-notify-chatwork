import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# GitHub API 설정
GITHUB_TOKEN = os.getenv("PR_GITHUB_TOKEN")
GITHUB_API_BASE = "https://api.github.com"

def get_user_repositories(username, repo_type="all"):
    """
    사용자의 repository 목록을 가져옵니다 (private repository 포함).
    
    Args:
        username (str): GitHub 사용자명
        repo_type (str): repository 타입
            - "all": 모든 repository (public + private) ✅
            - "owner": 소유한 repository만 (public + private) ✅
            - "member": 멤버인 repository만 (public + private) ✅
            - "public": public repository만 ❌
    
    Returns:
        list: repository 목록
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    url = f"{GITHUB_API_BASE}/users/{username}/repos"
    params = {
        "type": "all",
        "per_page": 100,
        "sort": "updated",
        "direction": "desc"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        repositories = response.json()
        print(f"repositories: {len(repositories)}!!!!")
        return repositories
        
    except requests.exceptions.RequestException as e:
        print(f"Repository 목록 가져오기 중 오류 발생: {e}")
        return []

def get_private_repositories_only(username):
    """
    사용자의 private repository만 가져옵니다.
    
    Args:
        username (str): GitHub 사용자명
    
    Returns:
        list: private repository 목록만
    """
    # 모든 repository를 가져옴 (private 포함)
    all_repos = get_user_repositories(username, "all")
    
    # private repository만 필터링
    private_repos = [repo for repo in all_repos if repo["private"]]
    
    return private_repos

def print_repository_list(repositories, title="Repository 목록"):
    """
    Repository 목록을 보기 좋게 출력합니다.
    """
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    
    if not repositories:
        print("Repository가 없습니다.")
        return
    
    print(f"총 {len(repositories)}개의 repository를 찾았습니다:\n")
    
    for i, repo in enumerate(repositories, 1):
        repo_name = repo['name']
        repo_private = repo['private']
        repo_visibility = '🔒 Private' if repo_private else '🌐 Public'
        repo_description = repo.get('description', '설명 없음')
        repo_url = repo['html_url']
        repo_created = repo['created_at'][:10]  # YYYY-MM-DD 형식
        repo_updated = repo['updated_at'][:10]
        
        print(f"{i:2d}. {repo_name}")
        print(f"    {repo_visibility}")
        print(f"    설명: {repo_description}")
        print(f"    URL: {repo_url}")
        print(f"    생성일: {repo_created}")
        print(f"    업데이트: {repo_updated}")
        print()

def print_repository_summary(repositories):
    """
    Repository 통계를 출력합니다.
    """
    if not repositories:
        return
    
    total_count = len(repositories)
    private_count = len([repo for repo in repositories if repo["private"]])
    public_count = total_count - private_count
    
    print(f"\n📊 Repository 통계:")
    print(f"   총 개수: {total_count}개")
    print(f"   Private: {private_count}개")
    print(f"   Public: {public_count}개")

def main():
    """
    메인 함수
    """
    username = "samdasoo2l"  # 여기에 실제 사용자명을 입력하세요
    
    print(f"GitHub 사용자: {username}")
    print("=" * 50)
    
    # 1. 모든 repository 가져오기 (public + private)
    print("\n🔍 모든 repository 검색 중...")
    all_repos = get_user_repositories(username, "all")
    print_repository_list(all_repos, "모든 Repository (Public + Private)")
    print_repository_summary(all_repos)
    
    # 2. Private repository만 가져오기
    print("\n🔍 Private repository만 검색 중...")
    private_repos = get_private_repositories_only(username)
    print_repository_list(private_repos, "Private Repository만")
    
    # 3. Repository 타입별 테스트
    print("\n🔍 Repository 타입별 테스트...")
    
    # "owner" 타입 (소유한 repository만)
    owner_repos = get_user_repositories(username, "owner")
    print(f"Owner repositories: {len(owner_repos)}개")
    
    # "member" 타입 (멤버인 repository만)
    member_repos = get_user_repositories(username, "member")
    print(f"Member repositories: {len(member_repos)}개")

if __name__ == "__main__":
    # main()
    get_user_repositories("samdasoo2l", "all")