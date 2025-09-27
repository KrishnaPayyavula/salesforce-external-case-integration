"""Mock service for product information API."""

import logging
from typing import Dict, Any
from app.models import MockProductInfoRequest, MockProductInfoResponse


logger = logging.getLogger(__name__)


class MockProductService:
    """Mock service for providing product information based on case details."""
    
    def __init__(self):
        # Mock product database with detailed information
        self.product_database = {
            "GC1040": {
                "name": "GC1040 - Advanced Control Panel",
                "description": "High-performance control panel with advanced diagnostics and monitoring capabilities. Designed for industrial automation systems.",
                "specifications": {
                    "power_consumption": "15W",
                    "operating_temperature": "-20°C to 70°C",
                    "input_voltage": "24V DC",
                    "communication": "Modbus RTU/TCP, Ethernet",
                    "dimensions": "120mm x 80mm x 35mm",
                    "certifications": ["CE", "UL", "FCC"]
                },
                "troubleshooting_steps": [
                    "Check power supply voltage (should be 24V DC ±5%)",
                    "Verify network connectivity and IP configuration",
                    "Check for loose connections on terminal blocks",
                    "Review system logs for error messages",
                    "Perform factory reset if communication fails"
                ],
                "documentation_links": [
                    "https://docs.example.com/gc1040/user-manual",
                    "https://docs.example.com/gc1040/installation-guide",
                    "https://docs.example.com/gc1040/troubleshooting"
                ],
                "warranty_info": {
                    "duration": "3 years",
                    "coverage": "Manufacturing defects and component failure",
                    "exclusions": "Physical damage, misuse, unauthorized modifications"
                },
                "support_contact": {
                    "email": "support-gc1040@example.com",
                    "phone": "+1-800-GC1040-1",
                    "hours": "24/7 Technical Support"
                }
            },
            "GC1060": {
                "name": "GC1060 - Smart Gateway Controller",
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
            },
            "GC3020": {
                "name": "GC3020 - Industrial Sensor Hub",
                "description": "Multi-protocol sensor hub designed for harsh industrial environments. Supports various sensor types and communication protocols.",
                "specifications": {
                    "power_consumption": "8W",
                    "operating_temperature": "-40°C to 85°C",
                    "input_voltage": "12-36V DC",
                    "sensor_inputs": "16 analog, 32 digital",
                    "communication": "RS485, Ethernet, Wireless",
                    "enclosure_rating": "IP67"
                },
                "troubleshooting_steps": [
                    "Check sensor wiring and connections",
                    "Verify power supply stability",
                    "Test individual sensor inputs",
                    "Check communication protocol settings",
                    "Inspect for physical damage or corrosion"
                ],
                "documentation_links": [
                    "https://docs.example.com/gc3020/sensor-configuration",
                    "https://docs.example.com/gc3020/protocol-guide",
                    "https://docs.example.com/gc3020/maintenance"
                ],
                "warranty_info": {
                    "duration": "2 years",
                    "coverage": "Component failure and calibration drift",
                    "exclusions": "Environmental damage, improper installation"
                },
                "support_contact": {
                    "email": "sensor-support@example.com",
                    "phone": "+1-800-GC3020-1",
                    "hours": "Mon-Fri 8AM-6PM EST"
                }
            },
            "GC3040": {
                "name": "GC3040 - Process Control Module",
                "description": "High-precision process control module with PID control algorithms and real-time data acquisition capabilities.",
                "specifications": {
                    "power_consumption": "12W",
                    "operating_temperature": "-20°C to 60°C",
                    "input_voltage": "24V DC",
                    "control_loops": "8 PID loops",
                    "scan_time": "100ms",
                    "accuracy": "±0.1% of full scale"
                },
                "troubleshooting_steps": [
                    "Verify control loop parameters and tuning",
                    "Check process variable readings",
                    "Review control output signals",
                    "Analyze historical trend data",
                    "Perform loop calibration check"
                ],
                "documentation_links": [
                    "https://docs.example.com/gc3040/control-tuning",
                    "https://docs.example.com/gc3040/process-setup",
                    "https://docs.example.com/gc3040/calibration-procedures"
                ],
                "warranty_info": {
                    "duration": "3 years",
                    "coverage": "Control accuracy and component failure",
                    "exclusions": "Process-related damage, incorrect tuning"
                },
                "support_contact": {
                    "email": "control-support@example.com",
                    "phone": "+1-800-GC3040-1",
                    "hours": "24/7 Process Support"
                }
            },
            "GC3060": {
                "name": "GC3060 - Data Logger",
                "description": "High-capacity data logger with long-term storage and advanced analytics capabilities for industrial monitoring applications.",
                "specifications": {
                    "power_consumption": "5W",
                    "operating_temperature": "-30°C to 70°C",
                    "input_voltage": "12-24V DC",
                    "storage_capacity": "1TB SSD",
                    "data_channels": "64 analog, 128 digital",
                    "sampling_rate": "Up to 1kHz per channel"
                },
                "troubleshooting_steps": [
                    "Check storage space and data retention settings",
                    "Verify data integrity and backup status",
                    "Review sampling configuration",
                    "Check battery backup system",
                    "Analyze data export functionality"
                ],
                "documentation_links": [
                    "https://docs.example.com/gc3060/data-configuration",
                    "https://docs.example.com/gc3060/analytics-guide",
                    "https://docs.example.com/gc3060/backup-procedures"
                ],
                "warranty_info": {
                    "duration": "4 years",
                    "coverage": "Storage system and data integrity",
                    "exclusions": "Data loss due to user error, storage media wear"
                },
                "support_contact": {
                    "email": "data-support@example.com",
                    "phone": "+1-800-GC3060-1",
                    "hours": "Mon-Fri 7AM-7PM EST"
                }
            },
            "GC5020": {
                "name": "GC5020 - Safety Relay Module",
                "description": "Fail-safe relay module with SIL 2 certification for critical safety applications in industrial environments.",
                "specifications": {
                    "power_consumption": "3W",
                    "operating_temperature": "-25°C to 55°C",
                    "input_voltage": "24V DC",
                    "safety_level": "SIL 2",
                    "relay_contacts": "4 NO + 4 NC",
                    "response_time": "< 50ms"
                },
                "troubleshooting_steps": [
                    "Verify safety circuit integrity",
                    "Check relay contact resistance",
                    "Test emergency stop functionality",
                    "Review safety logic configuration",
                    "Perform SIL 2 compliance check"
                ],
                "documentation_links": [
                    "https://docs.example.com/gc5020/safety-configuration",
                    "https://docs.example.com/gc5020/sil-compliance",
                    "https://docs.example.com/gc5020/installation-safety"
                ],
                "warranty_info": {
                    "duration": "5 years",
                    "coverage": "Safety functionality and relay operation",
                    "exclusions": "Misuse, improper safety circuit design"
                },
                "support_contact": {
                    "email": "safety-support@example.com",
                    "phone": "+1-800-GC5020-1",
                    "hours": "24/7 Safety Support"
                }
            },
            "GC5040": {
                "name": "GC5040 - Power Management Unit",
                "description": "Intelligent power management unit with load monitoring, surge protection, and energy optimization features.",
                "specifications": {
                    "power_consumption": "10W",
                    "operating_temperature": "-20°C to 65°C",
                    "input_voltage": "100-240V AC",
                    "output_power": "1000W max",
                    "efficiency": ">95%",
                    "protection": "Surge, overcurrent, short circuit"
                },
                "troubleshooting_steps": [
                    "Check input voltage and power quality",
                    "Verify load distribution and balance",
                    "Review power consumption analytics",
                    "Test surge protection functionality",
                    "Check for thermal overload conditions"
                ],
                "documentation_links": [
                    "https://docs.example.com/gc5040/power-configuration",
                    "https://docs.example.com/gc5040/load-monitoring",
                    "https://docs.example.com/gc5040/energy-optimization"
                ],
                "warranty_info": {
                    "duration": "3 years",
                    "coverage": "Power management and protection features",
                    "exclusions": "Power surge damage, overload conditions"
                },
                "support_contact": {
                    "email": "power-support@example.com",
                    "phone": "+1-800-GC5040-1",
                    "hours": "24/7 Power Support"
                }
            },
            "GC5060": {
                "name": "GC5060 - Communication Gateway",
                "description": "Multi-protocol communication gateway supporting legacy and modern industrial communication protocols with protocol translation capabilities.",
                "specifications": {
                    "power_consumption": "15W",
                    "operating_temperature": "-30°C to 70°C",
                    "input_voltage": "24V DC",
                    "supported_protocols": ["Modbus RTU/TCP", "Profibus", "Ethernet/IP", "OPC UA"],
                    "concurrent_connections": "100",
                    "throughput": "1000 messages/second"
                },
                "troubleshooting_steps": [
                    "Verify protocol configuration and mapping",
                    "Check network connectivity and routing",
                    "Review message translation accuracy",
                    "Test concurrent connection limits",
                    "Analyze communication performance metrics"
                ],
                "documentation_links": [
                    "https://docs.example.com/gc5060/protocol-setup",
                    "https://docs.example.com/gc5060/translation-guide",
                    "https://docs.example.com/gc5060/performance-tuning"
                ],
                "warranty_info": {
                    "duration": "4 years",
                    "coverage": "Protocol support and translation accuracy",
                    "exclusions": "Network infrastructure issues, protocol changes"
                },
                "support_contact": {
                    "email": "gateway-support@example.com",
                    "phone": "+1-800-GC5060-1",
                    "hours": "24/7 Gateway Support"
                }
            },
            "GC1020": {
                "name": "GC1020 - Basic I/O Module",
                "description": "Cost-effective basic I/O module for simple automation applications with reliable digital and analog I/O capabilities.",
                "specifications": {
                    "power_consumption": "4W",
                    "operating_temperature": "-10°C to 55°C",
                    "input_voltage": "24V DC",
                    "digital_io": "16 inputs, 16 outputs",
                    "analog_io": "4 inputs, 2 outputs",
                    "isolation": "500V optical"
                },
                "troubleshooting_steps": [
                    "Check I/O configuration and addressing",
                    "Verify signal levels and thresholds",
                    "Test input/output functionality",
                    "Review isolation and grounding",
                    "Check for loose connections"
                ],
                "documentation_links": [
                    "https://docs.example.com/gc1020/io-configuration",
                    "https://docs.example.com/gc1020/wiring-guide",
                    "https://docs.example.com/gc1020/troubleshooting"
                ],
                "warranty_info": {
                    "duration": "2 years",
                    "coverage": "I/O functionality and component failure",
                    "exclusions": "Wiring errors, incorrect voltage application"
                },
                "support_contact": {
                    "email": "io-support@example.com",
                    "phone": "+1-800-GC1020-1",
                    "hours": "Mon-Fri 8AM-5PM EST"
                }
            }
        }
    
    async def get_product_information(self, request: MockProductInfoRequest) -> MockProductInfoResponse:
        """Get mock product information based on case details."""
        try:
            case_id = request.case_id
            product_id = request.Product__c
            
            # Handle case when no product ID is provided
            if not product_id or product_id == "--None--":
                return MockProductInfoResponse(
                    case_id=case_id,
                    Product__c=product_id,
                    product_name="No Product Selected",
                    description="No product ID received. Please select a product ID in the case to get detailed product information.",
                    specifications={},
                    troubleshooting_steps=[
                        "Please update the case with a valid Product__c value",
                        "Contact support if you need assistance selecting the correct product"
                    ],
                    documentation_links=[
                        "https://docs.example.com/product-catalog"
                    ],
                    warranty_info={
                        "duration": "N/A",
                        "coverage": "N/A",
                        "exclusions": "N/A"
                    },
                    support_contact={
                        "email": "support@example.com",
                        "phone": "+1-800-HELP-NOW",
                        "hours": "24/7 Support"
                    }
                )
            
            # Get product information from database
            if product_id in self.product_database:
                product_data = self.product_database[product_id]
                
                response = MockProductInfoResponse(
                    case_id=case_id,
                    Product__c=product_id,
                    product_name=product_data["name"],
                    description=product_data["description"],
                    specifications=product_data["specifications"],
                    troubleshooting_steps=product_data["troubleshooting_steps"],
                    documentation_links=product_data["documentation_links"],
                    warranty_info=product_data["warranty_info"],
                    support_contact=product_data["support_contact"]
                )
                
                logger.info(f"Retrieved product information for case {case_id}, product {product_id}")
                return response
            else:
                # Product not found in database
                return MockProductInfoResponse(
                    case_id=case_id,
                    Product__c=product_id,
                    product_name=f"Unknown Product: {product_id}",
                    description=f"Product ID '{product_id}' is not recognized in our product database. Please verify the product ID or contact support.",
                    specifications={},
                    troubleshooting_steps=[
                        "Verify the product ID is correct",
                        "Check for typos in the product code",
                        "Contact support with the correct product information"
                    ],
                    documentation_links=[
                        "https://docs.example.com/product-catalog",
                        "https://docs.example.com/supported-products"
                    ],
                    warranty_info={
                        "duration": "Unknown",
                        "coverage": "Contact support for warranty information",
                        "exclusions": "N/A"
                    },
                    support_contact={
                        "email": "support@example.com",
                        "phone": "+1-800-HELP-NOW",
                        "hours": "24/7 Support"
                    }
                )
                
        except Exception as e:
            logger.error(f"Error retrieving product information for case {request.case_id}: {e}")
            raise Exception(f"Failed to retrieve product information: {e}")


# Global service instance
mock_product_service = MockProductService()
