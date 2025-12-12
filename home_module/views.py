import io
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from .forms import GeneratorForm
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

class HomeView(View):
    def get(self, request):
        return render(request, 'home_module/index.html', {
            'generator_form': GeneratorForm()
        })

    def post(self, request):
        generator_form = GeneratorForm(request.POST, request.FILES)

        if generator_form.is_valid():
            first_name = generator_form.cleaned_data['first_name']
            last_name = generator_form.cleaned_data['last_name']
            national_code = generator_form.cleaned_data['national_code']
            birthday = generator_form.cleaned_data['birthday']
            father_name = generator_form.cleaned_data['father_name']
            profile_image = generator_form.cleaned_data['image']
            expire_date = '1409/03/11'

            # باز کردن عکس کارت (در صورت نیاز، یا می‌توان کارت را حذف کرد و تصویر شفاف ساخت)
            bg = Image.open("static/img/ID-Card.png").convert("RGBA")
            draw = ImageDraw.Draw(bg)
            font = ImageFont.truetype("static/fonts/IRANSansWeb.ttf", 30)

            # تابع نوشتن متن فارسی راست‌چین
            def draw_rtl_text(draw, text, x, y, font, fill="black"):
                reshaped_text = arabic_reshaper.reshape(text)
                bidi_text = get_display(reshaped_text)
                bbox = draw.textbbox((0, 0), bidi_text, font=font)
                text_width = bbox[2] - bbox[0]
                draw.text((x - text_width, y), bidi_text, font=font, fill=fill)

            # نوشتن متن‌ها روی عکس
            draw_rtl_text(draw, national_code, 770, 147, font)
            draw_rtl_text(draw, first_name, 770, 210, font)
            draw_rtl_text(draw, last_name, 770, 275, font)
            draw_rtl_text(draw, birthday, 770, 335, font)
            draw_rtl_text(draw, father_name, 770, 395, font)
            draw_rtl_text(draw, expire_date, 770, 450, font)

            # باز کردن تصویر کاربر و حذف پس‌زمینه
            user_img = Image.open(profile_image).convert("RGBA")
            datas = user_img.getdata()
            new_data = []
            for item in datas:
                # اگر رنگ پس‌زمینه تقریباً سفید بود، شفافش کن
                if item[0] > 200 and item[1] > 200 and item[2] > 200:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            user_img.putdata(new_data)
            user_img = user_img.resize((200, 300))

            # جایگذاری تصویر کاربر روی کارت
            bg.paste(user_img, (30, 150), user_img)

            # خروجی نهایی
            buffer = io.BytesIO()
            bg.save(buffer, format="PNG")
            buffer.seek(0)

            response = HttpResponse(buffer, content_type="image/png")
            response["Content-Disposition"] = 'attachment; filename="card.png"'
            return response

        return render(request, 'home_module/index.html', {
            "generator_form": generator_form
        })
