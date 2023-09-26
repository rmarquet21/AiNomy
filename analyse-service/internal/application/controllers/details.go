package controllers

import (
	"ainomy/analyse-api/internal/application/services"
	"ainomy/analyse-api/internal/domain"
	"net/http"

	"github.com/labstack/echo"
)

type (
	DetailsController interface {
		GetDetails(c echo.Context) error
	}

	detailsController struct {
		services.DetailsService
	}
)

func (dc *detailsController) GetDetails(c echo.Context) error {
	name := c.QueryParam("name")
	resp, err := dc.DetailsService.GetDetails(name)
	if err != nil {
		return c.JSON(http.StatusBadRequest, domain.Error{
			Message: err.Error(),
		})
	}
	return c.JSON(http.StatusOK, resp)
}
