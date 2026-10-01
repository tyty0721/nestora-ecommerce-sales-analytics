"""Deterministic synthetic fixtures. The processor never reads validation answers."""
import csv, json, random
from pathlib import Path
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

ROOT = Path(__file__).resolve().parents[1]
FIELDS = 'channel order_id line_id order_date country sku quantity unit_price_usd discount_rate customer_type traffic_source'.split()

def write_csv(path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields or list(rows[0])); w.writeheader(); w.writerows(rows)

def generate(target, months=(7, 8, 9), seed=721):
    rng = random.Random(seed)
    products = [dict(sku=f'{cat[:3].upper()}{i:02}', product_name=f'{name} {i}', category=cat) for cat,name in [('Bedding','Linen duvet'),('Kitchen','Ceramic bowl'),('Decor','Oak frame'),('Storage','Woven basket'),('Lighting','Desk lamp')] for i in range(1,5)]
    rows=[]; refunds=[]; n=0
    for month in months:
        start=date(2025,month,1); end=date(2025,month+1,1)
        for day in range((end-start).days):
            d=start+timedelta(days=day)
            for channel in ['Shopify','Amazon']:
                for _ in range(11):
                    n+=1; order=f'N{n:05}'; country=rng.choice(['US','US','CA','UK','DE']); typ=rng.choice(['New','New','Returning']); traffic=rng.choice(['Organic','Paid search','Email','Direct','Marketplace'])
                    for line in range(1,rng.choice([2,2,3])):
                        p=rng.choice(products); cents=rng.choice([1499,2499,3999,5999,7999]); q=rng.randint(1,3); discount=rng.choice(['0','0','0.10','0.15'])
                        r=dict(zip(FIELDS,[channel,order,str(line),d.isoformat(),country,p['sku'],str(q),f'{cents/100:.2f}',discount,typ,traffic]));rows.append(r)
                        if rng.random()<0.065:
                            amount=(Decimal(q)*Decimal(r['unit_price_usd'])*(1-Decimal(discount))*Decimal('0.5')).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
                            refunds.append(dict(refund_id=f'R{len(refunds)+1:05}',channel=channel,order_id=order,line_id=str(line),refund_date=(d+timedelta(days=5)).isoformat(),refund_amount_usd=str(amount)))
    # Known faults affect whole orders. The oracle is computed BEFORE formatting/injection.
    blocked={rows[i]['order_id'] for i in [10,30,50,70,90,110,130,150]}
    expected_rows=[r for r in rows if r['order_id'] not in blocked]
    validkeys={(r['channel'],r['order_id'],r['line_id']) for r in expected_rows}
    expected_refunds=[r for r in refunds if (r['channel'],r['order_id'],r['line_id']) in validkeys]
    oracle={'lines':len(expected_rows),'orders':len({(r['channel'],r['order_id']) for r in expected_rows}), 'sales_cents':sum(int((Decimal(r['quantity'])*Decimal(r['unit_price_usd'])*(1-Decimal(r['discount_rate']))*100).quantize(Decimal('1'),rounding=ROUND_HALF_UP)) for r in expected_rows),'refund_cents':sum(int(Decimal(r['refund_amount_usd'])*100) for r in expected_refunds)}
    validation=ROOT/'validation'/('q3' if months==(7,8,9) else 'update');validation.mkdir(parents=True,exist_ok=True)
    write_csv(validation/'baseline.csv',rows,FIELDS); (validation/'expected.json').write_text(json.dumps(oracle,indent=2),encoding='utf-8')
    faults=[]
    for i,field,value in [(10,'quantity','0'),(30,'sku','UNKNOWN'),(50,'discount_rate','1.2'),(70,'order_date','07/08/2025'),(90,'country',''),(110,'unit_price_usd','')]:
        faults.append({'order_id':rows[i]['order_id'],'rule':field,'before':rows[i][field],'injected':value});rows[i][field]=value
    # Conflict and order-level disagreement.
    conflict=dict(rows[130]);conflict['quantity']='9';rows.append(conflict); faults.append({'order_id':conflict['order_id'],'rule':'same_key_conflict'})
    other=dict(rows[150]);other['line_id']='99';other['country']='CA' if other['country']!='CA' else 'DE';rows.append(other);faults.append({'order_id':other['order_id'],'rule':'order_attribute_conflict'})
    rows.extend([dict(rows[i]) for i in [200,400,600,800,1000,1200,1400,1600,1800,2000]])
    # Explicit, reversible formatting differences.
    for i,r in enumerate(rows):
        if i%17==0:r['country']=' '+r['country'].lower()+' '
        if i%19==0:r['unit_price_usd']='$'+r['unit_price_usd'] if r['unit_price_usd'] else ''
        if i%23==0:r['order_date']=r['order_date'].replace('-','/')
    for channel in ['Shopify','Amazon']:
        for month in months:
            rs=[r for r in rows if r['channel']==channel and (r['order_date'].startswith(f'2025-{month:02}') or r['order_date'].startswith(f'2025/{month:02}') or r['order_date']=='07/08/2025' and month==months[0])]
            if channel=='Amazon':
                aliases={'order_date':'Date','quantity':'Qty','unit_price_usd':'Unit price'}
                rs=[{aliases.get(k,k):v for k,v in r.items()} for r in rs]
            write_csv(target/f'{channel.lower()}-2025-{month:02}.csv',rs)
    write_csv(target/'products.csv',products+[dict(products[0])])
    refunds.extend([dict(refunds[0]),dict(refund_id='BAD-ORPHAN',channel='Shopify',order_id='MISSING',line_id='1',refund_date='2025-09-30',refund_amount_usd='10'),dict(refund_id='BAD-LIMIT',channel=rows[200]['channel'],order_id=rows[200]['order_id'],line_id=rows[200]['line_id'],refund_date='2025-10-01',refund_amount_usd='99999')])
    write_csv(target/'refunds.csv',refunds)
    (validation/'injected-errors.json').write_text(json.dumps(faults,indent=2),encoding='utf-8')
    return oracle

if __name__=='__main__':
    print(generate(ROOT/'data/raw'))
    print(generate(ROOT/'validation/update-input',(7,8,9,10)))
