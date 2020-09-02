
#Run OCR on meterimage
import pytesseract as tess
import pandas as pd
import io
from PIL import Image


meterI = Image.open('meterI.png')
meterII = Image.open('meterII.png')
# PSM = page segmentation mode, 13 is best so far
custom_config = r'--oem 3 --psm 13 outputbase digits'
meterI_string = (tess.image_to_string(meterI, config=custom_config))
meterII_string = (tess.image_to_string(meterII, config=custom_config))

print(meterI_string)
print(meterII_string)

I_int = int(meterI_string)
II_int = int(meterII_string)

df = pd.read_csv("output.csv")
d = { 'time':pd.datetime.now(),'meterI':I_int, 'meterII':II_int}
df = df.append(d, ignore_index=True )

df.to_csv('output.csv', index=False)

print(df)
