package services

import (
	"ainomy/analyse-api/internal/adapter"
	"ainomy/analyse-api/internal/domain"
	"ainomy/analyse-api/internal/domain/models"
	"encoding/json"
	"fmt"
)

type (
	AnalyseService interface {
		GetAnalyse(data []byte, kind string, filename string, owner string) (domain.Prediction, error)
		GetHistory(address string) ([]models.History, error)
	}
	analyseService struct {
		analyseRepo domain.AnalyseRepository
		PredictAPI  adapter.PredictAPI
	}
)

func (a analyseService) GetAnalyse(data []byte, kind string, filename string, owner string) (domain.Prediction, error) {
	var res []byte
	var err error

	switch kind {
	case "pneumonia":
		res, err = a.PredictAPI.PredictPneumonia(data)
		if err != nil {
			return domain.Prediction{}, nil
		}
	case "alzheimer":
		res, err = a.PredictAPI.PredictAlzheimer(data)
		if err != nil {
			return domain.Prediction{}, nil
		}
	default:
		return domain.Prediction{}, fmt.Errorf("Kind query parameter is incorrect")
	}

	var analyse domain.Prediction
	err = json.Unmarshal(res, &analyse)
	if err != nil {
		return domain.Prediction{}, fmt.Errorf("Data serialization error : %s", err)
	}

	err = a.analyseRepo.Create(domain.Analyse{
		Name:       filename,
		Owner:      owner,
		Prediction: analyse,
		Image:      data,
		Kind:       kind,
	})
	if err != nil {
		return domain.Prediction{}, fmt.Errorf("Database analyse history creation failed : %s", err)
	}
	return analyse, nil
}

func (a analyseService) GetHistory(address string) ([]models.History, error) {
	history, err := a.analyseRepo.FindAll(address)
	if err != nil {
		return nil, err
	}

	return history, nil
}
