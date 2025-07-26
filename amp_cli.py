#!/usr/bin/env python3
"""
AMP CLI - Automated Model Pipeline for GenX Trading Platform
Enhanced CLI with Typer for better user experience
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Typer app and Rich console
app = typer.Typer(help="AMP CLI - Automated Model Pipeline for GenX Trading Platform")
console = Console()

class AMPCLI:
    def __init__(self):
        self.project_root = Path.cwd()
        self.config_file = self.project_root / "amp_config.json"
        self.plugins_dir = self.project_root / "amp-plugins"
        self.env_file = self.project_root / ".env"
        
    def load_config(self) -> Dict:
        """Load AMP configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            "api_provider": "gemini",
            "plugins": [],
            "services": [],
            "dependencies": [],
            "env_vars": {}
        }
    
    def save_config(self, config: Dict):
        """Save AMP configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def update(self, env_file: Optional[str] = None, set_config: Optional[List[str]] = None, 
               add_dependency: Optional[List[str]] = None, add_env: Optional[List[str]] = None, 
               description: Optional[str] = None):
        """Main update command"""
        with console.status("[bold green]Starting GenX Trading Platform AMP Update..."):
            config = self.load_config()
            
            # Update configuration based on parameters
            if env_file:
                self._load_env_vars(env_file)
            
            if set_config:
                for setting in set_config:
                    if "=" in setting:
                        k, v = setting.split("=", 1)
                        config[k] = v
            
            if add_dependency:
                config.setdefault("dependencies", []).extend(add_dependency)
            
            if add_env:
                for env_var in add_env:
                    if "=" in env_var:
                        k, v = env_var.split("=", 1)
                        config.setdefault("env_vars", {})[k] = v
            
            if description:
                config["description"] = description
            
            self.save_config(config)
        
        console.print("✅ [bold green]Main AMP update complete!")
        
    def plugin_install(self, plugin_name: str, source: str = "genx-trading", 
                      enable_service: Optional[List[str]] = None, description: str = ""):
        """Install AMP plugin"""
        with console.status(f"[bold blue]Installing AMP plugin: {plugin_name}"):
            config = self.load_config()
            plugin_config = {
                "name": plugin_name,
                "source": source,
                "enabled": True,
                "services": enable_service or [],
                "description": description
            }
            
            config.setdefault("plugins", []).append(plugin_config)
            self.save_config(config)
        
        console.print(f"✅ [bold green]Plugin {plugin_name} installed successfully!")
    
    def config_set(self, api_provider: Optional[str] = None, enable_sentiment_analysis: Optional[bool] = None,
                   enable_social_signals: Optional[bool] = None, enable_news_feeds: Optional[bool] = None,
                   enable_websocket_streams: Optional[bool] = None):
        """Set AMP configuration"""
        with console.status("[bold blue]Configuring services..."):
            config = self.load_config()
            
            if api_provider:
                config["api_provider"] = api_provider
            
            if enable_sentiment_analysis is not None:
                config["enable_sentiment_analysis"] = enable_sentiment_analysis
            
            if enable_social_signals is not None:
                config["enable_social_signals"] = enable_social_signals
            
            if enable_news_feeds is not None:
                config["enable_news_feeds"] = enable_news_feeds
            
            if enable_websocket_streams is not None:
                config["enable_websocket_streams"] = enable_websocket_streams
            
            self.save_config(config)
        
        console.print("🔧 [bold green]Service configuration complete!")
    
    def service_enable(self, service: List[str]):
        """Enable services"""
        config = self.load_config()
        config.setdefault("enabled_services", []).extend(service)
        self.save_config(config)
        console.print(f"✅ [bold green]Services enabled: {', '.join(service)}")
    
    def verify(self, check_dependencies: bool = False, check_env_vars: bool = False,
               check_services: bool = False, check_api_keys: bool = False):
        """Verify installation"""
        with console.status("[bold blue]Verifying installation..."):
            config = self.load_config()
            
            if check_dependencies:
                self._check_dependencies(config.get("dependencies", []))
            
            if check_env_vars:
                self._check_env_vars(config.get("env_vars", {}))
            
            if check_services:
                self._check_services(config.get("enabled_services", []))
            
            if check_api_keys:
                self._check_api_keys()
        
        console.print("✅ [bold green]Installation verification complete!")
    
    def test(self, all_tests: bool = False):
        """Run tests"""
        if all_tests:
            with console.status("[bold blue]Running all tests..."):
                self._run_python_tests()
                self._run_node_tests()
        else:
            with console.status("[bold blue]Running specific tests..."):
                self._run_python_tests()
    
    def deploy(self):
        """Deploy to production"""
        with console.status("[bold blue]Deploying to production..."):
            self._run_docker_deploy()
    
    def _load_env_vars(self, env_file: str):
        """Load environment variables from file"""
        if Path(env_file).exists():
            console.print(f"📄 [blue]Loading environment variables from {env_file}")
    
    def _check_dependencies(self, dependencies: List[str]):
        """Check if dependencies are installed"""
        console.print("📦 [blue]Checking dependencies...")
        table = Table(title="Dependencies Status")
        table.add_column("Package", style="cyan")
        table.add_column("Status", style="green")
        
        for dep in dependencies:
            try:
                if ">=" in dep:
                    package = dep.split(">=")[0]
                else:
                    package = dep
                __import__(package.replace("-", "_"))
                table.add_row(package, "✅ Installed")
            except ImportError:
                table.add_row(package, "❌ Not installed")
        
        console.print(table)
    
    def _check_env_vars(self, env_vars: Dict[str, str]):
        """Check environment variables"""
        console.print("🔑 [blue]Checking environment variables...")
        table = Table(title="Environment Variables Status")
        table.add_column("Variable", style="cyan")
        table.add_column("Status", style="green")
        
        for key, value in env_vars.items():
            if os.getenv(key):
                table.add_row(key, "✅ Set")
            else:
                table.add_row(key, "❌ Not set")
        
        console.print(table)
    
    def _check_services(self, services: List[str]):
        """Check services"""
        console.print("🔧 [blue]Checking services...")
        table = Table(title="Services Status")
        table.add_column("Service", style="cyan")
        table.add_column("Status", style="green")
        
        for service in services:
            service_file = self.project_root / "api" / "services" / f"{service}.py"
            if service_file.exists():
                table.add_row(service, "✅ Available")
            else:
                table.add_row(service, "❌ Not found")
        
        console.print(table)
    
    def _check_api_keys(self):
        """Check API keys"""
        console.print("🔑 [blue]Checking API keys...")
        table = Table(title="API Keys Status")
        table.add_column("API Key", style="cyan")
        table.add_column("Status", style="green")
        
        required_keys = [
            "GEMINI_API_KEY",
            "BYBIT_API_KEY", 
            "BYBIT_API_SECRET"
        ]
        
        for key in required_keys:
            if os.getenv(key):
                table.add_row(key, "✅ Set")
            else:
                table.add_row(key, "❌ Not set")
        
        console.print(table)
    
    def _run_python_tests(self):
        """Run Python tests"""
        try:
            import subprocess
            subprocess.run([sys.executable, "run_tests.py"], check=True)
            console.print("✅ [bold green]Python tests passed!")
        except subprocess.CalledProcessError:
            console.print("❌ [bold red]Python tests failed!")
        except FileNotFoundError:
            console.print("⚠️ [yellow]run_tests.py not found")
    
    def _run_node_tests(self):
        """Run Node.js tests"""
        try:
            import subprocess
            subprocess.run(["npm", "test"], check=True)
            console.print("✅ [bold green]Node.js tests passed!")
        except subprocess.CalledProcessError:
            console.print("❌ [bold red]Node.js tests failed!")
        except FileNotFoundError:
            console.print("⚠️ [yellow]npm not found")
    
    def _run_docker_deploy(self):
        """Run Docker deployment"""
        try:
            import subprocess
            subprocess.run(["docker-compose", "-f", "docker-compose.production.yml", "up", "-d"], check=True)
            console.print("✅ [bold green]Docker deployment successful!")
        except subprocess.CalledProcessError:
            console.print("❌ [bold red]Docker deployment failed!")
        except FileNotFoundError:
            console.print("⚠️ [yellow]docker-compose not found")
    
    def show_status(self):
        """Show current AMP status"""
        config = self.load_config()
        
        # Create status panel
        status_text = f"""
