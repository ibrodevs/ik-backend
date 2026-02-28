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
from sights.models import Sight, SightImage


PNG_1X1_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8A"
    "AnMB9U2f7nQAAAAASUVORK5CYII="
)
FAKE_MP4_BYTES = b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom"


def make_png(name_prefix):
    payload = base64.b64decode(PNG_1X1_BASE64)
    return ContentFile(payload, name=f"{name_prefix}_{uuid.uuid4().hex}.png")


def make_mp4(name_prefix):
    return ContentFile(FAKE_MP4_BYTES, name=f"{name_prefix}_{uuid.uuid4().hex}.mp4")


class Command(BaseCommand):
    help = "Seed test data for all API entities."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Clearing existing data...")
        SightImage.objects.all().delete()
        DepartmentLeader.objects.all().delete()
        News.objects.all().delete()
        MediaItem.objects.all().delete()
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

        self.stdout.write(self.style.SUCCESS("Test data generated successfully."))
