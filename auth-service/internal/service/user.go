package service

import (
	"errors"
	"kleimak/ainomy-authentication-service/internal/repository"
	"kleimak/ainomy-authentication-service/internal/utils"
	"regexp"
	"strings"
	"time"

	"github.com/ethereum/go-ethereum/accounts"
	"github.com/ethereum/go-ethereum/common/hexutil"
	"github.com/ethereum/go-ethereum/crypto"
	"gorm.io/gorm"
)

type UserService struct {
	userRepository *repository.UserRepository
}

func NewUserService(ur *repository.UserRepository) *UserService {
	return &UserService{
		userRepository: ur,
	}
}

func (s *UserService) ChallengeUser(address string, nonce string) (*repository.User, error) {
	u, err := s.userRepository.FindOne(address)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			if err := s.userRepository.CreateOne(address, nonce); err != nil {
				return nil, err
			}
		} else {
			return nil, err
		}
	}

	err = s.userRepository.UpdateNonce(address, nonce)
	if err != nil {
		return nil, err
	}

	return u, nil
}

var ErrAuthError = errors.New("authentication error")
var ErrInvalidAddress = errors.New("invalid address")
var ErrInvalidSignature = errors.New("invalid signature")
var hexRegex *regexp.Regexp = regexp.MustCompile(`^0x[a-fA-F0-9]{40}$`)

func (s *UserService) Authorize(address string, signature string, sk string) (string, error) {
	user, err := s.userRepository.FindOne(address)
	if err != nil {
		return "", err
	}
	if !hexRegex.MatchString(address) {
		return "", ErrInvalidAddress
	}

	sig, err := hexutil.Decode(signature)
	if err != nil {
		return "", ErrInvalidSignature
	}

	sig[crypto.RecoveryIDOffset] -= 27
	msg := accounts.TextHash([]byte(user.Nonce))
	recovered, err := crypto.SigToPub(msg, sig)
	if err != nil {
		return "", err
	}
	recoveredAddr := crypto.PubkeyToAddress(*recovered)
	if user.Address != strings.ToLower(recoveredAddr.Hex()) {
		return "", ErrAuthError
	}
	// update the nonce & prevent the usage of double signature
	nonce, err := utils.GenerateNonce()
	err = s.userRepository.UpdateNonce(address, nonce)
	if err != nil {
		return "", err
	}

	maker, err := utils.NewPasetoMaker(sk)
	if err != nil {
		return "", err
	}

	token, err := maker.CreateToken(user.Address, time.Hour*24)
	if err != nil {
		return "", err
	}

	return token, nil
}
