import unittest
from app import create_app, db
from app.posts.models import Post
from app.config import TestingConfig

class PostModelTestCase(unittest.TestCase):

    def setUp(self):
        """
        Налаштування перед кожним тестом.
        """
        self.app = create_app(config_name='testing')

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        """
        Очищення після кожного тесту.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_post(self):
        """Тест створення нового поста (US01)"""
        
        response = self.client.post('/post/create', data={
            'title': 'Test Post Title',
            'content': 'This is the content of the test post.',
            'category': 'tech'
        }, follow_redirects=True) 
        

        self.assertEqual(response.status_code, 200)

        post = db.session.scalar(db.select(Post).where(Post.title == 'Test Post Title'))
        self.assertIsNotNone(post)
        self.assertEqual(post.content, 'This is the content of the test post.')

        self.assertIn(b'Post added successfully', response.data)

        self.assertIn(b'List of all posts', response.data)
        self.assertIn(b'Test Post Title', response.data)
    def test_list_posts(self):
        """Тест перегляду списку всіх постів (US02)"""

        post1 = Post(title="First Test Post", content="Content 1", category="tech")
        post2 = Post(title="Second Test Post", content="Content 2", category="news")
        db.session.add_all([post1, post2])
        db.session.commit()

        response = self.client.get('/post/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'First Test Post', response.data)
        self.assertIn(b'Second Test Post', response.data)

    def test_view_post_detail(self):
        """Тест перегляду одного поста (US03)"""

        post = Post(title="Full Content Post", content="This is the full content.", category="tech")
        db.session.add(post)
        db.session.commit() # post.id тепер = 1

        response = self.client.get('/post/1')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Full Content Post', response.data)
        self.assertIn(b'This is the full content.', response.data)

    def test_404_not_found(self):
        """Тест 404 при відсутньому пості (US06)"""
        response = self.client.get('/post/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404', response.data)
        self.assertIn('Сторінку не знайдено'.encode('utf-8'), response.data)

    def test_update_post(self):
        """Тест редагування поста (US04)"""

        post = Post(title="Original Title", content="Original Content", category="tech")
        db.session.add(post)
        db.session.commit()

        response = self.client.post('/post/1/update', data={
            'title': 'Updated Title',
            'content': 'Updated Content',
            'category': 'news'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        updated_post = db.get_or_404(Post, 1)
        self.assertEqual(updated_post.title, 'Updated Title')
        self.assertEqual(updated_post.content, 'Updated Content')
        self.assertEqual(updated_post.category, 'news')

        self.assertIn(b'Post has been updated!', response.data)

def test_delete_post(self):
        """Тест видалення поста (US05)"""

        post_to_delete = Post(title="Delete Me", content="Content to delete", category="other")
        db.session.add(post_to_delete)
        db.session.commit()
        post_id = post_to_delete.id

        response = self.client.post(f'/post/{post_id}/delete', follow_redirects=True)
        

        self.assertEqual(response.status_code, 200)

        deleted_post = db.session.get(Post, post_id)
        self.assertIsNone(deleted_post)

        self.assertIn(b'List of all posts', response.data)

        self.assertIn(b'Post has been deleted', response.data)