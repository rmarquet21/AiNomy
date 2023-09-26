package models

import (
	"github.com/google/uuid"
	"gorm.io/datatypes"
)

type History struct {
	ID         uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4()"`
	Owner      string         `gorm:"column:owner"`
	FileName   string         `gorm:"column:filename"`
	Image      []byte         `gorm:"column:image;type:bytea"`
	Kind       string         `gorm:"column:kind"`
	Prediction datatypes.JSON `gorm:"column:prediction; type:jsonb"`
}

func (History) TableName() string {
	return "history"
}
