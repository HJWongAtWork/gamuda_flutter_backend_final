import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.models.database import User
from app.api.dependencies import get_current_user

router = APIRouter(tags=["Analytics"])

@router.post("/analytics/by_city")
async def get_users_by_city(current_user = Depends(get_current_user)):
    """Get user statistics grouped by city."""
    db = SessionLocal()
    try:
        df = pd.read_sql(db.query(User).statement, db.bind)
        city_stats = df.groupby('city').agg({
            'id': 'count',
            'salary': 'mean',
            'age': 'mean'
        }).round(2).to_dict('index')
        return city_stats
    finally:
        db.close()

@router.post("/analytics/by_age_range")
async def get_users_by_age_range(current_user = Depends(get_current_user)):
    """Get user statistics grouped by age range."""
    db = SessionLocal()
    try:
        df = pd.read_sql(db.query(User).statement, db.bind)
        
        age_ranges = {
            '18-30': (18, 30),
            '31-45': (31, 45),
            '46-60': (46, 60),
            '60+': (61, 100)
        }
        
        result = {}
        for range_name, (min_age, max_age) in age_ranges.items():
            age_group = df[(df['age'] >= min_age) & (df['age'] <= max_age)]
            result[range_name] = {
                'count': len(age_group),
                'avg_salary': round(age_group['salary'].mean(), 2)
            }
        
        return result
    finally:
        db.close()

@router.post("/analytics/salary_histogram")
async def get_salary_histogram(current_user = Depends(get_current_user)):
    """Get salary distribution histogram data."""
    db = SessionLocal()
    try:
        df = pd.read_sql(db.query(User).statement, db.bind)
        
        hist, bin_edges = np.histogram(df['salary'], bins=10)
        
        histogram_data = {
            'counts': hist.tolist(),
            'bin_edges': bin_edges.tolist(),
            'statistics': {
                'mean': round(df['salary'].mean(), 2),
                'median': round(df['salary'].median(), 2),
                'std': round(df['salary'].std(), 2),
                'min': round(df['salary'].min(), 2),
                'max': round(df['salary'].max(), 2)
            }
        }
        
        return histogram_data
    finally:
        db.close()