[bold cyan]API Provider:[/bold cyan] {config.get('api_provider', 'Not set')}
[bold cyan]Plugins Installed:[/bold cyan] {len(config.get('plugins', []))}
[bold cyan]Services Enabled:[/bold cyan] {len(config.get('enabled_services', []))}
        """
        
        console.print(Panel(status_text, title="[bold blue]AMP Status Report", border_style="blue"))
        
        # Plugins table
        if config.get('plugins'):
            table = Table(title="Installed Plugins")
            table.add_column("Plugin", style="cyan")
            table.add_column("Source", style="blue")
            table.add_column("Status", style="green")
            table.add_column("Description", style="white")
            
            for plugin in config.get('plugins', []):
                status = "✅ Enabled" if plugin.get('enabled') else "❌ Disabled"
                table.add_row(
                    plugin['name'],
                    plugin.get('source', 'N/A'),
                    status,
                    plugin.get('description', 'No description')
                )
            
            console.print(table)
        
        # Services table
        if config.get('enabled_services'):
            table = Table(title="Enabled Services")
            table.add_column("Service", style="cyan")
            
            for service in config.get('enabled_services', []):
                table.add_row(service)
            
            console.print(table)
        
        # Features table
        features = [
            ('Sentiment Analysis', 'enable_sentiment_analysis'),
            ('Social Signals', 'enable_social_signals'),
            ('News Feeds', 'enable_news_feeds'),
            ('WebSocket Streams', 'enable_websocket_streams')
        ]
        
        table = Table(title="Features Status")
        table.add_column("Feature", style="cyan")
        table.add_column("Status", style="green")
        
        for feature_name, feature_key in features:
            status = '✅ Enabled' if config.get(feature_key) else '❌ Disabled'
            table.add_row(feature_name, status)
        
        console.print(table)

# Global AMP CLI instance
amp = AMPCLI()

@app.command()
def update(
    env_file: Optional[str] = typer.Option(None, "--env", help="Environment file"),
    set_config: Optional[List[str]] = typer.Option(None, "--set", help="Set configuration values"),
    add_dependency: Optional[List[str]] = typer.Option(None, "--add-dependency", help="Add dependencies"),
    add_env: Optional[List[str]] = typer.Option(None, "--add-env", help="Add environment variables"),
    description: Optional[str] = typer.Option(None, "--description", help="Description")
):
    """Update AMP configuration"""
    amp.update(env_file, set_config, add_dependency, add_env, description)

@app.command()
def plugin_install(
    plugin_name: str = typer.Argument(..., help="Plugin name"),
    source: str = typer.Option("genx-trading", "--source", help="Plugin source"),
    enable_service: Optional[List[str]] = typer.Option(None, "--enable-service", help="Enable services"),
    description: str = typer.Option("", "--description", help="Description")
):
    """Install AMP plugin"""
    amp.plugin_install(plugin_name, source, enable_service, description)

@app.command()
def config_set(
    api_provider: Optional[str] = typer.Option(None, "--api-provider", help="API provider"),
    enable_sentiment_analysis: Optional[bool] = typer.Option(None, "--enable-sentiment-analysis", help="Enable sentiment analysis"),
    enable_social_signals: Optional[bool] = typer.Option(None, "--enable-social-signals", help="Enable social signals"),
    enable_news_feeds: Optional[bool] = typer.Option(None, "--enable-news-feeds", help="Enable news feeds"),
    enable_websocket_streams: Optional[bool] = typer.Option(None, "--enable-websocket-streams", help="Enable WebSocket streams")
):
    """Set AMP configuration"""
    amp.config_set(api_provider, enable_sentiment_analysis, enable_social_signals, enable_news_feeds, enable_websocket_streams)

@app.command()
def service_enable(
    service: List[str] = typer.Argument(..., help="Services to enable")
):
    """Enable services"""
    amp.service_enable(service)

@app.command()
def verify(
    check_dependencies: bool = typer.Option(False, "--check-dependencies", help="Check dependencies"),
    check_env_vars: bool = typer.Option(False, "--check-env-vars", help="Check environment variables"),
    check_services: bool = typer.Option(False, "--check-services", help="Check services"),
    check_api_keys: bool = typer.Option(False, "--check-api-keys", help="Check API keys")
):
    """Verify installation"""
    amp.verify(check_dependencies, check_env_vars, check_services, check_api_keys)

@app.command()
def test(
    all_tests: bool = typer.Option(False, "--all", help="Run all tests")
):
    """Run tests"""
    amp.test(all_tests)

@app.command()
def deploy():
    """Deploy to production"""
    amp.deploy()

@app.command()
def status():
    """Show AMP status"""
    amp.show_status()

@app.command()
def run():
    """Run the next job"""
    console.print("🚀 [bold blue]AMP Job Runner - Starting Next Job")
    console.print("=" * 50)
    
    # Import and run the job runner
    try:
        from amp_job_runner import AMPJobRunner
        runner = AMPJobRunner()
        asyncio.run(runner.run_next_job())
    except ImportError:
        console.print("❌ [bold red]AMP Job Runner not found. Please ensure amp_job_runner.py exists.")

@app.command()
def auth(
    token: Optional[str] = typer.Option(None, "--token", help="Authentication token"),
    logout: bool = typer.Option(False, "--logout", help="Logout current user"),
    status: bool = typer.Option(False, "--status", help="Show authentication status")
):
    """Manage authentication"""
    try:
        from amp_auth import authenticate_user, check_auth, logout_user, get_user_info
        
        if logout:
            logout_user()
        elif status:
            if check_auth():
                user_info = get_user_info()
                console.print(f"✅ [bold green]Authenticated as: {user_info['user_id']}")
            else:
                console.print("❌ [bold red]Not authenticated")
        elif token:
            if authenticate_user(token):
                console.print("✅ [bold green]Authentication successful!")
            else:
                console.print("❌ [bold red]Authentication failed!")
        else:
            console.print("Please provide a token with --token or use --status to check current auth")
            
    except ImportError:
        console.print("❌ [bold red]Authentication module not found")

def main():
    """Main function"""
    app()

if __name__ == "__main__":
    main()