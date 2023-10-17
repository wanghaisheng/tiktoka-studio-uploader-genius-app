https://stackoverflow.com/questions/76142431/how-to-run-another-application-within-the-same-running-event-loop

run both tk and fastapi

```
printing_app.py

import asyncio

async def go():
    counter = 0
    while True:
        counter += 1
        print(counter)
        await asyncio.sleep(1)

       
def run():
    asyncio.run(go())

```
    
```
from fastapi import FastAPI
import printing_app
import asyncio
import uvicorn

app = FastAPI()


@app.get('/')
def main():
    return 'Hello World!'
    

def start_uvicorn(loop):
    config = uvicorn.Config(app, loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())
    

def start_printing_app(loop):
    loop.create_task(printing_app.go())  # pass go() (coroutine), not run() 

            
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_printing_app(loop)
    start_uvicorn(loop)
```