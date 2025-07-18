from celery.result import AsyncResult
import sys

sys.path.append(
    "/mnt/e/3_Resources/TIL/Web_Frameworks/FastAPI/clean-architecture/common"
)
from common.messaging import celery

if __name__ == "__main__":
    async_result = AsyncResult("fed97183-2284-4fdf-b5cd-2750247cd77b", app=celery)
    result = async_result.result
    print(result)
