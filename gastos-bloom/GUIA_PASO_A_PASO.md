# Guía para Sarai: abrir, ejecutar y entregar

## 1. Abrir la carpeta correcta

1. Abre **Visual Studio Code**.
2. Haz clic en **Archivo > Abrir carpeta**.
3. Busca `C:\Users\sarai\Downloads\Nueva carpeta (9)\gastos-bloom`.
4. Selecciona **gastos-bloom** y pulsa **Seleccionar carpeta**. Si aparece la pregunta de confianza, acepta si reconoces esta carpeta creada para tu práctica.
5. A la izquierda deben aparecer `app.py`, `requirements.txt`, `templates`, `static` y `README.md`.

No tienes que copiar el código: los archivos ya están creados.

## 2. Abrir la terminal

En la barra superior, selecciona **Terminal > Nueva terminal**. La terminal aparece debajo del código. Comprueba que la ruta termina en `gastos-bloom`.

## 3. Crear el entorno virtual

Escribe y pulsa Enter:

```powershell
python -m venv .venv
```

Si no reconoce `python`, prueba:

```powershell
py -m venv .venv
```

Si ninguno funciona, instala Python y marca la opción de añadir Python al PATH. Cierra y vuelve a abrir VS Code antes de repetir. Este paso crea una carpeta `.venv`; puede tardar un momento.

## 4. Instalar Flask

Escribe y pulsa Enter (necesitas conexión a internet):

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Espera a que finalice y reaparezca la línea para escribir. SQLite ya viene con Python; no necesitas instalarlo aparte. Los comandos usan el Python del entorno directamente, por lo que no necesitas cambiar la política de PowerShell ni activar el entorno.

## 5. Ejecutar

Escribe:

```powershell
.\.venv\Scripts\python.exe app.py
```

Debes ver `Running on http://127.0.0.1:5000`. Abre esa dirección en Chrome o Edge. Si la dirección ya funciona porque el servidor de la preparación sigue abierto, puedes probarlo directamente. Si aparece un conflicto de puerto, detén la otra ejecución antes de volver a iniciar.

La advertencia de que es un servidor de desarrollo es normal en esta práctica local.

## 6. Probar tu práctica

1. Ingresa con usuario **admin**, clave **123**.
2. Registra, por ejemplo: fecha `14/11/2026` (según el formato de tu navegador), descripción `Compra de cuaderno`, monto `8.50`.
3. Haz clic en **Guardar gasto** y observa el historial.
4. Abre **Ver reporte**, revisa el total y prueba el filtro.
5. Descarga el CSV o usa **Imprimir / PDF > Guardar como PDF**.
6. Cierra sesión para comprobar el acceso.

Los tres gastos incluidos en la base local son ficticios y se usaron para las capturas. Los nuevos gastos se sumarán a ellos. La base local no se sube a GitHub.

## 7. Entender el código para explicarlo

- **app.py:** crea la aplicación, comprueba `admin` / `123`, administra la sesión, valida los gastos y consulta SQLite.
- **templates/login.html:** pantalla de acceso.
- **templates/inicio.html:** formulario e historial.
- **templates/reporte.html:** filtros, tabla, total y botones del reporte.
- **templates/base.html:** encabezado, mensajes y pie compartidos.
- **static/style.css:** colores, tamaños, tablas y vista móvil.
- **instance/gastos.db:** base de datos creada al ejecutar. Guarda los datos aunque cierres el programa.
- **requirements.txt:** indica qué instalar.

Puedes explicar: «Mi aplicación usa Flask para recibir las solicitudes, plantillas Jinja2 para mostrar las páginas y SQLite para guardar fecha, descripción y monto de cada gasto. Después de iniciar sesión, puedo registrar gastos y generar un reporte por fechas con un total».

## 8. Subir a GitHub desde la web

1. Entra a tu cuenta de GitHub.
2. Crea un repositorio llamado `gastos-bloom` y elige **Public**.
3. Crea el repositorio y utiliza la opción para subir archivos (**uploading an existing file** o **Add file > Upload files**, según la pantalla).
4. Desde el Explorador de Windows abre la carpeta `gastos-bloom`.
5. Arrastra `app.py`, `requirements.txt`, `README.md`, `GUIA_PASO_A_PASO.md`, `.gitignore` y las carpetas `templates`, `static`, `capturas` y `tests` a la página de subida.
6. No arrastres `.venv`, `instance` ni `__pycache__`. En la subida manual debes excluirlos tú; `.gitignore` se aplica al usar Git.
7. Escribe un mensaje como `Agregar práctica de registro de gastos` y confirma con **Commit changes**.
8. Comprueba que `app.py` y `README.md` estén directamente en la raíz del repositorio. Abajo del listado debe aparecer el README con las capturas visibles.
9. Abre el repositorio en una ventana privada para comprobar que es público.
10. Copia el enlace del repositorio y entrega **solo ese enlace** en Moodle.

No subas el PDF original: la entrega solicitada es el repositorio de esta aplicación. No necesitas publicar la web en un servicio de alojamiento para compartir el código.

## 9. Volver a abrir otro día

Abre la misma carpeta en VS Code, abre la terminal y ejecuta solamente:

```powershell
.\.venv\Scripts\python.exe app.py
```

No repitas la instalación si ya está hecha. Para apagar la aplicación, pulsa **Ctrl+C** en la terminal. No borres `instance/gastos.db` si quieres conservar tus registros.
