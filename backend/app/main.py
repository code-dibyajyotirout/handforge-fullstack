from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.security import generate_csp_headers
from app.routers import health, projects, gallery, telemetry

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="High-performance backend and microservice layer for HandForge 3D digital sculpting studio."
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security and CSP header middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    csp_headers = generate_csp_headers()
    for header, value in csp_headers.items():
        response.headers[header] = value
    return response

# Mount routers
app.include_router(health.router)
app.include_router(projects.router)
app.include_router(gallery.router)
app.include_router(telemetry.router)

@app.get("/")
def root():
    return {
        "message": "HandForge Distributed Backend Active",
        "documentation": "/docs",
        "health": "/health",
        "api_v1": settings.API_V1_STR
    }
