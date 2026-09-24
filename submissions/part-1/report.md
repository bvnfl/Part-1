# RoamReady - Part 1

## Repository and commit

GitHub repository: <https://github.com/bvnfl/Part-1>

Exact Part 1 commit: [`72bab0d00e6180301610d2802d20f8ab1fbf0a1a`](https://github.com/bvnfl/Part-1/commit/72bab0d00e6180301610d2802d20f8ab1fbf0a1a)

## Implementation

RoamReady is a local travel-search application with separate Vue 3 and Python/FastAPI applications. The Vue frontend provides a hotel-name search field and Search button. It sends the search term to FastAPI, displays each matching hotel stay in a table with clear Hotel, Location, Dates, Nightly Price, and Rooms Available columns, and displays a clear message when no stays match.

The FastAPI backend reads `hotels.csv` and `trips.csv`. The repository joins each trip to its hotel through `hotel_id` and performs a case-insensitive, partial-name search. FastAPI returns the matching combined records as a typed JSON response. The frontend is responsible for input and presentation, FastAPI defines the HTTP contract, and the Python repository is responsible for reading and relating the CSV data.

## Verification

I manually reviewed the changed source files and checked the application behavior. I also ran the frontend production build and both configured frontend linters successfully. Python source compilation passed, and a direct backend smoke check confirmed both matching and no-result search behavior.

| Action | Expected result | Observed result | Evidence |
| --- | --- | --- | --- |
| Search for `Boston` | Trips `T001`, `T002`, `T009`, and `T010` appear in the results table. | Four options appeared with the expected trip IDs, hotels, dates, nightly rates, and stay prices. | [Boston search results](screenshots/boston-search-results.png) |
| Search for `Miami` | A clear "No stays found" message appears. | Zero options appeared with a clear "No stays found" message. | [Miami no-results state](screenshots/miami-no-results.png) |

The official course data pack is installed. Its text IDs, column names, dates, and relationships are preserved. The browser results matched the supplied data guide and are documented in the linked screenshots above.

## Project context and next steps

Project documentation is available in the repository:

- [README setup and run instructions](../../README.md)
- [Project-specific agent instructions](../../AGENTS.md)
- [Current design and handoff note](../../handoffs/current.md)
- `[ADD A LINK TO YOUR SELECTED PROMPTS IF REQUIRED]`

The Part 1 scope supports hotel-name search backed by related CSV records. The next task is Part 2: seed SQLite with the demo travelers and bookings, add persistent booking history, and implement create, read, update, and delete operations through FastAPI and Vue.
