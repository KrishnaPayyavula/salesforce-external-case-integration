# Salesforce External Case Integration

A production-grade FastAPI application for integrating with Salesforce to create and manage cases, with a mock external service for product information.

## Features

- ✅ **OAuth 2.0 Authentication** with Salesforce using Client Credentials flow
- ✅ **Case Management** - Create and retrieve cases in Salesforce
- ✅ **Mock External Service** - Simulates external product information API
- ✅ **Production-Ready Code** - Comprehensive error handling, logging, and validation
- ✅ **Interactive Documentation** - Swagger UI and ReDoc integration
- ✅ **Health Checks** - API and service health monitoring
- ✅ **Environment Configuration** - Secure credential management

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Salesforce

Copy the environment template and configure your Salesforce credentials:

```bash
cp env.example .env
```

Edit `.env` with your Salesforce Connected App details:
```env
SALESFORCE_CLIENT_ID=your_client_id_here
SALESFORCE_CLIENT_SECRET=your_client_secret_here
SALESFORCE_BASE_URL=https://your-instance.salesforce.com
```

### 3. Run the Application

```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Full Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## Key Endpoints

### Salesforce Integration
- `POST /api/salesforce/cases` - Create a new case
- `GET /api/salesforce/cases/{case_id}` - Get case details
- `GET /api/salesforce/health` - Salesforce connectivity check

### Mock External Service
- `POST /api/mock/product-info` - Get product information
- `GET /api/mock/products` - List available products
- `GET /api/mock/health` - Mock API health check

## Example Usage

### Create a Case
```bash
curl -X POST "http://localhost:8000/api/salesforce/cases" \
  -H "Content-Type: application/json" \
  -d '{
    "Subject": "Product Support Request",
    "Description": "Customer needs help with GC1060 setup",
    "Type": "Technical",
    "Priority": "High",
    "Product__c": "GC1060"
  }'
```

### Get Product Information
```bash
curl -X POST "http://localhost:8000/api/mock/product-info" \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "500WU00001LIROYYA5",
    "Product__c": "GC1060"
  }'
```

## Supported Products

The mock service supports these product IDs:
- `GC1040` - Advanced Control Panel
- `GC1060` - Smart Gateway Controller
- `GC3020` - Industrial Sensor Hub
- `GC3040` - Process Control Module
- `GC3060` - Data Logger
- `GC5020` - Safety Relay Module
- `GC5040` - Power Management Unit
- `GC5060` - Communication Gateway
- `GC1020` - Basic I/O Module

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models.py            # Pydantic models
│   ├── api/
│   │   ├── salesforce.py    # Salesforce endpoints
│   │   └── mock.py          # Mock API endpoints
│   └── services/
│       ├── salesforce_service.py  # Salesforce API client
│       └── mock_service.py        # Mock product service
├── requirements.txt         # Python dependencies
├── env.example             # Environment template
├── API_DOCUMENTATION.md    # Comprehensive API docs
└── README.md              # This file
```

## Requirements

- Python 3.8+
- FastAPI 0.104.1
- httpx for HTTP client
- pydantic for data validation
- python-dotenv for environment management

## Development

### Running in Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API
Use the interactive documentation at http://localhost:8000/docs to test all endpoints.

## Production Deployment

1. Set `DEBUG=False` in your environment
2. Configure proper CORS origins
3. Use secure credential management
4. Enable HTTPS
5. Set up monitoring and logging

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions or issues:
- Check the [API Documentation](API_DOCUMENTATION.md)
- Use the health check endpoints to verify service status
- Review application logs for detailed error information