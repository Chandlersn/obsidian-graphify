# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

| Version | Date | Description | Features |
|---------|------|-------------|----------|
| 1.0.0 | 2026-04-16 | First stable release | 12 core features |
| 0.9.0 | 2026-04-15 | Beta version | 4 basic features |

---

<div align="center">

*Graphify 持续进化中。*

</div>