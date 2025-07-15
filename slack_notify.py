import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Slack Webhook URL (실제 webhook URL로 교체하세요)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_message(message, channel="#general", username="Bot", icon_emoji=":robot_face:"):
    """
    Slack webhook을 사용하여 메시지를 보냅니다.
    
    Args:
        message (str): 보낼 메시지
        channel (str): 채널명 (예: "#general", "@username")
        username (str): 봇 이름
        icon_emoji (str): 봇 아이콘 이모지
    """
    payload = {
        "text": message,
        "channel": channel,
        "username": username,
        "icon_emoji": icon_emoji
    }
    
    if SLACK_WEBHOOK_URL is None:
        print("SLACK_WEBHOOK_URL이 설정되어 있지 않습니다.")
        return False
    
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print(f"메시지 전송 성공: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"메시지 전송 실패: {e}")
        return False

def send_slack_rich_message(title, text, color="good", channel="#general"):
    """
    Slack webhook을 사용하여 rich message(attachments)를 보냅니다.
    
    Args:
        title (str): 메시지 제목
        text (str): 메시지 내용
        color (str): 색상 ("good", "warning", "danger", 또는 hex color)
        channel (str): 채널명
    """
    payload = {
        "channel": channel,
        "username": "GitHub Bot",
        "icon_emoji": ":octocat:",
        "attachments": [
            {
                "title": title,
                "text": text,
                "color": color,
                "footer": "GitHub Notification",
                "ts": int(datetime.now().timestamp())
            }
        ]
    }
    
    if SLACK_WEBHOOK_URL is None:
        print("SLACK_WEBHOOK_URL이 설정되어 있지 않습니다.")
        return False
    
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print(f"Rich 메시지 전송 성공: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Rich 메시지 전송 실패: {e}")
        return False

def send_github_pr_notification(repo_name, pr_number, pr_title, author, url, channel="#github"):
    """
    GitHub Pull Request 알림을 Slack으로 보냅니다.
    """
    title = f"🔔 New Pull Request: #{pr_number}"
    text = f"""
*Repository:* {repo_name}
*Title:* {pr_title}
*Author:* {author}
*URL:* {url}
    """.strip()
    
    return send_slack_rich_message(title, text, "good", channel)

def send_github_pr_status_notification(repo_name, pr_number, pr_title, status, url, channel="#github"):
    """
    GitHub Pull Request 상태 변경 알림을 Slack으로 보냅니다.
    """
    status_emoji = {
        "merged": "✅",
        "closed": "❌",
        "opened": "🔔",
        "reopened": "🔄"
    }
    
    status_color = {
        "merged": "good",
        "closed": "danger",
        "opened": "good",
        "reopened": "warning"
    }
    
    emoji = status_emoji.get(status, "📝")
    color = status_color.get(status, "good")
    
    title = f"{emoji} PR {status.title()}: #{pr_number}"
    text = f"""
*Repository:* {repo_name}
*Title:* {pr_title}
*Status:* {status.title()}
*URL:* {url}
    """.strip()
    
    return send_slack_rich_message(title, text, color, channel)

def send_error_notification(error_message, channel="#alerts"):
    """
    에러 알림을 Slack으로 보냅니다.
    """
    title = "🚨 Error Alert"
    text = f"*Error:* {error_message}"
    
    return send_slack_rich_message(title, text, "danger", channel)

def send_daily_summary(summary_data, channel="#daily-summary"):
    """
    일일 요약 정보를 Slack으로 보냅니다.
    """
    title = "📊 Daily Summary"
    
    text = f"""
*Date:* {datetime.now().strftime('%Y-%m-%d')}
*Total PRs:* {summary_data.get('total_prs', 0)}
*New PRs:* {summary_data.get('new_prs', 0)}
*Merged PRs:* {summary_data.get('merged_prs', 0)}
*Closed PRs:* {summary_data.get('closed_prs', 0)}
    """.strip()
    
    return send_slack_rich_message(title, text, "good", channel)

def main():
    """
    메인 함수 - 사용 예시
    """
    print("Slack Webhook 테스트 시작...")
    
    # 1. 간단한 메시지 전송
    print("\n1. 간단한 메시지 전송")
    send_slack_message("안녕하세요! 이것은 테스트 메시지입니다.", "#general")
    
    # 2. Rich 메시지 전송
    print("\n2. Rich 메시지 전송")
    send_slack_rich_message(
        "테스트 알림",
        "이것은 rich message 테스트입니다.",
        "good",
        "#general"
    )
    
    # 3. GitHub PR 알림 예시
    print("\n3. GitHub PR 알림 예시")
    send_github_pr_notification(
        "my-project",
        123,
        "새로운 기능 추가",
        "john_doe",
        "https://github.com/user/repo/pull/123",
        "#github"
    )
    
    # 4. PR 상태 변경 알림 예시
    print("\n4. PR 상태 변경 알림 예시")
    send_github_pr_status_notification(
        "my-project",
        123,
        "새로운 기능 추가",
        "merged",
        "https://github.com/user/repo/pull/123",
        "#github"
    )
    
    # 5. 에러 알림 예시
    print("\n5. 에러 알림 예시")
    send_error_notification(
        "API 요청 실패: 404 Not Found",
        "#alerts"
    )
    
    # 6. 일일 요약 예시
    print("\n6. 일일 요약 예시")
    summary_data = {
        "total_prs": 15,
        "new_prs": 5,
        "merged_prs": 8,
        "closed_prs": 2
    }
    send_daily_summary(summary_data, "#daily-summary")

if __name__ == "__main__":
    # 실제 사용하기 전에 SLACK_WEBHOOK_URL을 설정하세요
    print("⚠️  실제 사용하기 전에 SLACK_WEBHOOK_URL을 설정하세요!")
    print("Slack App 설정에서 Incoming Webhooks를 활성화하고 URL을 복사하세요.")
    
    # main()  # 주석을 해제하여 테스트 실행 