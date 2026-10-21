# Check a CSV before feeding it into an automated workflow

Disclosure: Hawre Toolworks is my API toolkit. This walkthrough uses its published synthetic example to explain what a dataset-quality report can and cannot tell you. The example files are public; production API calls are paid through OKX.AI.

A CSV can parse successfully and still be unsuitable for a downstream calculation. A missing value, a repeated record or a numeric column that contains text can change the meaning of an analysis. The first useful step is to inspect the dataset before deciding whether to clean it.

## Start with a small, inspectable fixture

The [sample request](https://github.com/danamohammad/hawre-toolworks-examples/blob/main/dataset-quality-report-request.json) contains this entirely synthetic dataset. The well names and measurements are examples, not field observations:

```csv
well,field,oil_bbl_d,water_cut_pct,spud_date
KRD-01,North,1250,12.5,2021-03-14
KRD-02,North,980,22.1,2021-07-02
KRD-03,South,1510,8.9,2022-01-20
KRD-04,South,605,35.4,2022-05-11
```

The request wraps the CSV string in a JSON object with a `csv` property. The published [input schema](https://github.com/danamohammad/hawre-toolworks-examples/blob/main/dataset-quality-report-schema.json) is the reference for accepted inputs; do not assume that a file path or an arbitrary URL is interchangeable with the CSV content.

The [saved result](https://github.com/danamohammad/hawre-toolworks-examples/blob/main/dataset-quality-report-result.json) is a locally computed demonstration. It is not a captured paid production response or a receipt. Its summary is:

```json
{
  "source": "csv",
  "rows": 4,
  "columns": 5,
  "duplicate_rows": 0,
  "completeness_pct": 100.0,
  "column_issues": 0
}
```

The full file also shows per-column type counts, missing values, distinct values, common values, string lengths and numeric summaries where applicable. For `oil_bbl_d`, the example reports a mean of 1086.25 and median of 1115.0.

## Independently check the basic result

After downloading or cloning the examples repository, save this script beside the JSON files and run it with Python 3. It uses only the standard library, makes no network requests and performs no payments.

```python
import csv
import io
import json
import statistics
from pathlib import Path

root = Path(__file__).resolve().parent
request = json.loads((root / "dataset-quality-report-request.json").read_text())
report = json.loads((root / "dataset-quality-report-result.json").read_text())
reader = csv.DictReader(io.StringIO(request["csv"]))
columns = reader.fieldnames or []
rows = list(reader)
assert columns and rows, "This walkthrough expects a nonempty fixture"
assert all(None not in row and all(v is not None for v in row.values())
           for row in rows), "CSV rows must match the header width"

keys = [tuple(row[column] for column in columns) for row in rows]
missing = sum(not row[column].strip() for row in rows for column in columns)
completeness = 100 * (1 - missing / (len(rows) * len(columns)))
oil_rates = [float(row["oil_bbl_d"]) for row in rows]

assert report["rows"] == len(rows) == 4
assert report["columns"] == len(columns) == 5
assert report["duplicate_rows"] == len(keys) - len(set(keys)) == 0
assert report["completeness_pct"] == completeness == 100.0
assert statistics.mean(oil_rates) == 1086.25
assert statistics.median(oil_rates) == 1115.0
print("Fixture checked: 4 rows, 5 columns, no exact duplicates or blank cells.")
```

These checks deliberately cover only this fixture and a few transparent statistics. They do not reimplement the service's type inference, issue detection or outlier rules. In a real application, define your missing-value tokens and duplicate policy explicitly: a blank cell, `NA` and `0` need not mean the same thing, and two equal measurements need not be duplicate records.

## Separate endpoint availability from successful execution

The public Dataset Quality Report endpoint is:

```text
https://a2mcp-tools.danamohammadkhidhir.workers.dev/v2/dataset-quality-report
```

The repository's `probe.py` sends synthetic sample requests without payment credentials. An unpaid request is expected to receive HTTP 402 with payment requirements. That checks whether the payment-gated route responds; it does not retrieve a paid report, prove successful paid execution, or prove customer revenue.

The probe does not sign a transaction, follow the payment challenge or authorize spending. Do not add automatic payment retries to a monitoring script. For a production purchase, use the [Dataset utilities listing on OKX.AI](https://www.okx.ai/agents/13989), review the current price and network requirements there, and use the official purchase flow. Listing status and prices can change.

## Use the report to decide, not to silently rewrite data

A complete table can still contain wrong units, impossible values or invented measurements. This fixture's 100% completeness says nothing about scientific validity. A statistical outlier is a reason to inspect a record, not permission to delete it. Date-like text also needs application-specific validation before use.

For a production workflow, keep the original input, review flagged records, record any approved transformation and validate the output against the downstream contract. Start with synthetic or non-sensitive data. Do not upload confidential files without checking the applicable processing and retention terms.

A local CSV library is often enough for a small script, including the independent checks above. A structured API can be useful when several workflows need the same reporting interface, but it adds network availability, payment and data-handling considerations. Choose it for that integration need, not because a simple calculation requires a paid service.

The [examples repository](https://github.com/danamohammad/hawre-toolworks-examples) contains the input schema, synthetic request, full saved report and unpaid probe so you can inspect each part separately. Snapshot date: 21 October 2026.
