#!/bin/bash
# Discover AirPlay (and RAOP) devices via Bonjour in the background — no UI.
# Uses dns-sd to browse _airplay._tcp and _raop._tcp, then merges and dedupes names.

DISCOVER_TIMEOUT="${DISCOVER_TIMEOUT:-4}"
tmp_air=$(mktemp)
tmp_raop=$(mktemp)
trap 'rm -f "$tmp_air" "$tmp_raop"' EXIT

# Extract instance name: everything after "_airplay._tcp." (names can contain spaces)
parse_airplay() {
    if [[ "$line" == *" Add "* ]]; then
        echo "$line" | sed 's/.*_airplay\._tcp\. *//'
    fi
}
# Extract "DeviceName" from "MAC@DeviceName" (raop instance names)
parse_raop() {
    if [[ "$line" == *" Add "* ]]; then
        name=$(echo "$line" | sed 's/.*_raop\._tcp\. *//')
        if [[ "$name" == *@* ]]; then
            echo "${name#*@}"
        else
            echo "$name"
        fi
    fi
}

# Browse _airplay._tcp
dns-sd -B _airplay._tcp local. 2>/dev/null | while read -r line; do parse_airplay; done > "$tmp_air" &

# Browse _raop._tcp
dns-sd -B _raop._tcp local. 2>/dev/null | while read -r line; do parse_raop; done > "$tmp_raop" &

sleep "$DISCOVER_TIMEOUT"
# Kill dns-sd so pipes close and we get whatever was collected
pkill -f "dns-sd -B _airplay._tcp" 2>/dev/null
pkill -f "dns-sd -B _raop._tcp" 2>/dev/null
wait 2>/dev/null

cat "$tmp_air" "$tmp_raop" 2>/dev/null | sort -u
