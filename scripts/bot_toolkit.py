#!/usr/bin/env python3
"""
🤖 BAARLICLAW BOT TOOLKIT
Slack og Discord bot-rammeverk
"""

import os
import sys
import json
import re
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from datetime import datetime

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("BotToolkit")

@dataclass
class BotMessage:
    """Bot message structure"""
    text: str
    channel: str
    user: Optional[str] = None
    timestamp: Optional[str] = None
    attachments: List[Dict] = None
    
    def __post_init__(self):
        if self.attachments is None:
            self.attachments = []

class SlackBot:
    """Slack bot framework"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get('SLACK_BOT_TOKEN', '')
        self.commands: Dict[str, Callable] = {}
        self.handlers: Dict[str, List[Callable]] = {
            'message': [],
            'mention': [],
            'reaction': []
        }
    
    def command(self, name: str):
        """Decorator for bot commands"""
        def decorator(func: Callable):
            self.commands[name] = func
            return func
        return decorator
    
    def on(self, event: str):
        """Decorator for event handlers"""
        def decorator(func: Callable):
            if event in self.handlers:
                self.handlers[event].append(func)
            return func
        return decorator
    
    def parse_command(self, text: str) -> tuple:
        """Parse command from message text"""
        # Match !command or /command
        match = re.match(r'^[!/](\w+)\s*(.*)', text)
        if match:
            return match.group(1), match.group(2).strip()
        return None, None
    
    def process_message(self, message: Dict) -> Optional[str]:
        """Process incoming message"""
        text = message.get('text', '')
        channel = message.get('channel', '')
        user = message.get('user', '')
        
        # Check for commands
        cmd_name, args = self.parse_command(text)
        if cmd_name and cmd_name in self.commands:
            try:
                result = self.commands[cmd_name](args, user, channel)
                return result
            except Exception as e:
                logger.error(f"Command error: {e}")
                return f"Error: {e}"
        
        # Trigger message handlers
        for handler in self.handlers['message']:
            try:
                handler(text, user, channel)
            except Exception as e:
                logger.error(f"Handler error: {e}")
        
        return None
    
    def send_message(self, channel: str, text: str, 
                    attachments: Optional[List[Dict]] = None) -> bool:
        """Send message to Slack"""
        # This would use Slack API in production
        logger.info(f"[SLACK] #{channel}: {text}")
        return True
    
    def send_dm(self, user: str, text: str) -> bool:
        """Send direct message"""
        logger.info(f"[SLACK DM] @{user}: {text}")
        return True

class DiscordBot:
    """Discord bot framework"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get('DISCORD_BOT_TOKEN', '')
        self.prefix = '!'
        self.commands: Dict[str, Callable] = {}
        self.event_handlers: Dict[str, List[Callable]] = {
            'message': [],
            'ready': [],
            'member_join': []
        }
    
    def command(self, name: str, description: str = ""):
        """Register a command"""
        def decorator(func: Callable):
            self.commands[name] = {
                'func': func,
                'description': description
            }
            return func
        return decorator
    
    def event(self, event_type: str):
        """Register event handler"""
        def decorator(func: Callable):
            if event_type in self.event_handlers:
                self.event_handlers[event_type].append(func)
            return func
        return decorator
    
    def parse_message(self, content: str) -> tuple:
        """Parse command from message"""
        if content.startswith(self.prefix):
            parts = content[len(self.prefix):].split(maxsplit=1)
            cmd = parts[0] if parts else None
            args = parts[1] if len(parts) > 1 else ""
            return cmd, args
        return None, None
    
    def process_message(self, message: Dict) -> Optional[str]:
        """Process a message"""
        content = message.get('content', '')
        author = message.get('author', {})
        channel = message.get('channel_id', '')
        
        # Ignore bot messages
        if author.get('bot', False):
            return None
        
        # Parse command
        cmd_name, args = self.parse_message(content)
        if cmd_name and cmd_name in self.commands:
            try:
                return self.commands[cmd_name]['func'](args, author, channel)
            except Exception as e:
                logger.error(f"Command error: {e}")
                return f"Error: {e}"
        
        # Trigger event handlers
        for handler in self.event_handlers['message']:
            try:
                handler(content, author, channel)
            except Exception as e:
                logger.error(f"Handler error: {e}")
        
        return None
    
    def send_message(self, channel_id: str, content: str) -> bool:
        """Send message to channel"""
        logger.info(f"[DISCORD] #{channel_id}: {content}")
        return True
    
    def send_embed(self, channel_id: str, title: str, 
                  description: str, color: int = 0x3498db) -> bool:
        """Send embed message"""
        logger.info(f"[DISCORD EMBED] #{channel_id}: {title}")
        return True

