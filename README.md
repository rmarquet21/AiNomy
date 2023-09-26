![Logo](documents/logo.png)

# AiNomy

AiNomy is a tool that helps doctors detect diseases and anomalies. It is available as a software-as-a-service (SaaS) platform and can be accessed by doctors anywhere, anytime. Doctors can also contribute data to help train AiNomy's artificial intelligence (AI) and improve its accuracy. The goal of AiNomy is to provide doctors with a reliable tool for detecting diseases and anomalies that they may not have been able to identify on their own.

## Try It Out

You can try AiNomy right now! Visit [http://ainomy.fr](http://ainomy.fr) to access the platform and experience its disease detection capabilities.

## Deployment

To deploy AiNomy on your own system, follow the steps below:

### Prerequisites

Make sure you have the following prerequisites installed on your system:

1. Docker: [Install Docker](https://docs.docker.com/get-docker/)
2. Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

### Clone the Repository

Clone the AiNomy repository to your local machine:

```bash
git clone https://github.com/rmarquet21/ainomy.git
cd ainomy
```

### Configuration

1. Copy the `XXX.env.tpl` files for the necessary components to `XXX.env` files.

```bash
cp ai.env.tpl ai.env
cp auth.env.tpl auth.env
cp analyse.env.tpl analyse.env
```

2. Edit the `.env` files and fill in the required configuration values, such as database connection details, API keys, and any other environment-specific settings.

### Start Docker Compose

Run Docker Compose to start the AiNomy services:

```bash
docker-compose up -d
```

This command will start all the containers defined in the `docker-compose.yml` file in detached mode (in the background). AiNomy should now be up and running.

### Access AiNomy

You can access the AiNomy platform by opening a web browser and navigating to `http://localhost` (or the appropriate URL if you configured a different host). The application should be accessible to doctors for disease and anomaly detection.

## Contributing

If you would like to contribute to AiNomy's development, please follow our [Contributing Guidelines](CONTRIBUTING.md).

## License

AiNomy is open-source software licensed under the [MIT License](LICENSE).