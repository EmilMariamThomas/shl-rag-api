from typing import List


def latest_user_message(messages: List[dict]) -> str:
    for message in reversed(messages):
        if message["role"] == "user":
            return message["content"]
    return ""


def needs_clarification(query: str) -> bool:
    query = query.lower()

    vague_queries = [
        "assessment",
        "test",
        "hire",
        "hiring",
        "recommend",
        "developer",
        "engineer",
        "candidate",
        "employee"
    ]

    if len(query.split()) < 5:
        return True

    matches = sum(word in query for word in vague_queries)

    return matches <= 1


def build_recommendations(docs):
    recommendations = []

    for doc in docs[:10]:
        recommendations.append({
            "name": doc.metadata.get("name", ""),
            "url": doc.metadata.get("url", ""),
            "test_type": doc.metadata.get("type", "")
        })

    return recommendations