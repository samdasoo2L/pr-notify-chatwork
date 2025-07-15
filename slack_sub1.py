import requests
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


send_slack_message("와 이게 진짜 레알루defefefdf 되네...", "#general")