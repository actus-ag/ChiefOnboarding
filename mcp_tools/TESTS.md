  Testing the MCP Server Setup

  1. Set Environment Variables

  export ENV_PATH=.env

  2. Run Database Migrations

  python manage.py migrate

  3. Create a Superuser (optional but recommended)

  python manage.py createsuperuser

  4. Start the Django Development Server

  python manage.py runserver

  5. Test MCP Endpoint Accessibility

  Once the server is running, you can test the MCP endpoint in several ways:

  Method 1: Check if endpoint responds
  curl http://localhost:8000/mcp/

  Method 2: Check MCP server info
  curl -X POST http://localhost:8000/mcp/ \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc": "2.0", "id": 1, "method": "list_tools", "params": {}}'

  Method 3: Test our health check tool
  curl -X POST http://localhost:8000/mcp/ \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc": "2.0", "id": 1, "method": "health_check", "params": {}}'

  6. Expected Results

  - The Django server should start without errors
  - The /mcp/ endpoint should be accessible
  - You should see MCP-related responses (JSON-RPC format)
  - Our basic MCP tools should be discoverable