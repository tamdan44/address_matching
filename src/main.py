from fastapi import FastAPI
import uvicorn
from views import router 

app = FastAPI()

# Register all routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
