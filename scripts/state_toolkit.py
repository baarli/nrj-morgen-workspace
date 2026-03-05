#!/usr/bin/env python3
"""
🔄 BAARLICLAW STATE TOOLKIT
Tilstandshåndtering
"""

from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass, field
from copy import deepcopy

@dataclass
class StateChange:
    """State change record"""
    key: str
    old_value: Any
    new_value: Any
    timestamp: float

class StateManager:
    """Manage application state"""
    
    def __init__(self, initial_state: Optional[Dict] = None):
        self._state = initial_state or {}
        self._listeners: Dict[str, List[Callable]] = {}
        self._history: List[StateChange] = []
        self._max_history = 100
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get state value"""
        return self._state.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set state value"""
        old_value = self._state.get(key)
        
        if old_value != value:
            self._state[key] = value
            
            # Record change
            import time
            change = StateChange(key, old_value, value, time.time())
            self._history.append(change)
            
            if len(self._history) > self._max_history:
                self._history.pop(0)
            
            # Notify listeners
            self._notify(key, old_value, value)
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple values"""
        for key, value in updates.items():
            self.set(key, value)
    
    def subscribe(self, key: str, callback: Callable):
        """Subscribe to state changes"""
        if key not in self._listeners:
            self._listeners[key] = []
        self._listeners[key].append(callback)
    
    def unsubscribe(self, key: str, callback: Callable):
        """Unsubscribe from state changes"""
        if key in self._listeners and callback in self._listeners[key]:
            self._listeners[key].remove(callback)
    
    def _notify(self, key: str, old_value: Any, new_value: Any):
        """Notify listeners"""
        for callback in self._listeners.get(key, []):
            try:
                callback(key, old_value, new_value)
            except Exception as e:
                print(f"Error notifying listener: {e}")
    
    def get_state(self) -> Dict:
        """Get full state copy"""
        return deepcopy(self._state)
    
    def set_state(self, state: Dict):
        """Set full state"""
        self._state = deepcopy(state)
    
    def get_history(self) -> List[StateChange]:
        """Get change history"""
        return self._history.copy()
    
    def reset(self):
        """Reset state"""
        self._state.clear()
        self._history.clear()

class ObservableValue:
    """Observable value"""
    
    def __init__(self, initial_value: Any = None):
        self._value = initial_value
        self._listeners: List[Callable] = []
    
    @property
    def value(self) -> Any:
        return self._value
    
    @value.setter
    def value(self, new_value: Any):
        if self._value != new_value:
            old_value = self._value
            self._value = new_value
            self._notify(old_value, new_value)
    
    def subscribe(self, callback: Callable):
        """Subscribe to changes"""
        self._listeners.append(callback)
    
    def unsubscribe(self, callback: Callable):
        """Unsubscribe from changes"""
        if callback in self._listeners:
            self._listeners.remove(callback)
    
    def _notify(self, old_value: Any, new_value: Any):
        """Notify listeners"""
        for callback in self._listeners:
            callback(old_value, new_value)

class Store:
    """Simple store (like Redux)"""
    
    def __init__(self, reducer: Callable, initial_state: Optional[Dict] = None):
        self._reducer = reducer
        self._state = initial_state or {}
        self._listeners: List[Callable] = []
    
    def get_state(self) -> Dict:
        """Get current state"""
        return deepcopy(self._state)
    
    def dispatch(self, action: Dict):
        """Dispatch action"""
        self._state = self._reducer(self._state, action)
        self._notify()
    
    def subscribe(self, callback: Callable):
        """Subscribe to changes"""
        self._listeners.append(callback)
        return lambda: self._listeners.remove(callback)
    
    def _notify(self):
        """Notify listeners"""
        for callback in self._listeners:
            callback(self.get_state())

# === CONVENIENCE FUNCTIONS ===
def create_state(initial: Optional[Dict] = None) -> StateManager:
    """Quick state creation"""
    return StateManager(initial)

def observable(value: Any = None) -> ObservableValue:
    """Quick observable"""
    return ObservableValue(value)

# === TESTING ===
if __name__ == "__main__":
    print("🔄 BaarliClaw State Toolkit - Testing")
    print("=" * 50)
    
    # Test state manager
    print("\n🧪 Testing State Manager")
    
    state = StateManager({'count': 0})
    
    def on_count_change(key, old, new):
        print(f"  {key}: {old} -> {new}")
    
    state.subscribe('count', on_count_change)
    
    state.set('count', 1)
    state.set('count', 2)
    state.set('count', 2)  # No change, no notification
    
    print(f"  Current state: {state.get_state()}")
    
    # Test observable
    print("\n🧪 Testing Observable")
    
    obs = ObservableValue("initial")
    
    def on_change(old, new):
        print(f"  Observable: {old} -> {new}")
    
    obs.subscribe(on_change)
    obs.value = "changed"
    obs.value = "changed again"
    
    # Test store
    print("\n🧪 Testing Store")
    
    def counter_reducer(state, action):
        if action['type'] == 'INCREMENT':
            return {**state, 'count': state.get('count', 0) + 1}
        elif action['type'] == 'DECREMENT':
            return {**state, 'count': state.get('count', 0) - 1}
        return state
    
    store = Store(counter_reducer, {'count': 0})
    
    def on_state_change(state):
        print(f"  Store state: {state}")
    
    store.subscribe(on_state_change)
    
    store.dispatch({'type': 'INCREMENT'})
    store.dispatch({'type': 'INCREMENT'})
    store.dispatch({'type': 'DECREMENT'})
    
    print("\n✅ State Toolkit ready!")
