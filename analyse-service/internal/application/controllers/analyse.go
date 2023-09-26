package controllers

import (
	"ainomy/analyse-api/internal/adapter"
	"ainomy/analyse-api/internal/application/services"
	"ainomy/analyse-api/internal/domain"
	"ainomy/analyse-api/internal/domain/models"
	"io"
	"net/http"

	"github.com/labstack/echo"
)

type (
	AnalyseController interface {
		GetAnalyse(c echo.Context) error
		GetHistory(c echo.Context) error
	}

	analyseController struct {
		services.AnalyseService
	}
)

func (ctl *analyseController) GetAnalyse(c echo.Context) error {
	file, err := c.FormFile("image")
	kind := c.QueryParam("kind")
	if err != nil {
		return c.JSON(http.StatusBadRequest, domain.Error{
			Message: err.Error(),
		})
	}

	fileByte, err := file.Open()
	fb, err := io.ReadAll(fileByte)

	payload := c.Get("payload").(*adapter.AuthenticationPayload)
	res, err := ctl.AnalyseService.GetAnalyse(fb, kind, file.Filename, payload.Address)

	if err != nil {
		return c.JSON(http.StatusBadRequest, domain.Error{
			Message: err.Error(),
		})
	}
	return c.JSON(http.StatusCreated, res)
}

func (ctl *analyseController) GetHistory(c echo.Context) error {
	payload := c.Get("payload").(*adapter.AuthenticationPayload)
	res, err := ctl.AnalyseService.GetHistory(payload.Address)

	var history []models.History
	for _, r := range res {
		history = append(history, models.History{
			ID:         r.ID,
			Owner:      r.Owner,
			FileName:   r.FileName,
			Image:      r.Image,
			Kind:       r.Kind,
			Prediction: r.Prediction,
		})
	}

	if err != nil {
		return c.JSON(http.StatusBadRequest, domain.Error{
			Message: err.Error(),
		})
	}

	return c.JSON(http.StatusCreated, history)
}
