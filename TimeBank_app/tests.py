from datetime import datetime

from django.test import TestCase

# Create your tests here.
from TimeBank_account.models import User
from TimeBank_app.models import Post


def create_user():
    return User.object.create_user(username='test user', email='user@test.com', password='1234', name='테스트 유저')


class PostModelTests(TestCase):

    def setUp(self):
        self.user = create_user()
        self.post_data = {
            'date': '2021-04-05',
            'start_time': '19:00',
            'end_time': '20:00',
            'service': '서비스',
            'location': '장소',
            'mainwork': Post.main_list[0],
            'subwork': '서브',
            'content': '내용',
            'tok': 1,
            'status': '대기',
            'author': self.user
        }

    def test_create_post(self):
        post = Post.objects.create(
            date=self.post_data['date'],
            start_time=self.post_data['start_time'],
            end_time=self.post_data['end_time'],
            service=self.post_data['service'],
            location=self.post_data['location'],
            mainwork=self.post_data['mainwork'],
            subwork=self.post_data['subwork'],
            content=self.post_data['content'],
            author=self.post_data['author'],
            tok=self.post_data['tok'],
            status=self.post_data['status']
        )
        for key, value in self.post_data.items():
            if hasattr(post, key):
                self.assertEqual(getattr(post, key), value)

