from fastapi import FastAPI
from worker import add

app = FastAPI()

@app.post('/add-task')
async def trigger_add_task(a: int, b: int): # type: ignore
    task = add.delay(a, b) # type: ignore
    return {
        'message': 'задача принята в очередь',
        'task_id': task.id
    } # type: ignore