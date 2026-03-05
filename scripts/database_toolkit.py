#!/usr/bin/env python3
"""
🗄️ BAARLICLAW DATABASE TOOLKIT
Database-verktøy for SQLite, PostgreSQL, MySQL
"""

import os
import sys
import sqlite3
import json
from typing import List, Dict, Optional, Any, Tuple, Union
from dataclasses import dataclass
from contextlib import contextmanager

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("DatabaseToolkit")

@dataclass
class QueryResult:
    """Database query result"""
    rows: List[Dict[str, Any]]
    columns: List[str]
    row_count: int
    
    def to_dict(self) -> Dict:
        return {
            "rows": self.rows,
            "columns": self.columns,
            "row_count": self.row_count
        }

class SQLiteManager:
    """SQLite database manager"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_dir()
    
    def _ensure_dir(self):
        """Ensure database directory exists"""
        dir_path = os.path.dirname(self.db_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    @contextmanager
    def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def execute(self, query: str, params: Optional[Tuple] = None) -> QueryResult:
        """Execute a query"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                conn.commit()
                
                # Get results if SELECT
                if query.strip().upper().startswith('SELECT'):
                    columns = [desc[0] for desc in cursor.description] if cursor.description else []
                    rows = [dict(row) for row in cursor.fetchall()]
                    return QueryResult(rows, columns, len(rows))
                else:
                    return QueryResult([], [], cursor.rowcount)
                    
            except Exception as e:
                conn.rollback()
                logger.error(f"Query failed: {e}")
                raise
    
    def create_table(self, table_name: str, columns: Dict[str, str]):
        """
        Create a table
        
        Args:
            table_name: Name of the table
            columns: Dict of column_name -> column_type
        """
        cols = ", ".join([f"{name} {dtype}" for name, dtype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})"
        self.execute(query)
        logger.info(f"Table created: {table_name}")
    
    def insert(self, table_name: str, data: Dict[str, Any]) -> int:
        """Insert a row"""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(data.values()))
            conn.commit()
            return cursor.lastrowid
    
    def insert_many(self, table_name: str, data: List[Dict[str, Any]]):
        """Insert multiple rows"""
        if not data:
            return
        
        columns = ", ".join(data[0].keys())
        placeholders = ", ".join(["?" for _ in data[0]])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, [tuple(d.values()) for d in data])
            conn.commit()
            logger.info(f"Inserted {cursor.rowcount} rows into {table_name}")
    
    def select(self, table_name: str, 
               columns: Optional[List[str]] = None,
               where: Optional[str] = None,
               params: Optional[Tuple] = None,
               order_by: Optional[str] = None,
               limit: Optional[int] = None) -> QueryResult:
        """Select rows"""
        cols = ", ".join(columns) if columns else "*"
        query = f"SELECT {cols} FROM {table_name}"
        
        if where:
            query += f" WHERE {where}"
        if order_by:
            query += f" ORDER BY {order_by}"
        if limit:
            query += f" LIMIT {limit}"
        
        return self.execute(query, params)
    
    def update(self, table_name: str, data: Dict[str, Any], 
               where: str, params: Tuple):
        """Update rows"""
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where}"
        
        all_params = tuple(data.values()) + params
        result = self.execute(query, all_params)
        logger.info(f"Updated {result.row_count} rows in {table_name}")
        return result.row_count
    
    def delete(self, table_name: str, where: str, params: Tuple):
        """Delete rows"""
        query = f"DELETE FROM {table_name} WHERE {where}"
        result = self.execute(query, params)
        logger.info(f"Deleted {result.row_count} rows from {table_name}")
        return result.row_count
    
    def get_tables(self) -> List[str]:
        """Get list of tables"""
        result = self.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row['name'] for row in result.rows]
    
    def get_schema(self, table_name: str) -> List[Dict]:
        """Get table schema"""
        result = self.execute(f"PRAGMA table_info({table_name})")
        return result.rows
    
    def backup(self, backup_path: str):
        """Backup database"""
        with self._get_connection() as conn:
            backup_conn = sqlite3.connect(backup_path)
            conn.backup(backup_conn)
            backup_conn.close()
        logger.info(f"Database backed up to {backup_path}")
    
    def export_to_json(self, table_name: str, output_path: str):
        """Export table to JSON"""
        result = self.select(table_name)
        with open(output_path, 'w') as f:
            json.dump(result.rows, f, indent=2)
        logger.info(f"Exported {table_name} to {output_path}")
    
    def import_from_json(self, table_name: str, input_path: str):
        """Import from JSON"""
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        if data:
            self.insert_many(table_name, data)
        logger.info(f"Imported {len(data)} rows from {input_path}")

