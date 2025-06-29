# run_example.sh - Quick test script
#!/bin/bash

# Check if API keys are set
if [ -z "$OPENAI_API_KEY" ] || [ -z "$ANTHROPIC_API_KEY" ] || [ -z "$GOOGLE_API_KEY" ]; then
    echo "Error: Please set your API keys as environment variables:"
    echo "export OPENAI_API_KEY='your-key'"
    echo "export ANTHROPIC_API_KEY='your-key'"
    echo "export GOOGLE_API_KEY='your-key'"
    exit 1
fi

echo "Running travel planner example for Georgia..."

python travel_planner.py \
    --destination "Georgia" \
    --budget 1500 \
    --days 7 \
    --travelers 2 \
    --style balanced \
    --preferences culture food hiking wine \
    --output georgia_trip.json

if [ $? -eq 0 ]; then
    echo "Success! Check georgia_trip.json for results"
    echo "Processing times and summary:"
    python -c "
import json
with open('georgia_trip.json', 'r') as f:
    data = json.load(f)
    print(f'Total time: {data[\"total_processing_time\"]:.2f}s')
    for agent, time in data['agent_times'].items():
        print(f'{agent}: {time:.2f}s')
"
else
    echo "Error occurred during planning"
    exit 1
fi