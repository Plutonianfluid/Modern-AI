Project Overview:
The MCP server allows claude to look for ATP and WTA tennis rankings for singles aswell as the standings between 2 tennis players. The API is from: https://tennisapidoc.matchstat.com/getting-started and the API host key and sample code is found at: https://rapidapi.com/jjrm365-kIFr3Nx_odV/api/tennis-api-atp-wta-itf/playground/apiendpoint_e7025c2d-42fc-4451-8961-614f0ee7d8f0

Prerequisites:
    Python 3.12+
    uv
    Claude Desktop
    RapidAPI account
    Tennis API ATP/WTA/ITF subscription
    .env file with RAPID_API_KEY and RAPID_API_HOST

Environment setup:
    Go to the project folder: week3/tennisranking
    Install dependencies with uv add httpx python-dotenv mcp
    Create .env
    Add:
    RAPID_API_KEY=your_key_here
    RAPID_API_HOST=tennis-api-atp-wta-itf.p.rapidapi.com

Run instructions:
    Local test command: uv run tennis.py
    If the terminal waits with no output, the MCP server is running correctly.
    Stop it with Ctrl+C.

How to configure the MCP client:
    Open ~/Library/Application Support/Claude/claude_desktop_config.json
    Add your MCP server under mcpServers
    Use command: uv
    Use args:
        --directory
        absolute path to week3/tennisranking
        run
        tennis.py
    Save the file
    Quit and reopen Claude Desktop

Tool reference:
    get_singles_rankings
        Purpose: gets ATP or WTA singles rankings
        Parameters:
            tour: "atp" or "wta"
            limit: integer, default is 5
        Example input:
            tour="atp", limit=5
        Example output:
            player ranking position, player ID, name, country, ranking points
        Expected behavior:
            returns the requested number of ranked players
            handles ATP and WTA
            returns an error message if the API fails or rate limit is reached
    get_head_to_head_fixtures
        Purpose: gets head-to-head fixture data between two players
        Parameters:
            tour: "atp" or "wta"
            player1_id: integer
            player2_id: integer
        Example input:
            tour="atp", player1_id=5136, player2_id=47566
        Example output:
            fixture data between the two players
        Expected behavior:
            returns H2H fixture data if available
            returns a no-results message if no H2H data exists
            returns an error message for API failures or rate limits