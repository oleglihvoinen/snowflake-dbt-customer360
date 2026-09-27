from fastapi import FastAPI, HTTPException, Query
from .repository import CustomerRepository

app = FastAPI(
    title="Customer 360 Data Product API",
    version="1.0.0",
    description="Governed REST access to golden customer data."
)
repo = CustomerRepository()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/customers/{customer_key}")
def customer(customer_key: str):
    row = repo.get_customer(customer_key)
    if not row:
        raise HTTPException(status_code=404, detail="Customer not found")
    return row

@app.get("/api/v1/customers")
def customers(email: str | None = Query(default=None), limit: int = Query(50, ge=1, le=200)):
    return repo.search(email=email, limit=limit)

@app.get("/api/v1/customers/{customer_key}/quality")
def customer_quality(customer_key: str):
    return repo.quality(customer_key)
