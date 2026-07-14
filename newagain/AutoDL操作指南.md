# AutoDL 操作指南

> 整合自：AutoDL无卡模式操作指南、下载实验结果指南

---

## 一、无卡模式下载结果

### 1. 切换到无卡模式

1. 登录 AutoDL 控制台
2. 点击实例的「更多」→「无卡模式开机」
3. 等待实例启动（约1-2分钟）
4. 无卡模式费用极低（约 ¥0.1/时）

### 2. 连接实例

使用 MobaXterm 或终端：
```
主机: connect-web.gpuhub.com
端口: 见控制台
用户: root
```

### 3. 定位实验结果

```bash
# 消融实验结果
ls -lh /root/autodl-tmp/YOLOv11/ultralytics-main/runs/ablation/

# 对比实验结果
ls -lh /root/autodl-tmp/YOLOv11/ultralytics-main/runs/train/
```

### 4. 打包结果

```bash
cd /root/autodl-tmp/YOLOv11/ultralytics-main

# 打包消融实验结果
tar -czf ablation_results.tar.gz runs/ablation/

# 打包对比实验结果
tar -czf comparison_results.tar.gz runs/train/

# 打包所有结果
tar -czf all_results.tar.gz runs/
```

### 5. 下载到本地

**方法1：MobaXterm 拖拽下载**
1. 在左侧文件浏览器中定位到打包文件
2. 右键 → Download

**方法2：SCP 命令下载**
```bash
# 在本地终端执行
scp root@<服务器IP>:/root/autodl-tmp/YOLOv11/ultralytics-main/ablation_results.tar.gz ./
```

### 6. 本地解压与查看

```bash
# 解压
tar -xzf ablation_results.tar.gz

# 查看结果CSV
python -c "
import pandas as pd
df = pd.read_csv('runs/ablation/arconv_neck/results.csv')
print(df.tail())
"
```

---

## 二、需要下载的关键文件清单

| 文件 | 路径 | 说明 |
|------|------|------|
| best.pt | runs/ablation/*/weights/best.pt | 最佳模型权重 |
| last.pt | runs/ablation/*/weights/last.pt | 最后epoch权重 |
| results.csv | runs/ablation/*/results.csv | 训练指标数据 |
| results.png | runs/ablation/*/results.png | 训练曲线图 |
| data.yaml | /root/autodl-tmp/domestic_dataset/data.yaml | 数据集配置 |

---

## 三、本地文件组织建议

```
本地实验结果/
├── ablation/
│   ├── arconv_backbone/
│   ├── arconv_neck/
│   ├── arconv_head/
│   └── arconv_full/
├── comparison/
│   ├── yolov8n/
│   ├── yolo11n/
│   └── ...
└── analysis/
    └── summary/
```

---

## 四、费用说明

| 模式 | 费用 | 用途 |
|------|------|------|
| 有卡模式 | ¥2-3/时 | 训练实验 |
| 无卡模式 | ¥0.1/时 | 下载结果、检查文件 |
| 关机 | ¥0 | 不使用时 |

**建议**：训练完成后立即切无卡模式下载结果，然后关机。

---

## 五、注意事项

1. 无卡模式下不能运行GPU训练，只能操作文件
2. 确保实例处于运行状态才能连接
3. 下载前检查文件完整性（文件大小是否合理）
4. 大文件建议先压缩再下载，节省传输时间
5. 训练日志和配置文件也要下载，以备查证
