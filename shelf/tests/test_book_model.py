from django.test import TestCase
from ..models import Book


class BookModelTests(TestCase):
    def test_create_book_successful(self):
        name = 'Cursed Days'
        annotation = 'Interesting book'
        circulation = 10000
        published = 1925
        Book.objects.create(
            name=name,
            annotation=annotation,
            circulation=circulation,
            published=published
        )

        exists = Book.objects.filter(
            name=name
        ).exists()

        self.assertTrue(exists)

    def test_new_book_invalid_type_published(self):
        with self.assertRaises(TypeError):
            name = 'Cursed Days'
            annotation = 'Interesting book'
            circulation = 10000
            published = 1925,
            Book.objects.create(
                name=name,
                annotation=annotation,
                circulation=circulation,
                published=published
            )

