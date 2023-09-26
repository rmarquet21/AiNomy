package handler

import (
	"kleimak/ainomy-authentication-service/internal/service"
	"kleimak/ainomy-authentication-service/internal/utils"
	"net/http"
	"strings"

	"github.com/labstack/echo"
)

type challengeRequest struct {
	Address string `json:"address" validate:"required"`
}

type authorizeRequest struct {
	Address   string `json:"address" validate:"required"`
	Signature string `json:"signature" validate:"required"`
}
type challengeResponse struct {
	Challenge string `json:"challenge"`
}
type authorizeResponse struct {
	Token string `json:"token" validate:"required"`
}

type verifyRequest struct {
	Token   string `json:"token" validate:"required"`
	Address string `json:"address" validate:"required"`
}
type verifyResponse struct {
	Status  int            `json:"status" validate:"required"`
	Message string         `json:"message" validate:"required"`
	Data    *utils.Payload `json:"data" validate:"required"`
}

func Challenge(c echo.Context, svc *service.UserService) error {
	req := new(challengeRequest)
	if err := c.Bind(req); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := c.Validate(req); err != nil {
		return echo.NewHTTPError(http.StatusUnprocessableEntity, err.Error())
	}

	nonce, err := utils.GenerateNonce()
	if err != nil {
		echo.NewHTTPError(http.StatusInternalServerError)
	}

	res := &challengeResponse{
		Challenge: nonce,
	}

	_, err = svc.ChallengeUser(req.Address, nonce)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
	return c.JSON(http.StatusOK, res)
}

func Auhtorize(c echo.Context, svc *service.UserService, sk string) error {
	req := new(authorizeRequest)
	if err := c.Bind(req); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	if err := c.Validate(req); err != nil {
		return err
	}
	t, err := svc.Authorize(req.Address, req.Signature, sk)
	if err != nil {
		return echo.NewHTTPError(http.StatusUnauthorized, err.Error())
	}

	return c.JSON(http.StatusOK, &authorizeResponse{
		Token: t,
	})
}

func VerifyToken(c echo.Context, svc *service.UserService, sk string) error {
	token := c.Request().Header.Get("Authorization")
	const prefix = "Bearer "
	if !strings.HasPrefix(token, prefix) {
		return echo.NewHTTPError(http.StatusUnauthorized, "invalid token format")
	}
	token = strings.TrimPrefix(token, prefix)
	maker, err := utils.NewPasetoMaker(sk)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError)
	}
	payload, err := maker.VerifyToken(token)
	if err != nil {
		return echo.NewHTTPError(http.StatusUnauthorized, err.Error())
	}

	return c.JSON(http.StatusOK, &verifyResponse{
		Status:  200,
		Message: "valid token",
		Data:    payload,
	})
}
