#!/bin/bash

config_file="$HOME/.ssh/config"
host="$1"
instance_id="$2"

# Check if the instance_id is provided as a command-line argument
if [ -z "$instance_id" ]; then
  echo "Usage: $0 [instance_id]"
  exit 1
fi

# Retrieve the public IP of the EC2 instance
new_hostname=$(aws ec2 describe-instances --instance-ids "$instance_id" --query "Reservations[0].Instances[0].PublicIpAddress" --output text)

# Check if the new_hostname is empty
if [ -z "$new_hostname" ]; then
  echo "Failed to retrieve the public IP for the instance ID: $instance_id"
  exit 1
fi


# Check if the config file exists
if [ ! -f "$config_file" ]; then
  echo "The config file $config_file does not exist."
  exit 1
fi

# Check if the Host exists in the config file
if ! grep -q "Host $host" "$config_file"; then
  echo "The Host $host does not exist in the config file."
  exit 1
fi

# Update the HostName entry using awk
awk -v host="$host" -v new_hostname="$new_hostname" '
  $1 == "Host" && $2 == host {
    print $0
    while (getline > 0) {
      if ($1 == "HostName") {
        print "  " $1, new_hostname
      } else if ($1 != "") {
        sub(/^\s+/, "")
        print $0
      }
      if ($0 == "") {
        break
      }
    }
  }
  { print }
' "$config_file" > "$config_file.tmp" && mv "$config_file.tmp" "$config_file"

echo "The HostName for $host has been updated to $new_hostname."
