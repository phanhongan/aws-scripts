#!/bin/bash

INSTANCE_ID="$1"
CPU_THRESHOLD=5
CHECK_INTERVAL=100  # Interval in seconds
MAX_CHECKS=3  # Number of consecutive checks required

counter=0

echo "Instance ID: $INSTANCE_ID"

while [ $counter -lt $MAX_CHECKS ]; do
  # Get the CPU utilization of the EC2 instance
  CPU_UTILIZATION=$(aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --start-time "$(date -u -v -5M +%FT%T)" \
    --end-time "$(date -u +%FT%T)" \
    --period 300 \
    --statistics Average \
    --dimensions Name=InstanceId,Value="$INSTANCE_ID" \
    --output json | jq -r '.Datapoints[].Average')

  # Check if CPU_UTILIZATION is empty or contains no values
  if [ -z "$CPU_UTILIZATION" ]; then
    echo "Error: No CPU utilization data found."
    continue
  fi

  # Print the CPU utilization
  echo "CPU Utilization: $CPU_UTILIZATION%"

  # Check if CPU utilization is below threshold
  if (( $(echo "$CPU_UTILIZATION < $CPU_THRESHOLD" | bc -l) )); then
    ((counter++))
    echo "CPU utilization is below $CPU_THRESHOLD% - Check $counter of $MAX_CHECKS"

    if [ $counter -eq $MAX_CHECKS ]; then
      echo "CPU utilization consistently below $CPU_THRESHOLD% - Turning off the EC2 instance..."
      aws ec2 stop-instances --instance-ids "$INSTANCE_ID"
      break
    fi
  else
    counter=0
  fi

  # Sleep for the specified interval
  sleep $CHECK_INTERVAL
done
