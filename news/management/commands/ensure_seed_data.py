from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from departments.models import Department, DepartmentCategory, DepartmentLeader
from media.models import MediaCategory, MediaItem
from news.models import News, NewsCategory
from office_content.models import LeadershipMember, OfficialDocument, ProcurementItem, Project
from sights.models import Sight, SightImage

from .seed_test_data import make_mp4, make_pdf, make_png


class Command(BaseCommand):
    help = "Ensure demo data exists for fresh deployments without overwriting existing content."

    @transaction.atomic
    def handle(self, *args, **options):
        created_sections = []

        dep_categories = {}
        for item in [
            ("administration", "Администрация", "Administration", "Администрация", 1),
            ("culture", "Культура", "Culture", "Маданият", 2),
            ("tourism", "Туризм", "Tourism", "Туризм", 3),
        ]:
            category, _ = DepartmentCategory.objects.get_or_create(
                slug=item[0],
                defaults={
                    "name_ru": item[1],
                    "name_en": item[2],
                    "name_kg": item[3],
                    "order": item[4],
                    "is_active": True,
                },
            )
            dep_categories[item[0]] = category

        news_categories = {}
        for item in [
            ("official", "Официально", "Official", "Расмий", 1),
            ("events", "События", "Events", "Окуялар", 2),
            ("tourism-news", "Туризм", "Tourism", "Туризм", 3),
        ]:
            category, _ = NewsCategory.objects.get_or_create(
                slug=item[0],
                defaults={
                    "name_ru": item[1],
                    "name_en": item[2],
                    "name_kg": item[3],
                    "order": item[4],
                    "is_active": True,
                },
            )
            news_categories[item[0]] = category

        media_categories = {}
        for item in [
            ("photo-reports", "Фотоотчеты", "Photo Reports", "Сүрөт баяндар", 1),
            ("videos", "Видео", "Videos", "Видеолор", 2),
        ]:
            category, _ = MediaCategory.objects.get_or_create(
                slug=item[0],
                defaults={
                    "name_ru": item[1],
                    "name_en": item[2],
                    "name_kg": item[3],
                    "order": item[4],
                    "is_active": True,
                },
            )
            media_categories[item[0]] = category

        if not Department.objects.exists():
            for idx, item in enumerate(
                [
                    (
                        "Отдел стратегического развития",
                        "Strategic Development Department",
                        "Стратегиялык өнүгүү бөлүмү",
                        dep_categories["administration"],
                    ),
                    (
                        "Отдел культуры и молодежи",
                        "Culture and Youth Department",
                        "Маданият жана жаштар бөлүмү",
                        dep_categories["culture"],
                    ),
                    (
                        "Отдел туризма",
                        "Tourism Department",
                        "Туризм бөлүмү",
                        dep_categories["tourism"],
                    ),
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
                    category=item[3],
                    is_active=True,
                    order=idx,
                )
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
            created_sections.append("departments")

        if not Sight.objects.exists():
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
                for order in range(1, 3):
                    SightImage.objects.create(
                        sight=sight,
                        image=make_png("sight_gallery"),
                        title_ru=f"Галерея {idx}-{order}",
                        title_en=f"Gallery {idx}-{order}",
                        title_kg=f"Галерея {idx}-{order}",
                        order=order,
                    )
            created_sections.append("sights")

        if not News.objects.exists():
            now = timezone.now()
            for idx, item in enumerate(
                [
                    ("Главная новость проекта", "Main project news", "Долбоордун башкы жаңылыгы", True, True, "official"),
                    ("Открытие туристического сезона", "Tourism season opening", "Туризм сезону ачылды", True, False, "events"),
                    ("Фестиваль на побережье", "Festival on the coast", "Жээктеги фестиваль", False, False, "events"),
                    ("Новая инфраструктура", "New infrastructure", "Жаңы инфраструктура", False, False, "tourism-news"),
                    ("Молодежная инициатива", "Youth initiative", "Жаштар демилгеси", True, False, "official"),
                ],
                start=1,
            ):
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
                    category=news_categories[item[5]],
                    image=make_png("news_image"),
                    is_hot=item[3],
                    is_main=item[4],
                    is_active=True,
                )
            created_sections.append("news")

        if not MediaItem.objects.exists():
            for idx in range(1, 3):
                MediaItem.objects.create(
                    category=media_categories["photo-reports"],
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
                    category=media_categories["videos"],
                    type=MediaItem.TYPE_VIDEO,
                    title_ru=f"Видео материал {idx}",
                    title_en=f"Video material {idx}",
                    title_kg=f"Видео материалы {idx}",
                    file=make_mp4("media_video"),
                    preview_image=make_png("media_video_preview"),
                    order=idx,
                    is_active=True,
                )
            created_sections.append("media")

        if not LeadershipMember.objects.exists():
            for idx, item in enumerate(
                [
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
                ],
                start=1,
            ):
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
            created_sections.append("leadership")

        if not OfficialDocument.objects.exists():
            for idx, item in enumerate(
                [
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
                ],
                start=1,
            ):
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
            created_sections.append("documents")

        if not ProcurementItem.objects.exists():
            for idx, item in enumerate(
                [
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
                ],
                start=1,
            ):
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
            created_sections.append("procurements")

        if not Project.objects.exists():
            for idx, item in enumerate(
                [
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
                ],
                start=1,
            ):
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
            created_sections.append("projects")

        if created_sections:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Demo data ensured successfully. Created sections: {', '.join(created_sections)}."
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS("Demo data already exists. Nothing was created."))
