import os
import subprocess

def convert_svg_to_png(svg_path, output_path, size):
    """使用 Inkscape 将 SVG 转换为 PNG"""
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 使用 sips 命令转换（macOS 自带工具）
        # 首先创建一个临时的 PNG 文件
        temp_png = 'icons/temp_icon.png'
        subprocess.run([
            'sips',
            '-s', 'format', 'png',
            svg_path,
            '--out', temp_png
        ], check=True)
        
        # 然后调整大小
        subprocess.run([
            'sips',
            '-z', str(size), str(size),
            temp_png,
            '--out', output_path
        ], check=True)
        
        # 删除临时文件
        os.remove(temp_png)
        
        print(f'Successfully created icon: {output_path}')
    except subprocess.CalledProcessError as e:
        print(f'Error converting SVG: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')

if __name__ == '__main__':
    # 输入和输出路径
    svg_path = 'icons/icon.svg'
    output_path = 'store-assets/store_icon_300x300.png'
    
    # 转换为 300x300 的图标
    convert_svg_to_png(svg_path, output_path, 300) 