from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'user_test@test.com'
        password = '123qwe!@#'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # assert email == user.email, 'erhdfghf'
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalize(self):
        email = 'user_test@TEST.coM'
        user = get_user_model().objects.create_user(
            email=email,
            password='123qwe!@#'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='123qwe!@#'
            )
