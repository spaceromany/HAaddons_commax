ARG BUILD_ARCH
FROM ghcr.io/home-assistant/${BUILD_ARCH}-base:3.19

ENV LANG C.UTF-8
ENV TZ=Asia/Seoul

RUN apk add --no-cache nodejs-current npm \
  && npm install -g pnpm@10.13.1

WORKDIR /app

COPY pnpm-workspace.yaml package.json pnpm-lock.yaml ./
COPY frontend/package.json frontend/package.json

RUN pnpm install --frozen-lockfile

COPY frontend frontend

RUN pnpm --filter frontend build

EXPOSE 4173

CMD ["pnpm", "--filter", "frontend", "preview", "--", "--host", "0.0.0.0", "--port", "4173"]
