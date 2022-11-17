from django.test import TestCase
from .models import Article


# Create your tests here.
class ArticleTestCase(TestCase):
    def setUp(self):
        self.number_of_articles = 100
        for i in range(0, self.number_of_articles):
            Article.objects.create(id=i, title='Hello world', content='testing info')

    def test_article_search_manager(self):
        qs = Article.objects.search(query='hello world')
        self.assertEqual(qs.count(), self.number_of_articles)

        qs = Article.objects.search(query='llo wor')
        self.assertEqual(qs.count(), self.number_of_articles)

        qs = Article.objects.search(query='testing info')
        self.assertEqual(qs.count(), self.number_of_articles)
