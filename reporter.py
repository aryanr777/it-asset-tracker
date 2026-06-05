from rich.console import Console
from rich.table import Table
from rich import box
from typing import List
from tracker import Asset

# Console is the Rich object that handles all output
console = Console()

# Status → colour mapping for the table
STATUS_COLOURS = {
    "active": "green",
    "offboarded": "dim",
    "unassigned": "yellow",
}

def print_assets_table(assets: List[Asset], title: str = "Asset Inventory"):
    """Print a formatted table of assets to the terminal."""
    if not assets:
        console.print("[yellow]No assets found matching your filters.[/yellow]")
        return

    # Create a Rich Table. box.ROUNDED gives it nice rounded corners.
    table = Table(title=title, box=box.ROUNDED, show_header=True)

    # Add columns — style= controls the colour of that column's text
    table.add_column("Tag", style="bold cyan", no_wrap=True)
    table.add_column("Model")
    table.add_column("Assignee")
    table.add_column("Location")
    table.add_column("Status")
    table.add_column("Days Assigned", justify="right")
    table.add_column("Notes", style="dim")

    for a in assets:
        colour = STATUS_COLOURS.get(a.status, "white")
        days = a.days_assigned()
        days_str = str(days) if days is not None else "—"
        
        # Highlight overdue assets in red
        if a.is_overdue():
            days_str = f"[bold red]{days_str} ⚠[/bold red]"

        table.add_row(
            a.asset_tag,
            a.model,
            a.assignee or "[dim]Unassigned[/dim]",
            a.location,
            f"[{colour}]{a.status}[/{colour}]",
            days_str,
            a.notes,
        )

    console.print(table)
    console.print(f"[dim] {len(assets)} asset(s) shown[/dim]")

def print_audit_report(overdue: List[Asset]):
    """Print a summary of overdue/flagged assets."""
    if not overdue:
        console.print("[bold green]✓ All assets are within acceptable assignment periods.[/bold green]")
        return

    console.print(f"\n[bold red]⚠ {len(overdue)} asset(s) flagged for audit[/bold red]\n")
    print_assets_table(overdue, title="Overdue Assets")

def export_report(assets: List[Asset], output_path: str):
    """Export the asset list to a plain-text file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"IT Asset Report — Generated {__import__('datetime').date.today()}\n")
        f.write("=" * 60 + "\n\n")
        for a in assets:
            overdue_flag = " *** OVERDUE ***" if a.is_overdue() else ""
            f.write(f"[{a.asset_tag}] {a.model}{overdue_flag}\n")
            f.write(f"  Assignee : {a.assignee or 'Unassigned'}\n")
            f.write(f"  Location : {a.location}\n")
            f.write(f"  Status   : {a.status}\n")
            f.write(f"  Days     : {a.days_assigned() or '—'}\n")
            if a.notes:
                f.write(f"  Notes    : {a.notes}\n")
            f.write("\n")

    console.print(f"[green]✓ Report exported to [bold]{output_path}[/bold][/green]")