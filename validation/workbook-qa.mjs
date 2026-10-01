import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const root='D:/upwork/projects/01-ecommerce-sales-analytics';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(root+'/deliverables/cleaned-data.xlsx'));
console.log((await wb.inspect({kind:'table',range:"'Monthly summary'!A1:H4",include:'values',tableMaxRows:4,tableMaxCols:8,maxChars:2500})).ndjson);
for(const [name,range] of [['Monthly summary','A1:H4'],['Orders','A1:F8'],['Products','A1:C8'],['Refunds','A1:H8'],['Exceptions','A1:E8'],['Row ledger','A1:E8'],['Normalizations','A1:F8'],['Definitions','A1:B9']]){
 const blob=await wb.render({sheetName:name,range,scale:1.5,format:'png'});
 await fs.writeFile(root+'/validation/workbook-'+name.toLowerCase().replaceAll(' ','-')+'.png',new Uint8Array(await blob.arrayBuffer()));
}
// Independent spreadsheet formulas recompute September from the published clean rows.
const orders=wb.worksheets.getItem('Orders');
orders.getRange('U1:Y1').values=[['Month','Independent sales cents','Reported sales cents','Difference','Line rounding check']];
orders.getRange('U2').values=[['2025-09']];
orders.getRange('V2').formulas=[['=SUMIFS(N2:N2692,D2:D2692,">="&DATE(2025,9,1),D2:D2692,"<="&DATE(2025,9,30))']];
orders.getRange('W2').formulas=[["='Monthly summary'!B4"]];
orders.getRange('X2').formulas=[['=V2-W2']];
orders.getRange('Y2').formulas=[['=ROUND(G2*H2*(1-I2)*100,0)-N2']];
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'Orders!U1:Y2',include:'values,formulas',tableMaxRows:2,tableMaxCols:5,maxChars:3000})).ndjson);
await fs.writeFile(root+'/validation/workbook-independent-check.json',JSON.stringify(orders.getRange('U1:Y2').values,null,2));
// Validation formulas are disposable; exported client workbook is unchanged.
