import base64
import uuid
from datetime import timedelta

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from departments.models import Department, DepartmentCategory, DepartmentLeader
from media.models import MediaCategory, MediaItem
from news.models import News, NewsCategory
from office_content.models import (
    Employee,
    LeadershipMember,
    OfficialDocument,
    ProcurementItem,
    Project,
)
from sights.models import Sight, SightImage


PNG_1X1_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8A"
    "AnMB9U2f7nQAAAAASUVORK5CYII="
)
FAKE_MP4_BYTES = b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom"
MINIMAL_PDF_BYTES = b"""%PDF-1.1
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 300 144]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj
4 0 obj<</Length 44>>stream
BT
/F1 24 Tf
72 72 Td
(Test PDF) Tj
ET
endstream
endobj
5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj
xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000053 00000 n 
0000000102 00000 n 
0000000226 00000 n 
0000000320 00000 n 
trailer<</Size 6/Root 1 0 R>>
startxref
390
%%EOF
"""


def make_png(name_prefix):
    payload = base64.b64decode(PNG_1X1_BASE64)
    return ContentFile(payload, name=f"{name_prefix}_{uuid.uuid4().hex}.png")


def make_mp4(name_prefix):
    return ContentFile(FAKE_MP4_BYTES, name=f"{name_prefix}_{uuid.uuid4().hex}.mp4")


def make_pdf(name_prefix):
    return ContentFile(MINIMAL_PDF_BYTES, name=f"{name_prefix}_{uuid.uuid4().hex}.pdf")