class QueryBuilder:
    """Build SQL queries programmatically"""
    
    def __init__(self, table_name: str):
        self.table = table_name
        self._select = "*"
        self._where = []
        self._where_params = []
        self._order = None
        self._limit = None
        self._joins = []
    
    def select(self, *columns):
        """Select columns"""
        self._select = ", ".join(columns) if columns else "*"
        return self
    
    def where(self, column: str, operator: str, value: Any):
        """Add WHERE clause"""
        self._where.append(f"{column} {operator} ?")
        self._where_params.append(value)
        return self
    
    def where_in(self, column: str, values: List[Any]):
        """Add WHERE IN clause"""
        placeholders = ", ".join(["?" for _ in values])
        self._where.append(f"{column} IN ({placeholders})")
        self._where_params.extend(values)
        return self
    
    def order_by(self, column: str, direction: str = "ASC"):
        """Add ORDER BY"""
        self._order = f"{column} {direction}"
        return self
    
    def limit(self, n: int):
        """Add LIMIT"""
        self._limit = n
        return self
    
    def join(self, table: str, on: str, join_type: str = "INNER"):
        """Add JOIN"""
        self._joins.append(f"{join_type} JOIN {table} ON {on}")
        return self
    
    def build(self) -> Tuple[str, Tuple]:
        """Build the query"""
        query = f"SELECT {self._select} FROM {self.table}"
        
        for join in self._joins:
            query += f" {join}"
        
        if self._where:
            query += " WHERE " + " AND ".join(self._where)
        
        if self._order:
            query += f" ORDER BY {self._order}"
        
        if self._limit:
            query += f" LIMIT {self._limit}"
        
        return query, tuple(self._where_params)

# === CONVENIENCE FUNCTIONS ===
def quick_query(db_path: str, query: str, params: Optional[Tuple] = None) -> QueryResult:
    """Quick one-off query"""
    db = SQLiteManager(db_path)
    return db.execute(query, params)

def create_db(db_path: str, schema: Dict[str, Dict[str, str]]):
    """Create database with schema"""
    db = SQLiteManager(db_path)
    for table_name, columns in schema.items():
        db.create_table(table_name, columns)
    return db

def migrate_json_to_sqlite(json_path: str, db_path: str, table_name: str):
    """Migrate JSON file to SQLite"""
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    if not data:
        logger.warning("No data to migrate")
        return
    
    # Infer schema from first row
    first_row = data[0]
    columns = {}
    for key, value in first_row.items():
        if isinstance(value, int):
            columns[key] = "INTEGER"
        elif isinstance(value, float):
            columns[key] = "REAL"
        else:
            columns[key] = "TEXT"
    
    db = SQLiteManager(db_path)
    db.create_table(table_name, columns)
    db.insert_many(table_name, data)
    
    logger.info(f"Migrated {len(data)} rows from {json_path} to {db_path}.{table_name}")

# === TESTING ===
if __name__ == "__main__":
    print("🗄️ BaarliClaw Database Toolkit - Testing")
    print("=" * 50)
    
    # Test SQLite
    print("\n🧪 Testing SQLite Manager")
    db = SQLiteManager("/tmp/test.db")
    
    # Create table
    db.create_table("users", {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "email": "TEXT UNIQUE",
        "age": "INTEGER"
    })
    print("✅ Table created")
    
    # Insert
    user_id = db.insert("users", {"name": "John Doe", "email": "john@example.com", "age": 30})
    print(f"✅ Inserted user with ID: {user_id}")
    
    # Insert many
    db.insert_many("users", [
        {"name": "Jane Doe", "email": "jane@example.com", "age": 25},
        {"name": "Bob Smith", "email": "bob@example.com", "age": 35}
    ])
    print("✅ Inserted multiple users")
    
    # Select
    result = db.select("users", where="age > ?", params=(25,))
    print(f"✅ Selected {result.row_count} users over 25")
    for row in result.rows:
        print(f"   - {row['name']} ({row['age']})")
    
    # Query Builder
    print("\n🧪 Testing Query Builder")
    qb = QueryBuilder("users")
    query, params = qb.select("name", "email").where("age", ">", 25).order_by("name").build()
    print(f"✅ Built query: {query}")
    print(f"   Params: {params}")
    
    # Execute built query
    result = db.execute(query, params)
    print(f"✅ Query returned {result.row_count} rows")
    
    # Cleanup
    import os
    os.remove("/tmp/test.db")
    
    print("\n✅ Database Toolkit ready!")
