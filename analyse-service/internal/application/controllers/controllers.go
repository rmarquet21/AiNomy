package controllers

import (
	"ainomy/analyse-api/internal/application/services"
	"net/http"

	"github.com/labstack/echo"
)

type Controllers struct {
	AnalyseController AnalyseController
	DetailsController DetailsController
}

func New(s *services.Services) *Controllers {
	return &Controllers{
		AnalyseController: &analyseController{s.Analyse},
		DetailsController: &detailsController{s.Details},
	}
}

func SetDefault(e *echo.Echo) {
	e.GET("/healthcheck", func(c echo.Context) error {
		return c.String(http.StatusOK, "OK")
	})
}
func SetApi(e *echo.Echo, ctl *Controllers, m echo.MiddlewareFunc) {
	g := e.Group("/api/v1")
	g.Use(m)

	// Analyse
	g.POST("/analyse", ctl.AnalyseController.GetAnalyse)
	g.GET("/analyse", ctl.AnalyseController.GetHistory)

	// Details
	g.GET("/details", ctl.DetailsController.GetDetails)

}
