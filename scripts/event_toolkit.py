#!/usr/bin/env python3
"""
📡 BAARLICLAW EVENT TOOLKIT
Event-drevet programmering
"""

from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    """Event data"""
    name: str
    data: Any
    timestamp: datetime
    source: Optional[str] = None

class EventEmitter:
    """Event emitter (like Node.js)"""
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
        self._once_listeners: Dict[str, List[Callable]] = {}
    
    def on(self, event: str, listener: Callable):
        """Add event listener"""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(listener)
        return self
    
    def once(self, event: str, listener: Callable):
        """Add one-time listener"""
        if event not in self._once_listeners:
            self._once_listeners[event] = []
        self._once_listeners[event].append(listener)
        return self
    
    def off(self, event: str, listener: Callable):
        """Remove event listener"""
        if event in self._listeners:
            if listener in self._listeners[event]:
                self._listeners[event].remove(listener)
        return self
    
    def emit(self, event: str, data: Any = None):
        """Emit event"""
        timestamp = datetime.now()
        event_obj = Event(event, data, timestamp)
        
        # Call regular listeners
        for listener in self._listeners.get(event, []):
            try:
                listener(event_obj)
            except Exception as e:
                print(f"Error in listener: {e}")
        
        # Call once listeners
        for listener in self._once_listeners.get(event, []):
            try:
                listener(event_obj)
            except Exception as e:
                print(f"Error in once listener: {e}")
        
        # Clear once listeners
        self._once_listeners[event] = []
    
    def listener_count(self, event: str) -> int:
        """Get number of listeners"""
        return len(self._listeners.get(event, []))
    
    def remove_all_listeners(self, event: Optional[str] = None):
        """Remove all listeners"""
        if event:
            self._listeners.pop(event, None)
            self._once_listeners.pop(event, None)
        else:
            self._listeners.clear()
            self._once_listeners.clear()

class EventBus:
    """Global event bus"""
    
    _instance: Optional['EventBus'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._emitter = EventEmitter()
        return cls._instance
    
    def subscribe(self, event: str, callback: Callable):
        """Subscribe to event"""
        self._emitter.on(event, callback)
    
    def publish(self, event: str, data: Any = None):
        """Publish event"""
        self._emitter.emit(event, data)

class Signal:
    """Simple signal/slot pattern"""
    
    def __init__(self):
        self._slots: List[Callable] = []
    
    def connect(self, slot: Callable):
        """Connect slot"""
        self._slots.append(slot)
    
    def disconnect(self, slot: Callable):
        """Disconnect slot"""
        if slot in self._slots:
            self._slots.remove(slot)
    
    def emit(self, *args, **kwargs):
        """Emit signal"""
        for slot in self._slots:
            slot(*args, **kwargs)

# === CONVENIENCE FUNCTIONS ===
def create_event_bus() -> EventBus:
    """Create/get event bus"""
    return EventBus()

def emit(event: str, data: Any = None):
    """Quick emit to global bus"""
    EventBus().publish(event, data)

def on(event: str, callback: Callable):
    """Quick subscribe to global bus"""
    EventBus().subscribe(event, callback)

# === TESTING ===
if __name__ == "__main__":
    print("📡 BaarliClaw Event Toolkit - Testing")
    print("=" * 50)
    
    # Test event emitter
    print("\n🧪 Testing Event Emitter")
    
    emitter = EventEmitter()
    
    def on_message(event):
        print(f"  Received: {event.name} = {event.data}")
    
    def on_once(event):
        print(f"  Once: {event.name} = {event.data}")
    
    emitter.on('message', on_message)
    emitter.once('message', on_once)
    
    emitter.emit('message', 'Hello!')
    emitter.emit('message', 'World!')
    
    # Test event bus
    print("\n🧪 Testing Event Bus")
    
    bus = EventBus()
    
    def handler(event):
        print(f"  Bus received: {event.name}")
    
    bus.subscribe('test', handler)
    bus.publish('test', {'key': 'value'})
    
    # Test signal
    print("\n🧪 Testing Signal")
    
    signal = Signal()
    
    def slot1(value):
        print(f"  Slot 1: {value}")
    
    def slot2(value):
        print(f"  Slot 2: {value}")
    
    signal.connect(slot1)
    signal.connect(slot2)
    signal.emit("Hello Signals!")
    
    print("\n✅ Event Toolkit ready!")
