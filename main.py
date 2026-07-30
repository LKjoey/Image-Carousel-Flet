
import flet

from ui.Image_Slider import ImageSlider

def main(page:flet.Page):
    page.bgcolor = "white"
    page.title = "Image Slider"
    page.padding = 0
    page.horizontal_alignment = flet.MainAxisAlignment.CENTER
    page.vertical_alignment = flet.CrossAxisAlignment.CENTER

    page.add(
        ImageSlider([
            flet.Image("1.png", aspect_ratio=16/9, fit=flet.BoxFit.COVER),
            flet.Image("2.png", aspect_ratio=16/9, fit=flet.BoxFit.COVER),
            flet.Image("3.png", aspect_ratio=16/9, fit=flet.BoxFit.COVER),
            flet.Image("4.png", aspect_ratio=16/9, fit=flet.BoxFit.COVER)
        ])
    )


if __name__ == '__main__':
    flet.run(main, assets_dir="assets")