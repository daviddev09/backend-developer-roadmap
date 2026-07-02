from fastapi import FastAPI
from celery.result import AsyncResult # type: ignore
from worker import celery_app, heavy_computation

app = FastAPI()

@app.post('/reports/')
async def heavy_computate(a: int, b: int): # type: ignore
    task_id = heavy_computation.delay(a, b) # type: ignore
    return {
        'message': 'Задача поставлена в очередь',
        'task_id': task_id.id
    } # type: ignore

@app.get('/reports/{task_id}')
async def get_task_status(task_id: str): # type: ignore
    task_result = AsyncResult(id=task_id, app=celery_app)

    response = { # type: ignore
        'tasl_id': task_id,
        'status': task_result.state, # type: ignore
        'result': None
    }

    if task_result.state == 'SUCCESS': # type: ignore
        response['result'] = task_result.result # type: ignore

    elif task_result.state == 'FAILURE': # type: ignore
        response['result'] = str(task_result.info) # type: ignore

    return response # type: ignore