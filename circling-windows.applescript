-- AppleScript to open 5 Finder windows and move them together in a circle
-- The windows are spaced evenly around the circle (72 degrees apart)

-- Parameters for the circular motion
property centerX : 700 -- X coordinate of the circle's center
property centerY : 450 -- Y coordinate of the circle's center
property radius : 250 -- Radius of the circle in pixels
property totalSteps : 90 -- Total number of positions in the circle (should be divisible by windowCount)
property delay_time : 0.05 -- Time between movements (in seconds)
property rotations : 3 -- Number of complete rotations
property windowCount : 5 -- Number of windows going around the circle
property halfW : 150 -- Half of each window's width
property halfH : 100 -- Half of each window's height

-- Precompute the circle positions once with a single shell call,
-- instead of calling bc twice per window per step.
-- awk prints integer offsets "dx dy" on each line.
set awkScript to "awk 'BEGIN{pi=atan2(0,-1); for(i=0;i<" & totalSteps & ";i++){t=i*2*pi/" & totalSteps & "; printf \"%d %d\\n\", " & radius & "*cos(t), " & radius & "*sin(t)}}'"
set offsetLines to paragraphs of (do shell script awkScript)

set offsetsX to {}
set offsetsY to {}
repeat with aLine in offsetLines
	set end of offsetsX to (word 1 of aLine) as integer
	set end of offsetsY to (word 2 of aLine) as integer
end repeat

-- How many steps apart each window is on the circle
set spacing to totalSteps div windowCount

tell application "Finder"
	activate

	-- Open the windows and keep a stable reference to each one (by id)
	set theWindows to {}
	repeat windowCount times
		set newWindow to make new Finder window
		set end of theWindows to Finder window id (id of newWindow)
	end repeat
	delay 1

	-- Move all windows in a circle
	repeat rotations times
		repeat with i from 0 to totalSteps - 1
			repeat with k from 1 to windowCount
				-- Each window is shifted along the circle by (k - 1) * spacing steps
				set idx to ((i + (k - 1) * spacing) mod totalSteps) + 1
				set newX to centerX + (item idx of offsetsX)
				set newY to centerY + (item idx of offsetsY)

				set bounds of (item k of theWindows) to {newX - halfW, newY - halfH, newX + halfW, newY + halfH}
			end repeat

			-- Wait briefly before moving again
			delay delay_time
		end repeat
	end repeat
end tell
