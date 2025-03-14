import os
from PIL import Image, ImageDraw

# 确保icons目录存在
if not os.path.exists('icons'):
    os.makedirs('icons')

def create_hourglass_icon(size):
    # 创建新图像，使用RGBA模式支持透明度
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 计算缩放比例
    scale = size / 128
    stroke_width = max(int(8 * scale), 1)  # 增加线条粗细
    
    # 计算中心点和半径
    center = size // 2
    radius = int(64 * scale)  # 增加整体尺寸到最大
    
    # 绘制渐变背景圆形（通过多个同心圆实现简单渐变效果）
    colors = ['#E8F5E9', '#C8E6C9', '#A5D6A7']
    ratios = [1.0, 0.85, 0.7]
    for color, ratio in zip(colors, ratios):
        r = int(radius * ratio)
        draw.ellipse([
            center - r,
            center - r,
            center + r,
            center + r
        ], fill=color)
    
    # 计算沙漏的点（使用更圆润的轮廓，增加尺寸）
    top_width = 56 * scale  # 增加宽度
    bottom_width = 56 * scale
    top_y = 24 * scale  # 调整位置
    bottom_y = 104 * scale
    mid_y = 64 * scale
    
    points = [
        (center - top_width/2, top_y),     # 左上
        (center + top_width/2, top_y),     # 右上
        (center + 8 * scale, mid_y),       # 右中
        (center + bottom_width/2, bottom_y),# 右下
        (center - bottom_width/2, bottom_y),# 左下
        (center - 8 * scale, mid_y),       # 左中
    ]
    
    # 绘制沙漏外框（带渐变填充效果）
    draw.polygon(points, fill='white')
    
    # 绘制边框
    draw.line(points + [points[0]], fill='#43A047', width=stroke_width, joint='curve')
    
    # 绘制装饰性横线
    line_gradient = ['#66BB6A', '#43A047', '#2E7D32']
    for i, color in enumerate(line_gradient):
        y_offset = i * stroke_width/3
        # 上横线
        draw.line([
            (center - top_width/2 - 12*scale, top_y + y_offset),
            (center + top_width/2 + 12*scale, top_y + y_offset)
        ], fill=color, width=stroke_width-i)
        # 下横线
        draw.line([
            (center - bottom_width/2 - 12*scale, bottom_y + y_offset),
            (center + bottom_width/2 + 12*scale, bottom_y + y_offset)
        ], fill=color, width=stroke_width-i)
    
    # 绘制沙子（带阴影效果）
    sand_height = 20 * scale  # 增加沙子高度
    sand_width = 24 * scale   # 增加沙子宽度
    
    # 上部沙子（较大）
    upper_sand = [
        (center - sand_width/2, top_y + 12*scale),
        (center + sand_width/2, top_y + 12*scale),
        (center, top_y + 24*scale)
    ]
    draw.polygon(upper_sand, fill='#66BB6A')
    
    # 下部沙子（更大，带堆积效果）
    lower_sand = [
        (center - sand_width/1.5, bottom_y - sand_height),
        (center + sand_width/1.5, bottom_y - sand_height),
        (center + sand_width, bottom_y - sand_height/2),
        (center, bottom_y - 8*scale),
        (center - sand_width, bottom_y - sand_height/2)
    ]
    draw.polygon(lower_sand, fill='#43A047')
    
    # 绘制沙漏中间的细沙流动效果
    draw.line([
        (center, mid_y - 12*scale),
        (center, mid_y + 12*scale)
    ], fill='#66BB6A', width=max(int(3 * scale), 1))
    
    return img

# 生成不同尺寸的图标
sizes = [16, 32, 48, 128]
for size in sizes:
    icon = create_hourglass_icon(size)
    icon.save(f'icons/icon{size}.png')

print("图标生成完成！") 