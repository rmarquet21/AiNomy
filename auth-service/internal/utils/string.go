package utils

import (
	"crypto/ecdsa"
	cryptoRand "crypto/rand"
	"math/rand"
	mathRand "math/rand"
	"strings"
	"time"

	"github.com/ethereum/go-ethereum/crypto"
)

const alphabet = "abcdefghijklmnopqrstuvwxyz"

func init() {
	rand.Seed(time.Now().UnixNano())
}

// RandomInt generates a random integer between min and max
func RandomInt(min, max int64) int64 {
	return min + mathRand.Int63n(max-min+1)
}

// RandomString generates a random string of length n
func RandomString(n int) string {
	var sb strings.Builder
	k := len(alphabet)

	for i := 0; i < n; i++ {
		c := alphabet[mathRand.Intn(k)]
		sb.WriteByte(c)
	}

	return sb.String()
}

func RandomEthereumAddress() (string, error) {
	// Créez une clé privée aléatoire pour le portefeuille Ethereum
	privateKey, err := ecdsa.GenerateKey(crypto.S256(), cryptoRand.Reader)
	if err != nil {
		return "", err
	}

	// Récupérez l'adresse publique Ethereum correspondant à la clé privée générée
	publicKey := privateKey.Public()
	publicKeyECDSA, ok := publicKey.(*ecdsa.PublicKey)
	if !ok {
		return "", err
	}
	address := crypto.PubkeyToAddress(*publicKeyECDSA).Hex()

	return address, nil
}
