import streamlit as st
from PIL import Image, ImageDraw, ImageColor, ImageFont
import io

# set sidebar for input
upload_file = st.sidebar.file_uploader("Upload image: ")
user_input = st.sidebar.text_area(
    "Watermark text: ", "Watermark text\ngoes here")
font_size = st.sidebar.slider("Font size: ", 1, 100, 32)
font_style = st.sidebar.selectbox(
    'Choose font: ', ('arial.ttf', 'arial.ttf'))
color_hex = st.sidebar.color_picker("Background color hex: ", "#eee")
alph = st.sidebar.slider("Opacity: ", 0, 255, 200)

# set font
font = ImageFont.truetype(font_style, size=font_size)

# sample image path
dir = './wm-maker/Lenna_(test_image).png'

# check uploaded file
if upload_file:
    dir = upload_file

image_data = Image.open(dir)
size = image_data.size  # (width, height)
st.text('Shape: '+str(size))

# set sidebar for axis input
x_axis = st.sidebar.slider("X: ", -200, size[0], size[0]//4)
y_axis = st.sidebar.slider("Y: ", -200, size[1], size[1]//2)

col1, col2 = st.columns(2)

# initial image
col1.subheader('Canvas')
col1.image(image_data, width=100, use_column_width=True)

# draw text to image
color_rgba = (*ImageColor.getcolor(color_hex, 'RGB'), alph)
txt = Image.new('RGBA', size, (255, 255, 255, 0))
draw = ImageDraw.Draw(txt)
draw.text((x_axis, y_axis), user_input, color_rgba, font=font)
image_data.paste(txt, (0, 0), txt)

# prepare image for download
img_byte = io.BytesIO()
image_data.save(img_byte, format='PNG')
img_byte = img_byte.getvalue()

# add draw image to col2
col2.subheader('Result')
col2.image(image_data, width=100, use_column_width=True, output_format='PNG')

# download image
st.download_button('Download file', data=img_byte,
                   file_name='result.png', mime='image/png')
