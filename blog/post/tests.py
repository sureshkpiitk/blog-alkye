from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.test import TestCase

from post.models import Post, Comment


class PostTestCase(TestCase):
    def setUp(self):
        # user create
        User.objects.create(username="user1", email="abc@gmail.com", is_staff=True, password="123")
        User.objects.create(username="user2", email="abc2@gmail.com", is_staff=False, password="123")
        self.user_1 = User.objects.get(username="user1")
        self.user_2 = User.objects.get(username="user2")
        # Post create
        Post.objects.create(title="title1", content="some content 1", auther=self.user_1)
        Post.objects.create(title="title2", content="some content 2", auther=self.user_2)

    def test_posts(self):
        post_1 = Post.objects.get(title="title1")
        post_2 = Post.objects.get(title="title2")
        self.assertEqual(post_1.title, 'title1')
        self.assertEqual(post_1.content, 'some content 1')
        self.assertEqual(post_1.auther, self.user_1)
        self.assertEqual(post_1.created, datetime.now().date())

        self.assertEqual(post_2.title, 'title2')
        self.assertEqual(post_2.content, 'some content 2')
        self.assertEqual(post_2.auther, self.user_2)
        self.assertEqual(post_2.created, datetime.now().date())


class CommentTestCase(TestCase):
    def setUp(self):
        # user create
        User.objects.create(username="user1", email="abc@gmail.com", is_staff=True, password="123")
        User.objects.create(username="user2", email="abc2@gmail.com", is_staff=False, password="123")
        self.user_1 = User.objects.get(username="user1")
        self.user_2 = User.objects.get(username="user2")
        # Post create
        self.post_1 = Post.objects.create(title="title1", content="some content 1", auther=self.user_1)
        self.post_2 = Post.objects.create(title="title2", content="some content 2", auther=self.user_2)

    def test_posts(self):
        # create comments
        Comment.objects.create(text="comment1", post=self.post_1, auther=self.user_1)
        Comment.objects.create(text="comment2", post=self.post_2, auther=self.user_1)

        comment_1 = Comment.objects.get(text="comment1", post=self.post_1, auther=self.user_1)
        comment_2 = Comment.objects.get(text="comment2", post=self.post_2, auther=self.user_1)
        self.assertEqual(comment_1.text, 'comment1')
        self.assertEqual(comment_1.post, self.post_1)
        self.assertEqual(comment_1.auther, self.user_1)
        self.assertEqual(comment_1.created, datetime.now().date())

        self.assertEqual(comment_2.text, 'comment2')
        self.assertEqual(comment_2.post, self.post_2)
        self.assertEqual(comment_2.auther, self.user_1)
        self.assertEqual(comment_2.created, datetime.now().date())


class APIRequestTest(APITestCase):
    def setUp(self):
        User.objects.create(username="user1", email="abc@gmail.com", is_staff=True, password="123")
        User.objects.create(username="user2", email="abc2@gmail.com", is_staff=False, password="123")
        self.user_1 = User.objects.get(username="user1")
        self.user_2 = User.objects.get(username="user2")
        self.client.force_authenticate(user=self.user_1)

    def test_create_post(self):
        """
        Ensure we can create a new posts object.
        """
        url = reverse('post')
        data = {
            "title": "Some Post 1",
            "content": "some content 1",
            "auther": self.user_1.id,
            "comments": []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Post.objects.all(), [])
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Some Post 1')
        # get posts
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["count"], 1)
        updated_data = data
        updated_data["id"] = 1
        updated_data["created"] = str(datetime.now().date())
        self.assertDictEqual(response.data["results"][0], updated_data)

    def test_posts_with_filter_auther(self):
        url = reverse('post')
        data = {
            "title": "Some Post 1",
            "content": "some content 1",
            "auther": self.user_1.id,
            "comments": []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Some Post 1')
        # filter posts with auther
        response = self.client.get(url, data={"auther": self.user_1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        updated_data = data
        updated_data["id"] = 1
        updated_data["created"] = str(datetime.now().date())
        self.assertDictEqual(response.data["results"][0], updated_data)

    def test_post_filter_with_created(self):
        url = reverse('post')
        data = {
            "title": "Some Post 1",
            "content": "some content 1",
            "auther": self.user_1.id,
            "comments": []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Some Post 1')
        # filter posts with auther
        response = self.client.get(url, data={"created": str(datetime.now().date())})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        updated_data = data
        updated_data["id"] = 1
        updated_data["created"] = str(datetime.now().date())
        self.assertDictEqual(response.data["results"][0], updated_data)

    def test_post_filter_with_created_and_auther(self):
        url = reverse('post')
        data = {
            "title": "Some Post 1",
            "content": "some content 1",
            "auther": self.user_1.id,
            "comments": []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Some Post 1')
        # filter posts with auther
        response = self.client.get(url, data={"created": str(datetime.now().date()),
                                              "auther": self.user_1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        updated_data = data
        updated_data["id"] = 1
        updated_data["created"] = str(datetime.now().date())
        self.assertDictEqual(response.data["results"][0], updated_data)

    def test_post_filter_with_created_and_auther_with_empty_result(self):
        url = reverse('post')
        data = {
            "title": "Some Post 1",
            "content": "some content 1",
            "auther": self.user_1.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Some Post 1')
        # filter posts with auther
        response = self.client.get(url, data={"created": str(datetime.now().date()),
                                              "auther": self.user_2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
