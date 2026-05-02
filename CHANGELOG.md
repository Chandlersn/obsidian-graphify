# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.5.0] - 2026-05-02

**Batch optimization & Knowledge network expansion.**

### Highlights

**批量优化成果**：8篇哲学文档完成质量优化，平均提升8.6分，达到92-95分标准。

|| 文档标题 | 原始评分 | 优化后评分 | 提升幅度 ||
||---------|---------|-----------|---------||
|| 沟通的艺术 | 84 | 95 | +11 ||
|| 别再囤知识了 | 78 | 92 | +14 ||
|| 这个世界最大的悲剧 | 82 | 93 | +11 ||
|| 人的认知转变 | 89 | 94 | +5 ||
|| 真正的智慧从何而来 | 87 | 93 | +6 ||
|| 创造力如何才能拥有 | 86 | 93 | +7 ||
|| 你的认知体系 | 84 | 92 | +8 ||
|| 客观时间与意识时间 | 85 | 92 | +7 ||

### Knowledge Network Growth

- **知识节点**: 18 → 38 (+111%)
- **Wiki连接**: 22 → 100 (+355%)
- **健康度**: 65.8% healthy notes
- **知识密度**: 平均每个节点有 2.6 个连接

### Quality Standards Established

**开头格式标准化**：
```
引用块（3句话）→ 提点性描述 → 总结性点睛 → 数据震撼 → 两问题揭示
```

**质量评分标准**：
- 数据支撑密度
- 哲学洞察犀利度
- 语言简洁力
- 论证层层深入度
- 情感共鸣真实度

### Documentation Updates

- `index.md` → v1.1 (批量优化成果版)
- `SOUL-定位说明.md` → v1.1
- `笔记指南与创作方法论.md` → v1.1
- 新增 `README.md` (笔记系统总览)

### Technical Improvements

- Wiki链接重建流程优化
- 知识图谱可视化更新
- 备份文件清理机制

---

## [2.4.0] - 2026-04-24

**Island detection, quality tools, and graph analysis.**

**Repository maintenance and fixes.**

### Fixed

|| # | Issue | Fix |
||---|-------|-----|
|| 01 | feishu_importer.py truncated code | Line 31: `os.environ.get('FEISHU_TOKEN', '')` |
|| 02 | graphify.sh missing | Created unified CLI entry script (70+ lines) |
|| 03 | demo_notes incomplete | Added Wisdom/Architecture notes, Templates |
|| 04 | CATEGORY_RULES hardcoded | note_collector.py now reads from config.yaml |

### Added

- `config.yaml` expanded with full category rules structure
- `skills/scripts/graphify.sh` - unified CLI entry point
- Demo notes:
  - `02-Knowledge/Wisdom/真正的智慧从何而来.md`
  - `02-Knowledge/Wisdom/认知体系的建立.md`
  - `02-Knowledge/Architecture/模块化架构设计原则.md`
  - `05-Templates/知识笔记模板.md`
  - `05-Templates/项目笔记模板.md`

### Changed

- `note_collector.py` uses `load_category_rules()` function
- Categories now configurable via `config.yaml` (no more hardcoded rules)
- Better error handling with fallback to default rules

---

## [1.0.0] - 2026-04-16

**First stable release.**

### Added

| # | Feature | Description |
|---|---------|-------------|
| 01 | 3-level folder structure | 原创/收藏分离，结构化管理 |
| 02 | Interactive graph visualization | vis-network 渲染，节点可点击 |
| 03 | Dynamic filter buttons | 数据驱动渲染，自动同步分类 |
| 04 | Path tracing | BFS 最短路径算法 |
| 05 | Heat map statistics | localStorage 点击计数 |
| 06 | Influence analysis | PageRank 简化版 |
| 07 | Island detection | 高亮无连接节点 |
| 08 | PNG export | canvas 截图导出 |
| 09 | Dark/Light theme | Linear 设计风格 |
| 10 | Auto-update daemon | watchdog 监控 vault |
| 11 | Feishu importer | 消息自动导入笔记 |
| 12 | Note templates | 通用/项目/知识模板 |

### UI/UX

- Keyboard shortcuts: `Ctrl+K` (search), `ESC` (close), `Ctrl+R` (refresh)
- Status bar with glassmorphism effect
- Sidebar layout for feature buttons
- Node click popup with preview
- Double-click to open in Obsidian
- Label truncation (max 12 chars, tooltip shows full)

### Documentation

- README with quick start guide
- Getting started (docs/getting-started.md)
- Folder structure design (docs/folder-structure.md)
- Features detailed (docs/features.md)
- Customization guide (docs/customization.md)
- Troubleshooting FAQ (docs/troubleshooting.md)
- Installation script (scripts/install.sh)

---

## [0.9.0] - 2026-04-15

**Beta version.**

### Added

- Basic graph visualization
- Simple filter buttons (hardcoded)
- Basic dark mode
- Initial Python scripts

### Known Issues

| Issue | Status in 1.0.0 |
|-------|-----------------|
| Filter buttons hardcoded | ✅ Fixed: data-driven rendering |
| Theme switching incomplete | ✅ Fixed: full CSS variables |
| Modal close button not working | ✅ Fixed: proper event binding |
| Template string errors | ✅ Fixed: proper `${}` syntax |

---

## Future Plans

### [1.1.0] - Planned

| Feature | Description |
|---------|-------------|
| Multi-language | English, Chinese, Japanese |
| Layout algorithms | Force-directed, hierarchical |
| Export formats | JSON, CSV |
| Search history | Recent searches panel |
| Collaborative editing | Multi-user support |

### [1.2.0] - Planned

| Feature | Description |
|---------|-------------|
| Mobile responsive | Touch-friendly UI |
| Touch gestures | Pinch zoom, swipe |
| Offline-first | Service worker caching |
| Plugin system | Custom feature hooks |

---

## Version Summary

|| Version | Date | Description | Features ||
||---------|------|-------------|----------||
|| 1.1.0 | 2026-04-19 | Repository maintenance | 4 fixes, 5 demo notes ||
|| 1.0.0 | 2026-04-16 | First stable release | 12 core features ||
|| 0.9.0 | 2026-04-15 | Beta version | 4 basic features ||

---

<div align="center">

*Graphify 持续进化中。*

</div>