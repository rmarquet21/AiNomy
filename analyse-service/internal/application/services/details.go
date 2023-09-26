package services

import (
	"ainomy/analyse-api/internal/adapter"
	"ainomy/analyse-api/internal/domain"
	"encoding/json"
)

type (
	DetailsService interface {
		GetDetails(name string) (domain.Definition, error)
	}
	detailsService struct {
		PredictAPI adapter.PredictAPI
	}
)

func (ds detailsService) GetDetails(name string) (domain.Definition, error) {
	var definition domain.Definition
	resp, err := ds.PredictAPI.GetDefinition(name)
	if err != nil {
		return domain.Definition{}, err
	}
	err = json.Unmarshal(resp, &definition)
	if err != nil {
		return domain.Definition{}, nil
	}
	return definition, nil
}
