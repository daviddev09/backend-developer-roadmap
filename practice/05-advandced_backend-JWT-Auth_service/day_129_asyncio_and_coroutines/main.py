import asyncio
import time

async def download_file(i: int):
    print(f'\nНачинается скачивание файла {i}')
    await asyncio.sleep(2)
    print(f'\n Закончил скачивание файла{i}')

async def main_sequential():
    print(f'-----\nRunning function {main_sequential.__name__}')
    start_time = time.perf_counter()
    for i in range(6):
        await download_file(i)
    print(f'Общее время выполнения функции {main_sequential.__name__}: {time.perf_counter()-start_time}')
        
async def main_concurrent():
    print(f'-----\nRunning function {main_concurrent.__name__}')
    start_time = time.perf_counter()
    files_to_download = [download_file(i) for i in range(6)]

    await asyncio.gather(*files_to_download)

    print(f'Общее время выполнения функции {main_concurrent.__name__}: {time.perf_counter()-start_time}')

if __name__ == '__main__':
    asyncio.run(main_sequential())
    asyncio.run(main_concurrent())