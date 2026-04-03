# ⛏ Minecraft Server Downloader

> **Effortlessly download and set up Minecraft server JARs with a sleek, interactive CLI tool.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Downloads](https://img.shields.io/badge/Downloads-Ready-orange.svg)]()

A powerful, single-file Python application that simplifies Minecraft server deployment. Choose from multiple server providers, select versions, and download with progress tracking—all in one streamlined script.

## ✨ Features

- **🎯 Multiple Providers**: Support for Paper, Purpur, Folia, Vanilla, Fabric, Quilt, Waterfall, Velocity, Mohist, and Spigot
- **📦 Single File**: Everything bundled into `main.py`—no dependencies on external modules
- **🎨 Rich Interface**: Beautiful terminal UI with colors, tables, and progress bars
- **⚡ Fast Downloads**: Optimized with progress tracking and error handling
- **🔄 Auto-Rename**: Downloaded JARs are automatically renamed to `server.jar` for easy startup
- **🌐 API Integration**: Fetches latest versions directly from official APIs
- **🛡️ Error Handling**: Robust connection and HTTP error management
- **🚀 Easy Setup**: Minimal dependencies, works out-of-the-box

## 📋 Requirements

- **Python**: 3.10 or higher
- **Internet Connection**: Required for API calls and downloads
- **Java**: 17+ recommended for running the server (not for the downloader)
- **Dependencies**: Listed in `requirements.txt`

## 🚀 Installation

1. **Clone or Download** this repository
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run**:
   ```bash
   python main.py
   ```

That's it! The tool is ready to use.

## 🎮 Usage

The interactive CLI guides you through 4 simple steps:

1. **Choose Provider**: Select from a table of available server types
2. **Pick Version**: Browse and select from fetched versions (defaults to latest)
3. **Set Folder**: Choose where to save the server JAR
4. **Download**: Confirm and watch the progress

### Example Session

```
  ⛏ Minecraft Server Downloader ⛏
  Paper · Purpur · Folia · Waterfall · Velocity
  Fabric · Quilt · Vanilla · Mohist · Spigot

┌─────────────────────────────────────────────────────────────┐
│                    Available server providers               │
├────┬──────────────┬─────────────────────────────────────────┤
│ #  │ Provider     │ Description                             │
├────┼──────────────┼─────────────────────────────────────────┤
│ 1  │ [bright_green]Paper[/bright_green]      │ High performance Bukkit/Spigot fork     │
│ 2  │ [magenta]Purpur[/magenta]      │ Community-enhanced Paper fork          │
│ 3  │ [bright_cyan]Folia[/bright_cyan]       │ Multi-threaded Paper fork              │
│ 4  │ [bright_white]Vanilla[/bright_white]     │ Official Mojang server                  │
│ 5  │ [bright_blue]Waterfall[/bright_blue]    │ BungeeCord proxy                        │
│ 6  │ [yellow]Velocity[/yellow]     │ High-performance proxy                  │
│ 7  │ [bright_yellow]Fabric[/bright_yellow]      │ Fabric modded server launcher          │
│ 8  │ [red]Mohist[/red]       │ Forge + Bukkit hybrid                   │
│ 9  │ [orange3]Spigot[/orange3]      │ Spigot server                           │
└────┴──────────────┴─────────────────────────────────────────┘

Enter provider number: 1

Selected: [bright_green]Paper[/bright_green] ✓

Fetching versions for Paper...

📋 Paper — Available versions:
    1.21.4    1.21.3    1.21.1    1.21     1.20.6
    1.20.4    1.20.2    1.20.1    1.20     1.19.4
    ... and 45 more

60 versions in total. Latest: 1.21.4

Enter desired version: 1.21.4

Selected: [cyan]1.21.4[/cyan] ✓

Where should the server jar be downloaded? ~/minecraft-server

Selected: [green]/home/user/minecraft-server[/green] ✓

┌─────────────────────────────────────────────────────────────┐
│                     📦 Download summary                     │
├─────────────────────────────────────────────────────────────┤
│ Provider: [bright_green]Paper[/bright_green]                           │
│ Version:  [cyan]1.21.4[/cyan]                               │
│ Folder:   [green]/home/user/minecraft-server[/green]        │
└─────────────────────────────────────────────────────────────┘

Download now? Yes

Resolving download URL...
URL: https://api.papermc.io/v2/projects/paper/versions/1.21.4/builds/58/downloads/paper-1.21.4-58.jar

Downloading: paper-1.21.4-58.jar
████████████████████████████████████████ 100% 45.2MB 2.1MB/s 0:00:21

✅ Download completed!

📁 File: /home/user/minecraft-server/server.jar
💾 Size: 45.23 MB

Start server:
  cd /home/user/minecraft-server
  java -Xmx2G -Xms1G -jar server.jar nogui
```

## 🏗️ Supported Providers

| Provider      | Description                                         | Type   | Website                                             |
| ------------- | --------------------------------------------------- | ------ | --------------------------------------------------- |
| **Paper**     | High-performance fork of Spigot with optimizations  | Server | [papermc.io](https://papermc.io)                    |
| **Purpur**    | Paper fork with community features and enhancements | Server | [purpurmc.org](https://purpurmc.org)                |
| **Folia**     | Multi-threaded Paper fork for better performance    | Server | [papermc.io](https://papermc.io/software/folia)     |
| **Vanilla**   | Official Mojang server, unmodified                  | Server | [minecraft.net](https://www.minecraft.net)          |
| **Fabric**    | Lightweight mod loader for Fabric mods              | Server | [fabricmc.net](https://fabricmc.net)                |
| **Quilt**     | Alternative mod loader compatible with Fabric       | Server | [quiltmc.org](https://quiltmc.org)                  |
| **Waterfall** | BungeeCord-based proxy server                       | Proxy  | [papermc.io](https://papermc.io/software/waterfall) |
| **Velocity**  | Modern, high-performance proxy                      | Proxy  | [papermc.io](https://papermc.io/software/velocity)  |
| **Mohist**    | Hybrid server combining Forge and Bukkit            | Server | [mohistmc.com](https://mohistmc.com)                |
| **Spigot**    | Popular server with plugin support                  | Server | [spigotmc.org](https://www.spigotmc.org)            |

## ⚙️ Server Startup

After download, navigate to your chosen folder and run:

```bash
cd /path/to/your/server/folder
java -Xmx2G -Xms1G -jar server.jar nogui
```

**Important**: On first run, the server will generate `eula.txt`. You must edit it to accept the EULA:

```txt
eula=true
```

### Recommended JVM Flags

For optimal performance, consider these flags:

```bash
java -Xmx4G -Xms2G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:MaxTenuringThreshold=1 -XX:G1SATBBufferEnqueueingThresholdPercent=30 -XX:G1ConcMarkStepDurationMillis=5 -XX:G1ConcRSHotCardLimit=16 -XX:G1ConcRefinementThreads=6 -jar server.jar nogui
```

## 🛠️ Development

This is a single-file application (`main.py`) with no external module dependencies. All providers and download logic are self-contained.

### Project Structure

```
minecraft-server-downloader/
├── main.py              # Main application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding New Providers

To add a new server provider:

1. Create a class inheriting from `ServerProvider`
2. Implement `get_versions()` and `get_download_url(version)`
3. Add to `get_all_providers()` list

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/minecraft-server-downloader/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/minecraft-server-downloader/discussions)

## 🙏 Acknowledgments

- [PaperMC](https://papermc.io) for their excellent server software
- [Rich](https://github.com/Textualize/rich) for the beautiful CLI interface
- [Requests](https://github.com/psf/requests) for HTTP handling

---

**Happy crafting!** 🎮⛏️
