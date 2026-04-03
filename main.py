#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich import box
from rich.align import Align
from rich.progress import (
    Progress,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    BarColumn,
    TextColumn,
)
from rich.status import Status

console = Console()
PAPERMC_API = "https://api.papermc.io/v2/projects"
MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
PURPUR_API = "https://api.purpurmc.org/v2/purpur"
QUILT_META = "https://meta.quiltmc.org/v3"
GETBUKKIT_API = "https://download.getbukkit.org/spigot"
MOHIST_API = "https://mohistmc.com/api/v2/projects/mohist"
KNOWN_SPIGOT_VERSIONS = [
    "1.21.4", "1.21.3", "1.21.1", "1.21",
    "1.20.6", "1.20.4", "1.20.2", "1.20.1", "1.20",
    "1.19.4", "1.19.3", "1.19.2", "1.19.1", "1.19",
    "1.18.2", "1.18.1", "1.18",
    "1.17.1", "1.17",
    "1.16.5", "1.16.4", "1.16.3", "1.16.2", "1.16.1",
    "1.15.2", "1.15.1", "1.15",
    "1.14.4", "1.14.3", "1.14.2", "1.14.1", "1.14",
    "1.13.2", "1.13.1", "1.13",
    "1.12.2", "1.12.1", "1.12",
    "1.11.2", "1.11",
    "1.10.2", "1.9.4", "1.8.8",
]

class ServerProvider:
    name = "Unknown"
    description = ""
    color = "white"
    def get_versions(self):
        raise NotImplementedError
    def get_download_url(self, version):
        raise NotImplementedError

class PaperMCProvider(ServerProvider):
    def __init__(self, project, name, desc, color):
        self.project = project
        self.name = name
        self.description = desc
        self.color = color
    def get_versions(self):
        resp = requests.get(f"{PAPERMC_API}/{self.project}", timeout=10)
        resp.raise_for_status()
        versions = resp.json().get("versions", [])
        return list(reversed(versions))
    def get_download_url(self, version):
        resp = requests.get(f"{PAPERMC_API}/{self.project}/versions/{version}", timeout=10)
        resp.raise_for_status()
        builds = resp.json().get("builds", [])
        if not builds:
            raise ValueError(f"No builds found for {version}.")
        latest = builds[-1]
        filename = f"{self.project}-{version}-{latest}.jar"
        url = f"{PAPERMC_API}/{self.project}/versions/{version}/builds/{latest}/downloads/{filename}"
        return url, filename

