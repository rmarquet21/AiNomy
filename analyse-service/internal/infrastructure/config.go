package infrastructure

import (
	"fmt"

	"github.com/spf13/viper"
)

type Config struct {
	DBUsername string `mapstructure:"DATABASE_USER"`
	DBPassword string `mapstructure:"DATABASE_PASSWORD"`
	DBHost     string `mapstructure:"DATABASE_HOST"`
	DBPort     string `mapstructure:"DATABASE_PORT"`
	DBName     string `mapstructure:"DATABASE_NAME"`
	DBSSLMode  string `mapstructure:"DATABASE_SSL_MODE"`
	ServerPort string `mapstructure:"SERVER_PORT"`
}

func Load() (*Config, error) {
	v := viper.New()
	

	v.AutomaticEnv()

	if err := v.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			// Config file not found; ignore error if desired
			v.BindEnv("DATABASE_USER")
			v.BindEnv("DATABASE_PASSWORD")
			v.BindEnv("DATABASE_HOST")
			v.BindEnv("DATABASE_PORT")
			v.BindEnv("DATABASE_NAME")
			v.BindEnv("DATABASE_SSL_MODE")
			v.BindEnv("SERVER_PORT")
		} else {
			return nil, fmt.Errorf("Unexpected error during file read %s", err)
		}
	}

	var C Config
	err := v.Unmarshal(&C)
	if err != nil {
		return nil, fmt.Errorf("Config file unmarshall failed, %v", err)
	}
	return &C, err

}

func (c *Config) GetDsn() string {
	return fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=%s", c.DBHost, c.DBPort, c.DBUsername, c.DBPassword, c.DBName, c.DBSSLMode)
}

func (c *Config) GetPort() string {
	return fmt.Sprintf(":%s", c.ServerPort)
}
