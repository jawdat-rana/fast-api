from fastapi import FastAPI
from routers import nbim
from mangum import Mangum
from fastapi.responses import HTMLResponse


app = FastAPI()
app.include_router(nbim.router)

handler = Mangum(app)

@app.get("/", response_class=HTMLResponse)
async def root():
    html = '''
        API Working - <a href="http://127.0.0.1:8000/docs">Click Here</a> to check documentation
    '''
    return html
