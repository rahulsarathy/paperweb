from datetime import datetime
from django.utils.timezone import make_aware
from blogs.models import Blog
from blogs.models import ReadingListItem
from blogs.models import Subscription
from blogs.views import get_reading_list
from blogs.views import get_subscriptions
from blogs.views import remove_from_reading_list
from blogs.views import subscribe
from blogs.views import unsubscribe
import json
from users.models import CustomUser
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate


class BlogsTest(APITestCase):
  def setUp(self):
    self.test_user1 = CustomUser.objects.create(username='postlight', email='postlight@mercurynews.org')
    self.test_user2 = CustomUser.objects.create(username='rsarathy', email='rsarathy@google.com')
    ReadingListItem.objects.create(
      reader=self.test_user1,
      title='postlight/mercury-parser',
      link='https://github.com/postlight/mercury-parser',
      archived=False, trashed=False, delivered=False,
      date_added=make_aware(datetime.now())
    )
    ReadingListItem.objects.create(
      reader=self.test_user2,
      title='Google',
      link='https://www.google.com',
      archived=False, trashed=False, delivered=False,
      date_added=make_aware(datetime.now())
    )
    self.factory = APIRequestFactory()

  def test_get_reading_list(self):
    """Checks that get_reading_list() returns all of a user's ReadingListItem(s)."""
    request = self.factory.get('/api/blogs/get_reading/')
    force_authenticate(request, user=self.test_user1)
    response = get_reading_list(request)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = json.loads(response.content)

    # We should only find the ReadingListItems associated with `test_user1`.
    self.assertEqual(len(data), 1)
    self.assertEqual(data[0]['title'], 'postlight/mercury-parser')
    self.assertEqual(data[0]['link'], 'https://github.com/postlight/mercury-parser')

  def test_remove_from_reading_list(self):
    """
    Checks that remove_from_reading_list() correctly deletes a ReadingListItem
    from a user's reading list.
    """
    request = self.factory.post('/api/blogs/remove_reading', {'link': 'https://github.com/postlight/mercury-parser'})
    force_authenticate(request, user=self.test_user1)
    response = remove_from_reading_list(request)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    data = json.loads(response.content)
    self.assertEquals(len(data), 0)

  def test_remove_from_reading_list_link_doesnt_exist(self):
    """
    Checks that remove_from_reading_list() returns 404 if a requested
    link for deletion doesn't exist within a user's reading list.
    """
    request = self.factory.post('/api/blogs/remove_reading', {'link': 'https://notnation.com/'})
    force_authenticate(request, user=self.test_user1)
    response = remove_from_reading_list(request)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class SubscriptionsTest(APITestCase):
  def setUp(self):
    self.factory = APIRequestFactory()
    self.test_user1 = CustomUser.objects.create(username='postlight', email='postlight@mercurynews.org')
    self.stratechery = Blog.objects.create(name='stratechery', last_polled_time=make_aware(datetime.now()), home_url='https://www.stratetchery.com', rss_url='https://www.stratetchery.com/feed/', scraped_old_posts=True)
    Subscription.objects.create(subscriber=self.test_user1, date_subscribed=make_aware(datetime.now()), blog=self.stratechery)

  def test_get_subscriptions(self):
    """
    Checks that get_subscriptions() returns the correct subscriptions for
    a given user.
    """
    request = self.factory.get('/api/blogs/get_subscriptions')
    force_authenticate(request, user=self.test_user1)
    response = get_subscriptions(request)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = json.loads(response.content)
    self.assertEqual(len(data), 1)
    self.assertEqual(data[0]['name_id'], 'stratechery')

  def test_subscribe(self):
    """Checks that subscribe() adds the Blog to a user's list of subscribed blogs."""
    # Add Ribbonfarm to the test database.
    Blog.objects.create(name='ribbonfarm', last_polled_time=make_aware(datetime.now()), home_url='https://www.ribbonfarm.com', rss_url='https://www.ribbonfarm.com/feed/', scraped_old_posts=True)

    request = self.factory.post('/api/blogs/subscribe', {'name_id': 'ribbonfarm'})
    force_authenticate(request, user=self.test_user1)
    response = subscribe(request)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Now verify that ribbonfarm is part of the user's subscriptions.
    request = self.factory.get('/api/blogs/get_subscriptions')
    force_authenticate(request, user=self.test_user1)
    response = get_subscriptions(request)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = json.loads(response.content)
    self.assertEqual(len(data), 2)
    self.assertEqual(data[0]['name_id'], 'stratechery')
    self.assertEqual(data[1]['name_id'], 'ribbonfarm')

  def test_unsubscribe(self):
    """Checks that unsubscribe() removes a Blog from a user's list of subscribed blogs."""
    request = self.factory.post('/api/blogs/unsubscribe', {'name_id': 'stratechery'})
    force_authenticate(request, user=self.test_user1)
    response = unsubscribe(request)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Check that the list of subscriptions reflects this deletion.
    request = self.factory.get('/api/blogs/get_subscriptions')
    force_authenticate(request, user=self.test_user1)
    response = get_subscriptions(request)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = json.loads(response.content)
    self.assertEqual(len(data), 0)    

  def test_unsubscribe_nonexistent_blog(self):
    """Checks that unsubscribe() when given a Blog that a user doesn't subscribe to returns 403."""
    # Add Ribbonfarm to the test database.
    Blog.objects.create(name='ribbonfarm', last_polled_time=make_aware(datetime.now()), home_url='https://www.ribbonfarm.com', rss_url='https://www.ribbonfarm.com/feed/', scraped_old_posts=True)

    request = self.factory.post('/api/blogs/unsubscribe', {'name_id': 'ribbonfarm'})
    force_authenticate(request, user=self.test_user1)
    response = unsubscribe(request)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # The list of subscriptions should be unchanged.
    request = self.factory.get('/api/blogs/get_subscriptions')
    force_authenticate(request, user=self.test_user1)
    response = get_subscriptions(request)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = json.loads(response.content)
    self.assertEqual(len(data), 1)
    self.assertEqual(data[0]['name_id'], 'stratechery')
    