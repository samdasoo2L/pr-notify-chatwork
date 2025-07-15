# GitHub Actions 설정 가이드

## 1. Repository Secrets 설정

GitHub repository에서 다음 secrets를 설정해야 합니다:

### 1.1 Repository Settings 접속
1. GitHub repository 페이지에서 **Settings** 탭 클릭
2. 왼쪽 메뉴에서 **Secrets and variables** → **Actions** 클릭

### 1.2 Secrets 추가

#### `SLACK_WEBHOOK_URL`
- **Name**: `SLACK_WEBHOOK_URL`
- **Value**: `https://hooks.slack.com/services/YOUR/WEBHOOK/URL`
- **설명**: Slack webhook URL

#### `GITHUB_TOKEN` (선택사항)
- **Name**: `GITHUB_TOKEN`
- **Value**: GitHub Personal Access Token
- **설명**: Private repository 접근용 (필요한 경우만)

## 2. 워크플로우 파일 위치

워크플로우 파일은 다음 경로에 있어야 합니다:
```
.github/workflows/daily-pr-notify.yml
```

## 3. 실행 시간 설정

현재 설정된 시간:
- **UTC**: 07:00 (오전 7시)
- **KST**: 16:00 (오후 4시)

### 시간 변경 방법

`.github/workflows/daily-pr-notify.yml` 파일에서 cron 표현식을 수정:

```yaml
- cron: '0 7 * * *'  # 분 시 일 월 요일
```

#### 예시:
- 매일 오전 9시: `'0 9 * * *'`
- 매일 오후 6시: `'0 18 * * *'`
- 매주 월요일 오후 2시: `'0 14 * * 1'`

## 4. 수동 실행

GitHub repository 페이지에서:
1. **Actions** 탭 클릭
2. **Daily PR Notification** 워크플로우 선택
3. **Run workflow** 버튼 클릭

## 5. 로그 확인

실행 후 로그를 확인하려면:
1. **Actions** 탭 클릭
2. 워크플로우 실행 기록 클릭
3. **notify** job 클릭
4. 각 step의 로그 확인

## 6. 문제 해결

### 6.1 Secrets 오류
```
Error: SLACK_WEBHOOK_URL이 설정되어 있지 않습니다.
```
→ Repository Secrets에서 `SLACK_WEBHOOK_URL` 설정 확인

### 6.2 권한 오류
```
Error: 403 Forbidden
```
→ GitHub Token 권한 확인 또는 `GITHUB_TOKEN` secret 추가

### 6.3 의존성 오류
```
Error: ModuleNotFoundError: No module named 'requests'
```
→ 워크플로우의 `Install dependencies` step 확인

## 7. 고급 설정

### 7.1 여러 시간에 실행
```yaml
on:
  schedule:
    - cron: '0 9 * * *'   # 오전 9시
    - cron: '0 18 * * *'  # 오후 6시
```

### 7.2 특정 브랜치에서만 실행
```yaml
on:
  schedule:
    - cron: '0 7 * * *'
  workflow_dispatch:
  push:
    branches: [ main ]
```

### 7.3 조건부 실행
```yaml
- name: Run PR notification script
  if: github.ref == 'refs/heads/main'
  run: python github_api_notify.py
```

## 8. 모니터링

### 8.1 이메일 알림
GitHub Settings → Notifications에서 워크플로우 실패 시 이메일 알림 설정

### 8.2 Slack 알림
워크플로우에 Slack 알림 step 추가:

```yaml
- name: Notify Slack on failure
  if: failure()
  run: |
    curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"GitHub Actions 워크플로우가 실패했습니다!"}' \
    ${{ secrets.SLACK_WEBHOOK_URL }}
``` 