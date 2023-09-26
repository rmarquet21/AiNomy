FROM golang:1.19-alpine AS build-stage
WORKDIR /app

COPY . ./
RUN go mod download

RUN CGO_ENABLED=0 GOOS=linux go build -o /server /app/cmd/api/

FROM alpine:latest
WORKDIR /

COPY --from=build-stage /server /server

EXPOSE 4545

CMD [ "/server" ]