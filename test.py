import requests

BASE_URL = "http://127.0.0.1:8000"


# ── Create todos ───────────────────────────────────────────────────────────

print("── Creating todos ──")

r = requests.post(f"{BASE_URL}/todos", json={
    "title": "Learn FastAPI",
    "description": "Complete the Layer 1 tutorial"
})
print(r.status_code, r.json())   # 201

r = requests.post(f"{BASE_URL}/todos", json={
    "title": "Build Todo API",
    "description": "First project from scratch",
    "completed": True
})
print(r.status_code, r.json())   # 201

r = requests.post(f"{BASE_URL}/todos", json={
    "title": "Learn databases"
})
print(r.status_code, r.json())   # 201 — description and completed use defaults


# ── Get all todos ──────────────────────────────────────────────────────────

print("\n── All todos ──")
r = requests.get(f"{BASE_URL}/todos")
print(r.status_code, r.json())

print("\n── Completed todos only ──")
r = requests.get(f"{BASE_URL}/todos", params={"completed": "true"})
print(r.status_code, r.json())

print("\n── Incomplete todos only ──")
r = requests.get(f"{BASE_URL}/todos", params={"completed": "false"})
print(r.status_code, r.json())

print("\n── Paginated — skip 1, limit 2 ──")
r = requests.get(f"{BASE_URL}/todos", params={"skip": 1, "limit": 2})
print(r.status_code, r.json())


# ── Get one todo ───────────────────────────────────────────────────────────

print("\n── Get todo id=1 ──")
r = requests.get(f"{BASE_URL}/todos/1")
print(r.status_code, r.json())

print("\n── Get todo that doesn't exist ──")
r = requests.get(f"{BASE_URL}/todos/999")
print(r.status_code, r.json())   # 404


# ── Update a todo ──────────────────────────────────────────────────────────

print("\n── Update todo id=1 ──")
r = requests.put(f"{BASE_URL}/todos/1", json={
    "title": "Learn FastAPI",
    "description": "Layer 1 complete!",
    "completed": True
})
print(r.status_code, r.json())

print("\n── Verify update ──")
r = requests.get(f"{BASE_URL}/todos/1")
print(r.status_code, r.json())


# ── Delete a todo ──────────────────────────────────────────────────────────

print("\n── Delete todo id=2 ──")
r = requests.delete(f"{BASE_URL}/todos/2")
print(r.status_code)   # 204 — no body returned

print("\n── Verify deletion ──")
r = requests.get(f"{BASE_URL}/todos")
print(r.status_code, r.json())   # id=2 should be gone

print("\n── Delete todo that doesn't exist ──")
r = requests.delete(f"{BASE_URL}/todos/999")
print(r.status_code, r.json())   # 404