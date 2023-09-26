
![Logo](documents/logo.png)


# AiNomy

AiNomy is a tool that helps doctors detect diseases and anomalies. It is available as a software-as-a-service (SaaS) platform and can be accessed by doctors anywhere, anytime. Doctors can also contribute data to help train AiNomy's artificial intelligence (AI) and improve its accuracy. The goal of AiNomy is to provide doctors with a reliable tool for detecting diseases and anomalies that they may not have been able to identify on their own.


## Deployment

To deploy this project

1. Duplicate .env
```bash
cp ./docker/.env.tpl ./docker/.env
```
2. Start the server
```bash
./prod.sh
```
3. Check API is started
```bash
curl -X 'GET' \
  'http://0.0.0.0:4000/api/health/' \
  -H 'accept: application/json' 
```