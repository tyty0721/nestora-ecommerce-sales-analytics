# E-commerce sales analytics QA report

Date: 2026-10-01. Self-initiated, AI-assisted project using synthetic data for a fictional homeware brand. This report distinguishes automated calculations, workbook inspection and operated browser results. It does not claim a real client engagement or measured business improvement.

## Data and calculation checks

- All six automated validation tests passed.
- The full-data independent oracle reconciled all four audited totals exactly. This is independent reconciliation evidence rather than a visual dashboard comparison alone.
- Artifact-tool imported and rendered all eight workbook tabs. A separately constructed September `SUMIFS` sales calculation matched the reported sales; independent row-level `ROUND` checks also produced zero difference.
- The September workbook reconciliation recorded 7,601,462 sales cents on each side ($76,014.62), a zero aggregate difference and a zero line-rounding difference. The saved result is `validation/workbook-independent-check.json`.

Workbook rendering demonstrates the inspected generated workbook through artifact-tool. Native Microsoft Excel opening, recalculation and interaction were **not tested**.

## Actual HTTP browser checks

The coordinating agent operated the local HTTP preview in the Codex in-app browser. At 375, 768 and 1440px the checked dashboard layouts had no horizontal overflow. Linked filters, pagination, an empty-result case and a zero-base-period case passed the operated checks.

CSV generation was verified for the September selection: 891 data rows with the correct amounts. A local captured export is `validation/browser-export-september.csv`; its selection totals can be compared with `validation/summary-facts.json` (September sales $76,014.62, refunds $2,372.89 and net sales $73,641.73).

The in-app browser download event did **not** confirm that a user-triggered download actually landed in the user's download folder. Successful CSV creation and amount checks must not be described as a verified browser download-to-disk result.

## Evidence

| File / directory | What it establishes |
|---|---|
| `validation/workbook-independent-check.json` | Independent September workbook sum and row-rounding reconciliation |
| `validation/workbook-*.png` | Actual rendered workbook tabs |
| `validation/browser-export-september.csv` | Captured 891-row generated CSV for inspected amounts |
| `validation/summary-facts.json` | Selection-level monetary/count figures for comparison |
| `portfolio/01-overview.png` | Real dashboard overview capture |
| `portfolio/02-filtered-report.png` | Filtered report capture |
| `portfolio/03-mobile-report.png` | Actual mobile layout capture |
| `portfolio/04-data-quality.png` | Data-quality report capture |
| `portfolio/05-order-details.png` | Order-details capture |

## Unverified items and limits

- Direct `file://` access was blocked by browser safety policy. Direct double-click opening and a fully disconnected session remain unverified. HTTP checks do not establish those paths.
- An attempted 200% browser zoom produced no observable change. Actual 200% zoom remains unverified; viewport resizing is not a substitute for that check.
- Native Excel behavior, browser download-to-disk completion and a second browser are unverified.
- The data is synthetic. Accurate reconciliation demonstrates the delivered calculations on this dataset, not an improvement in a real business.
