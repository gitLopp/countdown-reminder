from PIL import Image, ImageDraw

def create_clock_icon(size):
    # 创建一个新的图像，使用RGBA模式支持透明度
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 计算缩放比例
    scale = size / 128
    center = size // 2
    
    # 绘制闹钟主体（浅蓝色圆形）
    light_blue = (135, 206, 235)  # 天蓝色
    radius = int(45 * scale)
    draw.ellipse([center-radius, center-radius+int(8*scale), 
                  center+radius, center+radius+int(8*scale)], 
                 fill=light_blue)
    
    # 绘制顶部铃铛（金色）
    gold = (255, 215, 0)  # 金色
    bell_width = int(20 * scale)
    bell_height = int(16 * scale)
    bell_top = center - radius - int(4 * scale)
    
    # 左边的铃铛
    draw.ellipse([center-bell_width-int(12*scale), bell_top, 
                  center-int(12*scale), bell_top+bell_height], 
                 fill=gold)
    
    # 右边的铃铛
    draw.ellipse([center+int(12*scale), bell_top, 
                  center+bell_width+int(12*scale), bell_top+bell_height], 
                 fill=gold)
    
    # 铃铛连接处
    draw.rectangle([center-int(14*scale), bell_top, 
                   center+int(14*scale), bell_top+int(8*scale)], 
                  fill=gold)
    
    # 绘制时针（垂直线）
    dark_blue = (0, 0, 139)  # 深蓝色
    hour_length = int(20 * scale)
    line_width = max(1, int(6 * scale))
    draw.line([center, center+int(8*scale), 
               center, center-hour_length+int(8*scale)], 
              fill=dark_blue, width=line_width)
    
    # 绘制分针（水平线）
    minute_length = int(24 * scale)
    draw.line([center, center+int(8*scale), 
               center+minute_length, center+int(8*scale)], 
              fill=dark_blue, width=line_width)
    
    # 绘制支脚
    foot_color = (160, 160, 160)  # 灰色
    foot_width = int(8 * scale)
    foot_height = int(10 * scale)
    draw.ellipse([center-radius+int(10*scale), center+radius+int(4*scale), 
                  center-radius+foot_width+int(10*scale), center+radius+foot_height+int(4*scale)], 
                 fill=foot_color)
    draw.ellipse([center+radius-foot_width-int(10*scale), center+radius+int(4*scale), 
                  center+radius-int(10*scale), center+radius+foot_height+int(4*scale)], 
                 fill=foot_color)
    
    # 绘制中心点
    center_dot_radius = max(1, int(3 * scale))
    draw.ellipse([center-center_dot_radius, center-center_dot_radius+int(8*scale), 
                  center+center_dot_radius, center+center_dot_radius+int(8*scale)], 
                 fill=dark_blue)
    
    return image

# 生成不同尺寸的图标
sizes = [16, 32, 48, 128]
for size in sizes:
    icon = create_clock_icon(size)
    icon.save(f'icons/icon{size}.png')
    print(f'Generated icon{size}.png') 