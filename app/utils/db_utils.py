from datetime import datetime, timedelta
import random
from faker import Faker
from sqlalchemy.orm import Session

from app.config.database import SessionLocal, Base, engine
from app.models.database import User, Account
from app.core.security import get_password_hash

# Sample Data
CITIES = [
    'Amsterdam', 'Berlin', 'Chicago', 'Dublin', 'Edinburgh',
    'Florence', 'Geneva', 'Helsinki', 'Istanbul', 'Jakarta',
    'Kiev', 'London', 'Madrid', 'New York', 'Oslo',
    'Paris', 'Quebec', 'Rome', 'Sydney', 'Tokyo',
    'Uppsala', 'Venice', 'Warsaw', 'Xi\'an', 'Yokohama',
    'Zurich'
]

def init_db():
    """Initialize database and create sample data if not exists."""
    Base.metadata.create_all(engine)
    
    db = SessionLocal()
    
    # Create admin account if it doesn't exist
    if db.query(Account).count() == 0:
        admin_password = get_password_hash("admin123")
        admin_account = Account(
            email="admin@example.com",
            username="admin",
            hashed_password=admin_password
        )
        db.add(admin_account)
        db.commit()
    
    # Create sample users if they don't exist
    if db.query(User).count() == 0:
        fake = Faker()
        users = [
            User(
                name=fake.name(),
                age=random.randint(18, 70),
                city=random.choice(CITIES), 
                salary=round(random.uniform(30000, 120000), 2),
                join_date=datetime.now() - timedelta(days=random.randint(0, 1095))
            )
            for _ in range(1000)
        ]
        
        db.bulk_save_objects(users)
        db.commit()
    db.close()

def get_db_session() -> Session:
    """Get a new database session."""
    return SessionLocal()
