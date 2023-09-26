package services

import (
	"ainomy/analyse-api/internal/adapter"
	"ainomy/analyse-api/internal/infrastructure/repositories"
)

type Services struct {
	Analyse AnalyseService
	Details DetailsService
}

func New(repo *repositories.Repositories) *Services {
	predictAPI := adapter.NewPredictAPI()

	return &Services{
		Analyse: analyseService{
			analyseRepo: repo.AnalyseRepository,
			PredictAPI:  predictAPI,
		},
		Details: detailsService{
			PredictAPI: predictAPI,
		},
	}
}
