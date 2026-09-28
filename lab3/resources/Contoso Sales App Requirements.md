# Contoso Regional Sales Coaching

## Objective

Provide a focused review workspace for a global sales manager. The manager should be able to filter the latest sales period and market, identify repeatable store patterns, create a cohort, and record the next coaching action for the regional team.

Keep the experience compact: filter the model-backed population, compare store performance, inspect cohort metrics, and save the coaching brief beside the visual.

## Data and connection contract

The execution prompt supplies the Fabric workspace and semantic model. Use that exact model; Do not substitute another model based on its name or apparent schema match. If the supplied model cannot support the requirements, report the missing tables, columns, or measures before implementing the UI.

Before writing UI code, resolve the runtime model, validate the required schema, and run one populated-period query plus one grouped store query. Use the returned column names and fail clearly on connection, authorization, schema, or query errors.

Do not continue after a failed preflight or spend time on speculative query variations. Use model-provided measures where they are valid; if grouped measure references are incompatible, use an equivalent validated expression only when it preserves the metric definition.

### UI labels

- Header: **Regional coaching cohorts**
- Primary visual: **Find a coaching cohort**
- Writeback panel: **Save a cohort coaching brief**
- Detail section: **Store details & cohort refinement**

## Performance scatter

The primary visual is a store-level scatter plot:

| Encoding | Definition |
| --- | --- |
| Horizontal axis | Sales per Unit, derived as store Sales divided by store Units Sold; a customer-value proxy |
| Vertical axis | Model-evaluated Gross Margin percentage |
| Dot size | Store Sales |
| Dot color | Country/region |
| Legend | Compact expandable categorical legend mapping each dot color to its country/region |
| Reference guides | Median Sales per Unit and median Gross Margin for the current filtered population |

The quadrants are labeled **Margin strength** (upper-left), **Healthy value** (upper-right), **Priority watch** (lower-left), and **Margin opportunity** (lower-right). The labels are directional aids, not hard business thresholds; the lower-right label represents higher customer value with weaker margin than the current population median.

Points with missing Sales, Units Sold, or Gross Margin are not plotted but remain available in the detail table. No footfall, location, or other unavailable measure is invented.

## Metrics

Display the following metrics for the current selected cohort:

| Metric | Definition |
| --- | --- |
| Sales | Selected-cohort revenue from the semantic model |
| Gross profit | Sales less cost of goods from the semantic model |
| Gross margin | Model-evaluated gross margin percentage |
| Units sold | Selected-cohort units from the semantic model |
| Sales per unit | Total sales divided by total units |
| Stores | Number of stores in the selected cohort |

Missing or zero-denominator values display **Unavailable** rather than being converted to zero. Sales per unit is calculated from selected-cohort totals in the KPI strip, not by averaging store-level ratios.

## Selection behavior

Provide three scatter tools:

- **Select:** click a dot to replace the selection. Shift/Ctrl/Command-click, or keyboard Enter/Space, adds or removes a store.
- **Lasso:** draw a freeform loop around a performance pattern to replace the selection.
- **Box select:** drag a rectangle in any direction to replace the selection.

Reset to all stores returns to the current period and country/region filters. An empty lasso or box explicitly selects no stores; it must not be treated as an all-store selection.

The selection updates the KPI totals, selected-store count, adjacent coaching brief, and store detail table. Unselected points remain visible but subdued. Drawing is local and does not issue a semantic-model query until the gesture is released.

## Store details and cohort coaching brief

Keep the store detail table collapsed by default to reduce scrolling. The expanded section supports:

- Viewing stores in the current filtered population or selected cohort.
- Showing all stores under the active filters.
- Refining the selection with individual checkboxes.

When a non-empty cohort is selected, the adjacent panel provides:

- Cohort count, country/region count, Sales, average Gross Margin, and average Sales per Unit context.
- Coaching focus:
  - Margin recovery
  - Basket growth
  - Sales efficiency
  - Performance check-in
- Priority:
  - High
  - Normal
- Brief status:
  - Planned
  - In progress
  - Completed
