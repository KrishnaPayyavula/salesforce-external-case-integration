"""Salesforce API endpoints for case management."""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import logging
from typing import Dict, Any

from app.models import CaseCreateRequest, CaseCreateResponse, CaseDetailsResponse
from app.services.salesforce_service import salesforce_service

logger = logging.getLogger(__name__)

# Create router for Salesforce endpoints
router = APIRouter(prefix="/api/salesforce", tags=["Salesforce"])


@router.post("/cases", response_model=CaseCreateResponse)
async def create_case(case_request: CaseCreateRequest):
    """
    Create a new case in Salesforce.
    
    This endpoint creates a new case record in Salesforce using the provided case information.
    The case will be created with the specified subject, description, and other properties.
    
    Args:
        case_request: Case creation request containing all necessary case information
        
    Returns:
        CaseCreateResponse: Response containing the created case ID and success status
        
    Raises:
        HTTPException: If case creation fails or authentication issues occur
    """
    try:
        logger.info(f"Creating case with subject: {case_request.Subject}")
        
        # Create case in Salesforce
        result = await salesforce_service.create_case(case_request)
        
        if result.get("success", False):
            case_id = result.get("id")
            logger.info(f"Successfully created case: {case_id}")
            
            return CaseCreateResponse(
                case_id=case_id,
                case_number=None,  # Will be populated by Salesforce
                success=True,
                message="Case created successfully"
            )
        else:
            logger.error(f"Failed to create case: {result}")
            raise HTTPException(
                status_code=400,
                detail=f"Case creation failed: {result.get('errors', 'Unknown error')}"
            )
            
    except Exception as e:
        logger.error(f"Error creating case: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/cases/{case_id}", response_model=CaseDetailsResponse)
async def get_case_details(case_id: str):
    """
    Retrieve case details from Salesforce by Case ID.
    
    This endpoint retrieves detailed information about a specific case from Salesforce
    using the case ID. Returns comprehensive case information including status,
    priority, description, and custom fields.
    
    Args:
        case_id: The Salesforce Case ID (e.g., 500WU00001LIROYYA5)
        
    Returns:
        CaseDetailsResponse: Detailed case information
        
    Raises:
        HTTPException: If case retrieval fails or case not found
    """
    try:
        logger.info(f"Retrieving case details for ID: {case_id}")
        
        # Validate case ID format (basic validation)
        if not case_id or len(case_id) < 15:
            raise HTTPException(
                status_code=400,
                detail="Invalid case ID format"
            )
        
        # Get case details from Salesforce
        case_details = await salesforce_service.get_case_details(case_id)
        
        logger.info(f"Successfully retrieved case details: {case_id}")
        return case_details
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving case details for {case_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint for Salesforce API connectivity.
    
    This endpoint verifies that the service can authenticate with Salesforce
    and the API is functioning correctly.
    
    Returns:
        Dict: Health status and Salesforce connectivity information
    """
    try:
        # Test OAuth authentication
        token_response = await salesforce_service._get_oauth_token()
        
        return {
            "status": "healthy",
            "salesforce_connected": True,
            "instance_url": token_response.instance_url,
            "api_version": salesforce_service.api_version,
            "message": "Salesforce API is accessible"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "salesforce_connected": False,
            "error": str(e),
            "message": "Salesforce API is not accessible"
        }
