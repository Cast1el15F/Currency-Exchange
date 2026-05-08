"""Основной файл"""

from fastapi import FastAPI
import uvicorn
from app.api.endpoints.currency import currency_rourer
from app.api.endpoints.users import user_rourer
from app.db.users_dao import UsersDAO


app = FastAPI(title="CURRENCY-EXCHANGE")

@app.get("/find_all")
async def find_all():
    return await UsersDAO.find_all()

app.include_router(user_rourer)
app.include_router(currency_rourer)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)