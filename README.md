# Hospital Queue Management System

Modern web-based hospital queue management system built with React frontend and FastAPI backend.

## 🚀 Quick Start (1 Command)

```bash
docker-compose -f docker-compose.dev.yml up --build
```

**Access:**
- Frontend: http://localhost:3001
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

**Stop:** Press `Ctrl+C` or run `docker-compose -f docker-compose.dev.yml down`

---

## 📚 Complete Documentation

- **📘 Terminal Guide**: `TERMINAL-GUIDE.md` - All terminal commands
- **🚀 Quick Start**: See below
- **🔧 Troubleshooting**: See TERMINAL-GUIDE.md

---

## 🎯 Features

- **Real-time Queue Management**: Add, call, and manage patient queues
- **Multi-Department Support**: Handle multiple hospital departments (polies)
- **Voice Announcements**: Text-to-speech patient calling (headless mode in Docker)
- **Modern UI**: Responsive Material-UI design
- **Real-time Updates**: Auto-refresh queue status every 3 seconds
- **History Tracking**: View and manage called patients
- **RESTful API**: Clean API design for easy integration

---

## 🏗️ Architecture

```
├── backend/          # FastAPI Python backend
│   ├── app/
│   │   ├── models/   # Pydantic data models
│   │   ├── routers/  # API endpoints
│   │   ├── services/ # Business logic
│   │   └── database/ # Database operations
├── frontend/         # React TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── hooks/
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite** - Lightweight database
- **Pydantic** - Data validation
- **gTTS** - Text-to-speech
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Material-UI** - Component library
- **React Query** - Data fetching & caching
- **Axios** - HTTP client

---

## 📋 Prerequisites

- **Docker Desktop** (https://docker.com/products/docker-desktop)
- **Git** (optional)

---

## 🎮 Common Commands

### Start Application
```bash
# Development mode
docker-compose -f docker-compose.dev.yml up --build

# Production mode
docker-compose up --build -d

# Background mode (detached)
docker-compose -f docker-compose.dev.yml up -d --build
```

### Stop Application
```bash
# Stop development
docker-compose -f docker-compose.dev.yml down

# Stop production
docker-compose down
```

### View Logs
```bash
# All logs (follow)
docker-compose -f docker-compose.dev.yml logs -f

# Backend only
docker-compose -f docker-compose.dev.yml logs backend -f

# Frontend only
docker-compose -f docker-compose.dev.yml logs frontend -f
```

### Restart Services
```bash
# Restart all
docker-compose -f docker-compose.dev.yml restart

# Restart backend only
docker-compose -f docker-compose.dev.yml restart backend
```

### Clean Up
```bash
# Remove containers and networks
docker-compose -f docker-compose.dev.yml down

# Remove everything including volumes
docker-compose -f docker-compose.dev.yml down -v

# Clean Docker system
docker system prune -f
```

---

## 📝 API Endpoints

### Queue Management
- `GET /api/queue/polies` - Get available departments
- `POST /api/queue/add` - Add patient to queue
- `POST /api/queue/call` - Call next patient
- `POST /api/queue/recall` - Recall patient
- `GET /api/queue/status/{poly}` - Get queue status
- `GET /api/queue/status` - Get all queue statuses
- `DELETE /api/queue/history/{poly}` - Clear history

### Example Usage
```bash
# Test health
curl http://localhost:8001/health

# Get polies
curl http://localhost:8001/api/queue/polies

# Add patient
curl -X POST http://localhost:8001/api/queue/add \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "poly": "Poli Umum"}'

# Call next patient
curl -X POST http://localhost:8001/api/queue/call \
  -H "Content-Type: application/json" \
  -d '{"poly": "Poli Umum"}'
```

---

## 🔧 Development

### Using NPM Scripts
```bash
npm start          # Start development
npm run start:prod # Start production
npm run stop       # Stop all services
npm run logs       # View logs
npm run clean      # Clean up
```

### Using Make (Linux/Mac)
```bash
make start         # Start development
make stop          # Stop services
make logs          # View logs
make clean         # Clean up
make help          # Show all commands
```

---

## 🚀 Deployment

### Docker (Recommended)
```bash
# Production mode
docker-compose up --build -d
```

### Cloud Platforms
- **Heroku**: Deploy backend and frontend separately
- **Vercel/Netlify**: Frontend deployment
- **Railway/Render**: Full-stack deployment
- **AWS/GCP/Azure**: Container deployment

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Stop all containers
docker-compose -f docker-compose.dev.yml down

# Check ports
netstat -ano | findstr :8001
netstat -ano | findstr :3001
```

### Container Won't Start
```bash
# Check logs
docker-compose -f docker-compose.dev.yml logs backend
docker-compose -f docker-compose.dev.yml logs frontend

# Rebuild from scratch
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up --build --force-recreate
```

### Frontend Can't Connect to Backend
```bash
# Test backend
curl http://localhost:8001/health

# Check CORS settings in backend/app/main.py
```

---

## 📊 Monitoring

```bash
# Resource usage
docker stats

# Container status
docker-compose -f docker-compose.dev.yml ps

# Container processes
docker-compose -f docker-compose.dev.yml top
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🆘 Support

For detailed terminal commands and troubleshooting:
- **Terminal Guide**: `TERMINAL-GUIDE.md`
- **API Documentation**: http://localhost:8001/docs
- **Create an issue**: GitHub Issues

---

**Migration from Tkinter**: This system replaces the original Tkinter desktop application with a modern web-based solution, maintaining all core functionality while adding real-time updates and better scalability.