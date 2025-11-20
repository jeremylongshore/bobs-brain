#!/bin/bash
# ADK Documentation Download Script
# Downloads all ADK documentation for grounding storage

set -e

echo "Starting ADK documentation download..."
mkdir -p knowledge_store/{tools,custom-tools,gcp-tools,research}

# Download HTML pages (will need proper web scraping)
echo "Note: HTML pages need proper web scraping with BeautifulSoup or Playwright"
echo "For now, creating placeholder commands..."

# Tools documentation
# wget -O knowledge_store/tools/adk_tools_overview.html "https://google.github.io/adk-docs/tools/"
# wget -O knowledge_store/tools/adk_builtin_tools.html "https://google.github.io/adk-docs/tools/built-in-tools/"

# Custom tools documentation
# wget -O knowledge_store/custom-tools/adk_custom_tools.html "https://google.github.io/adk-docs/tools-custom/"
# wget -O knowledge_store/custom-tools/adk_function_tools.html "https://google.github.io/adk-docs/tools-custom/function-tools/"
# wget -O knowledge_store/custom-tools/adk_mcp_tools.html "https://google.github.io/adk-docs/tools-custom/mcp-tools/"

# GCP tools documentation
# wget -O knowledge_store/gcp-tools/mcp_toolbox_databases.html "https://google.github.io/adk-docs/tools/google-cloud/mcp-toolbox-for-databases/"

# Research papers (these can be downloaded directly)
echo "Downloading research paper..."
wget -O knowledge_store/research/chain_of_thought_prompting_2201.11903.pdf "https://arxiv.org/pdf/2201.11903"

echo "Download complete!"
echo "Next steps:"
echo "1. Use a proper web scraper for HTML pages"
echo "2. Convert HTML to clean text/markdown"
echo "3. Upload to GCS bucket: bob-vertex-agent-datastore"