class VanillaProvider(ServerProvider):
    name = "Vanilla"
    description = "Official Mojang server"
    color = "bright_white"
    def __init__(self):
        self._version_map = {}
    def get_versions(self):
        resp = requests.get(MANIFEST_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        versions = []
        for v in data.get("versions", []):
            if v.get("type") == "release":
                self._version_map[v["id"]] = v["url"]
                versions.append(v["id"])
        return versions
    def get_download_url(self, version):
        if version not in self._version_map:
            self.get_versions()
        version_url = self._version_map.get(version)
        if not version_url:
            raise ValueError(f"Vanilla version {version} not found.")
        resp = requests.get(version_url, timeout=10)
        resp.raise_for_status()
        server_info = resp.json().get("downloads", {}).get("server")
        if not server_info:
            raise ValueError(f"No server jar found for Vanilla {version}.")
        return server_info["url"], f"minecraft_server.{version}.jar"

class PurpurProvider(ServerProvider):
    name = "Purpur"
    description = "Community-enhanced Paper fork"
    color = "magenta"
    def get_versions(self):
        resp = requests.get(PURPUR_API, timeout=10)
        resp.raise_for_status()
        versions = resp.json().get("versions", [])
        return list(reversed(versions))
    def get_download_url(self, version):
        resp = requests.get(f"{PURPUR_API}/{version}", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        latest = data.get("builds", {}).get("latest")
        if not latest:
            raise ValueError(f"No Purpur build found for {version}.")
        return f"{PURPUR_API}/{version}/{latest}/download", f"purpur-{version}-{latest}.jar"

class FabricProvider(ServerProvider):
    name = "Fabric"
    description = "Fabric modded server launcher"
    color = "bright_yellow"
    def __init__(self):
        self._loader = ""
    def _latest_loader(self):
        if self._loader:
            return self._loader
        resp = requests.get(f"{FABRIC_META}/versions/loader", timeout=10)
        resp.raise_for_status()
        loaders = resp.json()
        stable = [l for l in loaders if l.get("stable")]
        self._loader = (stable[0] if stable else loaders[0])["version"]
        return self._loader
    def get_versions(self):
        resp = requests.get(f"{FABRIC_META}/versions/game", timeout=10)
        resp.raise_for_status()
        games = resp.json()
        return [g["version"] for g in games if g.get("stable")]
    def get_download_url(self, version):
        loader = self._latest_loader()
        resp = requests.get(f"{FABRIC_META}/versions/installer", timeout=10)
        resp.raise_for_status()
        installer = resp.json()[0]["version"]
        filename = f"fabric-server-mc.{version}-loader.{loader}-launcher.{installer}.jar"
        url = f"{FABRIC_META}/versions/loader/{version}/{loader}/{installer}/server/jar"
        return url, filename

class QuiltProvider(ServerProvider):
    name = "Quilt"
    description = "Quilt modded server launcher"
    color = "bright_magenta"
    def __init__(self):
        self._loader = ""
    def _latest_loader(self):
        if self._loader:
            return self._loader
        resp = requests.get(f"{QUILT_META}/versions/loader", timeout=10)
        resp.raise_for_status()
        loaders = resp.json()
        stable = [l for l in loaders if l.get("stable")]
        self._loader = (stable[0] if stable else loaders[0])["version"]
        return self._loader
    def get_versions(self):
        resp = requests.get(f"{QUILT_META}/versions/game", timeout=10)
        resp.raise_for_status()
        games = resp.json()
        return [g["version"] for g in games if g.get("stable")]
    def get_download_url(self, version):
        loader = self._latest_loader()
        resp = requests.get(f"{QUILT_META}/versions/installer", timeout=10)
        resp.raise_for_status()
        installer = resp.json()[0]["version"]
        filename = f"quilt-server-mc.{version}-loader.{loader}-launcher.{installer}.jar"
        url = f"{QUILT_META}/versions/loader/{version}/{loader}/{installer}/server/jar"
        return url, filename

class SpigotProvider(ServerProvider):
    name = "Spigot"
    description = "Spigot server";
    color = "orange3"
    def get_versions(self):
        return KNOWN_SPIGOT_VERSIONS
    def get_download_url(self, version):
        return f"{GETBUKKIT_API}/spigot-{version}.jar", f"spigot-{version}.jar"

class MohistProvider(ServerProvider):
    name = "Mohist"
    description = "Forge + Bukkit hybrid"
    color = "red"
    def get_versions(self):
        resp = requests.get(f"{MOHIST_API}/versions", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        versions = data.get("versions", data) if isinstance(data, dict) else data
        if isinstance(versions, list):
            return list(reversed(versions))
        raise ValueError("Mohist versions unavailable.")
    def get_download_url(self, version):
        resp = requests.get(f"{MOHIST_API}/{version}/builds", timeout=10)
        resp.raise_for_status()
        builds = resp.json()
        if not builds:
            raise ValueError(f"No Mohist builds found for {version}.")
        latest_build = None
        for b in reversed(builds):
            if b.get("result") == "SUCCESS" or "result" not in b:
                latest_build = b
                break
        if not latest_build:
            latest_build = builds[-1]
        url = latest_build.get("url") or latest_build.get("download_url", "")
        if not url:
            raise ValueError(f"No Mohist download URL for {version}.")
        return url, f"mohist-{version}-{latest_build.get('number','latest')}.jar"

def make_paper():
    return PaperMCProvider("paper", "Paper", "High performance Bukkit/Spigot fork", "bright_green")

def make_folia():
    return PaperMCProvider("folia", "Folia", "Multi-threaded Paper fork", "bright_cyan")

def make_waterfall():
    return PaperMCProvider("waterfall", "Waterfall", "BungeeCord proxy", "bright_blue")

def make_velocity():
    return PaperMCProvider("velocity", "Velocity", "High-performance proxy", "yellow")

def get_all_providers():
    return [
        make_paper(),
        PurpurProvider(),
        make_folia(),
        VanillaProvider(),
        make_waterfall(),
        make_velocity(),
        FabricProvider(),
        QuiltProvider(),
        MohistProvider(),
        SpigotProvider(),
    ]

def download_file(url, dest_folder, filename):
    dest = Path(dest_folder)
    dest.mkdir(parents=True, exist_ok=True)
    temp_file = dest / filename
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    total_size = int(response.headers.get("Content-Length", 0))
    with Progress(
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=40),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task(f"[cyan]Downloading: {filename}", total=total_size or None)
        with open(temp_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    progress.advance(task, len(chunk))
    final_file = dest / "server.jar"
    if final_file.exists():
        final_file.unlink()
    temp_file.rename(final_file)
    return final_file

def print_banner():
    banner = Text()
    banner.append("  ⛏ Minecraft Server Downloader ⛏\n", style="bold bright_green")
    banner.append("  Paper · Purpur · Folia · Waterfall · Velocity\n", style="dim")
    banner.append("  Fabric · Quilt · Vanilla · Mohist · Spigot\n", style="dim")
    console.print(Panel(Align.center(banner), style="green", padding=(0, 4)))
    console.print()

def pick_provider(providers):
    table = Table(title="[bold]Available server providers[/bold]", box=box.ROUNDED, show_lines=True, title_style="bold bright_white")
    table.add_column("#", style="bold cyan", justify="center", width=4)
    table.add_column("Provider", style="bold", width=14)
    table.add_column("Description", style="dim")
    for i, p in enumerate(providers, 1):
        table.add_row(str(i), f"[{p.color}]{p.name}[/{p.color}]", p.description)
    console.print(table)
    console.print()
    while True:
        choice = Prompt.ask("[bold yellow]Enter provider number[/bold yellow]", default="1")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(providers):
                return providers[idx]
            console.print(f"[red]Please enter a number between 1 and {len(providers)}.[/red]")
        except ValueError:
            console.print("[red]Invalid input, please type a number.[/red]")

def pick_version(provider):
    with Status(f"Fetching versions for {provider.name}...", spinner="dots"):
        versions = provider.get_versions()
    if not versions:
        console.print("[red]No versions found.[/red]")
        sys.exit(1)
    display = versions[:60]
    console.print(f"\n[bold {provider.color}]📋 {provider.name} — Available versions:[/bold {provider.color}]")
    for chunk in [display[i:i+6] for i in range(0, len(display), 6)]:
        console.print("  " + "  ".join(f"[cyan]{v:>8}[/cyan]" for v in chunk))
    if len(versions) > 60:
        console.print(f"  [dim]... and {len(versions) - 60} more[/dim]")
    console.print()
    console.print(f"[dim]{len(versions)} versions in total. Latest: [bold]{versions[0]}[/bold][/dim]")
    console.print()
    while True:
        choice = Prompt.ask("[bold yellow]Enter desired version[/bold yellow]", default=versions[0])
        if choice in versions:
            return choice
        close = [v for v in versions if v.startswith(choice)]
        if close:
            console.print(f"[yellow]Close matches: {', '.join(close[:5])}[/yellow]")
        else:
            console.print(f"[red]'{choice}' is not a valid version. Please choose one from the list.[/red]")

def pick_folder():
    console.print()
    default_path = str(Path.home() / "minecraft-server")
    folder = Prompt.ask("[bold yellow]Where should the server jar be downloaded?[/bold yellow]", default=default_path)
    folder = folder.strip().strip('"').strip("'")
    folder = os.path.expanduser(folder)
    dest = Path(folder)
    if dest.exists() and not dest.is_dir():
        console.print("[red]The path is a file. Please enter a folder.[/red]")
        return pick_folder()
    if not dest.exists():
        console.print(f"\n[yellow]Folder '{folder}' does not exist.[/yellow]")
        if not Confirm.ask("Create it?", default=True):
            console.print("[red]Cancelled.[/red]")
            sys.exit(0)
        dest.mkdir(parents=True, exist_ok=True)
    return str(dest)

def confirm_and_download(provider, version, folder):
    console.print()
    summary = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    summary.add_column(style="bold dim")
    summary.add_column(style="bold bright_white")
    summary.add_row("Provider", f"[{provider.color}]{provider.name}[/{provider.color}]")
    summary.add_row("Version", f"[cyan]{version}[/cyan]")
    summary.add_row("Folder", f"[green]{folder}[/green]")
    console.print(Panel(summary, title="[bold]📦 Download summary[/bold]", style="dim"))
    console.print()
    if not Confirm.ask("[bold]Download now?[/bold]", default=True):
        console.print("[yellow]Cancelled.[/yellow]")
        sys.exit(0)
    with Status("Resolving download URL...", spinner="bouncingBall"):
        url, filename = provider.get_download_url(version)
    console.print(f"[dim]URL: {url}[/dim]\n")
    try:
        downloaded = download_file(url, folder, filename)
    except requests.exceptions.HTTPError as e:
        console.print(f"\n[red]HTTP error: {e}[/red]")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        console.print("\n[red]Connection error! Check your internet.[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Download error: {e}[/red]")
        sys.exit(1)
    total_mb = downloaded.stat().st_size / 1024 / 1024
    message = Text()
    message.append("✅ Download completed!\n\n", style="bold bright_green")
    message.append("📁 File: ", style="bold")
    message.append(f"{downloaded}\n", style="cyan")
    message.append("💾 Size: ", style="bold")
    message.append(f"{total_mb:.2f} MB\n\n", style="white")
    message.append("Start server:\n", style="dim")
    message.append(f"  cd {folder}\n", style="bold green")
    message.append("  java -Xmx2G -Xms1G -jar server.jar nogui", style="bold green")
    console.print(Panel(message, style="green", padding=(1, 3)))

def main():
    print_banner()
    providers = get_all_providers()
    console.rule("[bold bright_white]Step 1 — Choose provider[/bold bright_white]")
    provider = pick_provider(providers)
    console.print(f"\n[bold]Selected:[/bold] [{provider.color}]{provider.name}[/{provider.color}] ✓")
    console.rule("[bold bright_white]Step 2 — Choose version[/bold bright_white]")
    version = pick_version(provider)
    console.print(f"[bold]Selected:[/bold] [cyan]{version}[/cyan] ✓")
    console.rule("[bold bright_white]Step 3 — Choose installation folder[/bold bright_white]")
    folder = pick_folder()
    console.print(f"[bold]Selected:[/bold] [green]{folder}[/green] ✓")
    console.rule("[bold bright_white]Step 4 — Download[/bold bright_white]")
    confirm_and_download(provider, version, folder)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user.[/yellow]")
        sys.exit(0)
