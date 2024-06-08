#!/bin/bash

# Get the system boot time
boot_time=$(uptime -s)

# Get the current time
current_time=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

echo "System boot time: $boot_time"
echo "Current time: $current_time"

# Calculate the time since last reboot
time_since_reboot=$(echo "$(date -d "$current_time" +"%s") - $(date -d "$boot_time" +"%s")" | bc)

# Print the time since last reboot in human-readable format
echo "Time since last reboot: $(date -u -d @"$time_since_reboot" +"%T")"
