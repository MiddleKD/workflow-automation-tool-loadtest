from locust import HttpUser, task, between
import random

# 테스트용 쿼리 예시
QUERIES = [
    "이 문서의 주요 내용은 무엇인가요?",
    "PDF에서 'AI'라는 단어가 등장하는 부분을 알려줘.",
    "문서의 저자는 누구입니까?",
    "요약을 해주세요.",
    "이 문서에서 중요한 날짜는 언제인가요?",
]

class ChatUser(HttpUser):
    wait_time = between(1, 2)  # 각 요청 사이 대기시간(초)

    @task
    def chat(self):
        query = random.choice(QUERIES)
        payload = {
            "query": query,
            "top_k": 3
        }
        with self.client.post(
            "/semantic_search",
            json=payload,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}: {response.text}")