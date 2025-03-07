from fastapi import FastAPI
import uvicorn
from views import router 

app = FastAPI(
    title="Address Matching API",
    description="API for address matching. `country_code` is optional and defaults to 'vn' if not provided.",
    version="1.0"
)

# Register all routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
