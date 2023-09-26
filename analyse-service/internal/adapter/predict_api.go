package adapter

import (
	"bytes"
	"fmt"
	"io"
	"net/http"

	"github.com/go-resty/resty/v2"
)

type PredictAPI interface {
	PredictPneumonia(img []byte) ([]byte, error)
	PredictAlzheimer(img []byte) ([]byte, error)
	GetDefinition(name string) ([]byte, error)
	GetHealth() (string, error)
}

type predictAPI struct {
	client *resty.Client
}

func NewPredictAPI() *predictAPI {
	c := resty.New()
	return &predictAPI{
		client: c,
	}
}
func (p *predictAPI) PredictPneumonia(img []byte) ([]byte, error) {
	resp, err := p.client.R().
		SetFileReader("img", "analyse.jpeg", bytes.NewReader(img)).
		Post("http://ai-server:4000/api/predict/pneumonia")
	if err != nil {
		return nil, err
	}
	switch resp.RawResponse.StatusCode {
	case http.StatusOK:
		return resp.Body(), nil
	default:
		return nil, fmt.Errorf("Something went wrong with the prediction API")
	}
}

func (p *predictAPI) PredictAlzheimer(img []byte) ([]byte, error) {
	resp, err := p.client.R().
		SetFileReader("img", "analyse.jpeg", bytes.NewReader(img)).
		Post("http://ai-server:4000/api/predict/alzheimer")
	if err != nil {
		return nil, err
	}
	switch resp.RawResponse.StatusCode {
	case http.StatusOK:
		return resp.Body(), nil
	default:
		return nil, fmt.Errorf("Something went wrong with the prediction API")
	}
}
func (p *predictAPI) GetDefinition(name string) ([]byte, error) {
	resp, err := p.client.R().
		SetPathParams(map[string]string{
			"name": name,
		}).
		Get("http://ai-server:4000/api/details/{name}")
	if err != nil {
		return nil, err
	}
	switch resp.RawResponse.StatusCode {
	case http.StatusOK:
		return resp.Body(), nil
	default:
		return nil, fmt.Errorf("Something went wrong with the prediction API")
	}

}
func (p *predictAPI) GetHealth() (string, error) {
	resp, err := http.Get("http://ai-server:4000/api/health")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	return string(body), nil
}
