package repositories

import (
	"ainomy/analyse-api/internal/domain"

	"gorm.io/gorm"
)

type Repositories struct {
	DB                *gorm.DB
	AnalyseRepository domain.AnalyseRepository
}

func NewRepositories(db *gorm.DB) *Repositories {
	analyseRepo := &Analyse{DB: db}

	return &Repositories{
		AnalyseRepository: analyseRepo,
	}
}
