#!/bin/bash

# Function to open a new tab with a specific profile
open_tab_with_profile() {
  PROFILE_NAME=$1
  osascript &>/dev/null <<EOF
tell application "iTerm2"
  tell current window
    create tab with profile "$PROFILE_NAME"
  end tell
end tell
EOF
}

# Open each profile in a new tab
open_tab_with_profile "Portal - Autoshop"
open_tab_with_profile "Notify - Autoshop"
open_tab_with_profile "Product - Autoshop"
open_tab_with_profile "Orders - Autoshop"