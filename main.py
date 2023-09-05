from fastapi import FastAPI
from routers import nbim
from fastapi.responses import HTMLResponse


app = FastAPI()
app.include_router(nbim.router)


@app.get("/", response_class=HTMLResponse)
async def root():
    html = '''
        API Working - <a href="https://fast-api-norges-bank-investment.onrender.com/docs">Click Here</a> to check documentation
    '''
    return html
