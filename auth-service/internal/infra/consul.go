package infra

import (
	"kleimak/ainomy-authentication-service/internal/config"
	"log"
	"os"
	"strconv"
	"time"

	"github.com/hashicorp/consul/api"
)

type ConsulService struct {
	cfg          *config.Config
	ConsulCLient *api.Client
}

const (
	ttl = time.Second * 8

	checkID = "check_health_authentication_service"
)

func NewConsulService(cfg *config.Config) (*ConsulService, error) {
	client, err := api.NewClient(&api.Config{})
	if err != nil {
		return nil, err
	}
	return &ConsulService{
		cfg:          cfg,
		ConsulCLient: client,
	}, nil
}
func (cc *ConsulService) updateHealthCheck() {
	ticker := time.NewTicker(time.Second * 5)
	for {
		err := cc.ConsulCLient.Agent().UpdateTTL(checkID, "online", api.HealthPassing)
		if err != nil {
			log.Fatal(err)
		}
		<-ticker.C
	}
}
func (cc *ConsulService) RegisterService() {
	check := &api.AgentServiceCheck{
		DeregisterCriticalServiceAfter: ttl.String(),
		TLSSkipVerify:                  true,
		TTL:                            ttl.String(),
		CheckID:                        checkID,
	}

	address := getHostname()
	port, err := strconv.Atoi(cc.cfg.Server.Port)
	if err != nil {
		log.Fatal(err)
	}

	registration := &api.AgentServiceRegistration{
		ID:      "auth-service",
		Name:    "ainomy-cluster",
		Tags:    []string{"authentication", "authorization", "golang"},
		Address: address,
		Port:    port,
		Check:   check,
	}

	if err := cc.ConsulCLient.Agent().ServiceRegister(registration); err != nil {
		log.Fatal(err)
	}

	go cc.updateHealthCheck()
}

func getHostname() (hostname string) {
	hostname, _ = os.Hostname()
	return
}
