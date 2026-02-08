'''Routing'''

from dataclasses import dataclass
from logging import getLogger
import asyncio
import flet as ft

logger = getLogger(__name__)
__all__ = ['Route']


##
@ft.observable
@dataclass
class Route:
    route: str

    def route_change(self, e: ft.RouteChangeEvent):
        logger.info("Route changed from: %s to: %s", self.route, e.route)
        self.route = e.route

    async def view_popped(self, e: ft.ViewPopEvent):
        logger.info('View poped')
        views = ft.unwrap_component(ft.context.page.views)
        if len(views) > 1:
            await ft.context.page.push_route('/')
            # await ft.context.page.push_route(views[-2].route)
