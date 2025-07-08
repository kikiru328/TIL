from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from user.interface.controllers.user_controller import router as user_routers

app = FastAPI()

# controller 모음
app.include_router(user_routers)


@app.get("/")
def hello():
    return {"Hello": "FastAPI"}


# 400 error handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=400,
        content=exc.errors(),
    )
