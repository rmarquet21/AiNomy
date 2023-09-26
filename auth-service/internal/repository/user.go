package repository

import (
	"time"

	"gorm.io/gorm"
)

type User struct {
	Address   string    `gorm:"column:address;not null"`
	Nonce     string    `gorm:"column:nonce;not null"`
	CreatedAt time.Time `gorm:"column:created_at;default:now()"`
	UpdatedAt time.Time `gorm:"column:updated_at;default:now()"`
}

type UserRepository struct {
	db *gorm.DB
}

func NewUserRepository(db *gorm.DB) *UserRepository {
	return &UserRepository{
		db: db,
	}
}
func (r *UserRepository) CreateOne(address string, nonce string) error {
	err := r.db.Create(&User{
		Address: address,
		Nonce:   nonce,
	}).Error
	if err != nil {
		return err
	}
	return nil
}

func (r *UserRepository) FindOne(address string) (*User, error) {
	var user User
	res := r.db.Where("address = ?", address).First(&user)
	if res.Error != nil {
		return nil, res.Error
	}
	return &user, nil
}

func (r *UserRepository) UpdateNonce(address string, newNonce string) error {
	// Met à jour le champ "nonce" de l'utilisateur correspondant à l'adresse spécifiée
	if err := r.db.Model(&User{}).Where("address = ?", address).Update("nonce", newNonce).Error; err != nil {
		return err
	}
	return nil
}
