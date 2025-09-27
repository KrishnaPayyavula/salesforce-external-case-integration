"""Salesforce API service for OAuth and case operations."""

import httpx
import logging
from typing import Dict, Any, Optional
from app.config import settings
from app.models import OAuthTokenResponse, CaseCreateRequest, CaseDetailsResponse


logger = logging.getLogger(__name__)


class SalesforceService:
    """Service class for Salesforce API interactions."""
    
    def __init__(self):
        self.base_url = settings.salesforce_base_url
        self.client_id = settings.salesforce_client_id
        self.client_secret = settings.salesforce_client_secret
        self.api_version = settings.salesforce_api_version
        self._access_token: Optional[str] = None
        self._instance_url: Optional[str] = None
    
    async def _get_oauth_token(self) -> OAuthTokenResponse:
        """Get OAuth access token using client credentials flow."""
        try:
            token_url = f"{self.base_url}{settings.oauth_token_url}"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    token_url,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": self.client_id,
                        "client_secret": self.client_secret
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                
                token_data = response.json()
                token_response = OAuthTokenResponse(**token_data)
                
                # Cache the token and instance URL
                self._access_token = token_response.access_token
                self._instance_url = token_response.instance_url
                
                logger.info("Successfully obtained OAuth token")
                return token_response
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to obtain OAuth token: {e}")
            raise Exception(f"Authentication failed: {e}")
    
    async def _ensure_valid_token(self):
        """Ensure we have a valid access token."""
        if not self._access_token:
            await self._get_oauth_token()
    
    async def create_case(self, case_data: CaseCreateRequest) -> Dict[str, Any]:
        """Create a new case in Salesforce."""
        try:
            await self._ensure_valid_token()
            
            # Convert Pydantic model to dict for Salesforce API
            case_payload = case_data.model_dump(exclude_none=True)
            
            # Ensure required fields are present
            if not case_payload.get("Subject"):
                raise ValueError("Subject is required")
            
            api_url = f"{self._instance_url}/services/data/{self.api_version}/sobjects/Case"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    api_url,
                    json=case_payload,
                    headers={
                        "Authorization": f"Bearer {self._access_token}",
                        "Content-Type": "application/json"
                    }
                )
                response.raise_for_status()
                
                result = response.json()
                logger.info(f"Successfully created case: {result.get('id')}")
                return result
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to create case: {e}")
            if e.response:
                error_detail = e.response.text
                logger.error(f"Salesforce API error: {error_detail}")
            raise Exception(f"Case creation failed: {e}")
    
    async def get_case_details(self, case_id: str) -> CaseDetailsResponse:
        """Retrieve case details from Salesforce."""
        try:
            await self._ensure_valid_token()
            
            api_url = f"{self._instance_url}/services/data/{self.api_version}/sobjects/Case/{case_id}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    api_url,
                    headers={
                        "Authorization": f"Bearer {self._access_token}",
                        "Content-Type": "application/json"
                    }
                )
                response.raise_for_status()
                
                case_data = response.json()
                
                # Map Salesforce response to our response model
                case_details = CaseDetailsResponse(
                    Id=case_data.get("Id"),
                    CaseNumber=case_data.get("CaseNumber"),
                    Subject=case_data.get("Subject"),
                    Description=case_data.get("Description"),
                    Type=case_data.get("Type"),
                    Status=case_data.get("Status"),
                    Reason=case_data.get("Reason"),
                    Origin=case_data.get("Origin"),
                    Priority=case_data.get("Priority"),
                    Product__c=case_data.get("Product__c"),
                    EngineeringReqNumber__c=case_data.get("EngineeringReqNumber__c"),
                    SLAViolation__c=case_data.get("SLAViolation__c"),
                    PotentialLiability__c=case_data.get("PotentialLiability__c"),
                    CreatedDate=case_data.get("CreatedDate"),
                    LastModifiedDate=case_data.get("LastModifiedDate"),
                    OwnerId=case_data.get("OwnerId")
                )
                
                logger.info(f"Successfully retrieved case details: {case_id}")
                return case_details
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to retrieve case details: {e}")
            if e.response:
                error_detail = e.response.text
                logger.error(f"Salesforce API error: {error_detail}")
            raise Exception(f"Failed to retrieve case details: {e}")


# Global service instance
salesforce_service = SalesforceService()
