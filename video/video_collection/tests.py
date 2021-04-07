from django.test import TestCase
from django.urls import reverse
from .models import Video

# Create your tests here.

class TestHomePageMessage(TestCase):
    def test_app_title_message_shown_on_homepage(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'Lofi Videos')

class TestAddVideos(TestCase):
    def test_add_video(self):

        valid_video = {
            'name': 'ac lofi',
            'url': 'https://www.youtube.com/watch?v=C7qV9A9Aljk',
            'notes': 'animal crossing lofi'
        }

        url = reverse('add_video')
        response = self.client.post(url, data=valid_video, follow=True)

        self.assertTemplateUsed('video_collection/video_list.html')

        #does the video list show the new video?
        self.assertContains(response, 'ac lofi')
        self.assertContains(response, 'animal crossing lofi')
        self.assertContains(response, 'https://www.youtube.com/watch?v=C7qV9A9Aljk')

        video_count = Video.objects.count()
        self.assertEqual(1, video_count)

        video = Video.objects.first()

        self.assertEqual('ac lofi', video.name)
        self.assertEqual('https://www.youtube.com/watch?v=C7qV9A9Aljk', video.url)
        self.assertEqual('animal crossing lofi', video.notes)

    def test_add_video_invalid_url_not_added(self):

        invalid_video_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?v=123',
            'https://www.youtube.com/watch?v=',
            'https://www.mctc.edu',
            'https://www.google.com',
        ]

        for invalid_video_url in invalid_video_urls:

            new_video = {
                'name': 'example',
                'url': invalid_video_url,
                'notes':'example notes' ,
            }

            url = reverse('add_video')
            response = self.client.post(url, new_video)

            self.assertTemplateNotUsed('video_collection/add.html')

            messages = response.context['messages']
            message_texts = [ message.message for message in messages ]
            self.assertIn('Invalid Youtube Url', message_texts)
            self.assertIn('please check data entered',message_texts)



class TestVideoList(TestCase):
    pass

class TestVideoSearch(TestCase):
    pass

class TestVideoModel(TestCase):
    pass