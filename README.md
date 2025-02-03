Crear un entorno virtual

Para evitar conflictos entre paquetes, activa un entorno virtual:
En Windows:
python -m venv venv
venv\Scripts\activate

En Mac/Linux:
python3 -m venv venv
source venv/bin/activate

Instalar dependencias
pip install -r requirements.txt
________________________________________

🚀 Ejecución del servidor

Para iniciar el servidor de desarrollo, usa:
python manage.py runserver
Esto iniciará el servidor en http://127.0.0.1:8000/, donde podrás acceder a la aplicación.
________________________________________

🔑 Acceso y Autenticación

Para acortar URLs, cada usuario debe estar registrado en el sistema.

📥 Iniciar sesión

Para acceder a la plataforma, inicia sesión en:
http://127.0.0.1:8000/auth/login/

Credenciales de prueba:
•	Usuario: juanito@gmail.com | Contraseña: juanito1234
•	Usuario: anael@gmail.com | Contraseña: anael1234
•	Usuario: ghia@gmail.com | Contraseña: ghia1234
•	Usuario: prueba4@gmail.com | Contraseña: prueba1234

🛑 Superusuario (Admin)
•	Usuario: admin@gmail.com | Contraseña: root1234

✍ Registro de usuario

Para registrarte, accede a:
http://127.0.0.1:8000/auth/registers/ y proporciona tu correo y contraseña, o bien en la vista de login, hasta abajo da clic en "Don't have an account?"

🚪 Cerrar sesión
Para cerrar sesión, haz clic en el botón "Cerrar sesión" en la parte superior derecha.
________________________________________

🔗 Gestión de URLs

Los usuarios pueden acortar, ver, filtrar y eliminar sus URLs.

1️⃣ Acortar una URL
En el dashboard de usuario (http://127.0.0.1:8000/dashboard/user/), ingresa una URL en el formulario y presiona "Acortar URL".
✔ La URL se acortará y aparecerá en la tabla automáticamente.
✔ Podrás copiarla o eliminarla desde la tabla.

2️⃣ Eliminar una URL
Cada URL tiene un icono de 🗑️. Al hacer clic, se pedirá confirmación antes de eliminarla.
________________________________________

📂 Acortar múltiples URLs

Puedes subir un archivo .txt con múltiples URLs para acortarlas en lote.
📤 Proceso:

1️⃣ Selecciona un archivo .txt con una URL por línea.
2️⃣ Haz clic en "Subir y Acortar" en la sección de subida de archivos.
3️⃣ Descarga el archivo generado con todas las URLs acortadas.
📥 Descargar archivo de URLs acortadas
Después de procesar las URLs, podrás descargar un archivo con el resultado.
✔ La tabla se actualizará automáticamente sin recargar la página.
________________________________________

📊 Panel de Administración

Disponible solo para superusuarios en:
http://127.0.0.1:8000/dashboard/admin/

🔎 Funciones del Panel de Administración:

✅ Filtrar URLs por usuario: Usa el selector para elegir un usuario y ver solo sus URLs.
✅ Eliminar URLs: Puedes eliminar URLs de cualquier usuario.
✅ Paginación: Se muestran 15 registros por página para mejorar la organización.
