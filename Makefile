.PHONY: help build up down migrate seed clean logs status restart shell-backend shell-db

help:
	@echo "Available commands:"
	@echo "  make build    - Build Docker images"
	@echo "  make up       - Start all services"
	echo "  make down     - Stop all services"
	@echo "  make migrate  - Run database migrations"
	@echo "  make seed     - Seed database with sample data"
	@echo "  make clean    - Remove containers and volumes"
	@echo "  make logs     - View all logs"
	@echo "  make status   - Show service status"
	@echo "  make restart  - Restart all services"
	@echo "  make shell-backend - Enter backend container"
	@echo "  make shell-db - Enter database container"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "   Backend: http://15.206.178.183:8000"
	@echo "   API Docs: http://15.206.178.183:8000/docs"

down:
	docker-compose down

migrate:
	docker-compose run --rm migrations

seed:
	docker-compose exec backend python scripts/seed.py

clean:
	docker-compose down -v
	docker system prune -f
	@echo "✅ Cleaned up"

logs:
	docker-compose logs -f

status:
	docker-compose ps

restart:
	docker-compose restart
	@echo "✅ Services restarted"

shell-backend:
	docker-compose exec backend bash

shell-db:
	docker-compose exec postgres psql -U postgres -d taskdb

shell-redis:
	docker-compose exec redis redis-cli

cache-clear:
	docker-compose exec backend python -c "from redis_config import task_cache, eligibility_cache; task_cache.delete_pattern('*'); eligibility_cache.delete_pattern('*'); print('Cache cleared')"
