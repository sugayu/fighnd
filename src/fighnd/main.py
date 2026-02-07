'''Prototype of original image viewer

About osascript:
    https://www.macscripter.net/t/copy-image-contents-to-clipboard-please-save-me/34350
'''

import os
import sys
import subprocess
import asyncio
from pathlib import Path
from dataclasses import dataclass
from logging import getLogger

# from PIL import Image
# import pyperclip
import flet as ft  # type:ignore

logger = getLogger(__name__)

DIRECTORY = Path(os.getenv('DIR_FIGHND', ''))

ft.View


##
# class TopViewMock(ft.View):
#     '''Top page view of the application.'''

#     ROUTE = '/'

#     def __init__(self, controls=None, **kwargs) -> None:
#         data = "Top data"
#         controls = [
#             ft.AppBar(title=ft.Text("Top view"), bgcolor=ft.colors.SURFACE_VARIANT),
#             ft.TextField(value=data),
#             ft.ElevatedButton("Go to View1"),
#         ]
#         super().__init__("/", controls=controls, **kwargs)
#         self.data = data


class TopView(ft.View):
    '''Top page view of the application.'''

    ROUTE = '/'

    def __init__(self, controls=None, **kwargs) -> None:
        # self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        # self.save_file_dialog = ft.FilePicker(on_result=self.save_file_result)
        self.selected_files = ft.Text()
        self.save_file_path = ft.Text()

        button_upload = ft.ElevatedButton(
            "Add a new image",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=self.handle_pick_files,
        )
        button_save = ft.ElevatedButton(
            "Save file",
            icon=ft.Icons.SAVE,
            on_click=lambda _: self.save_file_dialog.save_file(),
            # disabled=page.web,
        )

        # Image gallary
        images = ft.Row(
            width=1200,
            wrap=True,
            scroll="always",
            alignment=ft.MainAxisAlignment.CENTER,
        )
        iterator_files = DIRECTORY.iterdir()
        image_button = ImageSumnailButton(width=200, height=200)
        for f in iterator_files:
            logger.info(f)
            logger.info(f'{type(f)}')
            images.controls.append(image_button.get(f))

        if controls is None:
            controls = [
                ft.AppBar(
                    title=ft.Text("TopView"), bgcolor=ft.Colors.ON_SURFACE_VARIANT
                ),
                ft.Row([button_upload, self.selected_files]),
                ft.Row([button_save, self.save_file_path]),
                ft.Column(
                    width=1200,
                    height=300,
                    controls=[images],
                    scroll='always',
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
        super().__init__(route=self.ROUTE, controls=controls, **kwargs)

    def handle_pick_files(self, e: ft.Event[ft.Button]) -> None:
        '''Pick files.'''
        files = ft.FilePicker().pick_files(allow_multiple=True)
        if not files:
            return

        self.selected_files.value = ", ".join([f.path for f in files])
        self.save_file_path.update()

    def pick_files_result(self, e: ft.Event):
        '''Pick files dialog

        Note:
            DEPRECATED
        '''

        if not e.files:
            return

        self.selected_files.value = ", ".join([f.path for f in e.files])
        self.selected_files.update()

    def handle_save_file(self, e: ft.Event[ft.Button]) -> None:
        '''Save file.'''
        self.save_file_path.value = ft.FilePicker().save_file()
        # e.path if e.path else "Cancelled!"
        self.save_file_path.update()

    def save_file_result(self, e: ft.Event):
        '''Save file dialog

        Note:
            DEPRECATED
        '''

        self.save_file_path.value = e.path if e.path else "Cancelled!"
        self.save_file_path.update()


class ImageSumnailButton:
    '''Image sumanil button component.'''

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def get(self, fname: Path) -> ft.Stack:
        '''Create button.'''
        open_dialog = OpenImageDialog(fname)
        img = ft.Image(
            src=str(fname.absolute()),
            width=self.width,
            height=self.height,
            fit=ft.BoxFit.NONE,
            repeat=ft.ImageRepeat.REPEAT,
            border_radius=ft.border_radius.all(10),
        )
        button = ft.ElevatedButton(
            content='',
            # content=img,
            on_click=open_dialog,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                },
                overlay_color={
                    ft.ControlState.PRESSED: ft.Colors.BLUE_300,
                    ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                },
                shape=ft.RoundedRectangleBorder(radius=1),
                elevation=0,
            ),
            width=self.width,
            height=self.height,
            opacity=0.5,
        )
        return ft.Stack([img, button])


@dataclass
class DataContainer:
    path_image: Path
    filename: str
    explanation: str
    citation: str
    tags: list[str]


class MainImageButton:
    '''Main image button component.'''

    imageviewer = {
        'linux': 'xdg-open',
        'wind32': 'explorer',
        'darwin': 'open',
    }[sys.platform]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def get(self, data: DataContainer) -> ft.Stack:
        '''Create button.'''
        # open_dialog = OpenImageDialog(fname)
        img = ft.Image(
            src=str(data.path_image.absolute()),
            width=self.width,
            height=self.height,
            fit=ft.BoxFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
        )
        button = ft.ElevatedButton(
            content='',
            # content=img,
            on_click=lambda _: self.pbcopy(data.path_image),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                },
                overlay_color={
                    ft.ControlState.PRESSED: ft.Colors.BLUE_300,
                    ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                },
                shape=ft.RoundedRectangleBorder(radius=1),
                elevation=0,
            ),
            width=self.width,
            height=self.height,
            opacity=0.5,
        )
        return ft.Stack([img, button])

    def open_image(self, path: Path) -> None:
        '''Open image with a default viewr.'''
        subprocess.Popen([self.imageviewer, path])

    def pbcopy(self, path: Path) -> None:
        # image = Image.open(path)
        # # num_byteio = io.BytesIO()
        # # num_byteio.save(image, 'jpeg')
        # # pyperclip.copy(num_byteio.getvalue())
        # data = image.tobytes("jpeg")
        # pyperclip.copy(data)
        # # txt = str(path.absolute())
        # # subprocess.Popen(['pbcopy', '<', txt])
        # # task = subprocess.Popen(['pbcopy', '<', txt], close_fds=True)
        # # task.communicate(input=txt.encode('utf-8'))
        subprocess.Popen(['picclip', path])


