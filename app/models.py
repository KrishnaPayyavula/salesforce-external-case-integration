"""Pydantic models for request and response schemas."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class CaseCreateRequest(BaseModel):
    """Request model for creating a new case in Salesforce."""
    
    Subject: str = Field(..., description="Case subject/title")
    Description: Optional[str] = Field(None, description="Case description")
    Type: Optional[str] = Field("General", description="Case type")
    Status: str = Field("New", description="Case status")
    Reason: Optional[str] = Field(None, description="Case reason")
    Origin: str = Field("Web", description="Case origin")
    Priority: str = Field("Medium", description="Case priority")
    EngineeringReqNumber__c: Optional[str] = Field(None, description="Engineering requirement number")
    SLAViolation__c: Optional[str] = Field("No", description="SLA violation status")
    Product__c: Optional[str] = Field(None, description="Product identifier")
    PotentialLiability__c: Optional[str] = Field("No", description="Potential liability status")
    
    class Config:
        populate_by_name = True


class CaseCreateResponse(BaseModel):
    """Response model for case creation."""
    
    case_id: str = Field(..., description="Created case ID")
    case_number: Optional[str] = Field(None, description="Case number")
    success: bool = Field(True, description="Creation success status")
    message: str = Field("Case created successfully", description="Response message")


class CaseDetailsResponse(BaseModel):
    """Response model for case details retrieval."""
    
    Id: str
    CaseNumber: Optional[str]
    Subject: str
    Description: Optional[str]
    Type: Optional[str]
    Status: str
    Reason: Optional[str]
    Origin: str
    Priority: str
    Product__c: Optional[str]
    EngineeringReqNumber__c: Optional[str]
    SLAViolation__c: Optional[str]
    PotentialLiability__c: Optional[str]
    CreatedDate: Optional[datetime]
    LastModifiedDate: Optional[datetime]
    OwnerId: Optional[str]


class OAuthTokenResponse(BaseModel):
    """Response model for OAuth token."""
    
    access_token: str
    token_type: str = "Bearer"
    scope: Optional[str]
    instance_url: str
    signature: Optional[str]
    issued_at: Optional[str]


class MockProductInfoRequest(BaseModel):
    """Request model for mock product information API."""
    
    case_id: str = Field(..., description="Salesforce case ID")
    Product__c: Optional[str] = Field(None, description="Product ID")
    Type: Optional[str] = Field(None, description="Case type")


class MockProductInfoResponse(BaseModel):
    """Response model for mock product information."""
    
    case_id: str
    Product__c: Optional[str]
    product_name: str
    description: str
    specifications: Dict[str, Any]
    troubleshooting_steps: list[str]
    documentation_links: list[str]
    warranty_info: Dict[str, Any]
    support_contact: Dict[str, str]
