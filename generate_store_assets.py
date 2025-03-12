import os
import cairosvg
from PIL import Image, ImageDraw, ImageFont
import colorsys

def create_store_icon(size):
    """创建商店图标"""
    # 从 SVG 生成基础图标
    svg_path = 'icons/icon.svg'
    png_path = f'store-assets/store_icon_{size}x{size}.png'
    
    # 确保输出目录存在
    os.makedirs('store-assets', exist_ok=True)
    
    # 转换 SVG 到 PNG，保持透明度
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=size, output_height=size)
    
    # 打开生成的图片
    icon = Image.open(png_path)
    
    # 创建一个新的图片，使用渐变背景
    background = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(background)
    
    # 创建渐变背景
    for y in range(size):
        h = y / size  # 色相
        s = 0.8  # 饱和度
        v = 0.95  # 亮度
        r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(h, s, v)]
        draw.line([(0, y), (size, y)], fill=(r, g, b, 50))
    
    # 将图标粘贴到背景上
    background.paste(icon, (0, 0), icon)
    
    # 保存最终图片
    background.save(png_path, 'PNG')
    print(f'Created store icon: {png_path}')

def create_promotional_banner():
    """创建促销横幅"""
    width = 1400
    height = 560
    banner = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(banner)
    
    # 创建渐变背景
    for y in range(height):
        h = y / height  # 色相
        s = 0.3  # 饱和度
        v = 0.98  # 亮度
        r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(h, s, v)]
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 加载图标
    icon_size = 200
    cairosvg.svg2png(
        url='icons/icon.svg',
        write_to='store-assets/temp_icon.png',
        output_width=icon_size,
        output_height=icon_size
    )
    icon = Image.open('store-assets/temp_icon.png')
    
    # 在横幅上添加图标
    icon_x = (width - icon_size) // 2
    icon_y = (height - icon_size) // 2 - 50
    banner.paste(icon, (icon_x, icon_y), icon)
    
    # 添加文字
    try:
        font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 60)
    except:
        font = ImageFont.load_default()
    
    text = "事件倒计时提醒"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = icon_y + icon_size + 20
    
    draw.text((text_x, text_y), text, font=font, fill='#333333')
    
    # 保存横幅
    banner.save('store-assets/promotional_banner.png', 'PNG')
    print('Created promotional banner: store-assets/promotional_banner.png')
    
    # 清理临时文件
    os.remove('store-assets/temp_icon.png')

def main():
    # 创建商店图标（300x300 和 440x280）
    create_store_icon(300)
    
    # 创建促销横幅
    create_promotional_banner()

if __name__ == '__main__':
    main() 