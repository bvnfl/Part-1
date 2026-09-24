# RoamReady — Part 2

## Everything in Part 1

### Repository and commit

Repository URL: <https://github.com/bvnfl/Part-1>  
Part 1 commit: [`72bab0d00e6180301610d2802d20f8ab1fbf0a1a`](https://github.com/bvnfl/Part-1/commit/72bab0d00e6180301610d2802d20f8ab1fbf0a1a)  
Part 2 commit: [`b978be2a000c674299e1eb51a11e715c97f1ca24`](https://github.com/bvnfl/Part-1/commit/b978be2a000c674299e1eb51a11e715c97f1ca24)

### Implementation

The Vue 3 frontend accepts a hotel-name search, displays matching offered stays with clear columns, shows an explicit no-results state, and lets a demo traveler book a stay. FastAPI validates the requests and delegates data access to a focused repository. Hotel and trip records are joined from CSV files using `hotel_id`. Users and bookings are seeded into SQLite, where booking create, read, update, and delete actions persist across restarts. The history view enriches each booking with its traveler and stay details.

### Verification

The Vue production build and both frontend linters passed. Python compilation and a direct repository smoke check passed for a successful partial-name search, a no-result search, and the complete booking create/update/delete flow. The FastAPI integration test covers that same flow but still needs to be run after installing the backend requirements in the submission environment.

Manual browser evidence to record before submission:

| Action | Expected | Observed | Evidence |
| --- | --- | --- | --- |
| Search `Boston` | Trips T001, T002, T009, and T010 appear | Automated data check passed; browser check pending | `[link screenshot]` |
| Search `Miami` | Clear no-results message appears | Automated data check passed; browser check pending | `[link screenshot]` |
| View seeded history | Six supplied reservations appear | Six reservations appeared with IDs B001-B006 | [Initial history](submissions/part-2/screenshots/initial-booking-history.png) |
| Create a booking | New reservation appears in history | Confirmed booking B007 appeared as the seventh record | [Created B007](submissions/part-2/screenshots/booking-created-b007.png) |
| Refresh/read again | Created booking remains | API persistence test passed and B007 remained available | [Persisted B007](submissions/part-2/screenshots/booking-created-b007.png) |
| Edit booking | Traveler/status changes remain | B007 status changed from confirmed to cancelled | [Edited B007](submissions/part-2/screenshots/booking-edited-cancelled-b007.png) |
| Delete booking | Reservation disappears | B007 disappeared and the total returned to six | [Deleted B007](submissions/part-2/screenshots/booking-deleted.png) |

### Project context and next steps

See [README.md](README.md), [AGENTS.md](AGENTS.md), and [handoffs/current.md](handoffs/current.md). The official instructor data pack is installed. Before submission, complete the remaining browser evidence fields and add accessible screenshot links.

## Plus, a demo video

Demo video (under three minutes): `[add accessible video URL]`
