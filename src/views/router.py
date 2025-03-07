from fastapi import APIRouter
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from views.address_view import router as address_router

router = APIRouter()
router.include_router(address_router, prefix="/addresses", tags=["Addresses"])
