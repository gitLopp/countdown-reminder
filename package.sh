#!/bin/bash

# 创建临时打包目录
mkdir -p temp_package

# 复制必要文件
cp -r _locales temp_package/
cp -r icons temp_package/
cp manifest.json temp_package/
cp popup.html temp_package/
cp popup.js temp_package/
cp background.js temp_package/
cp styles.css temp_package/

# 创建 store-assets 目录（用于存储商店资源）
mkdir -p store-assets

# 进入临时目录
cd temp_package

# 创建 ZIP 包
zip -r ../store-assets/extension.zip *

# 返回上级目录
cd ..

# 清理临时目录
rm -rf temp_package

echo "打包完成！扩展包已保存到 store-assets/extension.zip" 