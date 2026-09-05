# Oudu Addons — Free Odoo Tools and Native Integrations

Official open-source server modules for **Oudu Software** products. Add shared instance identity and a capability manifest to Odoo, then connect your server to **Oudu Desktop**, the free native desktop client for Windows, macOS and Linux.

## Choose your Odoo version

Each branch is a rolling snapshot of the latest compatible modules for that Odoo series.

| Odoo | Browse source | Download latest | Odoo Apps |
| --- | --- | --- | --- |
| 19.0 | [Browse 19.0](https://github.com/oudusoft/oudu_addons/tree/19.0) | [Download 19.0 ZIP](https://github.com/oudusoft/oudu_addons/archive/refs/heads/19.0.zip) | [Instance Identity](https://apps.odoo.com/apps/modules/19.0/oudu_base) · [Desktop](https://apps.odoo.com/apps/modules/19.0/oudu_desktop) |
| 18.0 | [Browse 18.0](https://github.com/oudusoft/oudu_addons/tree/18.0) | [Download 18.0 ZIP](https://github.com/oudusoft/oudu_addons/archive/refs/heads/18.0.zip) | [Instance Identity](https://apps.odoo.com/apps/modules/18.0/oudu_base) · [Desktop](https://apps.odoo.com/apps/modules/18.0/oudu_desktop) |
| 17.0 | [Browse 17.0](https://github.com/oudusoft/oudu_addons/tree/17.0) | [Download 17.0 ZIP](https://github.com/oudusoft/oudu_addons/archive/refs/heads/17.0.zip) | [Instance Identity](https://apps.odoo.com/apps/modules/17.0/oudu_base) · [Desktop](https://apps.odoo.com/apps/modules/17.0/oudu_desktop) |
| 16.0 | [Browse 16.0](https://github.com/oudusoft/oudu_addons/tree/16.0) | [Download 16.0 ZIP](https://github.com/oudusoft/oudu_addons/archive/refs/heads/16.0.zip) | [Instance Identity](https://apps.odoo.com/apps/modules/16.0/oudu_base) · [Desktop](https://apps.odoo.com/apps/modules/16.0/oudu_desktop) |
| 15.0 | [Browse 15.0](https://github.com/oudusoft/oudu_addons/tree/15.0) | [Download 15.0 ZIP](https://github.com/oudusoft/oudu_addons/archive/refs/heads/15.0.zip) | [Instance Identity](https://apps.odoo.com/apps/modules/15.0/oudu_base) · [Desktop](https://apps.odoo.com/apps/modules/15.0/oudu_desktop) |
| 14.0 | [Browse 14.0](https://github.com/oudusoft/oudu_addons/tree/14.0) | [Download 14.0 ZIP](https://github.com/oudusoft/oudu_addons/archive/refs/heads/14.0.zip) | [Instance Identity](https://apps.odoo.com/apps/modules/14.0/oudu_base) · [Desktop](https://apps.odoo.com/apps/modules/14.0/oudu_desktop) |
| 13.0 | [Browse 13.0](https://github.com/oudusoft/oudu_addons/tree/13.0) | [Download 13.0 ZIP](https://github.com/oudusoft/oudu_addons/archive/refs/heads/13.0.zip) | [Instance Identity](https://apps.odoo.com/apps/modules/13.0/oudu_base) · [Desktop](https://apps.odoo.com/apps/modules/13.0/oudu_desktop) |

![Oudu Desktop multi-account workspace](https://desktop.oudu.top/assets/shots/en-US/01-workspace.png)

## Free modules

| Module | Odoo series | What it provides |
| --- | --- | --- |
| `oudu_base` | 13.0–19.0 | Shared Oudu Software settings, instance name/color/icon, and the public capability manifest. |
| `oudu_desktop` | 13.0–19.0 | Desktop capability contribution, connection guide, direct report print policy, file upload policy, and local source controls. |

Both modules install and remain usable in a standard web browser. Oudu Desktop adds native capabilities without modifying Odoo itself.

## Oudu Desktop

Oudu Desktop hosts Odoo's own frontend while keeping every server and account in an isolated session. Work across several Odoo environments at once, print reports directly, and use local files and devices without leaving your desktop.

![Direct Odoo report printing](https://desktop.oudu.top/assets/shots/en-US/02-print-bridge.png)

- **Multiple instances and accounts** — keep several Odoo servers or identities online side by side.
- **Direct report printing** — send reports to system and network printers with routing and history.
- **Local files and devices** — use native file sources, screenshots, cameras, microphones and scanners through explicit controls.
- **Native desktop experience** — windows, tray, notifications, badges, downloads and shortcuts.

![Native file and device sources](https://desktop.oudu.top/assets/shots/en-US/03-file-sources.png)

### Multi-page scanning and export

Scan business documents, reorder or remove pages, adjust their appearance, then export one PDF or a set of images.

![Multi-page scanner workbench](https://desktop.oudu.top/assets/shots/en-US/04-capture-workbench.png)

### One activity center across accounts

Keep Odoo messages, desktop jobs and items that need attention together without losing their account context.

![Cross-account activity center](https://desktop.oudu.top/assets/shots/en-US/05-activity-center.png)

**Free download: [desktop.oudu.top](https://desktop.oudu.top) · [Microsoft Store](https://apps.microsoft.com/detail/9NK0Z5PVPGJJ)**

## Compatibility

These server addons support **Odoo 13–19**. Each supported series is built from one private source tree and tested in its matching Odoo runtime before publication.

The Oudu Desktop client can still connect to Odoo 08–12 without these server addons; those older servers keep their normal Odoo behavior and simply do not expose the optional capability manifest and policies.

## Installation

1. Select the branch matching your Odoo series, such as `19.0` or `13.0`.
2. Copy `oudu_base` and `oudu_desktop` into an addons path.
3. Update the Apps list and install **Oudu Desktop**; Odoo installs `oudu_base` as its dependency.
4. Open **Settings → Oudu Software** to set the shared instance identity and desktop policies.

Every public branch is a generated, self-contained snapshot with one commit. Development history and compatibility transforms stay outside this distribution repository, so branch contents should not be edited by hand.

## Links

- Oudu Software: [www.oudu.net](https://www.oudu.net)
- Oudu Desktop: [desktop.oudu.top](https://desktop.oudu.top)
- Contact: [info@oudu.net](mailto:info@oudu.net)
- License: LGPL-3.0

---

## 中文简介

本仓库提供欧度软件产品的官方开源 Odoo 服务端模块：

- `oudu_base`：统一的“欧度软件”设置入口、实例名称/颜色/图标与聚合能力清单；
- `oudu_desktop`：向聚合能力清单贡献 Oudu Desktop 策略，并提供连接引导、报表打印策略、文件上传策略与本地来源控制。

服务端模块支持 **Odoo 13–19**，每个系列都由同一私有真源生成，并在对应 Odoo 运行时通过门禁后发布。Oudu Desktop 客户端仍可直接连接 Odoo 08–12，但这些旧系列不提供可选的服务端模块能力。

**选择 Odoo 版本：** [19.0](https://github.com/oudusoft/oudu_addons/tree/19.0) · [18.0](https://github.com/oudusoft/oudu_addons/tree/18.0) · [17.0](https://github.com/oudusoft/oudu_addons/tree/17.0) · [16.0](https://github.com/oudusoft/oudu_addons/tree/16.0) · [15.0](https://github.com/oudusoft/oudu_addons/tree/15.0) · [14.0](https://github.com/oudusoft/oudu_addons/tree/14.0) · [13.0](https://github.com/oudusoft/oudu_addons/tree/13.0)

模块在普通浏览器中也能正常安装使用；配合免费的 Oudu Desktop，可获得多实例、报表直接打印、本地文件与设备以及原生桌面体验。

免费下载：[desktop.oudu.top](https://desktop.oudu.top) ｜ [Microsoft Store](https://apps.microsoft.com/detail/9NK0Z5PVPGJJ) ｜ 官网：[www.oudu.net](https://www.oudu.net) ｜ 联系：[info@oudu.net](mailto:info@oudu.net)
