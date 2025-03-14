import os
import cairosvg
from PIL import Image, ImageDraw
import colorsys

def create_store_icon(size=300):
    """创建商店图标，默认尺寸为 300x300 像素"""
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

if __name__ == '__main__':
    # 创建 300x300 的图标
    create_store_icon(300)
    # 额外创建一个更大尺寸的图标以备用
    create_store_icon(440) 