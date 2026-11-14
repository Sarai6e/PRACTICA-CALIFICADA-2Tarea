from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
import shutil

ROOT = Path(__file__).parent
OUT = ROOT / 'output' / 'pdf'
OUT.mkdir(parents=True, exist_ok=True)
TMP = ROOT / 'tmp' / 'pdfs'
TMP.mkdir(parents=True, exist_ok=True)
shutil.copy2(r'C:/Users/sarai/AppData/Local/Temp/codex-clipboard-d8855d9c-8c65-4b07-826d-fa7b5806d83b.png', TMP / '05-vscode.png')
PURPLE = colors.HexColor('#7350b5')
INK = colors.HexColor('#302641')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleBloom', fontName='Helvetica-Bold', fontSize=32, leading=37, textColor=INK, spaceAfter=22))
styles.add(ParagraphStyle(name='SectionBloom', fontName='Helvetica-Bold', fontSize=18, leading=23, textColor=PURPLE, spaceAfter=15))
styles.add(ParagraphStyle(name='BodyBloom', fontName='Helvetica', fontSize=10.5, leading=16, textColor=INK, spaceAfter=12))
styles.add(ParagraphStyle(name='CaptionBloom', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#746d80'), spaceBefore=9, spaceAfter=16))
styles.add(ParagraphStyle(name='KickerBloom', fontName='Helvetica-Bold', fontSize=10, leading=15, textColor=PURPLE, spaceAfter=15))
story = []
def p(text, style='BodyBloom'):
    return Paragraph(text, styles[style])
def add(text, style='BodyBloom'):
    story.append(p(text, style))
def section(title):
    add(title, 'SectionBloom')
def image(path, maxw=495, maxh=420):
    w,h = ImageReader(str(path)).getSize()
    scale = min(maxw/w, maxh/h)
    return Image(str(path), width=w*scale, height=h*scale)
def screen(name, caption, maxh=420):
    story.append(image(ROOT/'gastos-bloom'/'capturas'/name, maxh=maxh))
    add(caption, 'CaptionBloom')
def page():
    story.append(PageBreak())

add('PROGRAMACIÓN Y DESARROLLO WEB · 2026-II', 'KickerBloom')
story.append(Spacer(1,32))
add('Gastos Bloom<br/>Sistema web para el<br/>registro de gastos', 'TitleBloom')
add('INFORME DE PRÁCTICA CALIFICADA 2', 'KickerBloom')
add('<b>Estudiante:</b> Sarai Rut Romero Villanueva<br/><b>Tecnologías:</b> Python, Flask, Jinja2 y SQLite<br/><b>Fecha:</b> 14 de noviembre de 2026')
story.append(Spacer(1,20))
section('1. Objetivo y alcance')
add('Desarrollar un sitio web que permita iniciar sesión con las credenciales solicitadas, registrar gastos mediante fecha, descripción y monto, y generar un reporte. El proyecto incluye almacenamiento persistente en SQLite y un repositorio público en GitHub con instrucciones y capturas de funcionamiento.')
add('La aplicación se denomina <b>Gastos Bloom</b>. Presenta una interfaz en tonos violeta, rosa y verde menta, formularios con etiquetas y un diseño que se adapta al ancho de la pantalla.')
section('2. Requisitos implementados')
for item in ['Acceso con usuario <b>admin</b> y contraseña <b>123</b>.', 'Registro y consulta de gastos con fecha, descripción y monto en soles.', 'Persistencia de los registros en una base de datos SQLite.', 'Reporte con total, filtro por fechas, descarga CSV e impresión.', 'Código compartido públicamente con README y evidencias visuales.']:
    add('• ' + item)
add('<b>Repositorio público:</b><br/><link href="https://github.com/Sarai6e/PRACTICA-CALIFICADA-2Tarea" color="#7350b5">github.com/Sarai6e/PRACTICA-CALIFICADA-2Tarea</link>')

page();section('3. Arquitectura y almacenamiento')
add('El navegador envía solicitudes HTTP a Flask. Las rutas de <b>app.py</b> comprueban la sesión, validan los formularios y ejecutan consultas SQL con parámetros. Las plantillas Jinja2 presentan los resultados y el archivo CSS define la apariencia de las páginas.')
rows=[['Componente','Responsabilidad'],['app.py','Rutas, autenticación, validación y operaciones SQLite'],['templates/','Vistas de acceso, registro y reporte'],['static/style.css','Diseño, vista móvil y estilos para imprimir'],['instance/gastos.db','Base de datos local creada automáticamente'],['capturas/ y README.md','Evidencias e instrucciones del proyecto'],['tests/test_app.py','Pruebas automatizadas del comportamiento']]
t=Table([[p(a),p(b)] for a,b in rows],colWidths=[135,360]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#ece4f8')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor('#e9e2ef'))]));story.append(t)
story.append(Spacer(1,16))
add('La tabla <b>gastos</b> contiene <b>id</b>, <b>fecha</b>, <b>descripcion</b> y <b>centimos</b>. El monto se guarda como un entero de céntimos para calcular totales exactos: S/ 18.50 se almacena como 1850. Los registros permanecen disponibles después de reiniciar el servidor.')
section('4. Validaciones y control de acceso')
add('Las páginas de gastos y reportes requieren una sesión iniciada. Las fechas deben ser válidas; la descripción admite de 1 a 200 caracteres; el monto debe ser positivo, finito, no superar S/ 9,999,999.99 y tener como máximo dos decimales. Un formulario incorrecto muestra un mensaje y conserva los valores enviados.')
add('Los formularios POST incluyen un token CSRF. Las consultas utilizan parámetros y Jinja2 escapa el contenido de las descripciones. La descarga CSV antepone una comilla a descripciones con posibles fórmulas. Las credenciales fijas corresponden al alcance académico de la consigna.')

page();section('5. Evidencia: acceso a la aplicación')
add('El usuario abre la aplicación, escribe <b>admin</b> y <b>123</b> y pulsa <b>Ingresar</b>. Si las credenciales son correctas, Flask crea la sesión y redirige al panel de gastos. Ante datos incorrectos, se muestra un mensaje de error.')
screen('01-login.png','Figura 1. Pantalla real de inicio de sesión de Gastos Bloom.',maxh=420)
section('6. Flujo de uso')
add('<b>1.</b> Iniciar sesión.<br/><b>2.</b> Seleccionar una fecha, describir el gasto e indicar el monto.<br/><b>3.</b> Pulsar Guardar gasto y revisar el historial.<br/><b>4.</b> Abrir el reporte, aplicar un intervalo y consultar el total.<br/><b>5.</b> Descargar CSV o imprimir; finalizar con Cerrar sesión.')

page();section('7. Evidencia: registro e historial')
add('El panel integra un formulario de registro, el total acumulado y el número de movimientos. Después de guardar un gasto válido, la aplicación lo inserta en SQLite y redirige al listado para evitar repetir el envío al actualizar la página.')
screen('02-gastos.png','Figura 2. Formulario e historial después de registrar tres gastos ficticios. El total mostrado es S/ 39.50.',maxh=435)
rows=[['Fecha','Descripción','Monto'],['2026-11-12','Pasajes a la universidad','S/ 6.00'],['2026-11-13','Materiales de estudio','S/ 18.50'],['2026-11-14','Almuerzo','S/ 15.00'],['','TOTAL','S/ 39.50']]
t=Table(rows,colWidths=[105,285,105]);t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#ece4f8')),('FONTSIZE',(0,0),(-1,-1),10),('PADDING',(0,0),(-1,-1),8),('ALIGN',(-1,0),(-1,-1),'RIGHT'),('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor('#e9e2ef'))]));story.append(t)

page();section('8. Evidencia: reporte de gastos')
add('El reporte lista los movimientos y calcula su suma. Los campos <b>Desde</b> y <b>Hasta</b> permiten consultar un periodo inclusivo; al dejarlos vacíos se incluyen todos los registros. El sistema comprueba que el inicio no sea posterior al fin.')
screen('03-reporte.png','Figura 3. Reporte real con tres movimientos y un total de S/ 39.50.',maxh=425)
add('<b>Descargar CSV:</b> genera un archivo con fecha, descripción, monto y total, respetando el filtro aplicado.<br/><b>Imprimir / PDF:</b> abre la ventana de impresión del navegador, donde puede elegirse Guardar como PDF. Los estilos de impresión ocultan los controles de navegación y los botones.')

page();section('9. Evidencia: diseño adaptable')
add('En una pantalla de celular, los indicadores y el formulario se organizan verticalmente. La captura conserva el acceso a la navegación, el registro y la tabla de movimientos.')
story.append(image(ROOT/'gastos-bloom'/'capturas'/'04-movil.png',maxw=495,maxh=575))
add('Figura 4. Vista completa de la aplicación en una pantalla de 390 píxeles de ancho.', 'CaptionBloom')

page();section('10. Evidencia: entorno de desarrollo')
add('La imagen proporcionada muestra el proyecto abierto en Visual Studio Code: las carpetas de capturas, plantillas, archivos estáticos y pruebas, junto con app.py, requirements.txt y README.md. También se observa una terminal con solicitudes del servidor y el selector de cuenta de GitHub.')
story.append(image(TMP/'05-vscode.png',maxh=330))
add('Figura 5. Captura proporcionada por la estudiante: estructura del proyecto y terminal en Visual Studio Code. El selector de cuenta visible no constituye por sí solo evidencia de publicación.', 'CaptionBloom')
section('11. Instalación y ejecución local')
add('Abrir la carpeta <b>gastos-bloom</b> en Visual Studio Code y seleccionar <b>Terminal &gt; Nueva terminal</b>. Ejecutar los siguientes comandos, uno por uno:')
for line in ['python -m venv .venv', '.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt', '.\\.venv\\Scripts\\python.exe app.py']:
    add('<font name="Courier" size="9">'+line+'</font>')
add('Abrir <b>http://127.0.0.1:5000</b> en el navegador. Mantener la terminal abierta durante el uso y pulsar <b>Ctrl+C</b> para detener el servidor. SQLite está incluido en Python. Si Windows no reconoce python, puede usarse py para crear el entorno virtual.')

page();section('12. Verificación y resultados')
add('Se ejecutaron <b>tres pruebas automatizadas integradas</b> mediante unittest; todas finalizaron correctamente. Cada prueba agrupa varias comprobaciones del funcionamiento:')
for item in ['<b>Acceso:</b> credenciales válidas e inválidas, protección de rutas y cierre de sesión.', '<b>Persistencia y reporte:</b> conservación de datos entre instancias, suma exacta de S/ 0.10 + S/ 0.20, filtro por fechas y descarga CSV.', '<b>Validaciones:</b> montos inválidos, fecha inexistente, rechazo de POST sin token CSRF, escape de HTML y protección de fórmulas en CSV.']:
    add('• '+item)
add('<b>Comando de verificación:</b><br/><font name="Courier" size="9">.\\.venv\\Scripts\\python.exe -m unittest discover -s tests -v</font>')
add('El recorrido real en el navegador incluyó iniciar sesión, registrar los tres gastos ficticios, consultar el panel y abrir el reporte. Las capturas documentan esos resultados; la vista móvil muestra la presentación de los mismos registros en un ancho reducido.')
section('13. Publicación y documentación')
add('El proyecto se publicó en un repositorio público de GitHub. El README de la portada incorpora las cuatro capturas de la aplicación, las instrucciones de instalación y una explicación de uso. La documentación indica que la aplicación se ejecuta localmente; GitHub comparte el código y no ejecuta el servidor Flask.')
add('<link href="https://github.com/Sarai6e/PRACTICA-CALIFICADA-2Tarea" color="#7350b5">https://github.com/Sarai6e/PRACTICA-CALIFICADA-2Tarea</link>')
section('14. Conclusiones y alcance')
add('Gastos Bloom cumple los requisitos de acceso, registro de gastos y generación de reportes con Python, Flask y SQLite. La persistencia permite recuperar los movimientos al reiniciar y los filtros facilitan revisar periodos concretos. El repositorio y su README permiten consultar y reproducir el proyecto.')
add('Se trata de una práctica académica con un único acceso fijo. No implementa cuentas individuales ni una configuración de producción. La base de datos local y el entorno virtual se excluyen del repositorio mediante .gitignore; una instalación nueva inicia sin gastos.')

def frame(canvas, doc):
    w,h=A4
    canvas.setStrokeColor(colors.HexColor('#e9e2ef'));canvas.line(50, h-44,w-50,h-44)
    canvas.setFont('Helvetica',8);canvas.setFillColor(PURPLE)
    canvas.drawString(50,h-32,'SARAI RUT ROMERO VILLANUEVA  |  GASTOS BLOOM')
    canvas.setFillColor(colors.HexColor('#746d80'));canvas.drawString(50,31,'Práctica Calificada 2 · Programación y Desarrollo Web')
    canvas.drawRightString(w-50,31,str(doc.page))

target=OUT/'Informe_Sarai_Romero_PC2_Gastos_Bloom.pdf'
doc=SimpleDocTemplate(str(target),pagesize=A4,rightMargin=50,leftMargin=50,topMargin=65,bottomMargin=55,title='Gastos Bloom - Informe de Práctica Calificada 2',author='Sarai Rut Romero Villanueva')
doc.build(story,onFirstPage=frame,onLaterPages=frame)
import pypdfium2 as pdfium
from pypdf import PdfReader
pdf=pdfium.PdfDocument(str(target))
for i in range(len(pdf)):
    pdf[i].render(scale=1.2).to_pil().save(TMP/f'pagina-{i+1:02}.png')
print('PDF:', target)
print('Páginas:',len(PdfReader(str(target)).pages))
