import csv
import os
from datetime import datetime, date
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Asset:
    # Each field maps directly to a column in assets.csv
    asset_tag: str
    model: str
    serial: str
    assignee: str
    location: str
    status: str
    assigned_date: Optional[date]
    return_date: Optional[date]
    notes: str

    def days_assigned(self) -> Optional[int]:
        """How many days since this asset was assigned."""
        if not self.assigned_date:
            return None
        # Use return_date if available, otherwise use today
        end = self.return_date or date.today()
        return (end - self.assigned_date).days

    def is_overdue(self, threshold_days: int = 90) -> bool:
        """True if active and assigned for more than threshold_days."""
        if self.status != "active":
            return False
        days = self.days_assigned()
        return days is not None and days > threshold_days
    

class AssetTracker:
    """Loads assets from CSV and provides filter/search methods."""

    def __init__(self, csv_path: str = "assets.csv"):
        self.csv_path = csv_path
        self.assets: List[Asset] = []
        self._load()

    def _parse_date(self, date_str: str) -> Optional[date]:
        if not date_str.strip():
            return None
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
        except ValueError:
            return None

    def _load(self):
        """Read CSV and convert every row into an Asset object."""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(
                f"Cannot find '{self.csv_path}'. Run from the project root."
            )
        with open(self.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.assets = []
            for row in reader:
                self.assets.append(Asset(
                    asset_tag=row["asset_tag"].strip(),
                    model=row["model"].strip(),
                    serial=row["serial"].strip(),
                    assignee=row["assignee"].strip(),
                    location=row["location"].strip(),
                    status=row["status"].strip().lower(),
                    assigned_date=self._parse_date(row["assigned_date"]),
                    return_date=self._parse_date(row["return_date"]),
                    notes=row["notes"].strip(),
                ))

    def filter_by_location(self, location: str) -> List[Asset]:
        return [a for a in self.assets if a.location.lower() == location.lower()]

    def filter_by_status(self, status: str) -> List[Asset]:
        return [a for a in self.assets if a.status == status.lower()]

    def find_by_assignee(self, name: str) -> List[Asset]:
        return [a for a in self.assets if name.lower() in a.assignee.lower()]

    def get_overdue(self, threshold_days: int = 90) -> List[Asset]:
        return [a for a in self.assets if a.is_overdue(threshold_days)]

    def add_asset(self, asset_tag, model, serial, assignee, location, notes=""):
        today = date.today().strftime("%Y-%m-%d")
        with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                asset_tag, model, serial, assignee,
                location, "active", today, "", notes
            ])
        self._load()    

        