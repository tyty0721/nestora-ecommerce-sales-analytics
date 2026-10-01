import unittest, sys, tempfile, json, csv, hashlib
from pathlib import Path
from decimal import Decimal
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from build_report import build, metrics, cents, money, parse_date, dedupe, ROOT, ORDER_FIELDS, PRODUCT_FIELDS, REFUND_FIELDS, dump_csv

class PipelineTests(unittest.TestCase):
    def test_golden_24_lines(self):
        """24 manually specified lines: two channels share IDs; multiple categories/order."""
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);rows=[]
            for channel in ['Shopify','Amazon']:
                for n in range(1,7):
                    for line in [1,2]:
                        rows.append(dict(zip(ORDER_FIELDS,[channel,f'G{n}',str(line),'2025-09-01','US','A' if line==1 else 'B','2' if line==1 else '1','10.005' if False else '10.01','0.1' if line==1 else '0','Returning' if n<=3 else 'New','Organic'])))
            dump_csv(p/'orders.csv',rows,ORDER_FIELDS)
            dump_csv(p/'products.csv',[dict(sku='A',product_name='A',category='Kitchen'),dict(sku='B',product_name='B',category='Decor')],PRODUCT_FIELDS)
            dump_csv(p/'refunds.csv',[dict(zip(REFUND_FIELDS,['F1','Shopify','G1','1','2025-09-02','5.00'])),dict(zip(REFUND_FIELDS,['F2','Amazon','G1','1','2025-09-02','0.00']))],REFUND_FIELDS)
            result=build(p,p/'out');m=result['totals']
            # Each order: round(2 * 10.01 * .9) + 10.01 = 18.02 + 10.01 = 28.03.
            self.assertEqual(m['sales_cents'],33636);self.assertEqual(m['refund_cents'],500);self.assertEqual(m['orders'],12);self.assertEqual(m['lines'],24);self.assertEqual(m['refunded_orders'],1);self.assertEqual(m['returning_share'],.5)
            self.assertEqual(metrics([r for r in result['rows'] if r['category']=='Kitchen'],result['refunds'])['orders'],12)
    def test_full_oracle_and_row_accounting(self):
        with tempfile.TemporaryDirectory() as tmp:
            before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'data/raw').glob('*')}
            result=build(ROOT/'data/raw',Path(tmp));expected=json.loads((ROOT/'validation/q3/expected.json').read_text())
            for k,v in expected.items():self.assertEqual(result['totals'][k],v,k)
            for kind in ['orders','products','refunds']:
                with (Path(tmp)/'row-ledger.csv').open(encoding='utf-8') as f:ledger=list(csv.DictReader(f))
                self.assertEqual(sum(result['quality'][kind].values()),sum(r['kind']==kind for r in ledger))
            self.assertEqual(before,{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'data/raw').glob('*')})
            second=build(ROOT/'data/raw',Path(tmp)/'repeat');self.assertEqual(result['totals'],second['totals']);self.assertEqual(result['rows'],second['rows'])
    def test_october_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=build(ROOT/'validation/update-input',Path(tmp));expected=json.loads((ROOT/'validation/update/expected.json').read_text())
            for k,v in expected.items():self.assertEqual(result['totals'][k],v)
            self.assertEqual(result['coverage'][1],'2025-10-31');self.assertEqual(len(result['monthly']),4)
    def test_invalid_dates_and_half_up(self):
        with self.assertRaises(ValueError):parse_date('07/08/2025')
        self.assertEqual(parse_date('2025/07/08'),'2025-07-08');self.assertEqual(cents(Decimal('1.005')),101)
        for v in ['','-1','NaN','Infinity']:
            with self.assertRaises((ValueError,ArithmeticError)):money(v)
    def test_schema_change_fails_loudly(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'orders.csv').write_text('new_unapproved_field\n1\n')
            with self.assertRaisesRegex(ValueError,'missing fields'):build(p,p/'out')
    def test_invalid_conflicted_product_blocks_entire_key(self):
        records=[{'value':dict(sku='A',product_name='One',category='Kitchen'),'status':'retained','reason':'valid'}, {'value':dict(sku='A',product_name='One',category='UNKNOWN'),'status':'pending','reason':'invalid_category'}]
        dedupe(records,['sku'],PRODUCT_FIELDS)
        self.assertEqual([r['status'] for r in records],['pending','pending'])
        self.assertTrue(all(r['reason']=='K02-same-key-conflict' for r in records))

if __name__=='__main__':unittest.main(verbosity=2)
