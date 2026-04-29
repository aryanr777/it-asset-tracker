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