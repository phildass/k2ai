#!/bin/bash

echo "=========================================="
echo "K2AI Live Assistant Integration Demo"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Step 1: Checking environment..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env file exists"
else
    echo -e "${RED}✗${NC} .env file missing"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}⚠${NC} Please edit .env and add your OpenAI API key"
fi

echo ""
echo "Step 2: Running connection test..."
python test_openai_connection.py
test_result=$?

echo ""
echo "=========================================="
if [ $test_result -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo "Your OpenAI integration is working correctly."
else
    echo -e "${YELLOW}⚠ Setup incomplete or API key not configured${NC}"
    echo "See OPENAI_SETUP_GUIDE.md for setup instructions"
fi
echo "=========================================="
