from aiogram import Router
from handlers.start import router as start_router
from handlers.callbacks import router as callbacks_router

router = Router()
router.include_router(start_router)
router.include_router(callbacks_router)
