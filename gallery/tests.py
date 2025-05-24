from django.test import TestCase
from django.urls import reverse
from .models import Category, Image
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile

class GalleryViewsTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Nature')
        self.image = Image.objects.create(
            title='Test Image',
            image=SimpleUploadedFile("test.jpg", b"image_content", content_type="image/jpeg"),
            created_date=date.today(),
            age_limit=0
        )
        self.image.categories.add(self.category)

    def test_gallery_view(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nature')
        self.assertContains(response, 'Test Image')

    def test_image_detail_view(self):
        response = self.client.get(reverse('image_detail', args=[self.image.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Image')
