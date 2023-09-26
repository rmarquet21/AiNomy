package infrastructure

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"time"

	"github.com/hashicorp/consul/api"
)

type ConsulService struct {
	cfg          *Config
	ConsulCLient *api.Client
}

const (
	ttl = time.Second * 8

	checkID = "check_health_analyse_service"
)

func NewConsulService(cfg *Config) (*ConsulService, error) {
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
	port, err := strconv.Atoi(cc.cfg.ServerPort)
	if err != nil {
		log.Fatal(err)
	}

	registration := &api.AgentServiceRegistration{
		ID:      "analyse-service",
		Name:    "ainomy-cluster",
		Tags:    []string{"analyse", "golang"},
		Address: address,
		Port:    port,
		Check:   check,
	}

	if err := cc.ConsulCLient.Agent().ServiceRegister(registration); err != nil {
		log.Fatal(err)
	}

	go cc.updateHealthCheck()
}

func (cc *ConsulService) GetServiceURL(name string) string {
	services, err := cc.ConsulCLient.Agent().Services()
	if err != nil {
		log.Fatal(err)
	}
	// TODO: if service isn't started, the server crash (hostname issue)
	service := services[name]
	address := service.Address
	port := service.Port
	url := fmt.Sprintf("http://%s:%v", address, port)

	return url
}
func getHostname() (hostname string) {
	hostname, _ = os.Hostname()
	return
}
