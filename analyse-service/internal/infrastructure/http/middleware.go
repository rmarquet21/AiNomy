package http

import (
	"ainomy/analyse-api/internal/adapter"
	"ainomy/analyse-api/internal/infrastructure"
	"net/http"
	"strings"

	"github.com/labstack/echo"
)

func PasetoMiddleware(consul *infrastructure.ConsulService) echo.MiddlewareFunc {
	return func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			token := c.Request().Header.Get("Authorization")
			if token == "" {
				return echo.NewHTTPError(http.StatusUnauthorized, "missing token")
			}

			const prefix = "Bearer "
			if !strings.HasPrefix(token, prefix) {
				return echo.NewHTTPError(http.StatusUnauthorized, "invalid token format")
			}
			token = strings.TrimPrefix(token, prefix)

			authentication_api_url := consul.GetServiceURL("auth-service")
			authorizationAPI := adapter.NewAuthenticationAPI(authentication_api_url)
			payload, err := authorizationAPI.Authorize(token)
			if err != nil {
				return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
			}

			c.Set("payload", &payload)

			return next(c)
		}
	}
}
