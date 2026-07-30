
import flet

class ImageSlider(flet.Container):
    """
    图片轮播组件
    功能：显示多张图片，底部有指示按钮，点击按钮切换图片
    """

    def __init__(self, images=list[flet.Image]):
        """
        初始化图片轮播组件

        参数:
            images: flet.Image 对象列表，即要显示的图片列表
        """
        super().__init__()          # 调用父类 flet.Container 的初始化方法
        self.images = images        # 保存图片列表到实例变量，供其他方法使用
        self.width = 768            # 设置轮播组件的宽度
        self.border_radius = 8      # 设置圆角大小
        self.shadow = flet.BoxShadow(0, 20, "black")    # 添加阴影效果

        # 创建底部指示按钮（小圆点）
        self.buttons = self._create_buttons()

        # 创建动画切换器，用于图片切换时的过渡动画
        # 初始显示第一张图片，切换动画持续 500 毫秒
        self.switcher = flet.AnimatedSwitcher(
            images[0],              # 默认显示第一张图片
            duration=500,           # 切换动画持续时间（毫秒）
            reverse_duration=500    # 反向切换动画持续时间（毫秒）
        )

        # 使用 Stack（堆叠布局）将图片和按钮叠加在一起
        # 图片在底层，按钮在顶层（因为后添加的在上层）
        self.content = flet.Stack([
            self.switcher,  # 图片切换器（底层）
            # 按钮行：水平排列，底部距离24像素，居中对齐
            flet.Row(self.buttons, bottom=24, alignment=flet.MainAxisAlignment.CENTER)
        ], alignment=flet.Alignment.CENTER)  # 所有子控件整体居中对齐

    def did_mount(self):
        """
        组件挂载到页面后自动调用的方法
        当 ImageSlider 被添加到页面时，自动显示第一张图片并高亮第一个按钮
        """
        self.set_current(0)  # 默认选中索引0（第一张图片）

    def set_current(self, index: int):
        """
        切换到指定索引的图片

        参数:
            index: 要显示的图片索引（从 0 开始）
        """
        # 遍历所有按钮，更新它们的透明度
        for i, button in enumerate(self.buttons):
            # 如果当前按钮的索引等于要显示的图片索引，设为不透明（高亮）
            # 否则设为半透明（未选中状态）
            button.opacity = 1 if i == index else 0.5
            button.update()  # 立即刷新这个按钮，使透明度变化生效

        # 更新切换器的内容为指定索引的图片
        self.switcher.content = self.images[index]
        self.switcher.update()  # 刷新切换器，触发切换动画

    def _create_buttons(self):
        """
        创建底部指示按钮（小圆点）

        返回:
            包含所有按钮的列表
        """
        return [
            # 为每张图片创建一个圆形按钮
            flet.Container(
                width=20,   # 按钮宽度
                height=20,  # 按钮高度
                border_radius=360,   # 圆角半径360度 → 正圆形
                bgcolor="white",     # 背景颜色为白色
                margin=flet.Margin.only(right=15),
                opacity=0.5,         # 初始透明度50%（半透明，未选中状态）
                data=index,          # 存储索引值，用于点击时识别是第几个按钮
                on_click=self._on_button_click  # 点击事件处理函数
            )
            for index in range(len(self.images))  # 遍历图片列表，为每张图片创建一个按钮
        ]

    def _on_button_click(self, e: flet.ControlEvent):
        """
        按钮点击事件处理函数

        参数:
            e: 事件对象，包含触发事件的控件信息
        """
        # e.control 是被点击的按钮控件
        # e.control.data 是按钮创建时存储的索引值（在 _create_buttons 中设置）
        # 调用 set_current 方法切换到对应的图片
        self.set_current(e.control.data)