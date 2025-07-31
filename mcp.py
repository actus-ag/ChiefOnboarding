"""
ChiefOnboarding MCP Server Configuration

This file defines all MCP tools and toolsets for the ChiefOnboarding application.
It serves as the main entry point for MCP clients to discover and use available tools.
"""

from mcp_server import MCPToolset

# Import all tool modules
from mcp_tools.base import BaseChiefOnboardingToolset


class ChiefOnboardingMCPServer(BaseChiefOnboardingToolset):
    """
    Main MCP server class that combines all ChiefOnboarding functionality.
    This serves as the entry point for MCP clients.
    """
    
    def get_server_info(self) -> dict:
        """Return information about the ChiefOnboarding MCP server."""
        return {
            "name": "ChiefOnboarding MCP Server",
            "version": "1.0.0",
            "description": "Complete MCP server for ChiefOnboarding platform",
            "capabilities": [
                "user_management",
                "organization_management", 
                "sequence_management",
                "template_management",
                "task_management",
                "integration_management",
                "file_management",
                "portal_functionality",
                "communication_tools",
                "reporting_analytics",
                "offboarding_management",
                "bulk_operations",
                "search_discovery",
                "security_compliance"
            ],
            "phase_count": 16,
            "total_tools": 400+
        }
    
    def health_check(self) -> dict:
        """Perform a health check of the MCP server."""
        try:
            # Basic health checks
            from django.db import connection
            from django.conf import settings
            
            # Check database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            return {
                "status": "healthy",
                "database": "connected",
                "debug_mode": settings.DEBUG,
                "installed_apps_count": len(settings.INSTALLED_APPS)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }


# Register the main toolset
class MainToolset(ChiefOnboardingMCPServer):
    """Main toolset that will be automatically discovered by django-mcp-server."""
    pass