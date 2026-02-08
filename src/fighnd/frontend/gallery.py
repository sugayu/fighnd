'''Base, gallery view front end.'''

import os
import asyncio
from logging import getLogger
from pathlib import Path
from dataclasses import dataclass

import flet as ft

from .share import selectedimage
from .. import backend

__all__ = [
    'galleryview',
]


logger = getLogger(__name__)

##
ROUTE = '/'


@ft.component
def galleryview() -> ft.View:
    controls = [functions(), gallery()]
    return ft.View(
        route=ROUTE,
        controls=controls,
        width=1200,
    )


@ft.component
def functions() -> ft.Control:
    '''Functional item list to manipulate the app and images.'''

    button_upload = ft.Button(
        "Add a new image",
        icon=ft.Icons.UPLOAD_FILE,
        # on_click=backend.handle_pick_files,
    )
    button_save = ft.Button(
        "Save file",
        icon=ft.Icons.SAVE,
        # on_click=lambda _: backend.save_file_dialog.save_file(),
        # disabled=page.web,
    )

    return ft.Row(controls=[button_upload, button_save])


@ft.component
def gallery() -> ft.Control:
    '''Main gallery.'''

    iterator_files = backend.get_imagepaths()
    controls = [sumnailbutton(f) for f in iterator_files]

    images = ft.Row(
        width=1200,
        wrap=True,
        scroll='always',
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5,
        run_spacing=5,
        controls=controls,
    )

    return ft.Column(
        # width=1200,
        height=400,
        controls=[images],
        scroll='always',
        alignment=ft.MainAxisAlignment.CENTER,
    )


@dataclass
class SumnailConfig:
    width: int
    height: int
    inner_ratio: float = 0.90

    def __post_init__(self) -> None:
        self.inner_width = self.width * 0.9
        self.inner_height = self.width * 0.9


SumnailConfigContext = ft.create_context(SumnailConfig(width=200, height=200))


@ft.component
def sumnailbutton(fname: Path) -> ft.Control:
    '''Image sumanil button component.'''

    config = ft.use_context(SumnailConfigContext)

    def _select_image():
        logger.info('change_page')
        selectedimage.data.set(fname)
        asyncio.create_task(ft.context.page.push_route('/fig'))

    # open_dialog = OpenImageDialog(fname)
    img = ft.Image(
        src=str(fname.absolute()),
        width=config.inner_width,
        height=config.inner_height,
        fit=ft.BoxFit.NONE,
        repeat=ft.ImageRepeat.REPEAT,
        border_radius=ft.BorderRadius.all(20),
    )
    button = ft.Button(
        content='',
        # content=img,
        # on_click=open_dialog,
        on_click=_select_image,
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
            },
            overlay_color={
                ft.ControlState.PRESSED: ft.Colors.BLUE_300,
                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
            },
            shape=ft.RoundedRectangleBorder(radius=20),
            elevation=0,
        ),
        width=config.inner_width,
        height=config.inner_height,
        opacity=0.3,
    )
    stack = ft.Stack(
        [img, button],
        alignment=ft.Alignment.CENTER,
    )
    return ft.Card(
        content=stack,
        shadow_color=ft.Colors.GREY_600,
        bgcolor=ft.Colors.GREY_300,
        width=config.width,
        height=config.height,
        shape=ft.RoundedRectangleBorder(radius=20),
    )


# class TopView(ft.View):
#     '''Top page view of the application.'''

#     ROUTE = '/'

#     def __init__(self, controls=None, **kwargs) -> None:
#         # self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
#         # self.save_file_dialog = ft.FilePicker(on_result=self.save_file_result)
#         self.selected_files = ft.Text()
#         self.save_file_path = ft.Text()

#         # Image gallary

#         if controls is None:
#             controls = [
#                 ft.AppBar(
#                     title=ft.Text("TopView"), bgcolor=ft.Colors.ON_SURFACE_VARIANT
#                 ),
#                 ft.Row([button_upload, self.selected_files]),
#                 ft.Row([button_save, self.save_file_path]),
#             ]
#         super().__init__(route=self.ROUTE, controls=controls, **kwargs)

#     def handle_pick_files(self, e: ft.Event[ft.Button]) -> None:
#         '''Pick files.'''
#         files = ft.FilePicker().pick_files(allow_multiple=True)
#         if not files:
#             return

#         self.selected_files.value = ", ".join([f.path for f in files])
#         self.save_file_path.update()

#     def pick_files_result(self, e: ft.Event):
#         '''Pick files dialog

#         Note:
#             DEPRECATED
#         '''

#         if not e.files:
#             return

#         self.selected_files.value = ", ".join([f.path for f in e.files])
#         self.selected_files.update()

#     def handle_save_file(self, e: ft.Event[ft.Button]) -> None:
#         '''Save file.'''
#         self.save_file_path.value = ft.FilePicker().save_file()
#         # e.path if e.path else "Cancelled!"
#         self.save_file_path.update()

#     def save_file_result(self, e: ft.Event):
#         '''Save file dialog

#         Note:
#             DEPRECATED
#         '''

#         self.save_file_path.value = e.path if e.path else "Cancelled!"
#         self.save_file_path.update()
