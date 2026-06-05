import click
from rich.console import Console
from tracker import AssetTracker
import reporter

console = Console()

# @click.group() means main.py is a group of sub-commands (list, find, audit, etc.)
@click.group()
def cli():
    """EdgeShield IT Asset Tracker — manage and audit device inventories."""
    pass

# ── list command ──────────────────────────────────────────────────────────────
@cli.command()
@click.option("--location", "-l", default=None, help="Filter by location (e.g. Rydalmere)")
@click.option("--status", "-s", default=None, help="Filter by status (active/offboarded/unassigned)")
def list(location, status):
    """List all assets, with optional filters."""
    tracker = AssetTracker()
    assets = tracker.assets
    
    if location:
        assets = tracker.filter_by_location(location)
    if status:
        assets = [a for a in assets if a.status == status.lower()]

    title = "Asset Inventory"
    if location: 
        title += f" · {location}"
    if status: 
        title += f" · {status}"

    reporter.print_assets_table(assets, title=title)

# ── find command ──────────────────────────────────────────────────────────────
@cli.command()
@click.option("--assignee", "-a", required=True, help="Name (or partial name) to search")
def find(assignee):
    """Find all assets assigned to a person (partial name match)."""
    tracker = AssetTracker()
    results = tracker.find_by_assignee(assignee)
    reporter.print_assets_table(results, title=f"Assets for '{assignee}'")

# ── audit command ─────────────────────────────────────────────────────────────
@cli.command()
@click.option("--days", "-d", default=90, help="Flag assets assigned longer than N days (default 90)")
def audit(days):
    """Flag active assets that have been assigned longer than --days."""
    tracker = AssetTracker()
    overdue = tracker.get_overdue(threshold_days=days)
    reporter.print_audit_report(overdue)

# ── report command ────────────────────────────────────────────────────────────
@cli.command()
@click.option("--output", "-o", default="report.txt", help="Output file path")
@click.option("--location", "-l", default=None, help="Only include assets from this location")
def report(output, location):
    """Export a full report to a text file."""
    tracker = AssetTracker()
    assets = tracker.filter_by_location(location) if location else tracker.assets
    reporter.export_report(assets, output)

# ── add command ───────────────────────────────────────────────────────────────
@cli.command()
@click.option("--tag", required=True, help="Asset tag (e.g. LAP-0042)")
@click.option("--model", required=True)
@click.option("--serial", default="")
@click.option("--assignee", default="")
@click.option("--location", required=True)
@click.option("--notes", default="")
def add(tag, model, serial, assignee, location, notes):
    """Add a new asset to the inventory."""
    tracker = AssetTracker()
    tracker.add_asset(tag, model, serial, assignee, location, notes)
    console.print(f"[bold green]✓ Added {tag} — {model}[/bold green]")

# This makes the CLI run when you execute "python main.py"
if __name__ == "__main__":
    cli()