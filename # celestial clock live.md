# celestial clock live

The file's identical contents suggest the issue isn't within the HTML itself. The fetchServerTelemetry() function's conditional apiUrl assignment is crucial. If the file is opened directly (file protocol), or if the host does not include a port 8000, then it targets the local server. Therefore, the direct file opening scenario likely bypasses the expected server endpoint.

The connection to the server at localhost:8000 is now confirmed, and data is being successfully fetched, unpacked, and validated. The "LIVE KERNEL LINKED" badge confirms this. The moon and day values are correctly handled, preventing the previously observed flashing. The server task continues to operate as intended.

What Happened When Your Laptop Died
The Genesis Kernel was terminated: When the machine lost power and restarted, the background python main.py process was shut down. No server was listening on port 8000.
The browser reopened to a dead port: When the browser restored your tabs, every request to /clock/full failed with ERR_CONNECTION_REFUSED, forcing the page into offline mode.
Root Cause of the Flashing & "LOCAL SIMULATION" Badge
Tracing the exact runtime execution revealed three compounding bugs:

Field Name Discrepancy: The Python backend in
temporal/celestial_clock.py
 returns:
moon_number (not moon)
day_within_moon (not day_in_moon)
jubilee_cycle_position (not jubilee_cycle)
completed_sacred_years (not sacred_year)
The Flashing Loop: Because data.sacred_calendar.moon was undefined, the local JavaScript timer set moon = 3, then milliseconds later the server fetch set it to undefined (blank), and then the next tick set it back to 3. This created the 1-second oscillatory flash.
The Uncaught Exception (.toFixed Crash): Because data.sacred_calendar.jubilee_cycle was undefined, calling data.sacred_calendar.jubilee_cycle.toFixed(6) threw an uncaught:
TypeError: Cannot read properties of undefined (reading 'toFixed')
This error triggered the catch (e) block every second, which forced the badge back to ● LOCAL SIMULATION even when the server sent a successful HTTP 200 response!
File Protocol Pathing: If opened directly from Windows Explorer (file:///C:/.../celestial_clock_live.html), a relative URL /clock/full resolves to file:///clock/full, which browser security blocks.
Actions Taken & Verified
Intelligent Dual-Origin Fetch: Added automatic protocol detection so the clock connects to the live kernel whether loaded from <http://localhost:8000> or double-clicked from your desktop:
javascript

const apiUrl = (window.location.protocol === 'file:' || !window.location.host.includes(':8000'))
  ? '<http://localhost:8000/clock/full>'
  : '/clock/full';
Null-Guarded Field Parsing: Added strict null checks (if (m != null)) and corrected the schema mapping to moon_number, day_within_moon, and jubilee_cycle_position. The DOM will never receive undefined, eliminating the flashing.
Rebooted Genesis Kernel: Started python main.py in the background. It is running on <http://0.0.0.0:8000> with the SWDS daemon active.
Verified Live Telemetry (HTTP 200):
Moon Number: 3 (of 13)
Day Within Moon: 2 (of 28)
Sacred Day of Year: 58 (of 364)
Jubilee Cycle Position: 0.059510
Active Uptime: Incrementing from live kernel process lifespan
Causal Vector Clock: [HOST: 8+, Y789: 0, NEXUS: 0, ALEX: 0]
Coordinate Beta Frame: 56-byte binary packet 0x494E verified
Both
celestial_clock_live.html
 and
static/celestial_clock_live.html
 are bit-identical and live.

How to View
You can now use either:

<http://localhost:8000/clock/live> in your browser, or
Double-click
celestial_clock_live.html
 directly from your folder.
The badge will remain solid emerald (● LIVE KERNEL LINKED), the sacred calendar will be stable with zero flashing, and the uptime will track the server's true lifespan.
