from handlers.start_handler import router as start_router
from handlers.message_handler import router as message_router

routers_list = [
    start_router,
    message_router,
]
