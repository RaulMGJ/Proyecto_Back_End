from django.test import TestCase
from django.urls import reverse
from usuarios.models import Usuario
from roles.models import Rol


class UsuariosViewTests(TestCase):
	def setUp(self):
		self.rol_admin = Rol.objects.create(nombre='Administrador', descripcion='Rol administrador')
		self.admin = Usuario.objects.create(
			username='admin', nombre='Admin', correo='admin@example.com', contrasena='dummy', id_rol=self.rol_admin
		)
		self.admin.set_password('Test1234!')
		self.admin.save()
		datos = [
			('juan', 'Juan', 'juan@example.com'),
			('ana', 'Ana', 'ana@example.com'),
			('pedro', 'Pedro', 'pedro@example.com'),
		]
		for username, nombre, correo in datos:
			u = Usuario.objects.create(
				username=username, nombre=nombre, correo=correo, contrasena='dummy', id_rol=self.rol_admin
			)
			u.set_password('Pass1234!')
			u.save()
		self.client.login(username='admin', password='Test1234!')

	def test_usuarios_view_pagination_and_ordering(self):
		url = reverse('dashboard:usuarios')
		response = self.client.get(url, {
			'order_by': 'nombre',
			'order_direction': 'asc',
			'per_page': 2,
			'page': 1,
		})
		self.assertEqual(response.status_code, 200)
		self.assertIn('order_by', response.context)
		self.assertIn('order_direction', response.context)
		self.assertEqual(response.context['order_by'], 'nombre')
		self.assertEqual(response.context['order_direction'], 'asc')
		self.assertEqual(response.context['per_page'], 2)
		page_obj = response.context['usuarios']
		self.assertEqual(page_obj.paginator.per_page, 2)

	def test_usuarios_view_per_page_session_persistence(self):
		url = reverse('dashboard:usuarios')
		resp1 = self.client.get(url, {'per_page': 3})
		self.assertEqual(resp1.status_code, 200)
		self.assertEqual(resp1.context['per_page'], 3)
		resp2 = self.client.get(url)
		self.assertEqual(resp2.status_code, 200)
		self.assertEqual(resp2.context['per_page'], 3)

	def test_obtener_usuario_endpoint(self):
		objetivo = Usuario.objects.get(username='juan')
		url = reverse('dashboard:obtener_usuario', args=[objetivo.id_usuario])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertTrue(data.get('success'))
		self.assertEqual(data['usuario']['id'], objetivo.id_usuario)
		self.assertEqual(data['usuario']['usuario'], objetivo.username)
		self.assertEqual(data['usuario']['email'], objetivo.email)


class ExportarUsuariosExcelTests(TestCase):
	def setUp(self):
		self.rol_admin = Rol.objects.create(nombre='Administrador', descripcion='Rol administrador')
		self.admin = Usuario.objects.create(
			username='admin', nombre='Admin', correo='admin@example.com', contrasena='dummy', id_rol=self.rol_admin
		)
		self.admin.set_password('Test1234!')
		self.admin.save()
		for i in range(5):
			u = Usuario.objects.create(
				username=f'user{i}', nombre=f'Usuario {i}', correo=f'user{i}@example.com', contrasena='dummy', id_rol=self.rol_admin
			)
			u.set_password('Pass1234!')
			u.save()
		self.client.login(username='admin', password='Test1234!')

	def test_exportar_usuarios_excel_pagina(self):
		url = reverse('dashboard:exportar_usuarios_excel')
		resp = self.client.get(url, {
			'order_by': 'id_usuario',
			'order_direction': 'asc',
			'per_page': 2,
			'page': 1,
		})
		self.assertEqual(resp.status_code, 200)
		self.assertIn('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', resp['Content-Type'])
		self.assertIn('pagina_1', resp['Content-Disposition'])

	def test_exportar_usuarios_excel_todos(self):
		url = reverse('dashboard:exportar_usuarios_excel')
		resp = self.client.get(url, {'all': 'true'})
		self.assertEqual(resp.status_code, 200)
		self.assertIn('todos', resp['Content-Disposition'])

	def test_exportar_usuarios_excel_unico(self):
		unico_username = 'user3'
		url = reverse('dashboard:exportar_usuarios_excel')
		resp = self.client.get(url, {'search': unico_username})
		self.assertEqual(resp.status_code, 200)
		self.assertIn('unico', resp['Content-Disposition'])


class AuditoriasViewTests(TestCase):
	def setUp(self):
		self.rol_admin = Rol.objects.create(nombre='Administrador', descripcion='Rol administrador')
		self.admin = Usuario.objects.create(
			username='admin', nombre='Admin', correo='admin@example.com', contrasena='dummy', id_rol=self.rol_admin
		)
		self.admin.set_password('Test1234!')
		self.admin.save()
		from dashboard.models import Auditoria
		acciones = ['CREAR', 'EDITAR', 'BORRAR']
		for i in range(6):
			Auditoria.objects.create(usuario=self.admin, accion=acciones[i % 3], entidad='Usuario', detalle=f'Operación {i}')
		self.client.login(username='admin', password='Test1234!')

	def test_auditorias_view_search_and_order(self):
		url = reverse('dashboard:auditorias')
		resp = self.client.get(url, {'search': 'Operación', 'order_by': 'accion', 'order_direction': 'asc', 'per_page': 2})
		self.assertEqual(resp.status_code, 200)
		self.assertIn('order_by', resp.context)
		self.assertEqual(resp.context['order_by'], 'accion')
		self.assertEqual(resp.context['per_page'], 2)
		page_obj = resp.context['page_obj']
		self.assertEqual(page_obj.paginator.per_page, 2)

	def test_auditorias_export_pagina(self):
		url = reverse('dashboard:exportar_auditorias_excel')
		resp = self.client.get(url, {'per_page': 2, 'page': 1})
		self.assertEqual(resp.status_code, 200)
		self.assertIn('pagina_1', resp['Content-Disposition'])

	def test_auditorias_export_todos(self):
		url = reverse('dashboard:exportar_auditorias_excel')
		resp = self.client.get(url, {'all': 'true'})
		self.assertEqual(resp.status_code, 200)
		self.assertIn('todos', resp['Content-Disposition'])
