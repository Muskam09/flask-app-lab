import unittest
from app import create_app, db
from app.users.models import User

class AuthTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        response = self.client.post('/users/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # Шукаємо текст, який точно є у views.py: "Акаунт створено"
        self.assertIn('Акаунт створено'.encode('utf-8'), response.data)

    def test_login(self):
        # 1. Створюємо юзера
        password = 'password123' 
        user = User(username='testuser', email='test@example.com')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()


        # 2. Логінимось
        response = self.client.post('/users/login', data={
            'username': 'testuser',
            'password': password
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Вітаємо, testuser'.encode('utf-8'), response.data)

    def test_logout(self):
        # 1. Створюємо і логінимо
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        self.client.post('/users/login', data={'username':'testuser', 'password':'password123'}, follow_redirects=True)

        # 2. Робимо Logout
        response = self.client.get('/users/logout', follow_redirects=True)

        # 3. Перевіряємо
        self.assertIn('Ви вийшли з системи'.encode('utf-8'), response.data)

if __name__ == '__main__':
    unittest.main()