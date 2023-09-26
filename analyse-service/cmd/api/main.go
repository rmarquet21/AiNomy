package main

import (
	"ainomy/analyse-api/internal/application/controllers"
	"ainomy/analyse-api/internal/application/services"
	"ainomy/analyse-api/internal/infrastructure"
	"ainomy/analyse-api/internal/infrastructure/http"
	"ainomy/analyse-api/internal/infrastructure/logger"
	"ainomy/analyse-api/internal/infrastructure/repositories"
	"log"

	"go.uber.org/zap"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func main() {
	err := logger.New()
	if err != nil {
		log.Fatal(err)
	}

	cfg, err := infrastructure.Load()
	db, err := gorm.Open(postgres.Open(cfg.GetDsn()), &gorm.Config{})
	if err != nil {
		panic(err)
	}
	e := http.Echo()

	repo := repositories.NewRepositories(db)
	consul, err := infrastructure.NewConsulService(cfg)
	if err != nil {
		panic(err)
	}
	consul.RegisterService()

	svc := services.New(repo)
	ctrls := controllers.New(svc)
	pasetoMlwr := http.PasetoMiddleware(consul)

	controllers.SetDefault(e)
	controllers.SetApi(e, ctrls, pasetoMlwr)

	logger.Fatal("failed to start server", zap.Error(e.Start(cfg.GetPort())))
}
