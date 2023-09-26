package main

import (
	"kleimak/ainomy-authentication-service/internal/config"
	"kleimak/ainomy-authentication-service/internal/handler"
	"kleimak/ainomy-authentication-service/internal/infra"
	"kleimak/ainomy-authentication-service/internal/repository"
	"kleimak/ainomy-authentication-service/internal/service"
	"kleimak/ainomy-authentication-service/internal/validation"
	"log"

	"github.com/go-playground/validator"
	"github.com/labstack/echo"
	"github.com/labstack/echo/middleware"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func main() {
	cfg, err := config.NewConfig("")
	if err != nil {
		panic(err)
	}
	e := echo.New()
	setupMiddleware(e)
	api := e.Group("/api/v1")

	db, err := gorm.Open(postgres.Open(cfg.GetDsn()), &gorm.Config{})

	if err != nil {
		log.Fatal(err)
	}
	userRepo := repository.NewUserRepository(db)
	userSvc := service.NewUserService(userRepo)

	auth := api.Group("/auth")
	auth.POST("/challenge", func(ctx echo.Context) error {
		return handler.Challenge(ctx, userSvc)
	})
	auth.POST("/authorize", func(ctx echo.Context) error {
		return handler.Auhtorize(ctx, userSvc, cfg.Server.SymmetricKey)
	})
	auth.POST("/verify", func(ctx echo.Context) error {
		return handler.VerifyToken(ctx, userSvc, cfg.Server.SymmetricKey)
	})

	consul, err := infra.NewConsulService(&cfg)
	consul.RegisterService()

	e.Logger.Fatal(e.Start(cfg.GetPort()))
}

func setupMiddleware(e *echo.Echo) {
	e.Use(middleware.Recover())
	e.Use(middleware.LoggerWithConfig(middleware.LoggerConfig{
		Format: "method=${method}, uri=${uri}, status=${status}\n",
	}))
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"*"},
		AllowHeaders: []string{echo.HeaderOrigin, echo.HeaderContentType, echo.HeaderAccept},
	}))
	e.Validator = &validation.CustomValidator{Validator: validator.New()}
}
