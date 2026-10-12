-- Open a list of URLs as tabs in Google Chrome.
--
-- Run it from Script Editor (press Run), or from Terminal:
--     osascript open_chrome_tabs.applescript
--     osascript open_chrome_tabs.applescript https://github.com https://apple.com
--
-- With no URLs given, the defaultURLs list below is opened.

property defaultURLs : {"https://www.google.com", "https://developer.mozilla.org", "https://github.com"}

on run argv
	set urlList to defaultURLs
	try
		if (count of argv) > 0 then set urlList to argv
	end try

	tell application "Google Chrome"
		activate

		-- If Chrome has no window open, make one and use its first tab.
		if (count of windows) = 0 then
			make new window
			set URL of active tab of front window to (item 1 of urlList)
			set urlList to rest of urlList
		end if

		tell front window
			repeat with theURL in urlList
				make new tab with properties {URL:(contents of theURL)}
			end repeat
		end tell
	end tell
end run
