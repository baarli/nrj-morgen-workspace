#!/usr/bin/env python3
"""
📅 BAARLICLAW DATE TOOLKIT
Dato- og tidshåndtering
"""

from datetime import datetime, timedelta, date
from typing import Optional, List, Tuple, Union
import calendar

class DateUtils:
    """Date utilities"""
    
    @staticmethod
    def now() -> datetime:
        """Get current datetime"""
        return datetime.now()
    
    @staticmethod
    def today() -> date:
        """Get current date"""
        return date.today()
    
    @staticmethod
    def parse(date_string: str, fmt: str = "%Y-%m-%d") -> Optional[datetime]:
        """Parse date from string"""
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            return None
    
    @staticmethod
    def format(dt: Union[datetime, date], fmt: str = "%Y-%m-%d") -> str:
        """Format date to string"""
        return dt.strftime(fmt)
    
    @staticmethod
    def add_days(dt: datetime, days: int) -> datetime:
        """Add days to date"""
        return dt + timedelta(days=days)
    
    @staticmethod
    def add_hours(dt: datetime, hours: int) -> datetime:
        """Add hours to datetime"""
        return dt + timedelta(hours=hours)
    
    @staticmethod
    def start_of_day(dt: datetime) -> datetime:
        """Get start of day"""
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def end_of_day(dt: datetime) -> datetime:
        """Get end of day"""
        return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    @staticmethod
    def start_of_week(dt: datetime) -> datetime:
        """Get start of week (Monday)"""
        return DateUtils.start_of_day(dt - timedelta(days=dt.weekday()))
    
    @staticmethod
    def end_of_week(dt: datetime) -> datetime:
        """Get end of week (Sunday)"""
        return DateUtils.end_of_day(dt + timedelta(days=6 - dt.weekday()))
    
    @staticmethod
    def start_of_month(dt: datetime) -> datetime:
        """Get start of month"""
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def end_of_month(dt: datetime) -> datetime:
        """Get end of month"""
        last_day = calendar.monthrange(dt.year, dt.month)[1]
        return dt.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)
    
    @staticmethod
    def is_weekend(dt: datetime) -> bool:
        """Check if weekend"""
        return dt.weekday() >= 5
    
    @staticmethod
    def is_today(dt: datetime) -> bool:
        """Check if date is today"""
        return dt.date() == date.today()
    
    @staticmethod
    def days_between(start: datetime, end: datetime) -> int:
        """Get days between two dates"""
        return (end.date() - start.date()).days
    
    @staticmethod
    def age(birth_date: date) -> int:
        """Calculate age from birth date"""
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

class TimeUtils:
    """Time utilities"""
    
    @staticmethod
    def seconds_to_human(seconds: int) -> str:
        """Convert seconds to human readable"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m {seconds % 60}s"
        elif seconds < 86400:
            hours = seconds // 3600
            mins = (seconds % 3600) // 60
            return f"{hours}h {mins}m"
        else:
            days = seconds // 86400
            hours = (seconds % 86400) // 3600
            return f"{days}d {hours}h"
    
    @staticmethod
    def human_to_seconds(time_str: str) -> int:
        """Convert human readable time to seconds"""
        total = 0
        parts = time_str.split()
        
        for part in parts:
            if part.endswith('d'):
                total += int(part[:-1]) * 86400
            elif part.endswith('h'):
                total += int(part[:-1]) * 3600
            elif part.endswith('m'):
                total += int(part[:-1]) * 60
            elif part.endswith('s'):
                total += int(part[:-1])
        
        return total

# === CONVENIENCE FUNCTIONS ===
def now_str(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Quick now string"""
    return DateUtils.format(DateUtils.now(), fmt)

def today_str() -> str:
    """Quick today string"""
    return DateUtils.format(DateUtils.today())

def parse_date(date_string: str) -> Optional[datetime]:
    """Quick date parse"""
    return DateUtils.parse(date_string)

# === TESTING ===
if __name__ == "__main__":
    print("📅 BaarliClaw Date Toolkit - Testing")
    print("=" * 50)
    
    # Test basic functions
    print("\n🧪 Testing Basic Functions")
    print(f"  Now: {now_str()}")
    print(f"  Today: {today_str()}")
    
    # Test parsing
    print("\n🧪 Testing Date Parsing")
    dt = parse_date("2026-02-27")
    print(f"  Parsed: {dt}")
    
    # Test date operations
    print("\n🧪 Testing Date Operations")
    now = DateUtils.now()
    print(f"  Start of day: {DateUtils.format(DateUtils.start_of_day(now))}")
    print(f"  Start of week: {DateUtils.format(DateUtils.start_of_week(now))}")
    print(f"  Start of month: {DateUtils.format(DateUtils.start_of_month(now))}")
    
    tomorrow = DateUtils.add_days(now, 1)
    print(f"  Tomorrow: {DateUtils.format(tomorrow)}")
    
    # Test time utils
    print("\n🧪 Testing Time Utils")
    print(f"  3665s = {TimeUtils.seconds_to_human(3665)}")
    print(f"  90061s = {TimeUtils.seconds_to_human(90061)}")
    print(f"  '2h 30m' = {TimeUtils.human_to_seconds('2h 30m')}s")
    
    # Test checks
    print("\n🧪 Testing Date Checks")
    print(f"  Is today today? {DateUtils.is_today(now)}")
    print(f"  Is weekend today? {DateUtils.is_weekend(now)}")
    
    print("\n✅ Date Toolkit ready!")
