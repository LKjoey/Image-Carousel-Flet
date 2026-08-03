

import flet as ft

import asyncio

from typing import List

# 创建轮播组件
def create_carousel(page: ft.Page, images: List[str]) -> ft.Stack:
    image_width, image_height = 300, 200
    # 复制图片列表实现无缝循环
    # valid_images * 2 表示将列表复制一份
    # 例如：[图1, 图2, 图3] * 2 = [图1, 图2, 图3, 图1, 图2, 图3]
    # 这样当第1组图片移出时，第2组图片正好补上，实现无缝效果
    loop_images = images * 2

    row = ft.Row(spacing=0, left=0)
    # 添加图片到水平行中
    for path in loop_images:
        row.controls.append(ft.Image(
            src=path,
            width=image_width,
            height=image_height,
            fit=ft.BoxFit.CONTAIN
        ))

    # Stack 是层叠容器，可以叠加多个组件
    # 这里将 Row 放在 Stack 中，并限制显示区域
    # Stack 会自动裁剪超出部分，实现"窗口"效果
    # 只显示可见区域的内容，超出部分被隐藏
    stack = ft.Stack([row], width=page.width, height=image_height)

    total_width = image_width * len(images)

    async def scroll():
        speed = 10          # 每帧移动的像素数（值越大滚动越快）
        interval = 0.1      # 每帧间隔时间（秒），0.1秒约10帧/秒

        while True:
            row.left -= speed       # 每次向左移动 speed 像素
            # 判断是否该重置位置
            # 当 row 向左移动的距离超过一组图片的总宽度时
            # 说明第一组图片已经完全移出屏幕
            if row.left <= -total_width:
                row.left = 0        # 重置到起始位置
                # 因为第二组图片和第一组完全相同
                # 所以重置时画面不会闪烁或跳跃

            page.update()   # 更新页面显示
            await asyncio.sleep(interval)   # 等待 0.1 秒，控制动画速度

    # 启动滚动任务
    # asyncio.create_task 创建异步任务，让滚动循环在后台运行
    # 这样不会阻塞主线程，页面可以正常响应
    asyncio.create_task(scroll())
    return stack


def main(page: ft.Page):
    page.title = "滚动图片轮播"
    page.bgcolor = "white"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 图片列表
    images = [f'{i}.jpg' for i in range(1, 9)]
    stack = create_carousel(page,images)
    page.add(stack)


if __name__ == '__main__':
    ft.run(main, assets_dir="assets")