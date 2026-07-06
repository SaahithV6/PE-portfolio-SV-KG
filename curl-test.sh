#!/bin/bash

# Generate unique values for testing
RANDOM_ID=$((1000 + RANDOM % 9000))
TEST_NAME="VPS_LocalTest_$RANDOM_ID"
TEST_EMAIL="vps_test_$RANDOM_ID@example.com"
TEST_CONTENT="Testing locally from inside the VPS terminal at $(date +'%Y-%m-%d %H:%M:%S')"

echo "========================================"
echo "1. Creating a timeline post (POST)..."
echo "========================================"

POST_RESPONSE=$(curl -s -X POST http://localhost:5000/api/timeline_post \
  -d "name=$TEST_NAME" \
  -d "email=$TEST_EMAIL" \
  -d "content=$TEST_CONTENT")

echo "Response from POST:"
echo "$POST_RESPONSE"
echo ""

echo "========================================"
echo "2. Fetching timeline posts (GET)..."
echo "========================================"

GET_RESPONSE=$(curl -s http://localhost:5000/api/timeline_post)

if echo "$GET_RESPONSE" | grep -q "$TEST_NAME"; then
    echo "SUCCESS: The timeline post for '$TEST_NAME' was verified!"
else
    echo "ERROR: New post was not found in the GET response data."
    exit 1
fi
