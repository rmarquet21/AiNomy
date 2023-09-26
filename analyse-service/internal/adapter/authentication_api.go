package adapter

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/go-resty/resty/v2"
)

type AuthenticationAPI interface {
	Authorize(token string) (*AuthenticationPayload, error)
}

type authenticationAPI struct {
	client *resty.Client
	svcUrl string
}
type response struct {
	Status  int                   `json:"status" validate:"required"`
	Message string                `json:"message" validate:"required"`
	Data    AuthenticationPayload `json:"data" validate:"required"`
}
type AuthenticationPayload struct {
	Address   string    `json:"address"`
	IssuedAt  time.Time `json:"issued_at"`
	ExpiredAt time.Time `json:"expired_at"`
}

func NewAuthenticationAPI(authentication_api_url string) *authenticationAPI {
	c := resty.New()
	return &authenticationAPI{
		client: c,
		svcUrl: authentication_api_url,
	}
}
func (p *authenticationAPI) Authorize(token string) (AuthenticationPayload, error) {
	var resp *resty.Response
	var err error

	resp, err = p.client.R().
		SetAuthToken(token).
		Post(p.svcUrl + "/api/v1/auth/verify")

	switch resp.StatusCode() {
	case http.StatusUnauthorized:
		return AuthenticationPayload{}, fmt.Errorf("Unauthorized")
	case http.StatusOK:
		var r response
		err = json.Unmarshal(resp.Body(), &r)
		if err != nil {
			return AuthenticationPayload{}, fmt.Errorf("Failed to serialize the response")
		}
		return r.Data, nil
	default:
		return AuthenticationPayload{}, err
	}
}

// func (p *predictAPI) GetHealth() (string, error) {
// 	resp, err := http.Get("http://localhost:8080/api/v1/healthcheck")
// 	if err != nil {
// 		return "", err
// 	}
// 	defer resp.Body.Close()
// 	body, err := io.ReadAll(resp.Body)
// 	if err != nil {
// 		return "", err
// 	}
// 	return string(body), nil
// }
