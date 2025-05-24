from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Image, Category


class GalleryViewsTests(TestCase):
    def setUp(self):
        # Створюємо категорію
        self.category = Category.objects.create(name='Test Category')

        # Створюємо "порожній" файл для зображення
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x00\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3B',
            content_type='image/gif'
        )

        # Створюємо Image з прив’язкою до категорії
        self.image = Image.objects.create(
            title='Test Image',
            image=image_file,
            created_date='2024-01-01',
            age_limit=0
        )
        self.image.categories.add(self.category)

    def test_gallery_view(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.category, response.context['categories'])

    def test_image_detail_view(self):
        response = self.client.get(reverse('image_detail', args=[self.image.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['image'], self.image)
