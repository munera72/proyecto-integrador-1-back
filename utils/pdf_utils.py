from fpdf import FPDF
import os
from PIL import Image

def pdf_creation_with_images(
    folder,
    output_dir='D:\\Projects\\proyecto-integrador-1-front\\public',
    filename="ResultDoc.pdf",
    temp_dir='temp_uploads'
):
    # Path for the public folder
    public_output_path = os.path.join(output_dir, filename)
    # Path for the temp_uploads folder
    temp_output_path = os.path.join(temp_dir, filename)

    # Remove existing files if they exist
    for path in [public_output_path, temp_output_path]:
        if os.path.exists(path):
            os.remove(path)

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_font('times', '', 12)

    images = [f for f in os.listdir(folder) if not f.endswith('_mask.png') and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    images.sort()

    for img_name in images:
        mask_name = os.path.splitext(img_name)[0] + '_mask.png'
        img_path = os.path.join(folder, img_name)
        mask_path = os.path.join(folder, mask_name)
        if not os.path.exists(mask_path):
            continue

        img = Image.open(img_path)
        mask = Image.open(mask_path)
        max_height_mm = 90
        dpi = 96
        max_height_px = int(max_height_mm / 25.4 * dpi)

        def resize_keep_aspect(im):
            w, h = im.size
            if h > max_height_px:
                ratio = max_height_px / h
                return im.resize((int(w * ratio), max_height_px))
            return im

        img = resize_keep_aspect(img)
        mask = resize_keep_aspect(mask)

        img_temp = os.path.join(folder, f'temp_img_{img_name}')
        mask_temp = os.path.join(folder, f'temp_mask_{img_name}')
        img.save(img_temp)
        mask.save(mask_temp)

        img_width_mm = img.width * 25.4 / dpi
        space_mm = 40

        pdf.add_page()
        pdf.cell(0, 10, img_name, ln=True, align='C')
        x_margin = 5
        y_start = 30
        pdf.image(img_temp, x=x_margin, y=y_start, h=max_height_mm)
        pdf.image(mask_temp, x=x_margin + img_width_mm + space_mm, y=y_start, h=max_height_mm)

        os.remove(img_temp)
        os.remove(mask_temp)

    # Save PDF in both locations
    pdf.output(public_output_path)
    pdf.output(temp_output_path)
    return temp_output_path