class OpenImageDialog:
    '''Class to open dialog, with holding image information.'''

    def __init__(self, fname: Path) -> None:
        self.fname = fname
        self.imagedata = DataContainer(
            path_image=fname.absolute(),
            filename=fname.name,
            explanation='This is explanation',
            citation='Citation',
            tags=['tagA', 'tagB'],
        )

    def __call__(self, e: ft.ControlEvent) -> None:
        '''Open dialog.'''
        e.page.views[-1].data = self.imagedata
        e.page.go('/image')


class ImageView(ft.View):
    '''Viewer of images'''

    ROUTE = '/image'

    def __init__(
        self, controls=None, data: DataContainer | None = None, **kwargs
    ) -> None:
        width, height = 600, 500
        if controls is None:
            assert isinstance(data, DataContainer)
            main_image = MainImageButton(width, height)
            controls = [
                ft.AppBar(
                    title=ft.Text(data.filename),
                    bgcolor=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Row(
                    controls=[main_image.get(data)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    # scroll="always",
                    # wrap=True,
                ),
                ft.Text(data.explanation),
                ft.Text(data.citation),
                ft.Text('; '.join(data.tags)),
            ]
        super().__init__(
            route=self.ROUTE, controls=controls, scroll=ft.ScrollMode.ALWAYS, **kwargs
        )
        self.data = data


def route_change(e: ft.RouteChangeEvent) -> None:
    '''Route_change function'''

    logger.info('Here route_change')

    if e.page.route == '/' and e.page.views:
        logger.info('Not Pass: Routing to route')
        return

    if e.page.route == '/':
        logger.info('Pass: Routing to route')
        e.page.views.clear()
        topview = TopView()
        # hide all dialogs in overlay
        # e.page.overlay.extend(
        #     [
        #         topview.pick_files_dialog,
        #         topview.save_file_dialog,
        #     ]
        # )
        e.page.views.append(topview)

    if e.page.route == '/image':
        data = e.page.views[-1].data
        e.page.views.append(ImageView(data=data))
        # e.page.add(ImageView(data=data))

    e.page.update()


def _main(page: ft.Page):
    page.title = 'Image Viewer'
    # # page.window_bgcolor = ft.colors.TRANSPARENT
    # # page.bgcolor = ft.colors.TRANSPARENT

    def route_change() -> None:
        '''Route_change function'''

        logger.info('Here route_change')
        # page.views.clear()

        # logger.info(f'views {page.views}')
        # if page.route == '/' and page.views:
        #     logger.info('Not Pass: Routing to route')
        #     return

        if page.route == '/':
            logger.info('Pass: Routing to route')
            page.views.clear()
            topview = TopView()
            # hide all dialogs in overlay
            # page.overlay.extend(
            #     [
            #         topview.pick_files_dialog,
            #         topview.save_file_dialog,
            #     ]
            # )
            page.views.append(topview)

        if page.route == '/image':
            data = page.views[-1].data
            page.views.append(ImageView(data=data))
            # page.add(ImageView(data=data))

        page.update()

    def view_pop(e: ft.ViewPopEvent) -> None:
        '''View pop function'''
        page.views.pop()
        previous = page.views[-1]
        page.go(previous.route, skip_route_change_event=True)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    # page.views.clear()
    logger.info('Pass: main views clear')
    # page.go('/')
    # topview = TopView()
    # page.add(topview)
    # page.add(ft.Text(f"Initial route: {page.route}"))
    # page.update()
    route_change()


@ft.observable
@dataclass
class Route:
    route: str

    def route_change(self, e: ft.RouteChangeEvent):
        logger.info("Route changed from: %s to: %s", self.route, e.route)
        self.route = e.route

    async def view_popped(self, e: ft.ViewPopEvent):
        logger.info("View popped")
        views = ft.unwrap_component(ft.context.page.views)
        if len(views) > 1:
            await ft.context.page.push_route(views[-2].route)


@ft.component
def app() -> list[ft.View]:
    '''Main UI of application.'''

    route, _ = ft.use_state(Route(route=ft.context.page.route))

    # subscribe to page events as soon as possible
    ft.context.page.on_route_change = route.route_change
    ft.context.page.on_view_pop = route.view_popped

    logger.info('Pass: main views clear')
    # topview = TopView()
    # page.add(topview)
    # page.add(ft.Text(f"Initial route: {page.route}"))

    views = [
        ft.View(
            route='/',
            controls=[
                ft.Button(
                    'Visit',
                    on_click=lambda _: asyncio.create_task(
                        ft.context.page.push_route('/fig')
                    ),
                )
            ],
        )
    ]
    if route.route == '/fig':
        views += [
            ft.View(
                route='/fig',
                controls=[
                    ft.Button(
                        'Figure',
                        on_click=lambda _: asyncio.create_task(
                            ft.context.page.push_route('/')
                        ),
                    )
                ],
            )
        ]
    return views


def main(page: ft.Page):
    page.title = 'Image Viewer'
    page.render_views(app)


def launch() -> None:
    '''Access point.'''
    # ft.app(target=main)
    from sugayutils.log import mylogconfig

    mylogconfig()

    ft.run(main)


if __name__ == '__main__':
    launch()
