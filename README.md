# MeowAutoChrome

> 基于 .NET 与 Electron 的 Chrome 自动化平台：多浏览器实例管理、可热插拔插件、实时画面与日志流。

[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-2ea44f?logo=github)](https://roslynmeow.github.io/MeowAutoChrome/)
[![Release](https://github.com/RoslynMeow/MeowAutoChrome/actions/workflows/release.yml/badge.svg)](https://github.com/RoslynMeow/MeowAutoChrome/actions/workflows/release.yml)
[![Latest Release](https://img.shields.io/github/v/release/RoslynMeow/MeowAutoChrome?display_name=tag)](https://github.com/RoslynMeow/MeowAutoChrome/releases)
[![.NET](https://img.shields.io/badge/.NET-10.0-512BD4?logo=dotnet)](https://dotnet.microsoft.com/)
[![License](https://img.shields.io/badge/license-GPL--3.0--or--later-blue)](LICENSE.txt)

MeowAutoChrome 将浏览器自动化能力拆分为「前端界面 + 后端服务 + 插件」三部分：Electron 提供桌面交互，WebAPI 暴露 HTTP / SignalR 接口，Core 负责业务逻辑、Playwright 运行时与插件主机。插件以可回收的 `AssemblyLoadContext` 动态加载，可实现热插拔与生命周期管理。

## 特性

- **多实例浏览器管理**：统一的实例创建/选择/关闭与生命周期控制，支持自定义 `UserDataDirectory`、Headless 等选项。
- **插件化架构**：基于 `[Plugin]` / `[PAction]` / `[PInput]` 声明式契约，自动发现动作与参数并生成前端表单。
- **实时通信**：通过 SignalR 推送插件输出、日志与画面流（Screencast）。
- **两种运行形态**：Electron 桌面前端 + 独立可部署的 WebAPI 后端。
- **自动化流水线**：合并到 `master` 自动生成多版本文档、推送 NuGet 包并打包 Release。

## 项目结构

| 项目 | 说明 |
| --- | --- |
| [`MeowAutoChrome.WebAPI`](MeowAutoChrome.WebAPI) | 后端 HTTP API 与 SignalR Hub |
| [`MeowAutoChrome.Core`](MeowAutoChrome.Core) | 业务逻辑、Playwright 运行时管理、插件主机 |
| [`MeowAutoChrome.Electron`](MeowAutoChrome.Electron) | Electron 桌面前端，与本地 WebAPI 配合运行 |
| [`MeowAutoChrome.Contracts`](MeowAutoChrome.Contracts) | 插件接口、基类与 attribute 定义（发布为 NuGet 包） |
| [`MeowAutoChrome.ExamplePlugin`](MeowAutoChrome.ExamplePlugin) | 参考插件示例 |

## 快速开始

**环境要求**：.NET SDK 10、Node.js 20+、Windows PowerShell（脚本依赖）。

```powershell
# 构建整个解决方案
dotnet build MeowAutoChrome.slnx

# 运行 WebAPI（开发）
dotnet run --project MeowAutoChrome.WebAPI/MeowAutoChrome.WebAPI.csproj

# 一键启动（发布 WebAPI 并拉起 Electron）
.\dev.ps1

# 打包桌面应用（installer / dir / zip）
.\pack.ps1
```

Electron 相关命令见 [`MeowAutoChrome.Electron/package.json`](MeowAutoChrome.Electron/package.json)。

## 插件开发

插件引用 [`MeowAutoChrome.Contracts`](MeowAutoChrome.Contracts)（保持版本一致），用 attribute 声明动作与参数：

```csharp
using MeowAutoChrome.Contracts;
using MeowAutoChrome.Contracts.Attributes;

[Plugin("com.example.hello", "Hello Plugin", "示例插件")]
public class HelloPlugin : PluginBase
{
    [PAction(Name = "Say Hello", Description = "返回问候文本")]
    public IResult SayHello([PInput(Label = "名字", Required = true)] string name)
        => Result.Ok(new { Text = $"Hello {name}" });
}
```

> 注意：插件发布包中**不要**包含 `MeowAutoChrome.Contracts.dll` 或 `Microsoft.Playwright.*`，它们由主机共享。

详见 [插件指南](docs/PLUGINS.md)。

## 文档

完整文档（多版本，支持切换）：**<https://roslynmeow.github.io/MeowAutoChrome/>**

| 文档 | 内容 |
| --- | --- |
| [SETUP](docs/SETUP.md) | 环境与依赖安装 |
| [USAGE](docs/USAGE.md) | 运行、调试与常用命令 |
| [ARCHITECTURE](docs/ARCHITECTURE.md) | 系统架构与组件交互 |
| [FOLDERS](docs/FOLDERS.md) | 仓库目录说明 |
| [PLUGINS](docs/PLUGINS.md) | 插件开发与加载规则 |
| [API](docs/API.md) | HTTP 与 SignalR 接口说明 |
| [TROUBLESHOOTING](docs/TROUBLESHOOTING.md) | 常见问题排查 |
| [CONTRIBUTING](docs/CONTRIBUTING.md) | 贡献准则 |
| [SECURITY](docs/SECURITY.md) | 安全与依赖管理 |

## 分发

`MeowAutoChrome.Contracts` 作为 NuGet 包发布到 [GitHub Packages](https://github.com/RoslynMeow?tab=packages)。

```powershell
dotnet add package MeowAutoChrome.Contracts --source "https://nuget.pkg.github.com/RoslynMeow/index.json"
```

## 贡献

欢迎提交 Issue 与 PR。开发分支为 `dev`，功能完成后合并至 `master`。请先阅读 [贡献准则](docs/CONTRIBUTING.md) 与 [行为准则](CODE_OF_CONDUCT.md)。

## 许可证

本项目采用 [GPL-3.0-or-later](LICENSE.txt) 许可。
