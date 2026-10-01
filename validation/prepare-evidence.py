from pathlib import Path
import csv,html,json,shutil
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/'deliverables/row-ledger.csv').open(encoding='utf-8') as f:ledger=list(csv.DictReader(f))
rows=[r for r in ledger if r['kind']=='orders' and r['status']!='retained'][:20]
tbody=''.join('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in [r['file'],r['row'],r['status'],r['reason'],r['original']])+'</tr>' for r in rows)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><title>Nestora raw input review</title><style>body{font:16px/1.6 Segoe UI,Arial;padding:40px;background:#f3f6fb;color:#13213b}h1{color:#1e3a8a}table{background:white;border-collapse:collapse;width:100%;font-size:12px}td,th{padding:12px;text-align:left;border-bottom:1px solid #dce4ef;vertical-align:top}th{background:#1e3a8a;color:white}td:last-child{min-width:400px}strong{color:#875000}</style><h1>Six exports. One traceable cleanup.</h1><p>Original synthetic source values, shown alongside the processor's row status. Raw files are unchanged.</p><p><strong>Known input problems:</strong> duplicate records, conflicting keys, missing values, unknown SKUs and ambiguous dates.</p><table><thead><tr><th>Source file</th><th>Row</th><th>Status</th><th>Reason</th><th>Original raw values</th></tr></thead><tbody>'''+tbody+'</tbody></table></html>'
(ROOT/'validation/raw-review.html').write_text(page,encoding='utf-8')
for name in ['index.html','styles.css','app.js','echarts.min.js','echarts-license.txt']:
    shutil.copyfile(ROOT/'deliverables/report'/name,ROOT/'validation/update-output/report'/name)
