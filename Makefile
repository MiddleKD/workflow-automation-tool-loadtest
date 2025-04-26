n8n-up:
	docker run -it --rm --name n8n -p 5678:5678 --network host \
	  -v $(PWD)/n8n/datas:/home/node/.n8n \
	  docker.n8n.io/n8nio/n8n:latest

n8n-log:
	docker logs -f n8n

n8n-down:
	docker stop n8n || true


dify-up:
	docker compose --env-file dify/.env -f dify/docker/docker-compose.yaml up

dify-log:
	docker compose -f dify/docker/docker-compose.yaml logs -f

dify-down:
	docker compose -f dify/docker/docker-compose.yaml down


ollama-up:
	docker run -d --gpus=all \
	  -v /home/middlek/Desktop/mnt/sda/models/ollama:/root/.ollama \
	  -v ./ollama/modelfiles:/root/modelfiles \
	  -p 11434:11434 \
	  -e OLLAMA_KV_CACHE_TYPE=1 \
	  -e OLLAMA_NUM_PARALLEL=16 \
	  --name ollama \
	  ollama/ollama

ollama-down:
	docker stop ollama || true
	docker rm ollama || true

langchain:
	uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir langchain

n8n-pdf-init:
	curl -X POST --data-binary @pdfs/sample.pdf -H "Content-Type: application/pdf" http://localhost:5678/webhook/upload

loadtest:
	@echo "Select target user:"
	@echo "1) LangchainUser"
	@echo "2) N8NUser"
	@echo "3) DifyUser"
	@read -p "Enter the number: " num; \
	case $$num in \
		1) uv run locust -f loadtest.py LangchainUser ;; \
		2) uv run locust -f loadtest.py N8NUser ;; \
		3) uv run locust -f loadtest.py DifyUser ;; \
		*) echo "Invalid input" ;; \
	esac

.PHONY: n8n-up n8n-down n8n-log dify-up dify-log dify-down ollama-up ollama-log ollama-down langchain n8n-pdf-init loadtest