- New coaching note, limited to 2,000 characters. When provided, it is appended once for every selected store. The app supplies the current browser-local date at save time; users do not enter a separate date field.
- A recent-note history shows the store, date added, and note text. Existing notes are retained and are not overwritten.

The app prompts before discarding an unsaved brief when the selected cohort changes. Loading, saving, saved, load-error, and save-error states must be visible. A failed save keeps the user's choices and note available for retry.

## Shared briefs and note history

Persist shared coaching briefs in the authenticated data service as `StoreCoachingCohort` records.

| Field | Behavior |
| --- | --- |
| `id` | Deterministic UUID derived from the canonical cohort key |
| `cohortKey` | Deterministic unique key derived from sorted store keys |
| `cohortLabel` | Human-readable store and country/region summary |
| `storeKeys` | Canonical JSON array serialized as text, up to 4,000 characters |
| `focus` | Required constrained coaching focus |
| `priority` | Required `High` or `Normal` value |
| `status` | Required `Planned`, `In progress`, or `Completed` value |
| `note` | Legacy optional text field retained for schema compatibility; active note history uses `StoreCoachingNote` |

Authenticated app users share the cohort briefs. Focus, priority, and status support standard create/read/update operations with last-write-wins behavior.

Append note history as authenticated `StoreCoachingNote` records. Each selected store receives one row with the same date and note text; repeated notes for the same store and date remain separate rows.

| Field | Behavior |
| --- | --- |
| `id` | Unique UUID per note row |
| `storeKey` | Required model store key; one row is created for each selected store |
| `noteDate` | Required local date in `YYYY-MM-DD` format, generated automatically when the note is saved |
| `note` | Required text up to 2,000 characters |

Generate the date from the browser's local calendar date, validate it before any write, and persist exactly `YYYY-MM-DD`. If the date is invalid, fail before changing the cohort record.

Note saves are append-only: the note entity permits authenticated create and read, but not update or delete.

After each create, read back an explicit projection of `id`, `storeKey`, `noteDate`, and `note`; do not rely on a primary-key-only lookup. Normalize date-only strings, ISO timestamps, and date objects without timezone shifting. Invalid dates or malformed responses remain errors, and every created row must match the submitted store, date, and note.

The brief records a team decision only. It does not modify sales data, require a model refresh, schedule a meeting, send a notification, or claim that coaching improved performance.

## Delivery and reliability

For repeat runs, reuse the existing project, dependencies, app backend, model binding, and data service. Do not scaffold a second app or reinstall unchanged dependencies.

Run the gates in this order:

1. **Preflight:** validate the runtime model binding, generated client, requirements file, and data-service configuration.
2. **Model smoke test:** run one populated-period query and one grouped store query before writing UI code. Stop on connection or schema errors.
3. **Focused validation:** test query parsing, selection, persistence, date handling, and error states.
4. **Build and deploy:** run the project validation command, redeploy the existing app backend, verify the hosted URL, and smoke-test filters, click/lasso/box selection, reset, and one brief save in the Fabric host.

An existing, authenticated project should target completion within 20 minutes. If a dependency or model-access issue threatens that target, report it rather than retrying alternate models or speculative queries.

The app must not produce unhandled Promise or event-handler errors during point selection, lasso, box selection, reset, or checkbox refinement. Async brief loads and saves must be invoked safely, caught, and surfaced without losing the user's selection or form values. A regression test must select a scatter point and verify that brief loading completes without an exception or visible error.

Date handling tests must cover canonical date strings, ISO timestamps, date-object readbacks, invalid calendar dates, rejection before a partial write, and full-field note confirmation. Query failures must show the model error and a retry action; they must not fabricate or silently zero-fill metrics.

Use `npm run preflight -- --requirements "<path>"` and `npm run validate -- --requirements "<path>"` as the standard repeat-run checks.

## Release acceptance

The app is ready when a regional sales manager can:

1. Filter the model-backed review period and country/region.
2. Identify a meaningful pattern in the Sales per Unit versus Gross Margin scatter.
3. Use click, box, and lasso selection to create a cohort.
4. See the six metrics update for the selected cohort.
5. Save and reopen a shared cohort coaching brief.
6. Add a note to one store and to a multi-store cohort, then verify that each save appears as a separate dated row in recent-note history.