class BotResponseBuilder:
    """Build rich bot responses"""
    
    @staticmethod
    def slack_attachment(title: str, text: str, 
                        color: str = "good",
                        fields: Optional[List[Dict]] = None) -> Dict:
        """Build Slack attachment"""
        attachment = {
            "title": title,
            "text": text,
            "color": color,
            "ts": datetime.now().timestamp()
        }
        if fields:
            attachment["fields"] = fields
        return attachment
    
    @staticmethod
    def discord_embed(title: str, description: str,
                     fields: Optional[List[Dict]] = None,
                     color: int = 0x3498db) -> Dict:
        """Build Discord embed"""
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.now().isoformat()
        }
        if fields:
            embed["fields"] = fields
        return embed
    
    @staticmethod
    def progress_bar(current: int, total: int, length: int = 20) -> str:
        """Create text progress bar"""
        filled = int(length * current / total) if total > 0 else 0
        bar = '█' * filled + '░' * (length - filled)
        pct = (current / total * 100) if total > 0 else 0
        return f"[{bar}] {pct:.1f}%"
    
    @staticmethod
    def table(headers: List[str], rows: List[List[str]]) -> str:
        """Create text table"""
        # Calculate column widths
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))
        
        # Build table
        lines = []
        
        # Header
        header_row = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
        lines.append(header_row)
        lines.append("-" * len(header_row))
        
        # Rows
        for row in rows:
            lines.append(" | ".join(str(c).ljust(w) for c, w in zip(row, widths)))
        
        return "\n".join(lines)

# === PRE-BUILT COMMANDS ===
def create_default_slack_bot() -> SlackBot:
    """Create a Slack bot with default commands"""
    bot = SlackBot()
    
    @bot.command("help")
    def help_cmd(args, user, channel):
        return """Available commands:
• !help - Show this help
• !status - Check system status
• !time - Show current time
• !ping - Check latency"""
    
    @bot.command("status")
    def status_cmd(args, user, channel):
        import subprocess
        try:
            load = subprocess.run(['uptime'], capture_output=True, text=True)
            return f"System status: {load.stdout.strip()}"
        except:
            return "Status unavailable"
    
    @bot.command("time")
    def time_cmd(args, user, channel):
        return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    @bot.command("ping")
    def ping_cmd(args, user, channel):
        return "🏓 Pong!"
    
    return bot

def create_default_discord_bot() -> DiscordBot:
    """Create a Discord bot with default commands"""
    bot = DiscordBot()
    
    @bot.command("help", "Show available commands")
    def help_cmd(args, author, channel):
        commands_list = "\n".join([
            f"`!{name}` - {cmd['description']}"
            for name, cmd in bot.commands.items()
        ])
        return f"**Available commands:**\n{commands_list}"
    
    @bot.command("ping", "Check bot latency")
    def ping_cmd(args, author, channel):
        return "🏓 Pong!"
    
    @bot.command("info", "Show bot info")
    def info_cmd(args, author, channel):
        return "🤖 BaarliClaw Bot v1.0"
    
    return bot

# === TESTING ===
if __name__ == "__main__":
    print("🤖 BaarliClaw Bot Toolkit - Testing")
    print("=" * 50)
    
    # Test Slack bot
    print("\n🧪 Testing Slack Bot")
    slack = create_default_slack_bot()
    
    test_messages = [
        {"text": "!help", "channel": "general", "user": "U123"},
        {"text": "!time", "channel": "general", "user": "U123"},
        {"text": "!ping", "channel": "general", "user": "U123"},
    ]
    
    for msg in test_messages:
        response = slack.process_message(msg)
        print(f"  Input: {msg['text']}")
        print(f"  Output: {response}")
        print()
    
    # Test Discord bot
    print("🧪 Testing Discord Bot")
    discord = create_default_discord_bot()
    
    test_msgs = [
        {"content": "!help", "channel_id": "123", "author": {"id": "U1", "bot": False}},
        {"content": "!ping", "channel_id": "123", "author": {"id": "U1", "bot": False}},
    ]
    
    for msg in test_msgs:
        response = discord.process_message(msg)
        print(f"  Input: {msg['content']}")
        print(f"  Output: {response}")
        print()
    
    # Test response builder
    print("🧪 Testing Response Builder")
    builder = BotResponseBuilder()
    
    progress = builder.progress_bar(75, 100)
    print(f"  Progress: {progress}")
    
    table = builder.table(
        ["Name", "Status", "Count"],
        [["Task 1", "Done", "10"], ["Task 2", "Pending", "5"]]
    )
    print(f"  Table:\n{table}")
    
    print("\n✅ Bot Toolkit ready!")
