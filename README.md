# Nestora Home: e-commerce cleanup & sales reporting

Self-initiated portfolio project using a fictional homeware brand and deterministic synthetic Q3 2025 data. No real clients, business improvement, profit, advertising ROI or retention claims.

## View the delivery
Open `deliverables/report/index.html` directly in a Chromium browser. All scripts and chart dependencies are local; no API keys or network are needed. Open `deliverables/cleaned-data.xlsx` for all clean tables, monthly aggregates, exceptions, full row ledger and metric definitions. Amount columns ending in `_cents` are integer USD cents, not dollars.

## Reproduce or update
Python 3.11+ is recommended. In this project directory:

```sh
python -m pip install -r requirements.txt
python src/build_report.py --input data/raw --output deliverables
python -m unittest discover -s tests -v
```

`python src/generate_demo.py` regenerates the seeded demo INPUTS and separate validation controls; do not use it with real customer files. The processor does not read validation controls. New CSV/XLSX batches go in an input directory alongside `products.csv` and `refunds.csv` (XLSX also accepted). All other CSV/XLSX files are order exports. Required headers are defined in `src/build_report.py`, approved aliases in `src/field-mapping.json`. Dates must be YYYY-MM-DD or YYYY/MM/DD; ambiguous dates require confirmation. USD amounts must be nonnegative, finite, cent precision. No currency conversion is implemented. Unknown fields are not guessed; required-header errors name the file and missing columns.

For the independent October update demonstration:
```sh
python src/build_report.py --input validation/update-input --output validation/update-output
```
This leaves the Q3 delivery unchanged. New output directories contain data/workbook; copy the four static report assets (index.html, app.js, styles.css, echarts.min.js) and license from the main report directory to view the new data interactively.

## Business rules
Line identity is channel + order ID + line ID. Exact business duplicates retain one row. Same-key conflicts are pending. Unknown SKU, missing required values, invalid quantity, discount and date make the entire affected order pending. Order date, country, customer type and source must agree within an order. Product conflicts are not arbitrarily resolved. Refund identity is channel + refund ID; refunds must link to retained sales. The whole refund group is pending if cumulative refunds exceed the linked line's sale.

Sales use Decimal ROUND_HALF_UP once per line, then integer cents. Refunds follow original SALES DATE, not cash-flow date. Sales exclude tax, shipping, fees and costs. Net sales are not profit. AOV with a category filter only counts selected merchandise. Returning orders use source labels, not unique customer retention. Refund order rate counts orders with positive valid refunds. Channel-qualified order IDs prevent accidental cross-channel merging.

Every input row has retained, deduplicated or pending status in `deliverables/row-ledger.csv`, with original/normalized fields and source file/row. Changes are recorded in `normalizations.csv`. Raw inputs remain unchanged. The quality panel covers all input rows, regardless of sales filters.

## Verification and review
Tests compare a 24-line manually calculated fixture and separately generated full-data oracle to cents, verify row accounting and source hashes, deterministic reruns, schema failure and October extension. Browser checks, workbook checks, independent monthly recomputation and human-review boundaries are in `validation/qa-report.md`. The owner still needs to perform the requested personal review; agent checks do not establish that it happened.

## Sources and license
Apache ECharts 5.6.0, Apache-2.0: https://github.com/apache/echarts/tree/5.6.0 . Local redistribution includes `echarts-license.txt`. Python dependencies: pandas (BSD-3-Clause), openpyxl (MIT). Demo generation, processing and interface are project-specific AI-assisted work. No whole third-party template is presented as original client work.
