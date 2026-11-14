import re
import tempfile
import unittest
from pathlib import Path
from app import create_app


class GastosTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.config = {'TESTING': True, 'SECRET_KEY': 'test', 'DATABASE': str(Path(self.tmp.name) / 'test.db')}
        self.app = create_app(self.config)
        self.client = self.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def post(self, url, **data):
        self.client.get('/login')
        with self.client.session_transaction() as sess:
            data['csrf'] = sess['csrf']
        return self.client.post(url, data=data)

    def login(self):
        return self.post('/login', usuario='admin', clave='123')

    def test_authentication_and_logout(self):
        self.assertEqual(self.client.get('/').status_code, 302)
        self.assertEqual(self.client.get('/reporte?formato=csv').status_code, 302)
        self.assertIn('incorrectos', self.post('/login', usuario='admin', clave='mal').text)
        self.assertEqual(self.login().status_code, 303)
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.post('/salir').status_code, 303)
        self.assertEqual(self.client.get('/').status_code, 302)

    def test_persistence_totals_filters_csv(self):
        self.login()
        for fecha, descripcion, monto in [('2026-11-10', 'Pasaje', '0.10'), ('2026-11-14', 'Almuerzo', '0.20')]:
            self.assertEqual(self.post('/', fecha=fecha, descripcion=descripcion, monto=monto).status_code, 303)
        self.assertIn('S/ 0.30', self.client.get('/reporte').text)
        filtered = self.client.get('/reporte?desde=2026-11-14&hasta=2026-11-14')
        self.assertIn('Almuerzo', filtered.text)
        self.assertNotIn('Pasaje', filtered.text)
        csv = self.client.get('/reporte?formato=csv').text
        self.assertIn('TOTAL,0.30', csv)
        new_client = create_app(self.config).test_client()
        with new_client.session_transaction() as sess:
            sess['usuario'] = 'admin'
        self.assertIn('Pasaje', new_client.get('/').text)

    def test_validation_csrf_and_escape(self):
        self.login()
        for monto in ['0', '-1', 'NaN', 'Infinity', '1.001', '10000000']:
            self.assertEqual(self.post('/', fecha='2026-11-14', descripcion='Prueba', monto=monto).status_code, 400)
        self.assertEqual(self.post('/', fecha='2026-02-30', descripcion='Prueba', monto='1').status_code, 400)
        self.assertEqual(self.client.post('/', data={}).status_code, 400)
        self.post('/', fecha='2026-11-14', descripcion='<script>alert(1)</script>', monto='10')
        self.assertIn('&lt;script&gt;', self.client.get('/').text)
        self.post('/', fecha='2026-11-14', descripcion='=1+1', monto='10')
        self.assertIn("'=1+1", self.client.get('/reporte?formato=csv').text)
        self.assertEqual(self.client.get('/reporte?desde=2026-12-01&hasta=2026-01-01').status_code, 302)


if __name__ == '__main__':
    unittest.main()
