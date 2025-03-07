# Modern ERP System

A full-stack Enterprise Resource Planning (ERP) system built with FastAPI and React.

## Features

- **Inventory Management**
  - Product tracking
  - Stock management
  - Warehouse management
  - Stock alerts

- **Sales Management**
  - Sales orders
  - Customer management
  - Invoice generation
  - Sales reporting

- **Purchase Management**
  - Purchase orders
  - Supplier management
  - Purchase receipts
  - Purchase reporting

## Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- MySQL (Database)
- Alembic (Database migrations)
- JWT Authentication

### Frontend
- React
- TypeScript
- Material-UI
- Axios
- React Router

## Prerequisites

- Docker and Docker Compose
- Node.js (v14 or higher)
- npm (v6 or higher)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd erp
```

2. Create a `.env` file in the backend directory:
```bash
# Database Configuration
DATABASE_URL=mysql://erp_user:erp_password@db:3306/erp_db

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=ERP System
VERSION=1.0.0
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Running the Application

1. Start all services (frontend, backend, and database):
```bash
cd frontend
npm run dev
```

This will:
- Start the React development server on `http://localhost:3000`
- Start the FastAPI backend server on `http://localhost:8000`
- Start the MySQL database on `localhost:3306`

## Database Configuration

The MySQL database is configured with the following default credentials:
- Database: `erp_db`
- User: `erp_user`
- Password: `erp_password`
- Root Password: `root_password`
- Port: `3306`

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Backend Development

The backend is structured as follows:
```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Core configurations
│   ├── db/           # Database configurations
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   └── services/     # Business logic
├── alembic/          # Database migrations
├── tests/            # Test files
└── requirements.txt  # Python dependencies
```

### Frontend Development

The frontend is structured as follows:
```
frontend/
├── src/
│   ├── components/   # Reusable components
│   ├── pages/        # Page components
│   ├── services/     # API services
│   ├── utils/        # Utility functions
│   └── types/        # TypeScript types
└── package.json      # Node.js dependencies
```

## Database Migrations

To create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "description"
```

To apply migrations:
```bash
cd backend
alembic upgrade head
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Build and start the containers:
```bash
docker-compose up --build
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 