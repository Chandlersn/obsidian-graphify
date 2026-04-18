# 常见问题解答 (FAQ)

## 安装问题

### Q: Python 脚本执行报错？

**错误信息**: `ModuleNotFoundError: No module named 'watchdog'`

**解决方法**:

```bash
pip install watchdog
```

***

### Q: install.sh 权限问题？

**错误信息**: `Permission denied`

**解决方法**:

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

***

### Q: Windows 上运行 .sh 脚本？

**解决方法**: 使用 Git Bash 或手动安装：

```powershell
# PowerShell 手动安装
pip install watchdog
Copy-Item -Recurse src\.graphify D:\obsidian-notes\
```

***

## 图谱显示问题

### Q: 图谱没有显示节点？

**可能原因**:

1. Vault 路径配置错误
2. 没有笔记文件
3. 数据生成脚本未执行

**解决方法**:

```bash
# 1. 检查路径
cat .graphify/config.yaml

# 2. 确保有笔记
ls /your/vault/*.md

# 3. 手动执行更新
python .graphify/update_graph_html.py /your/vault
```

***

### Q: 节点显示但看不见？

**可能原因**: 深色主题 + 白色节点颜色

**解决方法**: 修改 `config.yaml`：

```yaml
graph:
  colors:
    System: "#5e6ad2"  # 改成可见颜色
```

***

### Q: Wiki 链接不显示连线？

**可能原因**: 链接的笔记不存在

**解决方法**:

- 确保 `[[笔记名]]` 对应的 `.md` 文件存在
- 检查笔记名是否匹配（大小写敏感）

***

## 功能问题

### Q: 双击节点不跳转 Obsidian？

**可能原因**: Obsidian 未安装或 URL scheme 不支持

**解决方法**:

- 确保 Obsidian 已安装
- 检查 URL: `obsidian://open?vault=...`
- 手动测试: 浏览器打开 `obsidian://`

***

### Q: 路径追踪无反应？

**可能原因**: 点击了第一个节点但未点击第二个

**解决方法**:

1. 点击"路径"按钮激活
2. 点击第一个节点（起点）
3. 点击第二个节点（终点）
4. 等待路径显示

***

### Q: 热度统计数据消失？

**可能原因**: localStorage 被清除

**解决方法**:

- 数据存储在浏览器本地
- 换浏览器/清除缓存会丢失
- 无法恢复，重新积累

***

### Q: 导出 PNG 图片空白？

**可能原因**: canvas 未完全渲染

**解决方法**:

- 等图谱稳定后再导出
- 刷新页面重新导出

***

## 自动更新问题

### Q: 自动更新不工作？

**可能原因**:

1. watchdog 未安装
2. 路径参数错误
3. 守护进程未启动

**解决方法**:

```bash
# 1. 安装依赖
pip install watchdog

# 2. 正确启动
python auto_update.py /correct/path/to/vault

# 3. 检查进程
ps aux | grep auto_update
```

***

### Q: 更新延迟很长？

**可能原因**: 防抖间隔设置过大

**解决方法**: 修改 `config.yaml`：

```yaml
update:
  interval: 1  # 改成 1 秒
```

***

## 飞书集成问题

### Q: 飞书导入报错？

**错误信息**: `401 Unauthorized`

**解决方法**:

- 检查 API Token 是否正确
- 确保 Token 有读取消息权限

***

### Q: 飞书消息保存位置错误？

**解决方法**: 修改路径：

```yaml
feishu:
  save_dir: "04-Materials/Feishu"  # 确保路径存在
```

***

## 性能问题

### Q: 图谱加载很慢？

**可能原因**: 笔记数量过多（>500）

**解决方法**:

- 减少显示节点数（筛选分类）
- 提高更新间隔
- 分 vault 管理

***

### Q: 浏览器内存占用高？

**解决方法**:

- 关闭不必要的功能
- 定期刷新页面
- 减少笔记数量

***

## 其他问题

### Q: 如何备份图谱数据？

**解决方法**:

- 备份整个 vault 目录
- localStorage 数据无法备份（热度统计）

***

### Q: 如何分享图谱给别人？

**解决方法**:

- 导出 PNG 图片
- 或复制 `graph_fixed_beautiful.html` + 数据

***

### Q: 如何迁移到其他电脑？

**解决方法**:

```bash
# 1. 复制 vault 目录
scp -r /your/vault newcomputer:/path/

# 2. 重新安装依赖
pip install watchdog

# 3. 更新配置路径
vim .graphify/config.yaml
```

***

## 获取帮助

如果以上方法都无法解决：

1. 查看 [GitHub Issues](https://github.com/Chandlersn/obsidian-graphify/issues)
2. 提交新 Issue，附上错误信息和配置

   <br />

