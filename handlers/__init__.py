from aiogram import Router
from handlers.start import router as start_router
from handlers.callbacks import router as callbacks_router
from handlers.game import router as game_router
from handlers.admin import router as admin_router

router = Router()
router.include_router(start_router)
router.include_router(callbacks_router)
router.include_router(game_router)
router.include_router(admin_router)
