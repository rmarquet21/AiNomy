package repositories

import (
	"ainomy/analyse-api/internal/domain"
	"ainomy/analyse-api/internal/domain/models"
	"encoding/json"
	"fmt"

	"gorm.io/datatypes"
	"gorm.io/gorm"
)

type Analyse struct {
	DB *gorm.DB
}

func NewAnalyse(db *gorm.DB) *Analyse {
	return &Analyse{
		DB: db,
	}
}

func (a *Analyse) Create(analyse domain.Analyse) error {
	jsByte, err := json.Marshal(analyse.Prediction)
	if err != nil {
		return nil
	}
	history := models.History{
		Owner:      analyse.Owner,
		FileName:   analyse.Name,
		Image:      analyse.Image,
		Kind:       analyse.Kind,
		Prediction: datatypes.JSON(jsByte),
	}

	res := a.DB.Create(&history)
	if res.Error != nil {
		return fmt.Errorf(res.Error.Error())
	}

	return nil
}

func (a *Analyse) FindAll(address string) ([]models.History, error) {
	var history []models.History
	res := a.DB.Where("owner = ?", address).Find(&history)

	if res.Error != nil {
		return nil, res.Error
	}
	return history, nil
}
