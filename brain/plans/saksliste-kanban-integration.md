# VEV SAKSLISTE & KANBAN INTEGRATION PLAN
## Full Task Management System for NRJ Morgen

**Date:** 2026-03-05  
**Goal:** Complete saksliste functionality with Kanban board connected to Vev

---

## 🎯 SYSTEM OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│                     TASK MANAGEMENT SYSTEM                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   MORNING   │───▶│    VEV      │───▶│   KANBAN    │         │
│  │   ROUTINE   │    │   BRAIN     │    │    BOARD    │         │
│  │             │    │             │    │             │         │
│  │ • Fetch news│    │ • Analyze   │    │ • Backlog   │         │
│  │ • Generate  │    │ • Prioritize│    │ • Research  │         │
│  │ • Insert to │    │ • Assign    │    │ • Write     │         │
│  │   Supabase  │    │   tasks     │    │ • Review    │         │
│  └─────────────┘    └─────────────┘    │ • Done      │         │
│                                         └─────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 PHASE 1: SAKSLISTE DATA INTEGRATION

### Current State:
- Saksliste data is in Supabase `agenda_items` table
- Morning Routine inserts stories automatically
- No visualization in Mission Control

### Implementation:

#### 1.1 Create Saksliste Service
```javascript
// src/services/sakslisteService.js
export const fetchSaksliste = async (date) => {
  const { data, error } = await supabase
    .from('agenda_items')
    .select('*')
    .eq('date', date)
    .order('position', { ascending: true })
  
  return { data, error }
}

export const updateSakslisteItem = async (id, updates) => {
  const { data, error } = await supabase
    .from('agenda_items')
    .update(updates)
    .eq('id', id)
  
  return { data, error }
}

export const addSakslisteItem = async (item) => {
  const { data, error } = await supabase
    .from('agenda_items')
    .insert(item)
  
  return { data, error }
}
```

#### 1.2 Create Saksliste Widget
```jsx
// src/components/widgets/SakslisteWidget.jsx
export default function SakslisteWidget() {
  const [items, setItems] = useState([])
  const [selectedDate, setSelectedDate] = useState(new Date())
  
  useEffect(() => {
    loadSaksliste()
  }, [selectedDate])
  
  const loadSaksliste = async () => {
    const dateStr = format(selectedDate, 'yyyy-MM-dd')
    const { data } = await fetchSaksliste(dateStr)
    setItems(data || [])
  }
  
  return (
    <div className="glass p-4 rounded-panel border border-cyan-neon/20">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-white">Saksliste</h3>
        <span className="text-xs text-cyan-neon font-mono">
          {items.length} saker
        </span>
      </div>
      
      <div className="space-y-2 max-h-60 overflow-y-auto">
        {items.map((item, index) => (
          <div key={item.id} className="flex items-start gap-3 p-2 rounded-lg bg-white/5">
            <span className="text-xs font-mono text-cyan-neon">{index + 1}</span>
            <div className="flex-1">
              <p className="text-xs text-white font-medium">{item.title}</p>
              <p className="text-[10px] text-gray-500 truncate">{item.description}</p>
            </div>
            <div className={`w-2 h-2 rounded-full ${
              item.status === 'published' ? 'bg-status-online' : 'bg-status-warning'
            }`} />
          </div>
        ))}
      </div>
    </div>
  )
}
```

---

## 📋 PHASE 2: KANBAN BOARD FOR VEV

### Board Structure:
```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   BACKLOG   │  RESEARCH   │   WRITE     │   REVIEW    │    DONE     │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│             │             │             │             │             │
│  • Story 1  │  • Story 3  │  • Story 5  │  • Story 7  │  • Story 9  │
│  • Story 2  │  • Story 4  │  • Story 6  │             │  • Story 10 │
│             │             │             │             │             │
│  [+ Add]    │             │             │             │             │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

### Columns:
1. **Backlog** - New stories from Morning Routine
2. **Research** - Gathering information
3. **Write** - Creating content
4. **Review** - Quality check
5. **Done** - Published to saksliste

### Implementation:

#### 2.1 Update Database Schema
```sql
-- Add task management tables
CREATE TABLE vev_tasks (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  title text NOT NULL,
  description text,
  column_id text NOT NULL, -- 'backlog', 'research', 'write', 'review', 'done'
  priority text DEFAULT 'medium', -- 'low', 'medium', 'high', 'critical'
  source text, -- 'morning-routine', 'manual', 'telegram'
  agenda_item_id uuid REFERENCES agenda_items(id),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  completed_at timestamptz,
  assigned_to text DEFAULT 'vev',
  metadata jsonb DEFAULT '{}'::jsonb
);

