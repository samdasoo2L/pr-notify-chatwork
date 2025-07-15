# Slack Webhook 사용법

## 1. Slack App 설정

### 1.1 Slack App 생성
1. [Slack API 웹사이트](https://api.slack.com/apps)에 접속
2. "Create New App" 클릭
3. "From scratch" 선택
4. App 이름과 워크스페이스 선택

### 1.2 Incoming Webhooks 활성화
1. 왼쪽 메뉴에서 "Incoming Webhooks" 클릭
2. "Activate Incoming Webhooks" 토글 ON
3. "Add New Webhook to Workspace" 클릭
4. 채널 선택 (예: #general)
5. "Allow" 클릭
6. Webhook URL 복사 (예: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`)

## 2. 코드 설정

### 2.1 Webhook URL 설정
```python
# slack_webhook_example.py 파일에서
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```
위 부분을 실제 webhook URL로 교체하세요.

### 2.2 의존성 설치
```bash
pip install requests
```

## 3. 사용 예시

### 3.1 간단한 메시지 전송
```python
from slack_webhook_example import send_slack_message

send_slack_message("안녕하세요!", "#general")
```

### 3.2 Rich 메시지 전송
```python
from slack_webhook_example import send_slack_rich_message

send_slack_rich_message(
    "알림 제목",
    "알림 내용",
    "good",  # 색상: good(초록), warning(노랑), danger(빨강)
    "#general"
)

둘이 다른건
text만 사용할지, 더 많은 설정이 가능한 attachments를 사용할 것인지
```

### 3.3 GitHub PR 알림
```python
from slack_webhook_example import send_github_pr_notification

send_github_pr_notification(
    "my-project",
    123,
    "새로운 기능 추가",
    "john_doe",
    "https://github.com/user/repo/pull/123",
    "#github"
)
```

## 4. 메시지 타입

### 4.1 기본 메시지
```python
payload = {
    "text": "메시지 내용",
    "channel": "#general",
    "username": "Bot",
    "icon_emoji": ":robot_face:"
}
```

### 4.2 Rich 메시지 (Attachments)
```python
payload = {
    "channel": "#general",
    "attachments": [
        {
            "title": "제목",
            "text": "내용",
            "color": "good",
            "footer": "푸터",
            "ts": 1234567890
        }
    ]
}
```

## 5. 색상 옵션

- `"good"`: 초록색 (성공, 긍정적)
- `"warning"`: 노란색 (경고, 주의)
- `"danger"`: 빨간색 (에러, 위험)
- `"#36a64f"`: 커스텀 hex 색상

## 6. 채널 옵션

- `"#channel-name"`: 공개 채널
- `"@username"`: 개인 메시지
- `"#general"`: 기본 채널

## 7. 실행 방법

```bash
python slack_webhook_example.py
```

## 8. 보안 주의사항

⚠️ **중요**: Webhook URL은 민감한 정보입니다!
- 코드에 직접 하드코딩하지 마세요
- 환경 변수나 설정 파일을 사용하세요
- Git에 커밋하지 마세요

### 환경 변수 사용 예시:
```python
import os

SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
```

## 9. 에러 처리

```python
try:
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    response.raise_for_status()
    print("메시지 전송 성공")
except requests.exceptions.RequestException as e:
    print(f"메시지 전송 실패: {e}")
```

## 10. 추가 기능

- **스케줄링**: `schedule` 라이브러리와 함께 사용
- **로깅**: 전송 실패 시 로그 기록
- **재시도**: 실패 시 자동 재시도 로직
- **템플릿**: 메시지 템플릿 시스템

## 11. 제한사항

- Webhook URL당 초당 1개 메시지 제한
- 메시지 크기 제한 (약 3000자)
- 채널당 동시 webhook 개수 제한 