n8n-up:
	docker run -it --rm --name n8n -p 5678:5678 --network host \
	  -v $(PWD)/n8n/datas:/home/node/.n8n \
	  docker.n8n.io/n8nio/n8n:latest

n8n-down:
	docker stop n8n || true

# dify components
dify-up:
	docker compose -f dify/docker/docker-compose.yaml up

dify-log:
	docker compose -f dify/docker/docker-compose.yaml logs -f

dify-down:
	docker compose -f dify/docker/docker-compose.yaml down

.PHONY: n8n-up n8n-down dify-up dify-down
