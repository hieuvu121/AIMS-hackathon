# Light Carriers - Full-Stack Application

A modern full-stack web application built with Django REST Framework backend and React frontend, featuring beautiful animations and real-time data integration.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend (Django)
```bash
# Navigate to Django project
cd D:\AIMS

# Install Python dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Populate sample data
python manage.py populate_data

# Start Django server
python manage.py runserver
```
**Backend runs at:** `http://127.0.0.1:8000`

### Frontend (React)
```bash
# Navigate to React project
cd D:\AIMS\light-carriers-react

# Install dependencies
npm install

# Start React development server
npm start
```
**Frontend runs at:** `http://localhost:3000`

## 🌐 Application URLs

| Component | URL | Description |
|-----------|-----|-------------|
| **React Frontend** | `http://localhost:3000` | 🎨 **Main Application** - Beautiful UI with animations |
| **Django API** | `http://127.0.0.1:8000/api/` | 🔧 **REST API** - Data endpoints |
| **Django Admin** | `http://127.0.0.1:8000/admin/` | ⚙️ **Admin Panel** - Manage content |

## 📡 API Endpoints

### Newsletter
- `POST /api/newsletter/subscribe/` - Subscribe to newsletter
- `GET /api/newsletter/` - List subscribers

### Content
- `GET /api/case-studies/` - Get case studies
- `GET /api/methods/` - Get methods
- `GET /api/about-sections/` - Get about sections
- `GET /api/pages/{page}/` - Get page content

## 🎨 Features

### Frontend (React)
- ✨ **Framer Motion Animations** - Smooth page transitions and micro-interactions
- 📱 **Responsive Design** - Mobile-first approach
- 🎯 **TypeScript** - Type-safe development
- 🔄 **Real-time API Integration** - Live data from Django backend
- ⚡ **Loading States** - Beautiful loading spinners and error handling
- 🎨 **Modern UI** - Dawn color scheme with professional design

### Backend (Django)
- 🚀 **Django REST Framework** - Powerful API framework
- 🔒 **CORS Configuration** - Secure cross-origin requests
- 📊 **Admin Interface** - Easy content management
- 🗄️ **SQLite Database** - Lightweight data storage
- 📝 **Sample Data** - Pre-populated with realistic content

## 🛠️ Development

### Adding New Content
1. Use Django Admin at `http://127.0.0.1:8000/admin/`
2. Add/edit Case Studies, Methods, or About Sections
3. Content automatically appears in React frontend

### API Integration
The React frontend automatically fetches data from Django API:
- **Case Studies** - Dynamic content from database
- **Methods** - Real-time method data
- **About Sections** - Live about page content
- **Newsletter** - Functional subscription system

## 🎯 Key Technologies

### Frontend
- React 18 with TypeScript
- Framer Motion for animations
- React Router for navigation
- CSS3 with modern features
- Responsive design patterns

### Backend
- Django 5.2.5
- Django REST Framework
- SQLite database
- CORS headers for API access
- Admin interface for content management

## 🔧 Configuration

### CORS Settings
Django is configured to allow requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

### Database
- SQLite database with sample data
- Migrations included for easy setup
- Admin interface for content management

## 📱 Mobile Support
- Fully responsive design
- Touch-friendly interactions
- Optimized for all screen sizes
- Mobile navigation menu

## 🎨 Design System
- **Colors**: Dawn theme with blue and orange accents
- **Typography**: Roboto font family
- **Animations**: Smooth transitions and hover effects
- **Layout**: Card-based design with grid system

## 🚀 Production Deployment
For production deployment:
1. Build React app: `npm run build`
2. Configure Django for production
3. Set up proper database (PostgreSQL recommended)
4. Configure static file serving
5. Set up web server (Nginx + Gunicorn)

## 📞 Support
The application is fully functional with:
- ✅ Working API endpoints
- ✅ Real-time data integration
- ✅ Beautiful animations
- ✅ Responsive design
- ✅ Error handling
- ✅ Loading states

**Main Application:** `http://localhost:3000` 🎉

