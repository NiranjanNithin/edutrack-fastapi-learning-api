from fastapi import FastAPI

# ✅ DB Imports
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.db.init_db import seed_courses

# ✅ API Routers
from app.api import user, course,enrollment
from app.api import dashboard, analytics


# ✅ Create FastAPI app FIRST
app = FastAPI(title="EduTrack API")


# ✅ Create DB tables
Base.metadata.create_all(bind=engine)


# ✅ Include routers (after app creation)
app.include_router(user.router)
app.include_router(course.router)
app.include_router(enrollment.router)



app.include_router(dashboard.router)
app.include_router(analytics.router)



# ✅ Startup event (for seeding data)
@app.on_event("startup")
def startup():
    db = SessionLocal()
    seed_courses(db)
    db.close()


# ✅ Root endpoint
@app.get("/")
def root():
    return {"message": "EduTrack API Running"}
