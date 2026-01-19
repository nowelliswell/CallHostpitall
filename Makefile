.PHONY: start stop clean fresh logs test help

# Default target
start: ## Start the application (frontend + backend)
	@echo "🚀 Starting Hospital Queue Management System..."
	@echo "📱 Frontend: http://localhost:3001"
	@echo "🔧 Backend: http://localhost:8001"
	@echo "📚 API Docs: http://localhost:8001/docs"
	@echo ""
	docker-compose -f docker-compose.dev.yml up --build

start-prod: ## Start production version
	@echo "🚀 Starting production version..."
	docker-compose up --build -d

stop: ## Stop all services
	@echo "🛑 Stopping all services..."
	docker-compose -f docker-compose.dev.yml down
	docker-compose down

clean: ## Clean up containers and volumes
	@echo "🧹 Cleaning up..."
	docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
	docker system prune -f

fresh: clean start ## Clean setup and start

logs: ## Show logs
	docker-compose -f docker-compose.dev.yml logs -f

test: ## Test API connection
	@echo "🧪 Testing API..."
	curl -s http://localhost:8001/health || echo "❌ API not responding"

help: ## Show this help message
	@echo "Hospital Queue Management System - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Quick Start:"
	@echo "  make start    # Start development environment"
	@echo "  make stop     # Stop all services"
	@echo "  make fresh    # Clean start"