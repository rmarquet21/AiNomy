package config

import (
	"fmt"
	"os"
	"github.com/spf13/viper"
)

type db struct {
	Username string `mapstructure:"DATABASE_USER"`
	Password string `mapstructure:"DATABASE_PASSWORD"`
	Host     string `mapstructure:"DATABASE_HOST"`
	Port     string `mapstructure:"DATABASE_PORT"`
	Name     string `mapstructure:"DATABASE_NAME"`
	SSLMode  string `mapstructure:"DATABASE_SSL_MODE"`
}
type server struct {
	Port         string `mapstructure:"SERVER_PORT"`
	SymmetricKey string `mapstructure:"SERVER_SYMMETRIC_KEY"`
}

type Config struct {
	path     string
	Database db     `mapstructure:"database"`
	Server   server `mapstructure:"server"`
}

func (c *Config) loadConfig() (config Config, err error) {
	if c.path != "" {
		viper.AddConfigPath(c.path)
		viper.SetConfigName("config")
		viper.SetConfigType("env")
		viper.AutomaticEnv()
	} else {
		config = Config{
			Database: db{
				Username: os.Getenv("DATABASE_USER"),
				Password: os.Getenv("DATABASE_PASSWORD"),
				Host:	 os.Getenv("DATABASE_HOST"),
				Port:	 os.Getenv("DATABASE_PORT"),
				Name:  os.Getenv("DATABASE_NAME"),
				SSLMode:  os.Getenv("DATABASE_SSL_MODE"),
			},
			Server: server{
				Port:         os.Getenv("SERVER_PORT"),
				SymmetricKey: os.Getenv("SERVER_SYMMETRIC_KEY"),
			},
		}
		fmt.Println(config)
		return
	}
	

	err = viper.ReadInConfig()
	if err != nil {
		return
	}

	err = viper.Unmarshal(&config)
	return
}

func NewConfig(path string) (Config, error) {
	c := Config{path: path}
	return c.loadConfig()
}

func (c *Config) GetDsn() string {
	return fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=%s", c.Database.Host, c.Database.Port, c.Database.Username, c.Database.Password, c.Database.Name, c.Database.SSLMode)
}

func (c *Config) GetPort() string {
	return fmt.Sprintf(":%s", c.Server.Port)
}
