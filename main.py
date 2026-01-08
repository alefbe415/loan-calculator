import flet as ft
import math
import os
import urllib.request

# --- دانلودر خودکار فونت ---
def install_font():
    font_name = "Vazirmatn-Bold.ttf"
    font_url = "https://github.com/rastikerdar/vazirmatn/raw/master/fonts/ttf/Vazirmatn-Bold.ttf"
    if not os.path.exists(font_name):
        print("در حال دانلود فونت...")
        try:
            urllib.request.urlretrieve(font_url, font_name)
        except:
            return None
    return font_name

def main(page: ft.Page):
    font_path = install_font()
    
    # تنظیمات صفحه
    page.title = "محاسبه‌گر وام حرفه‌ای"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 390
    page.window_height = 844
    page.padding = 0 
    page.bgcolor = ft.Colors.BLUE_GREY_50 # رنگ پس زمینه کل صفحه
    
    if font_path:
        page.fonts = {"AppFont": font_path}
        page.theme = ft.Theme(font_family="AppFont")
    
    # --- پالت رنگی ---
    COLOR_PRIMARY = ft.Colors.BLUE_700
    COLOR_SECONDARY = ft.Colors.BLUE_900
    COLOR_ACCENT = ft.Colors.AMBER_600
    
    # --- توابع منطقی ---
    def format_currency(value):
        try: return "{:,.0f}".format(value)
        except: return str(value)

    def format_input_money(e):
        try:
            clean_val = e.control.value.replace(",", "")
            if clean_val:
                formatted_val = "{:,}".format(int(clean_val))
                e.control.value = formatted_val
                e.control.update()
        except:
            pass

    def calculate_loan(e):
        try:
            if not txt_amount.value or not txt_rate.value or not txt_months.value:
                page.open(ft.SnackBar(ft.Text("لطفاً تمام مقادیر را وارد کنید"), bgcolor=ft.Colors.RED_400))
                return

            principal = int(txt_amount.value.replace(',', ''))
            annual_rate = float(txt_rate.value)
            months = int(txt_months.value)

            if months == 0: return

            monthly_rate = annual_rate / 1200
            numerator = principal * monthly_rate * (math.pow(1 + monthly_rate, months))
            denominator = (math.pow(1 + monthly_rate, months)) - 1
            monthly_payment = numerator / denominator
            
            total_payment = monthly_payment * months
            total_interest = total_payment - principal

            lbl_monthly.value = f"{format_currency(monthly_payment)} تومان"
            lbl_total.value = f"{format_currency(total_payment)}"
            lbl_interest.value = f"{format_currency(total_interest)}"
            
            results_container.opacity = 1
            results_container.offset = ft.Offset(0, 0)
            results_container.update()
            page.update()

        except ValueError:
            page.open(ft.SnackBar(ft.Text("اعداد وارد شده صحیح نیستند")))

    # --- استایل‌های سفارشی ---
    def create_input(label, suffix, default_val="", on_change_handler=None):
        return ft.TextField(
            label=label,
            value=default_val,
            suffix=ft.Text(suffix, size=12, color=ft.Colors.GREY_500),
            text_size=16,
            label_style=ft.TextStyle(size=13, color=ft.Colors.GREY_700), # رنگ لیبل خنثی شد
            text_style=ft.TextStyle(color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD), # رنگ متن سیاه و بولد
            border_color=ft.Colors.GREY_200,
            focused_border_color=COLOR_PRIMARY,
            border_radius=12,
            filled=True,
            fill_color=ft.Colors.GREY_50, # پس زمینه فیلد کمی طوسی شد تا روی کارت سفید معلوم شود
            keyboard_type=ft.KeyboardType.NUMBER,
            content_padding=15,
            height=55,
            on_change=on_change_handler
        )

    # --- المان‌های UI ---

    # 1. هدر
    header = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED, size=40, color=ft.Colors.WHITE),
            ft.Text("محاسبه‌گر وام", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Text("مدیریت هوشمند اقساط بانکی", size=13, color=ft.Colors.WHITE_70),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        width=float("inf"),
        height=240, # ارتفاع کمی بیشتر شد تا جا برای کارت باز شود
        gradient=ft.LinearGradient(
            begin=ft.Alignment(1, -1),
            end=ft.Alignment(-1, 1),
            colors=[COLOR_PRIMARY, COLOR_SECONDARY],
        ),
        border_radius=ft.BorderRadius.only(bottom_left=30, bottom_right=30),
        padding=ft.Padding.only(top=40),
        alignment=ft.Alignment(0, -0.5) # محتوا کمی بالاتر رفت
    )

    # 2. کارت ورودی‌ها (اصلاح رنگ و تداخل)
    txt_amount = create_input("مبلغ وام", "تومان", on_change_handler=format_input_money)
    txt_rate = create_input("نرخ سود", "درصد", "23")
    txt_months = create_input("مدت بازپرداخت", "ماه", "12")
    
    input_card = ft.Container(
        content=ft.Column([
            txt_amount,
            ft.Container(height=5),
            ft.Row([
                ft.Container(content=txt_rate, expand=1),
                ft.Container(width=10),
                ft.Container(content=txt_months, expand=1),
            ])
        ]),
        bgcolor=ft.Colors.WHITE, # کارت کاملا سفید
        padding=20,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 5)),
        margin=ft.Margin.only(left=20, right=20, top=-60) # کارت روی هدر سوار می‌شود
    )

    # 3. دکمه اکشن
    btn_calculate = ft.Container(
        content=ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Text("محاسبه دقیق", size=18, weight=ft.FontWeight.BOLD),
                    ft.Icon(ft.Icons.ARROW_FORWARD_IOS_ROUNDED, size=16),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                bgcolor={"": COLOR_ACCENT},
                color={"": ft.Colors.WHITE},
                shape=ft.RoundedRectangleBorder(radius=16),
                elevation=0,
                padding=22,
            ),
            on_click=calculate_loan,
            width=float("inf")
        ),
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.ORANGE_200, offset=ft.Offset(0, 5)),
        padding=ft.Padding.symmetric(horizontal=25)
    )

    # 4. نتایج
    lbl_monthly = ft.Text("0 تومان", size=24, weight=ft.FontWeight.BOLD, color=COLOR_PRIMARY)
    lbl_total = ft.Text("0", size=14, color=ft.Colors.GREY_700)
    lbl_interest = ft.Text("0", size=14, color=ft.Colors.RED_400)

    def result_row(title, value_control):
        return ft.Row([
            ft.Text(title, size=13, color=ft.Colors.GREY_500),
            value_control
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    results_container = ft.Container(
        content=ft.Column([
            ft.Text("جزئیات پرداخت", size=12, color=ft.Colors.GREY_400, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20, color=ft.Colors.GREY_100),
            
            # بخش قسط ماهانه و متن سلب مسئولیت جدید
            ft.Column([
                ft.Text("قسط ماهانه شما", size=13, color=ft.Colors.GREY_600),
                lbl_monthly,
                # متن جدید دقیقاً زیر قسط
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=12, color=ft.Colors.GREY_400),
                        ft.Text("نرخ تقریبی بدون احتساب کارمزد", size=10, color=ft.Colors.GREY_400),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=3),
                    margin=ft.Margin.only(top=5)
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            
            ft.Container(height=20),
            
            ft.Container(
                content=ft.Column([
                    result_row("کل بازپرداخت:", lbl_total),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    result_row("سود بانکی:", lbl_interest),
                ]),
                bgcolor=ft.Colors.BLUE_GREY_50,
                padding=15,
                border_radius=12
            )
        ]),
        bgcolor=ft.Colors.WHITE,
        padding=25,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.GREY_200, offset=ft.Offset(0, 10)),
        margin=ft.Margin.symmetric(horizontal=25, vertical=20),
        
        opacity=0,
        offset=ft.Offset(0, 0.1),
        animate_opacity=300,
        animate_offset=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
    )

    layout = ft.Column(
        [
            header,
            input_card, # استفاده از کارت جدید به جای سکشن قبلی
            ft.Container(height=20),
            btn_calculate,
            results_container,
            ft.Container(height=20)
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=0
    )

    page.add(layout)

if __name__ == "__main__":
    ft.app(target=main)