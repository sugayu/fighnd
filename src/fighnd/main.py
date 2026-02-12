'''Prototype of original image viewer

About osascript:
    https://www.macscripter.net/t/copy-image-contents-to-clipboard-please-save-me/34350
'''

from logging import getLogger
import flet as ft

from fighnd import frontend, backend

logger = getLogger(__name__)


##
@ft.component
def app() -> list[ft.View]:
    '''Main UI of application.'''

    route, _ = ft.use_state(frontend.Route(route=ft.context.page.route))

    # subscribe to page events as soon as possible
    ft.context.page.on_route_change = route.route_change
    ft.context.page.on_view_pop = route.view_popped

    views = [frontend.galleryview()]
    if route.route == '/fig':
        views += [frontend.imageview()]
    logger.info(f'Now route is {route.route}')
    return views


def main(page: ft.Page):
    page.title = 'Image Viewer'
    page.render_views(app)


def launch() -> None:
    '''Access point.'''
    if not backend.exist_database():
        backend.initialize_database()

    ft.run(main)


if __name__ == '__main__':
    from sugayutils.log import mylogconfig

    mylogconfig()

    launch()
