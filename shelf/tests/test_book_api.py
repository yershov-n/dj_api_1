from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from ..models import Book
from ..serializers import BookSerializer

BOOK_LIST_URL = reverse('shelf:book-list')
BOOK_ADD_URL = reverse('shelf:book-add')


def detail_url(book_id):
    return reverse('shelf:book-detail', args=[book_id])


def sample_book(name='Sands of Mars', annotation='Book about Mars', circulation=100000, published=1993):
    return Book.objects.create(name=name, annotation=annotation, circulation=circulation, published=published)


class PublicBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_retrieve_book_list(self):
        Book.objects.create(
            name='Cursed Days',
            annotation='Interesting book',
            circulation=10000,
            published=1925
        )

        Book.objects.create(
            name='Kobzar',
            annotation='The most famous Ukrainian book',
            circulation=20000,
            published=1840
        )

        res = self.client.get(BOOK_LIST_URL)

        books = Book.objects.all().order_by('name')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_book_create_login_required(self):
        res = self.client.get(BOOK_ADD_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_detail_login_required(self):
        url = reverse('shelf:book-detail', args=[1])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test_user@test.com'
            'password'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_book_successful(self):

        payload = {
            'name': 'Cursed Days',
            'annotation': 'Interesting book',
            'circulation': 10000,
            'published': 1925
        }
        res = self.client.post(BOOK_ADD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Book.objects.filter(
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_book_invalid(self):
        payload = {
            'name': '',
            'annotation': 'Interesting book',
            'circulation': 10000,
            'published': 1925
        }
        res = self.client.post(BOOK_ADD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_book(self):
        book = sample_book()

        payload = {
            'name': 'Kobzar'
        }
        url = detail_url(book.id)

        self.client.put(url, payload)
        book.refresh_from_db()
        self.assertEqual(book.name, payload['name'])

    def test_full_update_book(self):
        book = sample_book()

        payload = {
            'name': 'Cursed Days',
            'annotation': 'Interesting book',
            'circulation': 10000,
            'published': 1925
        }
        url = detail_url(book.id)

        self.client.put(url, payload)
        book.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(book, key))

    def test_remove_book(self):
        book = sample_book()
        url = detail_url(book.id)
        self.client.delete(url)

        exists = Book.objects.filter(
            id=book.id
        ).exists()

        self.assertFalse(exists)
