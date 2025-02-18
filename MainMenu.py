#!/usr/bin/env python3

from typing import Dict, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn
from rich.layout import Layout
from rich.live import Live
import typer
import yaml
import asyncio
from pathlib import Path
from datetime import datetime

# Initialize console
console = Console()

# Tool categories and their commands
TOOL_CATEGORIES = {
    "Information Gathering": {
        "nmap": "Network scanning",
        "osif": "OSINT Framework",
        "red_hawk": "Information gathering",
        "seeker": "Geolocation tracker",
        "astranmap": "Advanced Nmap automation"
    },
    "Web Security": {
        "sqlmap": "SQL injection",
        "nikto": "Web server scanner",
        "websploit": "Web exploitation",
        "whatweb": "Web scanner",
        "wfuzz": "Web fuzzer"
    },
    "Network Security": {
        "wireshark": "Network analyzer",
        "routersploit": "Router exploitation",
        "hydra": "Password cracker",
        "aircrack-ng": "Wireless security"
    },
    "Exploitation Tools": {
        "metasploit": "Exploitation framework",
        "beef": "Browser exploitation",
        "commix": "Command injection",
        "xattacker": "Website vulnerability scanner"
    },
    "Forensics Tools": {
        "volatility": "Memory forensics",
        "autopsy": "Digital forensics",
        "foremost": "File recovery",
        "scalpel": "Data carving"
    }
}

class SecurityMenu:
    def __init__(self):
        self.layout = Layout()
        self.config = self.load_config()
        self.current_category = None
        self.tools_status = self.check_tools_status()

    def load_config(self) -> Dict:
        """Load menu configuration"""
        config_file = Path.home() / '.security_toolkit' / 'config.yml'
        try:
            if config_file.exists():
                return yaml.safe_load(config_file.read_text())
            return {}
        except Exception as e:
            console.print(f"[red]Error loading config: {e}")
            return {}

    def check_tools_status(self) -> Dict:
        """Check installation status of tools"""
        status = {}
        with Progress(SpinnerColumn(), "[progress.description]{task.description}") as progress:
            task = progress.add_task("Checking tools...", total=len(TOOL_CATEGORIES))
            for category, tools in TOOL_CATEGORIES.items():
                for tool in tools:
                    # Implement actual tool checking logic here
                    status[tool] = self.check_tool_installation(tool)
                progress.advance(task)
        return status

    def check_tool_installation(self, tool: str) -> bool:
        """Check if a tool is installed"""
        # Implement actual tool checking logic here
        return True

    def display_header(self):
        """Display menu header"""
        console.print(Panel(
            "[bold cyan]Security Toolkit[/bold cyan]\n"
            "[green]Educational Security Tools[/green]",
            title="Main Menu",
            subtitle=f"Version {self.config.get('version', '2.7.4')}"
        ))

    def display_categories(self):
        """Display tool categories"""
        table = Table(title="Tool Categories")
        table.add_column("Category", style="cyan")
        table.add_column("Tools", style="green")
        table.add_column("Status", style="yellow")

        for category, tools in TOOL_CATEGORIES.items():
            installed = sum(1 for tool in tools if self.tools_status.get(tool, False))
            total = len(tools)
            table.add_row(
                category,
                f"{len(tools)} tools",
                f"{installed}/{total} installed"
            )

        console.print(table)

    def display_tools(self, category: str):
        """Display tools in a category"""
        if category not in TOOL_CATEGORIES:
            console.print("[red]Invalid category")
            return

        table = Table(title=f"{category} Tools")
        table.add_column("Tool", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Status", style="yellow")

        for tool, description in TOOL_CATEGORIES[category].items():
            status = "[green]Installed" if self.tools_status.get(tool, False) else "[red]Not Installed"
            table.add_row(tool, description, status)

        console.print(table)

    async def run_tool(self, tool: str):
        """Run a security tool"""
        with Progress(SpinnerColumn(), "[progress.description]{task.description}") as progress:
            task = progress.add_task(f"Running {tool}...", total=None)
            try:
                # Implement actual tool execution logic here
                await asyncio.sleep(2)  # Simulated tool execution
                progress.update(task, description=f"Completed {tool}")
            except Exception as e:
                console.print(f"[red]Error running {tool}: {e}")

    def install_tool(self, tool: str):
        """Install a security tool"""
        with Progress(SpinnerColumn(), "[progress.description]{task.description}") as progress:
            task = progress.add_task(f"Installing {tool}...", total=None)
            try:
                # Implement actual installation logic here
                progress.update(task, description=f"Installed {tool}")
                self.tools_status[tool] = True
            except Exception as e:
                console.print(f"[red]Installation failed: {e}")

    def main_loop(self):
        """Main menu loop"""
        while True:
            self.display_header()
            self.display_categories()

            choice = Prompt.ask(
                "\n[cyan]Choose a category or command[/cyan]",
                choices=list(TOOL_CATEGORIES.keys()) + ["quit", "update", "help"]
            )

            if choice.lower() == "quit":
                break
            elif choice.lower() == "update":
                self.update_tools()
            elif choice.lower() == "help":
                self.show_help()
            else:
                self.current_category = choice
                self.category_menu()

    def category_menu(self):
        """Category submenu"""
        while True:
            console.clear()
            self.display_header()
            self.display_tools(self.current_category)

            tool = Prompt.ask(
                "\n[cyan]Choose a tool or command[/cyan]",
                choices=list(TOOL_CATEGORIES[self.current_category].keys()) + ["back", "install"]
            )

            if tool.lower() == "back":
                break
            elif tool.lower() == "install":
                self.install_category_tools()
            else:
                asyncio.run(self.run_tool(tool))

    def update_tools(self):
        """Update all tools"""
        with Progress() as progress:
            task = progress.add_task("Updating tools...", total=100)
            # Implement update logic here
            progress.update(task, advance=100)

    def show_help(self):
        """Display help information"""
        console.print(Panel(
            "\n".join([
                "[cyan]Available Commands:[/cyan]",
                "- Select category number to view tools",
                "- 'update' to update all tools",
                "- 'quit' to exit",
                "- 'help' to show this help",
                "\n[yellow]Tool Categories:[/yellow]",
                *[f"- {cat}" for cat in TOOL_CATEGORIES.keys()]
            ]),
            title="Help"
        ))
        input("\nPress Enter to continue...")

    def install_category_tools(self):
        """Install all tools in current category"""
        tools = TOOL_CATEGORIES[self.current_category]
        with Progress() as progress:
            task = progress.add_task("Installing tools...", total=len(tools))
            for tool in tools:
                self.install_tool(tool)
                progress.advance(task)

def main():
    """Main entry point"""
    try:
        menu = SecurityMenu()
        menu.main_loop()
    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting Security Toolkit...[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    main()
