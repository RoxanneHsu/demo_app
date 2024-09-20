from fastapi import FastAPI
from router.db_router import router as db_router
from router.fake_test_router import router as fake_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is available."}


app.include_router(db_router, prefix='/db_crud')
app.include_router(fake_router, prefix='/fake')