class Command(BaseCommand):
    help = "Seed test data for all API entities."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Clearing existing data...")
        SightImage.objects.all().delete()
        DepartmentLeader.objects.all().delete()
        News.objects.all().delete()
        MediaItem.objects.all().delete()
        LeadershipMember.objects.all().delete()
        Employee.objects.all().delete()
        OfficialDocument.objects.all().delete()
        ProcurementItem.objects.all().delete()
        Project.objects.all().delete()
        Department.objects.all().delete()
        Sight.objects.all().delete()
        NewsCategory.objects.all().delete()
        DepartmentCategory.objects.all().delete()
        MediaCategory.objects.all().delete()

        self.stdout.write("Creating categories...")
        dep_categories = [
            DepartmentCategory.objects.create(
                name_ru="Администрация",
                name_en="Administration",
                name_kg="Администрация",
                slug="administration",
                order=1,
                is_active=True,
            ),
            DepartmentCategory.objects.create(
                name_ru="Культура",
                name_en="Culture",
                name_kg="Маданият",
                slug="culture",
                order=2,
                is_active=True,
            ),
            DepartmentCategory.objects.create(
                name_ru="Туризм",
                name_en="Tourism",
                name_kg="Туризм",
                slug="tourism",
                order=3,
                is_active=True,
            ),
        ]

        news_categories = [
            NewsCategory.objects.create(
                name_ru="Официально",
                name_en="Official",
                name_kg="Расмий",
                slug="official",
                order=1,
                is_active=True,
            ),
            NewsCategory.objects.create(
                name_ru="События",
                name_en="Events",
                name_kg="Окуялар",
                slug="events",
                order=2,
                is_active=True,
            ),
            NewsCategory.objects.create(
                name_ru="Туризм",
                name_en="Tourism",
                name_kg="Туризм",
                slug="tourism-news",
                order=3,
                is_active=True,
            ),
        ]

        media_categories = [
            MediaCategory.objects.create(
                name_ru="Фотоотчеты",
                name_en="Photo Reports",
                name_kg="Сүрөт баяндар",
                slug="photo-reports",
                order=1,
                is_active=True,
            ),
            MediaCategory.objects.create(
                name_ru="Видео",
                name_en="Videos",
                name_kg="Видеолор",
                slug="videos",
                order=2,
                is_active=True,
            ),
        ]

        self.stdout.write("Creating departments and leaders...")
        departments = []
        for idx, item in enumerate(
            [
                ("Отдел стратегического развития", "Strategic Development Department", "Стратегиялык өнүгүү бөлүмү"),
                ("Отдел культуры и молодежи", "Culture and Youth Department", "Маданият жана жаштар бөлүмү"),
                ("Отдел туризма", "Tourism Department", "Туризм бөлүмү"),
            ],
            start=1,
        ):
            department = Department.objects.create(
                icon=make_png("department_icon"),
                title_ru=item[0],
                title_en=item[1],
                title_kg=item[2],
                short_description_ru="Тестовое краткое описание подразделения.",
                short_description_en="Test short description of the department.",
                short_description_kg="Бөлүмдүн тесттик кыскача сүрөттөмөсү.",
                category=dep_categories[idx - 1],
                is_active=True,
                order=idx,
            )
            departments.append(department)
            DepartmentLeader.objects.create(
                department=department,
                full_name=f"Руководитель {idx}",
                photo=make_png("leader_photo"),
                position_ru="Руководитель отдела",
                position_en="Head of Department",
                position_kg="Бөлүм башчысы",
                phone=f"+9967000000{idx}",
                email=f"leader{idx}@example.com",
                address_ru="г. Чолпон-Ата, ул. Советская, 1",
                address_en="Cholpon-Ata, Sovetskaya st. 1",
                address_kg="Чолпон-Ата ш., Совет көч. 1",
            )

        self.stdout.write("Creating sights and gallery...")
        sights = []
        for idx, item in enumerate(
            [
                ("Озеро Иссык-Куль", "Issyk-Kul Lake", "Ысык-Көл көлү"),
                ("Ущелье Джеты-Огуз", "Jety-Oguz Gorge", "Жети-Өгүз капчыгайы"),
                ("Культурный центр Рух Ордо", "Rukh Ordo Cultural Center", "Рух Ордо маданий борбору"),
            ],
            start=1,
        ):
            sight = Sight.objects.create(
                title_ru=item[0],
                title_en=item[1],
                title_kg=item[2],
                short_description_ru="Тестовое описание достопримечательности.",
                short_description_en="Test short description of the sight.",
                short_description_kg="Көрүнүктүү жердин тесттик кыскача сүрөттөмөсү.",
                description_ru="Подробное тестовое описание достопримечательности.",
                description_en="Detailed test description of the sight.",
                description_kg="Көрүнүктүү жердин кеңири тесттик сүрөттөмөсү.",
                main_image=make_png("sight_main"),
                is_active=True,
            )
            sights.append(sight)
            for order in range(1, 3):
                SightImage.objects.create(
                    sight=sight,
                    image=make_png("sight_gallery"),
                    title_ru=f"Галерея {idx}-{order}",
                    title_en=f"Gallery {idx}-{order}",
                    title_kg=f"Галерея {idx}-{order}",
                    order=order,
                )

        self.stdout.write("Creating news...")
        now = timezone.now()
        news_records = [
            ("Главная новость проекта", "Main project news", "Долбоордун башкы жаңылыгы", True, True, 0, 0),
            ("Открытие туристического сезона", "Tourism season opening", "Туризм сезону ачылды", True, False, 1, 1),
            ("Фестиваль на побережье", "Festival on the coast", "Жээктеги фестиваль", False, False, 2, 1),
            ("Новая инфраструктура", "New infrastructure", "Жаңы инфраструктура", False, False, 3, 2),
            ("Молодежная инициатива", "Youth initiative", "Жаштар демилгеси", True, False, 4, 0),
        ]
        for idx, item in enumerate(news_records, start=1):
            News.objects.create(
                title_ru=item[0],
                title_en=item[1],
                title_kg=item[2],
                short_description_ru="Тестовый анонс новости.",
                short_description_en="Test short news announcement.",
                short_description_kg="Жаңылыктын тесттик кыскача аннотациясы.",
                description_ru="Тестовое полное описание новости.",
                description_en="Test full news description.",
                description_kg="Жаңылыктын толук тесттик сүрөттөмөсү.",
                date=now - timedelta(days=idx),
                category=news_categories[item[6]],
                image=make_png("news_image"),
                is_hot=item[3],
                is_main=item[4],
                is_active=True,
            )

        self.stdout.write("Creating media items...")
        for idx in range(1, 3):
            MediaItem.objects.create(
                category=media_categories[0],
                type=MediaItem.TYPE_PHOTO,
                title_ru=f"Фото материал {idx}",
                title_en=f"Photo material {idx}",
                title_kg=f"Сүрөт материалы {idx}",
                file=make_png("media_photo"),
                preview_image=make_png("media_preview"),
                order=idx,
                is_active=True,
            )
        for idx in range(1, 3):
            MediaItem.objects.create(
                category=media_categories[1],
                type=MediaItem.TYPE_VIDEO,
                title_ru=f"Видео материал {idx}",
                title_en=f"Video material {idx}",
                title_kg=f"Видео материалы {idx}",
                file=make_mp4("media_video"),
                preview_image=make_png("media_video_preview"),
                order=idx,
                is_active=True,
            )

        self.stdout.write("Creating office leadership...")
        leadership_items = [
            (
                "Абдиев Марат Кемелович",
                "Marat Abdiev",
                "Абдиев Марат Кемелович",
                "Полномочный представитель",
                "Plenipotentiary Representative",
                "Ыйгарым укуктуу өкүл",
            ),
            (
                "Токтосунов Бакыт Эркинович",
                "Bakyt Toktosunov",
                "Токтосунов Бакыт Эркинович",
                "Первый заместитель",
                "First Deputy",
                "Биринчи орун басар",
            ),
            (
                "Джумабаева Айгуль Сапаровна",
                "Aigul Dzhumabaeva",
                "Жумабаева Айгүл Сапаровна",
                "Заместитель по социальным вопросам",
                "Deputy for Social Affairs",
                "Социалдык маселелер боюнча орун басар",
            ),
        ]
        for idx, item in enumerate(leadership_items, start=1):
            LeadershipMember.objects.create(
                full_name_ru=item[0],
                full_name_en=item[1],
                full_name_kg=item[2],
                position_ru=item[3],
                position_en=item[4],
                position_kg=item[5],
                photo=make_png("office_leadership"),
                order=idx,
                is_active=True,
            )

        self.stdout.write("Creating office employees...")
        employee_items = [
            (
                "Иванов Сергей Петрович",
                "Sergey Ivanov",
                "Иванов Сергей Петрович",
                "Главный специалист",
                "Chief Specialist",
                "Башкы адис",
                "+996555123456",
                "ivanov@issyk-kul.gov.kg",
            ),
            (
                "Касымова Алина Руслановна",
                "Alina Kasymova",
                "Касымова Алина Руслановна",
                "Ведущий консультант",
                "Senior Consultant",
                "Жетектөөчү консультант",
                "+996700987654",
                "kasymova@issyk-kul.gov.kg",
            ),
            (
                "Бектуров Нурлан Азаматович",
                "Nurlan Bekturov",
                "Бектуров Нурлан Азаматович",
                "Начальник отдела",
                "Department Head",
                "Бөлүм башчысы",
                "+996777456789",
                "bekturov@issyk-kul.gov.kg",
            ),
        ]
        for idx, item in enumerate(employee_items, start=1):
            Employee.objects.create(
                full_name_ru=item[0],
                full_name_en=item[1],
                full_name_kg=item[2],
                position_ru=item[3],
                position_en=item[4],
                position_kg=item[5],
                phone=item[6],
                email=item[7],
                photo=make_png("office_employee"),
                order=idx,
                is_active=True,
            )

        self.stdout.write("Creating official documents...")
        document_items = [
            (
                OfficialDocument.CATEGORY_REGULATION,
                "Положение об аппарате полномочного представителя",
                "Regulation on the Office of the Plenipotentiary Representative",
                "Ыйгарым укуктуу өкүлдүн аппараты жөнүндө жобо",
            ),
            (
                OfficialDocument.CATEGORY_ORDER,
                "Распоряжение о координации работы государственных органов",
                "Order on coordination of state authorities",
                "Мамлекеттик органдардын ишин координациялоо жөнүндө буйрук",
            ),
            (
                OfficialDocument.CATEGORY_REPORT,
                "Отчёт о социально-экономическом развитии области",
                "Report on socio-economic development of the region",
                "Облустун социалдык-экономикалык өнүгүүсү жөнүндө отчёт",
            ),
        ]
        for idx, item in enumerate(document_items, start=1):
            OfficialDocument.objects.create(
                category=item[0],
                title_ru=item[1],
                title_en=item[2],
                title_kg=item[3],
                file_ru=make_pdf("document_ru"),
                file_en=make_pdf("document_en"),
                file_kg=make_pdf("document_kg"),
                order=idx,
                is_active=True,
            )

        self.stdout.write("Creating procurements and tenders...")
        procurement_items = [
            (
                ProcurementItem.TYPE_PROCUREMENT,
                "Закупка компьютерного оборудования для аппарата",
                "Procurement of computer equipment for the office",
                "Аппарат үчүн компьютердик жабдууларды сатып алуу",
                "Поставка системных блоков, мониторов и оргтехники для структурных подразделений аппарата.",
                "Supply of desktop computers, monitors and office equipment for the office departments.",
                "Аппараттын бөлүмдөрү үчүн компьютерлерди, мониторлорду жана кеңсе жабдууларын жеткирүү.",
                "850000.00",
                timezone.now().date() + timedelta(days=15),
            ),
            (
                ProcurementItem.TYPE_PROCUREMENT,
                "Поставка офисной мебели для районных администраций",
                "Supply of office furniture for district administrations",
                "Райондук администрациялар үчүн кеңсе эмеректерин жеткирүү",
                "Закупка столов, кресел, шкафов и архивных стеллажей для районных подразделений.",
                "Procurement of desks, chairs, cabinets and archive shelving for district units.",
                "Райондук бөлүмдөр үчүн үстөлдөрдү, отургучтарды, шкафтарды жана архив текчелерин сатып алуу.",
                "1200000.00",
                timezone.now().date() + timedelta(days=22),
            ),
            (
                ProcurementItem.TYPE_TENDER,
                "Ремонт автодороги Каракол — Джети-Огуз",
                "Road repair on the Karakol — Jety-Oguz highway",
                "Каракол — Жети-Өгүз автоунаа жолун оңдоо",
                "Тендер на ремонт дорожного покрытия, устройство водоотвода и укрепление обочин.",
                "Tender for road surface repair, drainage works and shoulder reinforcement.",
                "Жолдун үстүн оңдоо, суу чыгаруу жана жол жээгин бекемдөө боюнча тендер.",
                "45000000.00",
                timezone.now().date() + timedelta(days=30),
            ),
            (
                ProcurementItem.TYPE_TENDER,
                "Установка системы видеонаблюдения в г. Балыкчы",
                "Installation of video surveillance system in Balykchy",
                "Балыкчы шаарында видеокөзөмөл системасын орнотуу",
                "Монтаж камер, серверного оборудования и интеграция в единый центр мониторинга.",
                "Installation of cameras, server equipment and integration into a unified monitoring center.",
                "Камераларды, сервер жабдууларын орнотуу жана бирдиктүү байкоо борборуна интеграциялоо.",
                "7200000.00",
                timezone.now().date() + timedelta(days=18),
            ),
        ]
        for idx, item in enumerate(procurement_items, start=1):
            ProcurementItem.objects.create(
                type=item[0],
                title_ru=item[1],
                title_en=item[2],
                title_kg=item[3],
                description_ru=item[4],
                description_en=item[5],
                description_kg=item[6],
                amount_som=item[7],
                deadline=item[8],
                order=idx,
                is_active=True,
            )

        self.stdout.write("Creating projects and state programs...")
        project_items = [
            (
                Project.TYPE_INVESTMENT,
                "Развитие туристической инфраструктуры северного берега",
                "Development of the northern shore tourism infrastructure",
                "Түндүк жээктеги туристтик инфраструктураны өнүктүрүү",
                "Строительство многофункционального туристического комплекса с объектами размещения и сервисной инфраструктурой.",
                "Construction of a multifunctional tourism complex with accommodation and service infrastructure.",
                "Жайгаштыруу жана тейлөө инфратүзүмү бар көп функционалдуу туристтик комплексти куруу.",
                "2025–2027",
                "2025–2027",
                "2025–2027",
            ),
            (
                Project.TYPE_INVESTMENT,
                "Технопарк «Иссык-Куль Digital»",
                "Issyk-Kul Digital Technopark",
                "«Ысык-Көл Digital» технопаркы",
                "Создание площадки для IT-компаний, образовательных программ и цифровых сервисов региона.",
                "Creation of a platform for IT companies, educational programs and regional digital services.",
                "IT-компаниялар, билим берүү программалары жана аймактык санарип кызматтары үчүн аянтча түзүү.",
                "2026–2028",
                "2026–2028",
                "2026–2028",
            ),
            (
                Project.TYPE_STATE_PROGRAM,
                "Программа «Туристический Иссык-Куль»",
                "Touristic Issyk-Kul Program",
                "«Туристтик Ысык-Көл» программасы",
                "Комплексная государственная программа по развитию туризма, повышению сервиса и привлечению инвестиций.",
                "Comprehensive state program for tourism development, service improvement and investment attraction.",
                "Туризмди өнүктүрүү, тейлөөнү жакшыртуу жана инвестиция тартуу боюнча комплекстүү мамлекеттик программа.",
                "2024–2028",
                "2024–2028",
                "2024–2028",
            ),
            (
                Project.TYPE_STATE_PROGRAM,
                "Государственная программа «Чистая вода»",
                "Clean Water State Program",
                "«Таза суу» мамлекеттик программасы",
                "Обеспечение населённых пунктов области качественной питьевой водой и модернизация инфраструктуры.",
                "Provision of quality drinking water to settlements and modernization of infrastructure.",
                "Калктуу конуштарды сапаттуу ичүүчү суу менен камсыз кылуу жана инфраструктураны жаңылоо.",
                "2023–2026",
                "2023–2026",
                "2023–2026",
            ),
        ]
        for idx, item in enumerate(project_items, start=1):
            Project.objects.create(
                type=item[0],
                title_ru=item[1],
                title_en=item[2],
                title_kg=item[3],
                description_ru=item[4],
                description_en=item[5],
                description_kg=item[6],
                implementation_period_ru=item[7],
                implementation_period_en=item[8],
                implementation_period_kg=item[9],
                image=make_png("office_project"),
                order=idx,
                is_active=True,
            )

        self.stdout.write(self.style.SUCCESS("Test data generated successfully."))
