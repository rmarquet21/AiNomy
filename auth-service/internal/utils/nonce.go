package utils

import (
	"crypto/rand"
	"math/big"
)

func GenerateNonce() (string, error) {
	var max *big.Int
	max = new(big.Int)
	max.Exp(big.NewInt(2), big.NewInt(130), nil).Sub(max, big.NewInt(1))
	n, err := rand.Int(rand.Reader, max)
	if err != nil {
		return "", err
	}
	return n.Text(10), nil
}
