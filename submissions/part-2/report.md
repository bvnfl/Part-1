# RoamReady - Part 2

## Everything in Part 1

GitHub repository: <https://github.com/bvnfl/Part-1>

Exact Part 1 commit: [`72bab0d00e6180301610d2802d20f8ab1fbf0a1a`](https://github.com/bvnfl/Part-1/commit/72bab0d00e6180301610d2802d20f8ab1fbf0a1a)

Exact Part 2 commit: [`b978be2a000c674299e1eb51a11e715c97f1ca24`](https://github.com/bvnfl/Part-1/commit/b978be2a000c674299e1eb51a11e715c97f1ca24)

RoamReady retains the Part 1 hotel search flow: Vue sends a hotel-name query to FastAPI, and the Python repository reads `hotels.csv` and `trips.csv`, joins the records through `hotel_id`, and returns matching stays. Results appear in a readable table, and searches with no matches display a clear empty state.

Part 2 adds persistent reservation management. On first run, the backend creates a SQLite database and seeds all four official CSV files. The Vue interface displays booking history and allows a demo traveler to create a booking, change its traveler or status, and delete it. FastAPI provides typed endpoints for every CRUD action. The repository uses SQL for all booking reads and writes and assigns sequential text IDs such as `B007` to new records. Booking history joins the persistent hotel, trip, traveler, and booking tables.

The source files and interface were manually reviewed. The frontend production build, Oxlint, and ESLint passed. Python compilation and a direct repository smoke check passed for a successful hotel search, a no-result search, and the complete create, update, and delete booking flow. A FastAPI integration test is included in `backend/tests/test_api.py`; it should be run with `pytest` after installing `backend/requirements.txt` in the final submission environment.

| Action | Expected result | Observed result | Evidence |
| --- | --- | --- | --- |
| Search for `Boston` | Trips `T001`, `T002`, `T009`, and `T010` appear. | Automated data check passed; browser observation pending. | `[PASTE A REPOSITORY SCREENSHOT LINK]` |
| Search for `Miami` | A clear "No stays found" message appears. | Automated data check passed; browser observation pending. | `[PASTE A REPOSITORY SCREENSHOT LINK]` |
| View the seeded booking history | Six supplied reservations appear with IDs `B001` through `B006`. | Six reservations appeared with the expected traveler, status, trip, and date information. | [Initial booking history](screenshots/initial-booking-history.png) |
| Create a booking | The new reservation appears in booking history with a unique ID. | A seventh confirmed reservation appeared as `B007` for Demo Traveler 1. | [Created booking B007](screenshots/booking-created-b007.png) |
| Refresh the page and read the database again | The newly created booking remains available. | The API persistence test passed and the created record remained available for the next update action. | [Persisted B007 record](screenshots/booking-created-b007.png) |
| Edit the booking | The changed traveler and status remain available. | Booking `B007` remained in history and its status changed from confirmed to cancelled. | [Edited and cancelled B007](screenshots/booking-edited-cancelled-b007.png) |
| Delete the booking | The reservation disappears from history. | Booking `B007` disappeared and the history count returned from seven to six. | [History after deleting B007](screenshots/booking-deleted.png) |

Project documentation is available in the repository:

- [README setup and run instructions](../../README.md)
- [Project-specific agent instructions](../../AGENTS.md)
- [Current design and handoff note](../../handoffs/current.md)
- `[ADD A LINK TO YOUR SELECTED PROMPTS IF REQUIRED]`

The official protected course data is installed. The remaining submission tasks are to run the final browser verification, add accessible screenshot links, and insert the final Part 2 commit information above.

## Plus, a demo video

Demo video, under three minutes: `[PASTE AN ACCESSIBLE VIDEO URL]`

The video should show a user searching for a hotel, viewing a no-result search, creating a booking, refreshing to demonstrate persistence, editing the booking, and deleting it.
