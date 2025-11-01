# Universal Wallpad Add-on

Universal Wallpad Add-on은 Home Assistant 환경에서 범용 월패드 장치를 통합하기 위한 실험적인 프론트엔드 기반 애드온입니다. 최신 Svelte 5와 TypeScript 기반의 웹 인터페이스를 제공하며, pnpm 워크스페이스 구조로 개발 및 빌드 파이프라인을 구성했습니다.

## 실행 방법
1. 애드온 디렉터리로 이동합니다.
   ```bash
   cd UniversalWallpadAddon
   ```
2. 의존성을 설치합니다.
   ```bash
   pnpm install
   ```
3. 개발 서버를 실행합니다(포트 4173, 모든 인터페이스 공개).
   ```bash
   pnpm --filter frontend dev -- --host 0.0.0.0 --port 4173
   ```
4. 프로덕션용 미리보기를 실행하려면 다음 명령을 사용합니다.
   ```bash
   pnpm --filter frontend preview -- --host 0.0.0.0 --port 4173
   ```

Home Assistant 애드온으로 배포 시에는 제공되는 Dockerfile과 `config.json`을 사용하여 컨테이너 이미지를 빌드하고 추가 설정을 적용할 수 있습니다.
