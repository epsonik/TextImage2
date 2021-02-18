# Save the images into a local folder
import os

import requests

img_ids = [
    "http://farm6.staticflickr.com/5266/5638052745_290ab274bc_z.jpg",
    "http://farm6.staticflickr.com/5466/8888583288_5c7457fdd9_z.jpg"
    "http://farm7.staticflickr.com/6001/5990968804_2f2bf4dcdc_z.jpg",
    "http://farm4.staticflickr.com/3176/5849219772_174bca00fc_z.jpg"
    "http://farm9.staticflickr.com/8422/7747689828_16bc6e44cb_z.jpg",
    "http://farm3.staticflickr.com/2654/3770940578_28d019bf96_z.jpg",
    "http://farm3.staticflickr.com/2845/9434091896_7088e4122e_z.jpg",
    "http://farm9.staticflickr.com/8461/7998588701_48ef81f2e9_z.jpg",
    "http://farm8.staticflickr.com/7133/7775781830_e93c63f661_z.jpg",
    "http://farm5.staticflickr.com/4053/4621536480_a7527cb9ba_z.jpg",
    "http://farm1.staticflickr.com/58/162744950_73058d9998_z.jpg",
    "http://farm8.staticflickr.com/7321/9897665473_13298e993a_z.jpg",
    "http://farm4.staticflickr.com/3354/3432507454_b4716b7c16_z.jpg",
    "http://farm5.staticflickr.com/4152/5180562425_cfc9daf3f6_z.jpg",
    "http://farm8.staticflickr.com/7093/7163004370_cd27ab0a59_z.jpg",
    "http://farm8.staticflickr.com/7191/6813627120_a222bcba0d_z.jpg",
    "http://farm4.staticflickr.com/3656/3347528711_fa777a292d_z.jpg",
    "http://farm4.staticflickr.com/3164/3119362097_98b99c9ff5_z.jpg",
    "http://farm7.staticflickr.com/6172/6190725271_3da48c068a_z.jpg",
    "http://farm3.staticflickr.com/2477/3739840478_e9efb7e783_z.jpg",
    "http://farm1.staticflickr.com/199/496083169_7e5ab493fb_z.jpg",
    "http://farm3.staticflickr.com/2259/1579578688_208763e3cc_z.jpg",
    "http://farm2.staticflickr.com/1389/1122190871_3f49be55d7_z.jpg",
    "http://farm6.staticflickr.com/5142/5610598335_cfa2376d6f_z.jpg",
    "http://farm3.staticflickr.com/2615/4238865433_e201afdb37_z.jpg",
    "http://farm7.staticflickr.com/6063/6080822032_d2aaf5b103_z.jpg",
    "http://farm5.staticflickr.com/4054/4628841371_e504764076_z.jpg",
    "http://farm3.staticflickr.com/2064/2207939623_4b7164c9b6_z.jpg",
    "http://farm9.staticflickr.com/8241/8604230408_b8eae446fa_z.jpg",
    "http://farm9.staticflickr.com/8058/8227739128_6f5a03196c_z.jpg",
    "http://farm1.staticflickr.com/196/505239544_9723a82ac3_z.jpg"
]
os.chdir(r'IMAGES')
os.chdir(r'COMPLICATED')
for im in img_ids:
    img_data = requests.get(im).content
    t = im.split("/")
    with open(t[-1], 'wb') as handler:
        handler.write(img_data)