-- Create index for fast queries
CREATE INDEX idx_vev_tasks_column ON vev_tasks(column_id);
CREATE INDEX idx_vev_tasks_created ON vev_tasks(created_at DESC);
```

#### 2.2 Create Kanban Board Component
```jsx
// src/components/KanbanBoard.jsx
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd'

const COLUMNS = [
  { id: 'backlog', title: 'Backlog', color: 'gray' },
  { id: 'research', title: 'Research', color: 'cyan' },
  { id: 'write', title: 'Write', color: 'violet' },
  { id: 'review', title: 'Review', color: 'amber' },
  { id: 'done', title: 'Done', color: 'green' }
]

export default function KanbanBoard() {
  const [tasks, setTasks] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  
  useEffect(() => {
    loadTasks()
    // Subscribe to real-time updates
    const subscription = supabase
      .from('vev_tasks')
      .on('*', payload => {
        loadTasks()
      })
      .subscribe()
    
    return () => subscription.unsubscribe()
  }, [])
  
  const loadTasks = async () => {
    const { data } = await supabase
      .from('vev_tasks')
      .select('*')
      .order('created_at', { ascending: false })
    
    setTasks(data || [])
    setIsLoading(false)
  }
  
  const onDragEnd = async (result) => {
    if (!result.destination) return
    
    const { draggableId, destination } = result
    const newColumn = destination.droppableId
    
    // Optimistic update
    setTasks(tasks.map(t => 
      t.id === draggableId ? { ...t, column_id: newColumn } : t
    ))
    
    // Update database
    await supabase
      .from('vev_tasks')
      .update({ 
        column_id: newColumn,
        updated_at: new Date().toISOString(),
        completed_at: newColumn === 'done' ? new Date().toISOString() : null
      })
      .eq('id', draggableId)
  }
  
  const tasksByColumn = COLUMNS.reduce((acc, col) => {
    acc[col.id] = tasks.filter(t => t.column_id === col.id)
    return acc
  }, {})
  
  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="flex gap-4 overflow-x-auto pb-4">
        {COLUMNS.map(column => (
          <div key={column.id} className="flex-shrink-0 w-72">
            <div className="glass p-3 rounded-panel border border-white/10">
              {/* Column Header */}
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold text-white">{column.title}</h3>
                <span className="text-xs text-gray-500 bg-white/5 px-2 py-0.5 rounded">
                  {tasksByColumn[column.id].length}
                </span>
              </div>
              
              {/* Tasks */}
              <Droppable droppableId={column.id}>
                {(provided) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.droppableProps}
                    className="space-y-2 min-h-[100px]"
                  >
                    {tasksByColumn[column.id].map((task, index) => (
                      <Draggable key={task.id} draggableId={task.id} index={index}>
                        {(provided, snapshot) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className={`
                              p-3 rounded-lg border transition-all
                              ${snapshot.isDragging 
                                ? 'bg-cyan-neon/10 border-cyan-neon/30 shadow-lg' 
                                : 'bg-white/5 border-white/10 hover:border-cyan-neon/20'}
                            `}
                          >
                            <p className="text-xs text-white font-medium mb-1">{task.title}</p>
                            <p className="text-[10px] text-gray-500 line-clamp-2">{task.description}</p>
                            
                            {/* Priority Badge */}
                            <div className="flex items-center gap-2 mt-2">
                              <span className={`
                                text-[9px] px-1.5 py-0.5 rounded
                                ${task.priority === 'critical' ? 'bg-status-danger/20 text-status-danger' :
                                  task.priority === 'high' ? 'bg-status-warning/20 text-status-warning' :
                                  task.priority === 'medium' ? 'bg-cyan-neon/20 text-cyan-neon' :
                                  'bg-gray-500/20 text-gray-400'}
                              `}>
                                {task.priority}
                              </span>
                              
                              {task.source === 'morning-routine' && (
                                <span className="text-[9px] text-violet-neon">🌅 Auto</span>
                              )}
                            </div>
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
              
              {/* Add Task Button */}
              {column.id === 'backlog' && (
                <button className="w-full mt-3 py-2 rounded-lg border border-dashed border-white/20 
                                 text-xs text-gray-500 hover:text-white hover:border-cyan-neon/30
                                 transition-colors">
                  + Legg til sak
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </DragDropContext>
  )
}
```

---

## 📋 PHASE 3: AUTOMATED TASK CREATION

### From Morning Routine to Kanban:
```javascript
// Automatic task creation when Morning Routine runs
const createTasksFromSaksliste = async (agendaItems) => {
  for (const item of agendaItems) {
    // Check if task already exists
    const { data: existing } = await supabase
      .from('vev_tasks')
      .select('id')
      .eq('agenda_item_id', item.id)
      .single()
    
    if (!existing) {
      // Create new task in backlog
      await supabase.from('vev_tasks').insert({
        title: item.title,
        description: item.description,
        column_id: 'backlog',
        priority: 'medium',
        source: 'morning-routine',
        agenda_item_id: item.id,
        metadata: {
          link_url: item.link_url,
          image_url: item.link_metadata?.image_url
        }
      })
    }
  }
}
```

### Auto-promotion Logic:
```javascript
// Vev can automatically move tasks based on rules
const autoPromoteTasks = async () => {
  // Move from backlog to research after 1 hour
  const staleTasks = await supabase
    .from('vev_tasks')
    .select('*')
    .eq('column_id', 'backlog')
    .lt('created_at', new Date(Date.now() - 3600000).toISOString())
  
  for (const task of staleTasks.data || []) {
    await supabase
      .from('vev_tasks')
      .update({ column_id: 'research' })
      .eq('id', task.id)
    
    // Notify user
    sendTelegramMessage(`📝 "${task.title}" er klar for research`)
  }
}
```

---

## 📋 PHASE 4: VEV INTEGRATION

### Task Commands:
```javascript
// Voice/Text commands Vev understands
const TASK_COMMANDS = {
  'flytt til research': (taskId) => moveTask(taskId, 'research'),
  'flytt til write': (taskId) => moveTask(taskId, 'write'),
  'marker ferdig': (taskId) => moveTask(taskId, 'done'),
  'legg til ny sak': (title) => createTask(title),
  'hva er neste': () => getNextTask(),
  'vis kanban': () => openKanbanBoard()
}
```

### Progress Updates:
```javascript
// Send progress to Telegram
const sendTaskUpdate = (task, oldColumn, newColumn) => {
  const messages = {
    'backlog→research': `🔍 Starter research på "${task.title}"`,
    'research→write': `✍️ Skriver om "${task.title}"`,
    'write→review': `👀 Kvalitetssjekk av "${task.title}"`,
    'review→done': `✅ "${task.title}" er publisert!`
  }
  
  const key = `${oldColumn}→${newColumn}`
  if (messages[key]) {
    sendTelegramMessage(messages[key])
  }
}
```

---

## 📋 PHASE 5: MISSION CONTROL PAGE

### New Route: `/saksliste`
```jsx
// src/pages/Saksliste.jsx
export default function Saksliste() {
  return (
    <div className="h-full overflow-y-auto p-4 lg:p-5 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">Saksliste & Kanban</h1>
          <p className="text-sm text-gray-500">NRJ Morgen - Story management</p>
        </div>
        
        <div className="flex items-center gap-3">
          <button className="btn-cyber">
            🌅 Kjør Morning Routine
          </button>
        </div>
      </div>
      
      {/* Stats Row */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard label="Backlog" value={12} color="gray" />
        <StatCard label="Research" value={5} color="cyan" />
        <StatCard label="Write" value={3} color="violet" />
        <StatCard label="Review" value={2} color="amber" />
        <StatCard label="Done" value={28} color="green" />
      </div>
      
      {/* Kanban Board */}
      <div className="panel p-4">
        <h2 className="text-sm font-semibold text-white mb-4">Kanban Board</h2>
        <KanbanBoard />
      </div>
      
      {/* Today's Saksliste */}
      <div className="panel p-4">
        <h2 className="text-sm font-semibold text-white mb-4">Dagens Saksliste</h2>
        <SakslisteWidget detailed />
      </div>
    </div>
  )
}
```

---

## ⏱️ IMPLEMENTATION TIMELINE

| Phase | Tasks | Time | Priority |
|-------|-------|------|----------|
| 1 | Saksliste service & widget | 2h | P1 |
| 2 | Database schema & Kanban | 3h | P1 |
| 3 | Auto-task creation | 1h | P2 |
| 4 | Vev integration & commands | 2h | P2 |
| 5 | Mission Control page | 2h | P1 |
| **Total** | | **10h** | |

---

## 🚀 NEXT ACTIONS

1. **Create Supabase tables** for vev_tasks
2. **Build Kanban component** with drag-and-drop
3. **Integrate with Morning Routine** for auto-task creation
4. **Add to Mission Control** as new page
5. **Connect to Telegram** for notifications

**Ready to implement!** 📝🤖✨
