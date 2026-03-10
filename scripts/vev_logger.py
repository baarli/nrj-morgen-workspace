#!/usr/bin/env python3
"""
VEV UNIFIED LOGGER
Standardisert logging for alle NRJ Morgen scripts
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

class VevLogger:
    """
    Standardisert logger for Vev-systemet
    
    Bruk:
        from vev_logger import VevLogger
        
        logger = VevLogger('my-script')
        logger.info("Starting process")
        logger.error("Something failed", extra={'context': 'details'})
    """
    
    BASE_LOG_DIR = Path('/root/.openclaw/workspace/brain/logs/vev')
    
    def __init__(self, name: str, log_dir: str = None, level=logging.INFO):
        """
        Initialize logger
        
        Args:
            name: Logger name (brukes i filnavn og logg-meldinger)
            log_dir: Custom log directory (default: brain/logs/vev/{name}/)
            level: Logging level (default: INFO)
        """
        self.name = name
        self.logger = logging.getLogger(f'vev.{name}')
        self.logger.setLevel(level)
        
        # Unngå duplikat handlers
        if self.logger.handlers:
            return
        
        # Setup directories
        if log_dir:
            self.log_dir = Path(log_dir)
        else:
            self.log_dir = self.BASE_LOG_DIR / name
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Formater
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 1. Daglig loggfil (INFO+)
        daily_file = self.log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        file_handler = logging.FileHandler(daily_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # 2. Roterende error-logg (ERROR+)
        error_file = self.log_dir / 'errors.log'
        error_handler = RotatingFileHandler(
            error_file, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        
        # 3. Konsoll output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
        
        # Structured logging file
        self.structured_file = self.log_dir / 'structured.jsonl'
    
    def debug(self, msg: str, extra: dict = None):
        """Log debug message"""
        self.logger.debug(msg, extra=extra)
    
    def info(self, msg: str, extra: dict = None):
        """Log info message"""
        self.logger.info(msg, extra=extra)
    
    def warning(self, msg: str, extra: dict = None):
        """Log warning message"""
        self.logger.warning(msg, extra=extra)
    
    def error(self, msg: str, extra: dict = None):
        """Log error message"""
        self.logger.error(msg, extra=extra)
        # Also write to structured log
        self._structured_log('ERROR', msg, extra)
    
    def critical(self, msg: str, extra: dict = None):
        """Log critical message"""
        self.logger.critical(msg, extra=extra)
        self._structured_log('CRITICAL', msg, extra)
    
    def _structured_log(self, level: str, message: str, data: dict = None):
        """Write structured JSON log entry"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'logger': self.name,
            'level': level,
            'message': message,
            'data': data or {}
        }
        
        with open(self.structured_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def log_metric(self, metric_name: str, value: float, unit: str = None):
        """Log a metric value"""
        self._structured_log('METRIC', metric_name, {
            'value': value,
            'unit': unit
        })
    
    def log_event(self, event_type: str, details: dict):
        """Log an event"""
        self._structured_log('EVENT', event_type, details)


# Convenience function for quick setup
def get_logger(name: str) -> VevLogger:
    """Get or create a VevLogger instance"""
    return VevLogger(name)


# Example usage
if __name__ == '__main__':
    # Demo
    logger = VevLogger('demo')
    
    logger.info("Starting demo")
    logger.warning("This is a warning")
    logger.error("This is an error", extra={'context': 'demo'})
    logger.log_metric('processing_time', 1.23, 'seconds')
    logger.log_event('user_action', {'action': 'click', 'target': 'button'})
    
    print(f"\nLogs written to: {logger.log_dir}")
