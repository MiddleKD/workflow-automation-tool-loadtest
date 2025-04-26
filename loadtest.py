import os
import random

from dotenv import load_dotenv
from locust import HttpUser, between, task

from constant import DIFY_HOST, LANGCHAIN_HOST, N8N_HOST

load_dotenv()

QUERIES = [
    "이 문서의 주요 내용은 무엇인가요?",
    "PDF에서 'AI'라는 단어가 등장하는 부분을 알려줘.",
    "문서의 저자는 누구입니까?",
    "요약을 해주세요.",
    "이 문서에서 중요한 날짜는 언제인가요?",
]

DIFY_HEADERS = {
    "Authorization": f"Bearer {os.getenv('DIFY_API_KEY')}",
    "Content-Type": "application/json",
}


class LangchainUser(HttpUser):
    wait_time = between(1, 2)  # 각 요청 사이 대기시간(초)
    host = LANGCHAIN_HOST

    @task
    def chat(self):
        query = random.choice(QUERIES)
        payload = {"query": query, "top_k": 5}
        with self.client.post("/chat", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Failed with status {response.status_code}: {response.text}"
                )


class N8NUser(HttpUser):
    wait_time = between(1, 2)  # 각 요청 사이 대기시간(초)
    host = N8N_HOST

    @task
    def chat(self):
        query = random.choice(QUERIES)
        payload = {"query": query, "top_k": 5}
        with self.client.post(
            "/webhook/chat", json=payload, catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Failed with status {response.status_code}: {response.text}"
                )


class DifyUser(HttpUser):
    wait_time = between(1, 2)  # 각 요청 사이 대기시간(초)
    host = DIFY_HOST

    @task
    def chat(self):
        query = random.choice(QUERIES)
        payload = {
            "inputs": {"query": query},
            "response_mode": "blocking",
            "user": "abc-123",
        }
        with self.client.post(
            "/v1/workflows/run", json=payload, headers=DIFY_HEADERS, catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Failed with status {response.status_code}: {response.text}"
                )
