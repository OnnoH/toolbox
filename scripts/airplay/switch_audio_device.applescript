on run argv
	if length of argv is 0 then
		return "Error: No device name provided."
	end if
	
	set targetDeviceName to item 1 of argv
	
	tell application "System Events"
		tell process "ControlCenter"
			set soundMenuNames to {"Sound", "Dźwięk", "Volume", "Audio", "Ton", "Son"}
			set soundItem to missing value
			
			repeat with currentName in soundMenuNames
				repeat with menuBarItem in every menu bar item of menu bar 1
					if description of menuBarItem as text is (currentName as text) then
						set soundItem to menuBarItem
						exit repeat
					end if
				end repeat
				if soundItem is not missing value then exit repeat
			end repeat
			
			if soundItem is missing value then
				return "Error: Sound menu not found. Please ensure it is visible in the menu bar."
			end if
			
			click soundItem
			delay 0.5
			
			repeat with currentCheckbox in every checkbox of scroll area 1 of group 1 of window "Control Center"
				set deviceId to value of attribute "AXIdentifier" of currentCheckbox
				try
					set deviceName to text 14 thru -1 of deviceId
					if deviceName contains targetDeviceName then
						click currentCheckbox
						click soundItem -- Close the menu
						return "Switched to " & deviceName
					end if
				end try
			end repeat
			
			click soundItem -- Close the menu
			return "Device '" & targetDeviceName & "' not found."
		end tell
	end tell
end run
