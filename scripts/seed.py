from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.dynasty import Dynasty
from app.models.decision_node import DecisionNode
from app.models.decision_option import DecisionOption

INITIAL_DATA = {
    "dynasties": [
        {"id": 1, "name": "شاهنشاهی هخامنشی", "country": "ایران", "start_year": -550, "end_year": -330, "description": "نخستین امپراتوری جهانی که بر پایه حقوق بشر، تسامح دینی و یکپارچگی فرهنگی بنا نهاده شد.", "image_url": "/images/dynasties/achaemenid.jpg", "opening_brief": "سال ۵۵۹ پیش از میلاد. جهان در آستانه یک دگرگونی عظیم است. شما، کوروش، فرزند کمبوجیه یکم، شاه انشان، رهبری قومی را بر عهده گرفته‌اید که خراج‌گزار مادها هستند. در شمال، امپراتوری قدرتمند ماد، در غرب، پادشاهی ثروتمند لیدیه و در شرق، بابل باشکوه، قدرت‌های زمانه هستند. آیا به عنوان یک حاکم دست‌نشانده باقی خواهید ماند یا سرنوشت خود را برای بنای بزرگترین امپراتوری جهان رقم خواهید زد؟", "start_decision_node_id": 1, "initial_resources": {"treasury": 800, "stability": 60, "military_strength": 120, "religious_influence": 50}},
        {"id": 2, "name": "شاهنشاهی اشکانی", "country": "ایران", "start_year": -247, "end_year": 224, "description": "سلسله‌ای که فرهنگ هلنیستی را با فرهنگ ایرانی درآمیخت و برای قرن‌ها سدی استوار در برابر امپراتوری روم بود.", "image_url": "/images/dynasties/parthian.jpg", "opening_brief": "سال ۲۴۷ پیش از میلاد. میراث اسکندر در حال فروپاشی است. سلوکیان، جانشینان یونانی او، بر سرزمین ایران حکمرانی می‌کنند، اما قدرتشان متزلزل است. شما، ارشک، رهبر قبیله پرنی، فرصت را برای شورش غنیمت می‌شمارید. در غرب، سلوکیان و در دوردست، جمهوری روم در حال ظهور است. آیا می‌توانید با تکیه بر سواران جنگاور خود، استقلال را به ارمغان آورده و یک شاهنشاهی جدید و پایدار را بنیان نهید؟", "start_decision_node_id": 2, "initial_resources": {"treasury": 600, "stability": 50, "military_strength": 150, "religious_influence": 30}},
        {"id": 3, "name": "شاهنشاهی ساسانی", "country": "ایران", "start_year": 224, "end_year": 651, "description": "آخرین شاهنشاهی بزرگ ایران باستان و احیاگر فرهنگ و دین زرتشتی که تأثیری عمیق بر تمدن اسلامی و جهان گذاشت.", "image_url": "/images/dynasties/sasanian.jpg", "opening_brief": "سال ۲۲۴ میلادی. اردشیر بابکان، حاکم پارس، علیه اردوان چهارم، آخرین شاه اشکانی، قیام کرده است. شما در نقش اردشیر، رویای احیای شکوه ایران باستان و بازگرداندن دین بهی را در سر دارید. اما رومیان در غرب و اقوام بیابان‌گرد در شرق، تهدیدهایی جدی هستند. آیا می‌توانید امپراتوری پراکنده را یکپارچه کرده و عظمت گذشته را بازگردانید؟", "start_decision_node_id": 3, "initial_resources": {"treasury": 1200, "stability": 65, "military_strength": 140, "religious_influence": 80}},
        {"id": 4, "name": "دولت صفوی", "country": "ایران", "start_year": 1501, "end_year": 1736, "description": "دولتی که با رسمی کردن مذهب تشیع، هویت ملی و مذهبی جدیدی به ایران بخشید و باعث احیای هنر و معماری شد.", "image_url": "/images/dynasties/safavid.jpg", "opening_brief": "سال ۱۵۰۱ میلادی. ایران‌زمین پس از قرن‌ها، تکه‌تکه و تحت حاکمیت‌های محلی است. شما، اسماعیل، نوجوانی سیزده ساله و رهبر طریقت صوفیانه صفوی، از تبعید بازگشته‌اید. با تکیه بر وفاداری بی‌چون و چرای قزلباشان، قصد دارید نه تنها یک حکومت، بلکه یک هویت جدید برای ایران بسازید. اما امپراتوری عثمانی در غرب و ازبکان در شرق، منتظر کوچکترین لغزش شما هستند", "start_decision_node_id": 4, "initial_resources": {"treasury": 500, "stability": 40, "military_strength": 90, "religious_influence": 90}},
        {"id": 5, "name": "دولت قاجار", "country": "ایران", "start_year": 1789, "end_year": 1925, "description": "دورانی از گذار ایران به دوران مدرن، مواجهه با قدرت‌های استعماری و آغاز جنبش‌های مشروطه‌خواهی.", "image_url": "/images/dynasties/qajar.jpg", "opening_brief": "سال ۱۷۹۴ میلادی. پس از آشوب‌های طولانی پس از صفویه، شما، آقامحمدخان، رهبر ایل قاجار، سرانجام بر تمام رقبای داخلی پیروز شده‌اید. اکنون باید یک کشور از هم گسیخته را یکپارچه کنید و تهران را به عنوان پایتخت جدید برگزینید. اما در شمال، امپراتوری روسیه تزاری و در جنوب، بریتانیا، چشم به خاک و منابع شما دارند. چگونه ایران را در این دنیای جدید و بی رحم رهبری خواهید کرد؟", "start_decision_node_id": 5, "initial_resources": {"treasury": 300, "stability": 35, "military_strength": 70, "religious_influence": 60}},
        {"id": 6, "name": "دولت پهلوی", "country": "ایران", "start_year": 1925, "end_year": 1979, "description": "عصر نوسازی سریع، تمرکزگرایی دولت، اصلاحات گسترده اجتماعی و اقتصادی و دگرگونی چهره ایران.", "image_url": "/images/dynasties/pahlavi.jpg", "opening_brief": "سال ۱۳۰۴ شمسی. مجلس مؤسسان به سلطنت قاجار پایان داده و شما، رضاخان، نخست‌وزیر قدرتمند، را به عنوان شاه جدید ایران انتخاب کرده است. کشور درگیر ضعف، ناامنی و نفوذ خارجی است. شما رویای یک ایران مدرن، صنعتی و یکپارچه را در سر دارید. اولین فرمان شما برای ساختن ایرانی نوین چیست؟", "start_decision_node_id": 6, "initial_resources": {"treasury": 400, "stability": 30, "military_strength": 80, "religious_influence": 20}}
    ],
    "decision_nodes": [
        {"id": 1, "node_text": "سال ۵۵۲ پ.م. آستیاگ، شاه ماد، به قدرت روزافزون شما مشکوک شده و شما را به هگمتانه فراخوانده است. بسیاری این را یک تله برای حذف شما می‌دانند. زمان انتخاب سرنوشت است."},
        {"id": 2, "node_text": "سال ۲۴۷ پ.م. شما، ارشک، استقلال خود را در ایالت پارت اعلام کرده‌اید. اما آنتیوخوس دوم، شاه سلوکی، برای بازپس‌گیری این سرزمین لشکرکشی کرده است."},
        {"id": 3, "node_text": "سال ۲۲۴ م. شما، اردشیر بابکان، اردوان چهارم اشکانی را شکست داده‌اید. اولین قدم شما برای تحکیم قدرت یک امپراتوری نوپا و آشفته چیست؟"},
        {"id": 4, "node_text": "سال ۱۵۰۱ م. شما، شاه اسماعیل جوان، تبریز را فتح کرده‌اید. اما بقایای آق‌قویونلوها هنوز یک تهدید هستند و امپراتوری قدرتمند عثمانی شما را یک مرتد خطرناک می‌داند."},
        {"id": 5, "node_text": "سال ۱۷۹۵ م. شما، آقامحمدخان، تهران را به عنوان پایتخت برگزیده‌اید. اما ایراکلی دوم، حاکم گرجستان، با روسیه پیمان بسته و از شما سرپیچی می‌کند."},
        {"id": 6, "node_text": "سال ۱۳۰۴ ش. شما، رضاخان، توسط مجلس به عنوان شاه جدید ایران انتخاب شده‌اید. کشور غرق در ضعف، ناامنی و نفوذ خارجی است. اولین فرمان شما برای ساختن ایرانی نوین چیست؟"}
    ],
    "decision_options": [
        # Achaemenid Options (Node 1)
        {"id": 1, "node_id": 1, "option_text": "[نظامی] زمان قیام است! سپاه پارس را برای جنگ با مادها آماده می‌کنم.", "effects": {"stability": {"operation": "add", "value": -20}, "military_strength": {"operation": "add", "value": 15}, "treasury": {"operation": "add", "value": -300}}},
        {"id": 2, "node_id": 1, "option_text": "[دیپلماسی] به هگمتانه می‌روم. باید به آستیاگ اطمینان دهم.", "effects": {"stability": {"operation": "set", "value": 80}, "military_strength": {"operation": "add", "value": -5}}},
        {"id": 3, "node_id": 1, "option_text": "[توطئه] با اشراف ناراضی ماد ارتباط برقرار می‌کنم تا او را از درون تضعیف کنند.", "effects": {"stability": {"operation": "add", "value": -5}, "treasury": {"operation": "add", "value": -50}}},
        {"id": 4, "node_id": 1, "option_text": "[اقتصادی] با ارسال هدایای گران‌بها، سعی در خریدن زمان و تقویت پارس می‌کنم.", "effects": {"stability": {"operation": "add", "value": 5}, "treasury": {"operation": "add", "value": -150}}},

        # Parthian Options (Node 2)
        {"id": 5, "node_id": 2, "option_text": "[جنگ پارتیزانی] از رویارویی مستقیم پرهیز کرده و با جنگ‌های غافلگیرانه، خطوط تدارکاتی سلوکیان را قطع می‌کنم.", "effects": {"military_strength": {"operation": "add", "value": 15}, "treasury": {"operation": "add", "value": -100}}},
        {"id": 6, "node_id": 2, "option_text": "[دیپلماسی] خود را به عنوان یک ساتراپ خودمختار اما وفادار به سلوکیان معرفی می‌کنم.", "effects": {"stability": {"operation": "add", "value": 15}, "military_strength": {"operation": "add", "value": -10}}},
        {"id": 7, "node_id": 2, "option_text": "[اتحاد] با باکتریا و دیگر ساتراپی‌های شرقی که از سلوکیان ناراضی هستند، پیمان اتحاد می‌بندم.", "effects": {"stability": {"operation": "add", "value": 5}, "military_strength": {"operation": "add", "value": 5}}},
        {"id": 8, "node_id": 2, "option_text": "[عقب‌نشینی] به سرزمین‌های شرقی عقب‌نشینی کرده و منتظر فرصت بهتر می‌مانم.", "effects": {"stability": {"operation": "add", "value": -15}, "treasury": {"operation": "add", "value": -50}}},

        # Sasanian Options (Node 3)
        {"id": 9, "node_id": 3, "option_text": "[تمرکزگرایی دینی] با اعلام دین زرتشتی به عنوان دین رسمی، پایه‌های ایدئولوژیک حکومت را محکم می‌کنم.", "effects": {"religious_influence": {"operation": "add", "value": 20}, "stability": {"operation": "add", "value": -15}}},
        {"id": 10, "node_id": 3, "option_text": "[پاکسازی سیاسی] اشراف قدرتمند پارتی که هنوز وفاداری کامل ندارند را حذف می‌کنم.", "effects": {"stability": {"operation": "add", "value": 20}, "treasury": {"operation": "add", "value": -100}}},
        {"id": 11, "node_id": 3, "option_text": "[اصلاحات اقتصادی] با ضرب سکه‌های جدید و اصلاحات مالی، وضعیت اقتصادی مردم را بهبود می‌بخشم.", "effects": {"treasury": {"operation": "add", "value": 150}, "stability": {"operation": "add", "value": 10}}},
        {"id": 12, "node_id": 3, "option_text": "[نمایش قدرت نظامی] با یک لشکرکشی سریع به مرزهای روم، هم غنیمت به دست می‌آورم و هم قدرت خود را به نمایش می‌گذارم.", "effects": {"military_strength": {"operation": "add", "value": 15}, "treasury": {"operation": "add", "value": 100}, "stability": {"operation": "add", "value": -10}}},
        
        # Safavid Options (Node 4)
        {"id": 13, "node_id": 4, "option_text": "[تحکیم قدرت مرکزی] ابتدا جایگاه خود را در تبریز محکم کرده و یک دولت مرکزی قدرتمند ایجاد می‌کنم.", "effects": {"stability": {"operation": "add", "value": 20}, "treasury": {"operation": "add", "value": -50}}},
        {"id": 14, "node_id": 4, "option_text": "[حذف تهدید] فوراً به تعقیب بقایای آق‌قویونلوها پرداخته و تهدید آن‌ها را برای همیشه از بین می‌برم.", "effects": {"military_strength": {"operation": "add", "value": 10}, "stability": {"operation": "add", "value": -10}}},
        {"id": 15, "node_id": 4, "option_text": "[یکپارچگی ایدئولوژیک] با تمام قوا، مذهب تشیع را در سراسر ایران گسترش می‌دهم تا یک هویت یکپارچه ایجاد کنم.", "effects": {"religious_influence": {"operation": "add", "value": 25}, "stability": {"operation": "add", "value": -15}}},
        {"id": 16, "node_id": 4, "option_text": "[دیپلماسی خارجی] با ارسال سفیر به اروپا، به دنبال متحدی علیه امپراتوری قدرتمند عثمانی می‌گردم.", "effects": {"treasury": {"operation": "add", "value": -50}, "military_strength": {"operation": "add", "value": 5}}},
        
        # Qajar Options (Node 5)
        {"id": 17, "node_id": 5, "option_text": "[پاسخ نظامی] با لشکرکشی به قفقاز، حاکمیت ایران بر گرجستان را با قدرت به کرسی می‌نشانم.", "effects": {"military_strength": {"operation": "add", "value": 10}, "treasury": {"operation": "add", "value": -300}, "stability": {"operation": "add", "value": -10}}},
        {"id": 18, "node_id": 5, "option_text": "[اخطار دیپلماتیک] با ارسال یک اولتیماتوم به ایراکلی و دربار روسیه، خواستار تمکین او می‌شوم.", "effects": {"stability": {"operation": "add", "value": 5}, "military_strength": {"operation": "add", "value": -5}}},
        {"id": 19, "node_id": 5, "option_text": "[تمرکز داخلی] گرجستان را نادیده گرفته و تمام تمرکز خود را بر روی یکپارچگی و بازسازی داخلی ایران می‌گذارم.", "effects": {"stability": {"operation": "add", "value": 15}, "treasury": {"operation": "add", "value": 50}}},
        {"id": 20, "node_id": 5, "option_text": "[ایجاد تفرقه] با حمایت از رقبای داخلی ایراکلی در گرجستان، سعی در بی‌ثبات کردن حکومت او می‌کنم.", "effects": {"treasury": {"operation": "add", "value": -100}, "stability": {"operation": "add", "value": -5}}},

        # Pahlavi Options (Node 6)
        {"id": 21, "node_id": 6, "option_text": "[ایجاد ارتش نوین] اولین اولویت، ایجاد یک ارتش ملی یکپارچه و قدرتمند برای پایان دادن به ناامنی است.", "effects": {"military_strength": {"operation": "set", "value": 150}, "treasury": {"operation": "add", "value": -400}, "stability": {"operation": "add", "value": 10}}},
        {"id": 22, "node_id": 6, "option_text": "[اصلاحات قضایی] با ایجاد یک سیستم دادگستری مدرن، کاپیتولاسیون را لغو کرده و حاکمیت ملی را بازمی‌گردانم.", "effects": {"stability": {"operation": "add", "value": 20}, "religious_influence": {"operation": "add", "value": -10}}},
        {"id": 23, "node_id": 6, "option_text": "[توسعه زیرساخت] تمام منابع را بر روی ساخت راه‌آهن سراسری و جاده‌ها برای اتصال کشور متمرکز می‌کنم.", "effects": {"treasury": {"operation": "add", "value": -250}, "stability": {"operation": "add", "value": 10}}},
        {"id": 24, "node_id": 6, "option_text": "[سرکوب مخالفان] با سرکوب سریع و قاطع ایلات و خوانین متمرد، قدرت دولت مرکزی را به تمام نقاط کشور گسترش می‌دهم.", "effects": {"stability": {"operation": "set", "value": 50}, "military_strength": {"operation": "add", "value": 10}, "treasury": {"operation": "add", "value": -150}}}
    ]
}

def seed_data(db: Session):
    """
    Seeds the database with initial data using modern SQLAlchemy 2.0 syntax.
    """
    print("Seeding initial data...")
    try:
        # This function seeds data from the INITIAL_DATA dictionary.
        # It checks for existence before adding to prevent duplicates on re-runs.
        
        for dynasty_data in INITIAL_DATA["dynasties"]:
            if not db.get(Dynasty, dynasty_data["id"]):
                db.add(Dynasty(**dynasty_data))
        
        for node_data in INITIAL_DATA["decision_nodes"]:
            if not db.get(DecisionNode, node_data["id"]):
                db.add(DecisionNode(**node_data))

        for option_data in INITIAL_DATA["decision_options"]:
            if not db.get(DecisionOption, option_data["id"]):
                db.add(DecisionOption(**option_data))

        db.commit()
        print("Data seeded successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()


def main():
    """Initializes a database session and runs the seeding process."""
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
