"""Encode REAL browser frames, resampling each recorded scene to 10 seconds."""
from pathlib import Path
import json, imageio.v2 as imageio, numpy as np
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1]
frames=sorted((root/'validation/recording-frames').glob('*.png'))
scenes=[(89,108,'01  Original exports: anomalies remain traceable'),(0,17,'02  Cleaned results: consistent merchandise metrics'),(17,35,'03  Filters: Shopify, US and Bedding'),(35,53,'04  Quality: pending records and source values'),(53,71,'05  Details: inspect order lines and amounts'),(71,89,'06  Responsive report on a 375 px viewport'),(108,len(frames),'07  New October batch: rerun the same processor')]
writer=imageio.get_writer(root/'portfolio/demo-walkthrough.mp4',fps=12,codec='libx264',quality=7,macro_block_size=1)
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',22)
for start,end,caption in scenes:
    seq=frames[start:end]
    for i in range(120):
        img=Image.open(seq[min(len(seq)-1,int(i*len(seq)/120))]).convert('RGB');img.thumbnail((1280,736),Image.Resampling.LANCZOS)
        canvas=Image.new('RGB',(1280,800),'#13213b');canvas.paste(img,((1280-img.width)//2,54+(736-img.height)//2));draw=ImageDraw.Draw(canvas);draw.text((25,13),caption,font=font,fill='white');writer.append_data(np.array(canvas))
writer.close()
(root/'portfolio/video-manifest.json').write_text(json.dumps({'duration_seconds':70,'fps':12,'source':'Actual Chromium browser screenshots captured every ~0.5 seconds during a scripted walkthrough. Resampled per scene. No generated product frames, real client results or voice-over.','scenes':scenes},indent=2),encoding='utf-8')
print(root/'portfolio/demo-walkthrough.mp4')
