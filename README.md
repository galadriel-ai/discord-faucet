# Discord faucet

### Local
```
pip install -r requirements.txt
cp template.env .env
nano .env
docker-compose up --build -f docker-compose-redis.yml
python main.py
```

### Deployment
```
docker compose down
docker compose up --build -d
```

