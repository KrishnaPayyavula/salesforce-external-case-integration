"""Mock API endpoints for product information."""

from fastapi import APIRouter, HTTPException
import logging

from app.models import MockProductInfoRequest, MockProductInfoResponse
from app.services.mock_service import mock_product_service

logger = logging.getLogger(__name__)

# Create router for mock API endpoints
router = APIRouter(prefix="/api/mock", tags=["Mock API"])


@router.post("/product-info", response_model=MockProductInfoResponse)
async def get_product_information(request: MockProductInfoRequest):
    """
    Get mock product information based on case details.
    
    This endpoint simulates an external service that provides detailed product information
    based on the case ID and product ID. It returns comprehensive product details including
    specifications, troubleshooting steps, documentation links, and support information.
    
    Args:
        request: MockProductInfoRequest containing case_id and optional product_id
        
    Returns:
        MockProductInfoResponse: Detailed product information and support details
        
    Raises:
        HTTPException: If product information retrieval fails
    """
    try:
        logger.info(f"Retrieving product information for case: {request.case_id}, product: {request.Product__c}")
        
        # Get product information from mock service
        product_info = await mock_product_service.get_product_information(request)
        
        logger.info(f"Successfully retrieved product information for case: {request.case_id}")
        return product_info
        
    except Exception as e:
        logger.error(f"Error retrieving product information for case {request.case_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/products")
async def list_available_products():
    """
    List all available product IDs in the mock database.
    
    This endpoint returns a list of all product IDs that are supported
    by the mock product information service.
    
    Returns:
        Dict: List of available product IDs and their basic information
    """
    try:
        products = {}
        
        # Get product information from the mock service database
        for product_id, product_data in mock_product_service.product_database.items():
            products[product_id] = {
                "name": product_data["name"],
                "description": product_data["description"][:100] + "..." if len(product_data["description"]) > 100 else product_data["description"]
            }
        
        logger.info("Retrieved list of available products")
        return {
            "available_products": products,
            "total_count": len(products),
            "message": "Available product IDs for testing the mock API"
        }
        
    except Exception as e:
        logger.error(f"Error listing products: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint for mock API.
    
    Returns:
        Dict: Health status of the mock API service
    """
    try:
        return {
            "status": "healthy",
            "service": "Mock Product Information API",
            "available_products": len(mock_product_service.product_database),
            "message": "Mock API is functioning correctly"
        }
        
    except Exception as e:
        logger.error(f"Mock API health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "Mock Product Information API",
            "error": str(e),
            "message": "Mock API is not functioning correctly"
        }
