# mac-cleaner

macOS 캐시 사용량 확인 및 정리 도구

## 설치

```bash
pip install -r requirements.txt
```

## 실행

```bash
python3 mac_cleaner.py
```

## 사용 흐름

실행하면 카테고리별로 캐시 사용량을 출력합니다.

```
🌐 브라우저 캐시 : 2.1G
──────────────────────────────────
1. 🌐 Chrome     : 1.3G
   1-1. Cache               : 1.2G    네트워크 리소스 캐시
   1-2. Code Cache          : 45M     JS/WebAssembly 바이트코드 캐시
2. 🦊 Firefox    : 820M
   2-1. Profiles            : 820M    프로필별 네트워크 리소스 캐시

💻 앱 캐시 : 3G
──────────────────────────────────
3. 💻 VSCode     : 2.6G
   3-1. Cache               : 12M     웹뷰 및 네트워크 리소스 캐시
   3-2. CachedData          : 180M    확장 바이트코드 캐시 (재시작 속도 향상용)
   3-3. CachedExtensionVSIXs: 2.4G    설치된 확장 패키지 원본 (삭제해도 무방)
4. 💬 Slack      : 340M
   4-1. Cache_Data          : 340M    채널 이미지·파일 등 네트워크 리소스 캐시

📦 패키지 관리도구 캐시 : 3.2G
──────────────────────────────────
5. 🍺 Homebrew   : 2.1G
   5-1. Cache               : 2.1G
6. 📦 npm        : 890M
   6-1. Cache               : 890M
7. 🐍 pip        : 204M
   7-1. Cache               : 204M
```

출력 이후 삭제 여부를 묻습니다.

```
모두 삭제하시겠습니까? [Y/n]:
```

- `y` 입력 시 모든 캐시 항목 내부를 삭제합니다.

```
삭제중... [████████████████████] 10/10

=== 삭제 완료! ===
```

- `n` 혹은 다른 입력 시 취소됩니다.

```
=== 작업 취소 ===
```

> **참고:** 각 경로의 디렉토리 자체는 유지하고, 내부 파일 및 하위 디렉토리만 삭제합니다.

## config.yaml 구조

`config.yaml`에서 정리할 캐시 경로를 직접 추가·수정할 수 있습니다.

```yaml
categories:
  - name: "카테고리 이름"
    items:
      - name: "앱 이름"
        paths:
          - name: "경로 이름"
            path: ~/Library/Caches/...
            note: "설명"
```

| 키 | 설명 |
|---|---|
| `categories` | 최상위 분류 목록 |
| `items` | 카테고리 내 앱,도구 목록 |
| `paths` | 앱별 캐시 경로 목록 |
| `name` | 표시 이름 |
| `path` | 실제 캐시 경로 (`~/` 사용 가능) |
| `note` | 경로에 대한 부연 설명 (생략 가능) |

## 파일 구조

- `mac_cleaner.py` — 진입점
- `utils.py` — 유틸리티 함수
- `config.yaml` — 캐시 경로 설정

## 라이센스

[MIT License](LICENSE)
