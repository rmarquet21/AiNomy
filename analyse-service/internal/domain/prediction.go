package domain

import (
	"database/sql/driver"
	"encoding/json"
	"fmt"
)

type Prediction []Accuracy

type Accuracy struct {
	Label       string  `json:"label"`
	Probability float64 `json:"probability"`
}

func (p Prediction) Value() (driver.Value, error) {
	return json.Marshal(p)
}

func (p *Prediction) Scan(src interface{}) error {
	if src == nil {
		return nil
	}
	source, ok := src.([]byte)
	if !ok {
		return fmt.Errorf("invalid type for Prediction")
	}

	err := json.Unmarshal(source, &p)
	if err != nil {
		return fmt.Errorf("could not unmarshal Prediction field: %v", err)
	}
	return nil
}
