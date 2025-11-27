# Commax Wallpad Addon (Performance Fork)

코맥스 월패드를 Home Assistant에 연동하기 위한 애드온입니다.

## 특징

- EW-11 + MQTT 통신 방식
- **반응 속도 최적화** - asyncio 루프 대기 없이 MQTT 콜백에서 직접 처리
- 원본 대비 명령 전송 및 상태 수신 지연 대폭 감소

## 원본 저장소

이 애드온은 [wooooooooooook/HAaddons](https://github.com/wooooooooooook/HAaddons/tree/master/CommaxWallpadAddon)를 기반으로 합니다.

## 설치

1. Home Assistant의 Supervisor > Add-on Store로 이동
2. 우측 상단 메뉴에서 "Repositories" 클릭
3. 이 저장소 URL 추가: `https://github.com/spaceromany/HAaddons_commax`
4. "Commax Wallpad Addon" 설치

## 주요 개선 사항

- 명령 전송: MQTT 콜백에서 즉시 전송 (asyncio 루프 대기 제거)
- 상태 수신: 동기 처리로 변경하여 지연 제거
- `max_send_count` 기본값 30으로 조정
