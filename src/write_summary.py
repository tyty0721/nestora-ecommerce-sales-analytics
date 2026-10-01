"""Write bilingual observations only from the published report data."""
import json, csv
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
from build_report import metrics

def main():
    text=(ROOT/'deliverables/report/data.js').read_text(encoding='utf-8');d=json.loads(text[len('window.REPORT_DATA = '):-1]);rs=d['rows'];refs=d['refunds'];sept=[r for r in rs if r['order_date'].startswith('2025-09')];aug=[r for r in rs if r['order_date'].startswith('2025-08')];s=metrics(sept,refs);a=metrics(aug,refs)
    by=defaultdict(list)
    for r in sept:by[r['category']].append(r)
    cm={k:metrics(v,refs) for k,v in by.items()};top=max(cm,key=lambda k:cm[k]['sales_cents']);channel={k:metrics([r for r in sept if r['channel']==k],refs) for k in ['Shopify','Amazon']}
    usd=lambda n:f'${n/100:,.2f}';pct=lambda n:f'{n*100:.1f}%'
    facts={'September':s,'August':a,'September_categories':cm,'September_channels':channel};(ROOT/'validation/summary-facts.json').write_text(json.dumps(facts,indent=2),encoding='utf-8')
    en=f'''# September sales review — Nestora Home

Self-initiated analysis of a fictional brand. All observations below use synthetic demo data. The default scope is September 1–30, 2025, all channels, countries and categories. The comparison period is August 1–31, 2025. Source: cleaned order lines and valid linked refunds; exact aggregates are saved in `validation/summary-facts.json`.

## Observations

1. September merchandise sales were {usd(s['sales_cents'])}, compared with {usd(a['sales_cents'])} in August, a {(s['sales_cents']/a['sales_cents']-1)*100:.1f}% increase. There were {s['orders']} valid orders, compared with {a['orders']} in August. Sales and order counts therefore moved in different directions. September average order value was {usd(s['aov_cents'])}, calculated from sales divided by valid orders; it is not a customer lifetime value measure.

2. September refunds attributed to original September sales totaled {usd(s['refund_cents'])}. Net sales were {usd(s['net_cents'])}. Positive valid refunds affected {s['refunded_orders']} orders, or {pct(s['refund_rate'])} of September orders, compared with {pct(a['refund_rate'])} in August. This is an order-level refund measure, not an item return rate or a statement of cash paid during September.

3. {top} was the highest-selling September category, with {usd(cm[top]['sales_cents'])} in selected merchandise sales. Category-filtered order counts can overlap when an order contains multiple categories. They must not be added to obtain the overall order count. This ranking describes sales value, with no inference about margin or product quality.

4. Shopify contributed {usd(channel['Shopify']['sales_cents'])}, while Amazon contributed {usd(channel['Amazon']['sales_cents'])} in September. Source-marked returning orders accounted for {pct(s['returning_share'])} of valid September orders. The source labels support an order-share description; they do not identify unique customers or establish retention.

## Explanations to validate

A larger average basket could explain the sales increase alongside fewer orders. Product mix, pricing and discount differences are alternative explanations. These possibilities require checking order composition rather than attributing the result to a promotion. Refund reasons are absent, so product defects, delivery problems and customer preference cannot be distinguished. Order-source charts measure the source labels of completed orders, not visits or conversion efficiency.

## Recommended actions

1. Review September basket composition by category and discount, keeping merchandise-only AOV consistent.
2. Obtain refund reasons and inspect the affected order lines before changing product or fulfilment decisions.
3. Resolve the eight excluded orders and the pending refund records with the source owner, then rerun the report and compare the corrected totals.

## Limits

The data is synthetic and is not evidence of real market performance. Pending records are excluded. Values are USD only; tax, shipping, platform fees, acquisition cost and product cost are absent. Net sales are not profit. No advertising ROI, conversion funnel, independent customer retention or forecasting is calculated. Refunds follow original sale dates and therefore do not form a cash-flow report.
'''
    zh=f'''# Nestora Home：9 月销售核验摘要

这是虚构家居品牌的自主作品集，所有数据均为固定种子生成的合成数据。以下观察范围为 2025 年 9 月 1—30 日，全部渠道、国家及品类；基期为 8 月 1—31 日。数值来自清洗后的明细和有效关联退款，精确汇总保存在 validation/summary-facts.json，两种语言使用同一份计算结果。

## 四项观察

1. 9 月商品销售额为 {usd(s['sales_cents'])}，8 月为 {usd(a['sales_cents'])}，增长 {(s['sales_cents']/a['sales_cents']-1)*100:.1f}%。有效订单由 {a['orders']} 张变为 {s['orders']} 张。销售额与订单数方向不同，9 月平均订单金额为 {usd(s['aov_cents'])}。这个值只包含商品金额，不能解释为客户终身价值。

2. 归属于 9 月原销售明细的退款为 {usd(s['refund_cents'])}，净销售额为 {usd(s['net_cents'])}。发生正额有效退款的订单有 {s['refunded_orders']} 张，退款订单率为 {pct(s['refund_rate'])}，8 月为 {pct(a['refund_rate'])}。这一口径按原销售日期归属，并非当月实际退款现金支出，也不代表商品退货率。

3. 9 月销售额最高的品类是 {top}，金额 {usd(cm[top]['sales_cents'])}。一张订单可包含多个品类，因此不同品类的订单数不能相加得到整体订单数。仅凭销售额排名无法判断利润或产品质量。

4. 9 月 Shopify 销售额为 {usd(channel['Shopify']['sales_cents'])}，Amazon 为 {usd(channel['Amazon']['sales_cents'])}。源数据标记为老客的订单占 {pct(s['returning_share'])}。这反映订单结构，不能当作独立客户数量或留存率。

## 待验证解释与建议

平均订单金额上升可能与购买组合、单价、折扣差异有关，需要进一步查看明细。数据没有退款原因，不能断言退款由质量或物流造成。订单来源只描述成交订单的标签，不能说明流量或转化效率。

建议一：分品类及折扣核对 9 月购物组合，保持商品金额口径一致。建议二：补充退款原因后，再决定是否调整产品或履约。建议三：与数据提供者确认被排除的 8 张订单及待确认退款，修正后重新生成并比较金额。

## 限制

合成数据不代表真实市场。待确认行未纳入相关指标。金额仅为 USD 商品金额，缺少税、运费、平台费、广告支出与采购成本，净销售额不是利润。本项目没有计算广告 ROI、转化漏斗、客户留存或销量预测，退款归属规则也使它不能充当现金流报表。
'''
    (ROOT/'deliverables/summary-en.md').write_text(en,encoding='utf-8');(ROOT/'deliverables/summary-zh.md').write_text(zh,encoding='utf-8')
    # A repeatable 20-row agent spot-check packet; not a claim of owner review.
    with (ROOT/'deliverables/row-ledger.csv').open(encoding='utf-8') as f:ledger=list(csv.DictReader(f))
    sample=[]
    for status in ['retained','deduplicated','pending']:
        matches=[r for r in ledger if r['kind']=='orders' and r['status']==status];sample.extend(matches[:8 if status=='retained' else 6])
    (ROOT/'validation/owner-spot-check.json').write_text(json.dumps(sample,ensure_ascii=False,indent=2),encoding='utf-8')
    portfolio={'title':'E-commerce Data Cleanup & Automated Sales Reporting','role':'Data cleaning, reporting and dashboard development (AI-assisted)','description':'Self-initiated project for a fictional homeware brand using synthetic data. Built a repeatable Python pipeline for six order exports, products and refunds: 2,691 valid lines, 2,016 orders, duplicates and conflicts traced by source row. Delivered clean CSV/XLSX, an offline dashboard with linked filters and CSV export, bilingual analysis and validation tests. Includes an October update example. No real client or business-performance claims.','skills':['Data Cleaning','Data Analysis','Python','Microsoft Excel','Data Visualization']}
    (ROOT/'portfolio/upwork-project.json').write_text(json.dumps(portfolio,indent=2),encoding='utf-8')
    (ROOT/'portfolio/asset-sources.md').write_text('Screenshots are captured from the real Chromium-rendered project. No generated dashboard pictures. ECharts 5.6.0 is locally redistributed under Apache-2.0. No personal or customer data. Video, if present, is assembled from observed UI frames and is labelled as a walkthrough; it is not an unscripted live customer recording.\n',encoding='utf-8')

if __name__=='__main__':main()
