@echo off
setlocal enabledelayedexpansion
REM 打包完整的ultralytics-main文件夹用于上传到服务器
REM 排除：runs/, *.pt, __pycache__, .git/, *.pyc
REM 使用方法：双击运行此脚本

echo ========================================
echo 正在打包完整的ultralytics-main文件夹...
echo ========================================
echo.

REM 检查是否安装了7-Zip
set SEVENZIP="C:\Program Files\7-Zip\7z.exe"
if not exist %SEVENZIP% (
    set SEVENZIP="C:\Program Files (x86)\7-Zip\7z.exe"
)

if not exist %SEVENZIP% (
    echo ❌ 错误：未找到7-Zip！
    echo.
    echo 请先安装7-Zip：
    echo 下载地址：https://www.7-zip.org/
    echo.
    echo 或者手动压缩ultralytics-main文件夹，排除以下内容：
    echo   - runs/
    echo   - *.pt
    echo   - __pycache__/
    echo   - .git/
    echo   - *.pyc
    echo.
    pause
    exit /b 1
)

echo ✅ 找到7-Zip: %SEVENZIP%
echo.

REM 创建排除列表文件
echo runs\> exclude_list.txt
echo .git\>> exclude_list.txt
echo __pycache__\>> exclude_list.txt
echo *.pt>> exclude_list.txt
echo *.pyc>> exclude_list.txt

echo 开始压缩...
echo 输出文件: ultralytics-main-complete.zip
echo.
echo 排除内容:
echo   - runs/
echo   - *.pt
echo   - __pycache__/
echo   - .git/
echo   - *.pyc
echo.

REM 压缩文件（使用排除列表文件）
cd ..
%SEVENZIP% a -tzip ultralytics-main-complete.zip ultralytics-main\ -x@ultralytics-main\exclude_list.txt
set RESULT=%ERRORLEVEL%
cd ultralytics-main

REM 删除临时排除列表
del exclude_list.txt

if %RESULT% EQU 0 (
    echo.
    echo ========================================
    echo ✅ 压缩完成！
    echo ========================================
    echo.
    
    REM 显示文件大小
    cd ..
    for %%A in (ultralytics-main-complete.zip) do (
        set /A SIZE_MB=%%~zA/1024/1024
    )
    cd ultralytics-main
    
    echo 文件名: ultralytics-main-complete.zip
    echo 文件大小: !SIZE_MB! MB
    echo 位置: 上级目录
    echo.
    
    echo 包含内容:
    echo   ✅ ultralytics/nn/modules/conv.py          (ARConv实现)
    echo   ✅ ultralytics/nn/modules/__init__.py      (模块注册)
    echo   ✅ ultralytics/cfg/models/11/*.yaml        (配置文件)
    echo   ✅ arconv_callback.py                      (训练回调)
    echo   ✅ run_arconv_ablation_experiments.py      (主脚本)
    echo   ✅ analyze_arconv_ablation.py              (分析脚本)
    echo   ✅ 所有其他必要文件
    echo.
    
    echo 排除内容:
    echo   ❌ runs/                                   (训练结果)
    echo   ❌ *.pt                                    (权重文件)
    echo   ❌ __pycache__/                            (Python缓存)
    echo   ❌ .git/                                   (Git仓库)
    echo.
    
    echo ========================================
    echo 📤 下一步：上传到服务器
    echo ========================================
    echo.
    echo 1. 使用MobaXterm连接到服务器:
    echo    主机: connect-web.gpuhub.com
    echo    端口: 20086
    echo    用户: root
    echo.
    echo 2. 将上级目录的 ultralytics-main-complete.zip 拖拽到服务器:
    echo    /root/autodl-tmp/YOLOv11/
    echo.
    echo 3. 在服务器上解压:
    echo    cd /root/autodl-tmp/YOLOv11/
    echo    mv ultralytics-main ultralytics-main-backup
    echo    unzip ultralytics-main-complete.zip
    echo.
    echo 4. 开始训练:
    echo    cd ultralytics-main
    echo    python run_arconv_ablation_experiments.py
    echo.
    echo 预计上传时间: 5-10分钟 (取决于网速)
    echo 预计训练时间: 4.0小时
    echo 预计总成本: 约¥8.5
    echo.
    
) else (
    echo.
    echo ========================================
    echo ❌ 压缩失败！
    echo ========================================
    echo.
    echo 错误代码: %RESULT%
    echo.
    echo 请尝试手动压缩ultralytics-main文件夹
    echo.
)

pause
