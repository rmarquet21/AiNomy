FROM node:18.14.2 as build-stage
WORKDIR /app
RUN corepack enable

COPY .npmrc package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm-store,target=/root/.pnpm-store \
    pnpm install --frozen-lockfile

COPY . .

EXPOSE 4173

CMD ["pnpm", "run", "dev"]