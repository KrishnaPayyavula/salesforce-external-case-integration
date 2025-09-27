# Salesforce External Case Integration API Documentation

## Overview

This FastAPI application provides a comprehensive solution for Salesforce case integration, including OAuth 2.0 authentication, case management, and a mock external service for product information.

## Table of Contents

1. [Setup and Installation](#setup-and-installation)
2. [Configuration](#configuration)
3. [API Endpoints](#api-endpoints)
4. [Authentication](#authentication)
5. [Examples](#examples)
6. [Error Handling](#error-handling)

## Setup and Installation

### Prerequisites

- Python 3.11+
- Salesforce Developer Account (I tried Trail Head Playground)
- External Connected App configured in Salesforce

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd salesforce-external-case-integration
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your Salesforce credentials
   ```

5. **Run the application**
   ```bash
   python -m app.main
   # Or
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## Configuration

### Environment Variables

Create a `.env` file based on `env.example`:

```env
# Salesforce Configuration
SALESFORCE_CLIENT_ID=your_client_id_here
SALESFORCE_CLIENT_SECRET=your_client_secret_here
SALESFORCE_BASE_URL=https://your-instance.salesforce.com
SALESFORCE_API_VERSION=v64.0

# Application Configuration
APP_NAME=Salesforce External Case Integration
APP_VERSION=1.0.0
DEBUG=True
HOST=0.0.0.0
PORT=8000

# OAuth Configuration
OAUTH_TOKEN_URL=/services/oauth2/token
```

### Salesforce Setup

1. **Create a External Connected App** in Salesforce:
   - Go to Setup → App Manager → New External Client App
   - Enable OAuth Settings
   - Set OAuth Scopes: "Manage user data via APIs (api)","Access the Salesforce API Platform (sfap_api)"
   - Note down the Consumer Key and Consumer Secret

2. **Configure OAuth**:
   - Use the Consumer Key as `SALESFORCE_CLIENT_ID`
   - Use the Consumer Secret as `SALESFORCE_CLIENT_SECRET`
   - Set the correct instance URL in `SALESFORCE_BASE_URL`

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Salesforce API Endpoints

### 1. Create Case

**Endpoint**: `POST /api/salesforce/cases`

**Description**: Creates a new case in Salesforce with the provided information.

**Request Body**:
```json
{
  "Subject": "Test Case - API Integration",
  "Description": "This is a test case created via API",
  "Type": "Electrical",
  "Status": "New",
  "Reason": "Installation",
  "Origin": "Web",
  "Priority": "Medium",
  "EngineeringReqNumber__c": "REQ-12345",
  "SLAViolation__c": "No",
  "Product__c": "GC1060",
  "PotentialLiability__c": "No"
}
```

**Response**:
```json
{
  "case_id": "500WU00001LIROYYA5",
  "case_number": null,
  "success": true,
  "message": "Case created successfully"
}
```

**Example cURL**:
```bash
curl -X POST "http://localhost:8000/api/salesforce/cases" \
  -H "Content-Type: application/json" \
  -d '{
    "Subject": "Test Case - API Integration",
    "Description": "This is a test case created via API",
    "Type": "Electrical",
    "Status": "New",
    "Reason": "Installation",
    "Origin": "Web",
    "Priority": "Medium",
    "EngineeringReqNumber__c": "REQ-12345",
    "SLAViolation__c": "No",
    "Product__c": "GC1060",
    "PotentialLiability__c": "No"
  }'
```

### 2. Get Case Details

**Endpoint**: `GET /api/salesforce/cases/{case_id}`

**Description**: Retrieves detailed information about a specific case from Salesforce.

**Path Parameters**:
- `case_id` (string): Salesforce Case ID (e.g., "500WU00001LIROYYA5")

**Response**:
```json
{
  "Id": "500WU00001LIROYYA5",
  "CaseNumber": "00001030",
  "Subject": "Test Case - API Integration",
  "Description": "This is a test case created via API",
  "Type": "Electrical",
  "Status": "New",
  "Reason": "Installation",
  "Origin": "Web",
  "Priority": "Medium",
  "Product__c": "GC1060",
  "EngineeringReqNumber__c": "REQ-12345",
  "SLAViolation__c": "No",
  "PotentialLiability__c": "No",
  "CreatedDate": "2025-01-27T10:30:00.000Z",
  "LastModifiedDate": "2025-01-27T10:30:00.000Z",
  "OwnerId": "005WU00000xFEVJYA4"
}
```

**Example cURL**:
```bash
curl -X GET "http://localhost:8000/api/salesforce/cases/500WU00001LIROYYA5"
```

### 3. Salesforce Health Check

**Endpoint**: `GET /api/salesforce/health`

**Description**: Verifies Salesforce API connectivity and authentication.

**Response**:
```json
{
  "status": "healthy",
  "salesforce_connected": true,
  "instance_url": "https://resourceful-hawk-ju6fdj-dev-ed.trailblaze.my.salesforce.com",
  "api_version": "v64.0",
  "message": "Salesforce API is accessible"
}
```

---

## Mock API Endpoints

### 1. Get Product Information

**Endpoint**: `POST /api/mock/product-info`

**Description**: Simulates an external service that provides detailed product information based on case details.

**Request Body**:
```json
{
  "case_id": "500WU00001LIROYYA5",
  "Product__c": "GC1060",
  "Type": "Electrical"
}
```

**Response**:
```json
{
  "case_id": "500WU00001LIROYYA5",
  "Product__c": "GC1060",
  "product_name": "GC1060 - Smart Gateway Controller",
  "description": "Intelligent gateway controller with cloud connectivity and remote monitoring. Features advanced security protocols and edge computing capabilities.",
  "specifications": {
    "power_consumption": "25W",
    "operating_temperature": "-25°C to 75°C",
    "input_voltage": "12-48V DC",
    "communication": "WiFi 802.11n, Ethernet, 4G LTE",
    "storage": "32GB eMMC",
    "cpu": "ARM Cortex-A53 Quad-core 1.4GHz"
  },
  "troubleshooting_steps": [
    "Verify internet connectivity and firewall settings",
    "Check cellular signal strength (if using 4G)",
    "Review cloud service connectivity status",
    "Examine system resource usage (CPU, memory)",
    "Check for firmware updates"
  ],
  "documentation_links": [
    "https://docs.example.com/gc1060/quick-start",
    "https://docs.example.com/gc1060/cloud-setup",
    "https://docs.example.com/gc1060/security-config"
  ],
  "warranty_info": {
    "duration": "5 years",
    "coverage": "Hardware and software support",
    "exclusions": "Physical damage, water damage, unauthorized access"
  },
  "support_contact": {
    "email": "cloud-support@example.com",
    "phone": "+1-800-GC1060-1",
    "hours": "24/7 Cloud Support"
  }
}
```

**Example cURL**:
```bash
curl -X POST "http://localhost:8000/api/mock/product-info" \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "500WU00001LIROYYA5",
    "Product__c": "GC1060",
    "Type": "Electrical"
  }'
```

### 2. List Available Products

**Endpoint**: `GET /api/mock/products`

**Description**: Returns a list of all available product IDs in the mock database.

**Response**:
```json
{
  "available_products": {
    "GC1040": {
      "name": "GC1040 - Advanced Control Panel",
      "description": "High-performance control panel with advanced diagnostics..."
    },
    "GC1060": {
      "name": "GC1060 - Smart Gateway Controller",
      "description": "Intelligent gateway controller with cloud connectivity..."
    }
  },
  "total_count": 9,
  "message": "Available product IDs for testing the mock API"
}
```

### 3. Mock API Health Check

**Endpoint**: `GET /api/mock/health`

**Description**: Verifies the mock API service status.

**Response**:
```json
{
  "status": "healthy",
  "service": "Mock Product Information API",
  "available_products": 9,
  "message": "Mock API is functioning correctly"
}
```

---

## Authentication

The API uses OAuth 2.0 Client Credentials flow to authenticate with Salesforce:

1. **Automatic Token Management**: The service automatically handles OAuth token acquisition and refresh
2. **Token Caching**: Access tokens are cached to minimize API calls
3. **Error Handling**: Authentication failures are properly handled with meaningful error messages

### OAuth Flow

1. Client sends request to Salesforce OAuth endpoint
2. Salesforce returns access token with instance URL
3. Access token is used for subsequent API calls
4. Token is automatically refreshed when needed

---

## Examples

### Complete Workflow Example

1. **Create a Case**:
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

2. **Get Case Details**:
   ```bash
   curl -X GET "http://localhost:8000/api/salesforce/cases/500WU00001LIROYYA5"
   ```

3. **Get Product Information**:
   ```bash
   curl -X POST "http://localhost:8000/api/mock/product-info" \
     -H "Content-Type: application/json" \
     -d '{
       "case_id": "500WU00001LIROYYA5",
       "Product__c": "GC1060"
     }'
   ```

### Python Client Example

```python
import httpx

# Create a case
async def create_case():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/salesforce/cases",
            json={
                "Subject": "API Test Case",
                "Description": "Created via Python client",
                "Type": "General",
                "Priority": "Medium"
            }
        )
        return response.json()

# Get product information
async def get_product_info(case_id, product_id):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/mock/product-info",
            json={
                "case_id": case_id,
                "Product__c": product_id
            }
        )
        return response.json()
```

---

## Error Handling

### HTTP Status Codes

- **200**: Success
- **400**: Bad Request (invalid input data)
- **401**: Unauthorized (authentication failed)
- **404**: Not Found (case not found)
- **500**: Internal Server Error

### Error Response Format

```json
{
  "error": "Error Type",
  "message": "Human-readable error message",
  "detail": "Detailed error information (only in debug mode)"
}
```

### Common Error Scenarios

1. **Invalid Salesforce Credentials**:
   ```json
   {
     "error": "Authentication failed",
     "message": "Invalid client credentials"
   }
   ```

2. **Case Not Found**:
   ```json
   {
     "error": "Case not found",
     "message": "No case found with the provided ID"
   }
   ```

3. **Missing Required Fields**:
   ```json
   {
     "error": "Validation error",
     "message": "Subject is required"
   }
   ```

---

## Available Product IDs

The mock service supports the following product IDs:

- `GC1040` - Advanced Control Panel
- `GC1060` - Smart Gateway Controller
- `GC3020` - Industrial Sensor Hub
- `GC3040` - Process Control Module
- `GC3060` - Data Logger
- `GC5020` - Safety Relay Module
- `GC5040` - Power Management Unit
- `GC5060` - Communication Gateway
- `GC1020` - Basic I/O Module

---

## Production Deployment

### Environment Configuration

1. Set `DEBUG=False` in production
2. Use proper CORS origins instead of `*`
3. Configure proper logging levels
4. Use environment-specific Salesforce instances

### Security Considerations

1. Store credentials securely (use secrets management)
2. Implement rate limiting
3. Add request validation and sanitization
4. Use HTTPS in production
5. Implement proper error logging and monitoring

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Support

For technical support or questions:

- **API Documentation**: Visit `/docs` endpoint
- **Health Checks**: Use `/health` endpoints to verify service status
- **Logs**: Check application logs for detailed error information

---

## Version History

- **v1.0.0**: Initial release with Salesforce integration and mock API
  - OAuth 2.0 authentication
  - Case creation and retrieval
  - Mock product information service
  - Comprehensive error handling
  - Interactive API documentation
