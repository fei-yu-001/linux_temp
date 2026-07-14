@echo off
REM 打包ARConv消融实验文件用于上传到服务器
REM 使用方法：双击运行此脚本

echo ========================================
echo 正在打包ARConv消融实验文件...
echo ========================================

REM 创建临时目录
if exist arconv_upload rmdir /s /q arconv_upload
mkdir arconv_upload
cd arconv_upload

REM 创建目录结构
mkdir ultralytics\nn\modules
mkdir ultralytics\cfg\models\11

REM 复制核心文件
echo 复制 conv.py...
copy ..\ultralytics\nn\modules\conv.py ultralytics\nn\modules\ >nul

echo 复制 __init__.py...
copy ..\ultralytics\nn\modules\__init__.py ultralytics\nn\modules\ >nul

REM 复制配置文件（4个）
echo 复制配置文件...
copy ..\ultralytics\cfg\models\11\yolo11n_arconv_backbone.yaml ultralytics\cfg\models\11\ >nul
copy ..\ultralytics\cfg\models\11\yolo11n_arconv_neck.yaml ultralytics\cfg\models\11\ >nul
copy ..\ultralytics\cfg\models\11\yolo11n_arconv_head.yaml ultralytics\cfg\models\11\ >nul
copy ..\ultralytics\cfg\models\11\yolo11n_arconv_full.yaml ultralytics\cfg\models\11\ >nul

REM 复制训练脚本
echo 复制训练脚本...
copy ..\arconv_callback.py . >nul
copy ..\run_arconv_ablation_experiments.py . >nul
copy ..\analyze_arconv_ablation.py . >nul

REM 复制部署指南
echo 复制部署指南...
copy ..\README_ARCONV_UPLOAD.md README.md >nul
copy ..\QUICK_START.md . >nul
copy ..\SERVER_DEPLOYMENT_CHECKLIST.md . >nul
copy ..\FINAL_ABLATION_GUIDE.md . >nul
copy ..\deploy_on_server.sh . >nul

cd ..

echo.
echo ========================================
echo ✅ 打包完成！
echo ========================================
echo.
echo 文件已打包到: arconv_upload 文件夹
echo.
echo 包含文件:
echo   - ultralytics/nn/modules/conv.py
echo   - ultralytics/nn/modules/__init__.py
echo   - ultralytics/cfg/models/11/yolo11n_arconv_backbone.yaml
echo   - ultralytics/cfg/models/11/yolo11n_arconv_neck.yaml
echo   - ultralytics/cfg/models/11/yolo11n_arconv_head.yaml
echo   - ultralytics/cfg/models/11/yolo11n_arconv_full.yaml
echo   - arconv_callback.py
echo   - run_arconv_ablation_experiments.py  (主脚本)
echo   - analyze_arconv_ablation.py          (分析脚本)
echo   - README.md                           (部署包说明)
echo   - QUICK_START.md                      (快速开始)
echo   - SERVER_DEPLOYMENT_CHECKLIST.md      (部署检查清单)
echo   - FINAL_ABLATION_GUIDE.md             (实验指南)
echo   - deploy_on_server.sh                 (服务器部署脚本)
echo.
echo 实验方案:
echo   1. Backbone替换 (5层Backbone Conv)
echo   2. Neck替换 (2层Neck Conv)
echo   3. Head替换 (2层Head Conv)
echo   4. 全部替换 (Backbone + Neck + Head)
echo.
echo 下一步：
echo 1. 使用MobaXterm连接到服务器
echo 2. 将 arconv_upload 文件夹拖拽到服务器的 /root/autodl-tmp/YOLOv11/ 目录
echo 3. 在服务器上运行部署脚本:
echo    cd /root/autodl-tmp/YOLOv11/arconv_upload
echo    bash deploy_on_server.sh
echo 4. 开始训练:
echo    cd /root/autodl-tmp/YOLOv11/ultralytics-main
echo    python run_arconv_ablation_experiments.py
echo 5. 训练完成后分析结果:
echo    python analyze_arconv_ablation.py
echo.
echo 预计总时间: 约4.8小时
echo 预计总成本: 约¥10
echo.
pause
