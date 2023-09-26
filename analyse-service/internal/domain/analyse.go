package domain

import "ainomy/analyse-api/internal/domain/models"

type AnalyseRepository interface {
	Create(data Analyse) error
	FindAll(address string) ([]models.History, error)
}

type Analyse struct {
	Name       string     `json:"name"`
	Owner      string     `json:"owner"`
	Prediction Prediction `json:"prediction`
	Image      []byte     `json:"image"`
	Kind       string     `json:"type"`
}

func (Analyse) TableName() string {
	return "history"
}
