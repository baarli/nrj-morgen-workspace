#!/usr/bin/env python3
"""
VEV PYDANTIC SCHEMAS
Datavalidering for Supabase og API-respons
"""

from datetime import date
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, HttpUrl, Field, validator

class AgendaItem(BaseModel):
    """Schema for agenda_items table"""
    
    # Required fields
    tenant_id: str = Field(..., pattern=r'^[a-f0-9-]{36}$')
    title: str = Field(..., min_length=1, max_length=200)
    show_date: date
    
    # Optional fields with defaults
    id: Optional[str] = None
    description: Optional[str] = Field(None, max_length=2000)
    category: str = Field(default='TALK', pattern=r'^(TALK|REALITY_TV|KJENDIS|FILM_TV|MUSIKK|INTERNASJONALT|STATS)$')
    order_index: int = Field(default=0, ge=0)
    
    # URLs and metadata
    link_url: Optional[HttpUrl] = None
    link_metadata: Optional[Dict[str, Any]] = None
    
    # Status fields
    is_pinned: bool = False
    is_completed: bool = False
    
    # Audit fields
    created_by: Optional[str] = None
    
    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()
    
    @validator('description')
    def description_max_length(cls, v):
        if v and len(v) > 2000:
            return v[:2000]
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "tenant_id": "a0000000-0000-0000-0000-000000000001",
                "title": "Farmen-vinner avslører hemmelighet",
                "show_date": "2026-03-11",
                "category": "REALITY_TV"
            }
        }


class NielsenData(BaseModel):
    """Schema for Nielsen Radio API response"""
    
    week_number: int = Field(..., ge=1, le=53)
    year: int = Field(..., ge=2020, le=2030)
    daily_reach: int = Field(..., ge=0)
    weekly_reach: int = Field(..., ge=0)
    market_share: float = Field(..., ge=0, le=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "week_number": 10,
                "year": 2026,
                "daily_reach": 69000,
                "weekly_reach": 125000,
                "market_share": 8.5
            }
        }


class PodtoppenData(BaseModel):
    """Schema for Podtoppen API response"""
    
    week_number: str
    year: str
    rank: int = Field(..., ge=1)
    unique_listeners: int = Field(..., ge=0)
    downloads: int = Field(..., ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "week_number": "10",
                "year": "2026",
                "rank": 62,
                "unique_listeners": 16470,
                "downloads": 33405
            }
        }


class BraveSearchResult(BaseModel):
    """Schema for Brave Search API result"""
    
    title: str
    url: HttpUrl
    description: Optional[str] = None
    source: Optional[str] = None
    published_at: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Farmen Kjendis: Vinneren er kåret",
                "url": "https://www.vg.no/rampelys/i/abc123",
                "description": "Se hvem som vant årets Farmen Kjendis",
                "source": "vg.no"
            }
        }


class NewsArticle(BaseModel):
    """Schema for aggregated news article"""
    
    title: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    url: HttpUrl
    source: str
    score: int = Field(default=50, ge=0, le=100)
    
    @validator('score')
    def score_range(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Score must be between 0 and 100')
        return v


# Validation functions
def validate_agenda_item(data: dict) -> AgendaItem:
    """Validate agenda item data"""
    return AgendaItem(**data)

def validate_nielsen_data(data: dict) -> NielsenData:
    """Validate Nielsen data"""
    return NielsenData(**data)

def validate_podtoppen_data(data: dict) -> PodtoppenData:
    """Validate Podtoppen data"""
    return PodtoppenData(**data)

# Example usage
if __name__ == '__main__':
    # Test validation
    try:
        item = AgendaItem(
            tenant_id="a0000000-0000-0000-0000-000000000001",
            title="Test Article",
            show_date=date.today(),
            category="TALK",
            link_url="https://example.com/article"
        )
        print(f"✅ Valid: {item.title}")
        print(item.json(indent=2))
    except Exception as e:
        print(f"❌ Validation error: {e}")
