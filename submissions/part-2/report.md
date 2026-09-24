# RoamReady - Part 2

## Everything in Part 1

GitHub repository: `[PASTE YOUR PUBLIC GITHUB REPOSITORY URL]`

Exact Part 1 commit: `[PASTE THE PART 1 COMMIT HASH]`

Exact Part 2 commit: `[PASTE THE PART 2 COMMIT HASH]`

RoamReady retains the Part 1 hotel search flow: Vue sends a hotel-name query to FastAPI, and the Python repository reads `hotels.csv` and `trips.csv`, joins the records through `hotel_id`, and returns matching stays. Results appear in a readable table, and searches with no matches display a clear empty state.

Part 2 adds persistent reservation management. On first run, the backend creates a SQLite database and seeds its users and bookings from `users.csv` and `bookings.csv`. The Vue interface displays booking history and allows a demo traveler to create a booking, change its traveler or guest count, and cancel it. FastAPI provides typed endpoints for every CRUD action. The repository uses SQL for all booking reads and writes and assigns new booking IDs through SQLite. Booking history combines the persistent booking and traveler records with stay information from the CSV data.

The source files and interface were manually reviewed. The frontend production build, Oxlint, and ESLint passed. Python compilation and a direct repository smoke check passed for a successful hotel search, a no-result search, and the complete create, update, and delete booking flow. A FastAPI integration test is included in `backend/tests/test_api.py`; it should be run with `pytest` after installing `backend/requirements.txt` in the final submission environment.

| Action | Expected result | Observed result | Evidence |
| --- | --- | --- | --- |
| Search for `Harbor` | Two Harbor Light Hotel stays appear. | `[RECORD YOUR BROWSER RESULT]` | `[PASTE A REPOSITORY SCREENSHOT LINK]` |
| Search for `Missing` | A clear "No stays found" message appears. | `[RECORD YOUR BROWSER RESULT]` | `[PASTE A REPOSITORY SCREENSHOT LINK]` |
| Create a booking | The new reservation appears in booking history with a unique ID. | `[RECORD YOUR BROWSER RESULT]` | `[PASTE A REPOSITORY SCREENSHOT LINK]` |
| Refresh the page and restart the backend | The newly created booking remains available. | `[RECORD YOUR BROWSER RESULT]` | `[PASTE A REPOSITORY SCREENSHOT LINK]` |
| Edit the booking and refresh | The changed traveler and guest count remain available. | `[RECORD YOUR BROWSER RESULT]` | `[PASTE A REPOSITORY SCREENSHOT LINK]` |
| Delete the booking and refresh | The deleted reservation does not return. | `[RECORD YOUR BROWSER RESULT]` | `[PASTE A REPOSITORY SCREENSHOT LINK]` |

Project documentation is available in the repository:

- [README setup and run instructions](../../README.md)
- [Project-specific agent instructions](../../AGENTS.md)
- [Current design and handoff note](../../handoffs/current.md)
- `[ADD A LINK TO YOUR SELECTED PROMPTS IF REQUIRED]`

The remaining submission tasks are to replace the schema-compatible demo CSVs with the official protected course data, run the final browser verification, add accessible screenshot links, and insert the final repository and commit information above.

## Plus, a demo video

Demo video, under three minutes: `[PASTE AN ACCESSIBLE VIDEO URL]`

The video should show a user searching for a hotel, viewing a no-result search, creating a booking, refreshing to demonstrate persistence, editing the booking, and deleting it.
