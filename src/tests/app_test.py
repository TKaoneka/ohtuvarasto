import unittest

from app import app, store


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        store.varastot.clear()
        store.next_id = 1

    def test_index_empty(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Varastot', response.data)
        self.assertIn(b'No varastot yet', response.data)

    def test_create_varasto_get(self):
        response = self.client.get('/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Varasto', response.data)

    def test_create_varasto_post(self):
        response = self.client.post('/create', data={
            'nimi': 'Test Varasto',
            'tilavuus': '100',
            'alku_saldo': '50'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Varasto', response.data)
        self.assertEqual(len(store.varastot), 1)

    def test_view_varasto(self):
        self.client.post('/create', data={
            'nimi': 'Test Varasto',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        response = self.client.get('/varasto/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Varasto', response.data)
        self.assertIn(b'50', response.data)

    def test_view_nonexistent_varasto(self):
        response = self.client.get('/varasto/999')
        self.assertEqual(response.status_code, 302)

    def test_add_to_varasto(self):
        self.client.post('/create', data={
            'nimi': 'Test',
            'tilavuus': '100',
            'alku_saldo': '0'
        })
        response = self.client.post('/varasto/1/add', data={
            'maara': '30'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(store.varastot[1]['varasto'].saldo, 30)

    def test_remove_from_varasto(self):
        self.client.post('/create', data={
            'nimi': 'Test',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        response = self.client.post('/varasto/1/remove', data={
            'maara': '20'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(store.varastot[1]['varasto'].saldo, 30)

    def test_delete_varasto(self):
        self.client.post('/create', data={
            'nimi': 'Test',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        self.assertEqual(len(store.varastot), 1)
        response = self.client.post('/varasto/1/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(store.varastot), 0)

    def test_edit_varasto_get(self):
        self.client.post('/create', data={
            'nimi': 'Original',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        response = self.client.get('/varasto/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Original', response.data)

    def test_edit_varasto_post(self):
        self.client.post('/create', data={
            'nimi': 'Original',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        response = self.client.post('/varasto/1/edit', data={
            'nimi': 'Updated'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(store.varastot[1]['nimi'], 'Updated')

    def test_edit_nonexistent_varasto(self):
        response = self.client.get('/varasto/999/edit')
        self.assertEqual(response.status_code, 302)
