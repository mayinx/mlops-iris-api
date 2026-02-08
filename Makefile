# ==============================================================================
# 🛠️ INDIVIDUAL SERVICE TESTING (Use these to debug the API alone)
# ==============================================================================

# Build only the API image
build-api:
	docker build -t mlops-iris-api -f ./src/api/Dockerfile .

# Run the API as a standalone container (maps port 8000 to 8000)
run-api:
	docker run --rm -d --name iris-api -p 8000:8000 mlops-iris-api

# Kill the standalone API container
stop-api:
	docker stop iris-api 

# ==============================================================================
# 🚀 FULL PROJECT ORCHESTRATION (The "Production" Stack)
# ==============================================================================

# Launch everything: 3x API replicas, Nginx, Exporter, Prometheus, Grafana
start-project:
	docker compose -p mlops up -d --build

# Shutdown the entire stack and remove internal networks
stop-project:
	docker compose -p mlops down

# 📋 View real-time logs for the whole stack (Handy for debugging!)
logs:
	docker compose -p mlops logs -f

# 🛡️ View only Nginx logs (To see Rate Limiting in action)
logs-nginx:
	docker logs -f nginx_revproxy

# ==============================================================================
# 🔗 DASHBOARD ACCESS
# ==============================================================================

links:
	@echo "------------------------------------------------"
	@echo "🚀 API Endpoint:  https://localhost/predict"
	@echo "🔥 Prometheus:    http://localhost:9090"
	@echo "📊 Grafana:       http://localhost:3000"
	@echo "🛡️ Nginx Status:  http://localhost:8080/nginx_status"
	@echo "------------------------------------------------"