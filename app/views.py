from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Peticionarios, Documents, RtasFinales
from .forms import MiFormulario, PeticionarioForm, RtasForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import folium
from folium.plugins import FastMarkerCluster
from folium.plugins import MarkerCluster
import pandas as pd
import shutil
from datetime import datetime as dt
from urllib.parse import quote
from docxtpl import DocxTemplate
from io import BytesIO
import base64
from datetime import datetime
import simplekml
import zipfile
from django.db import transaction


# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def list_dps(_request):
    peticionarios=list(Peticionarios.objects.values())
    data={'peticionarios':peticionarios}
    return JsonResponse(data)

@login_required
def edit_dp(request, programmer_id):
    user = get_object_or_404(Peticionarios, pk=programmer_id)
    global old_nombre; global old_fecha_llegada
    nombre_encabezado= (str(user.nombre) + ' ' + str(user.fecha_llegada.strftime('%Y-%m-%d')))
    if request.method == 'GET':
        form = PeticionarioForm(instance=user)
        old_nombre = user.nombre
        old_fecha_llegada = user.fecha_llegada
        return render(request, 'edit_dp.html',{
            'form': form,
            'nombre_encabezado': nombre_encabezado
        })
    else:
        form = PeticionarioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if user.nombre != old_nombre or str(user.fecha_llegada) != old_fecha_llegada:
                old_folder_name = (str(old_nombre).replace(" ", "_") + ' ' + str(old_fecha_llegada))
                new_folder_name = (str(user.nombre).replace(" ", "_") + ' ' + str(user.fecha_llegada))
                old_folder_path = os.path.join(settings.MEDIA_ROOT, 'documents\\', old_folder_name)
                new_folder_path = os.path.join(settings.MEDIA_ROOT, 'documents\\', new_folder_name)
                for documento in Documents.objects.filter(peticionario=user.id):
                    old_url = documento.archivo
                    new_url=(str(old_url)).replace(old_folder_name,new_folder_name)
                    documento.archivo = new_url
                    documento.save()
                if os.path.exists(old_folder_path):
                    os.rename(old_folder_path, new_folder_path)
                    print(f'Carpeta renombrada de "{old_folder_name}" a "{new_folder_name}"')
            return redirect('index') 

        if form.errors:
            print('ERROR EN EL FORMS:')
            print(form.errors)
            return redirect('index') 

@login_required
def delete_user(request, programmer_id):
    user = get_object_or_404(Peticionarios, pk=programmer_id)
    nombre_busqueda= (str(user.nombre).replace(" ", "_") + ' ' + str(user.fecha_llegada.strftime('%Y-%m-%d')))
    delete_folder = os.path.join(settings.BASE_DIR, f'media\\documents\\{nombre_busqueda}')
    if request.method == 'GET':
        user.delete()
        shutil.rmtree(delete_folder, ignore_errors=True)
        return redirect('index')

@login_required   
def new_dp(request):
    if request.method == 'GET':
        return render(request,'new_dp.html',{
            'form':PeticionarioForm()
        })
    else:
        try:
            form = PeticionarioForm(request.POST)
            new_dp = form.save(commit=False)
            new_dp.save()
            return redirect('index')
        except ValueError:
            print('eerrooooorrroooo')
            return render(request, 'new_dp.html',{
            'form': PeticionarioForm,
            'error': 'Please provide valid data'
        })

def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
                'form': AuthenticationForm
            })
    else:
        user = authenticate(request, username=request.POST['username'],
            password=request.POST['password'])
        print(user)
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos'
            })
        else: 
            login(request, user)
            return redirect('index')

@login_required
def signout(request):
    logout(request)
    return redirect('index')

@login_required
def archivos2(request, programmer_id):
    user = get_object_or_404(Peticionarios, pk=programmer_id)
    data = {
        'fecha_llegada': user.fecha_llegada,
        'fecha_radicado':user.fecha_radicado,
        'fecha_entrega':user.fecha_entrega,
        'nombre': user.nombre,
        'radicado':user.radicado,
        'correo': user.correo,
        'direccion':user.direccion,
        'latitud':user.latitud,
        'longitud':user.longitud,
        'ciudad':user.ciudad,
        'localidad':user.localidad,
        'barrio':user.barrio,
        'tipo_dp':user.tipo_dp,
        'tema_dp':user.tema_dp,
        'asunto':user.asunto,
        'peticion':user.peticion,
        'enviada':user.enviada,
        'enviada_aerocivil':user.enviada_aerocivil,
        'radicado_salida':user.radicado_salida,
        'fecha_salida': user.fecha_salida
        # y así sucesivamente, incluye todos los campos que no deseas modificar
    }
    
    form = PeticionarioForm(instance=user)
    nombre_busqueda= (str(user.nombre).replace(" ", "_") + ' ' + str(user.fecha_llegada.strftime('%Y-%m-%d')))
    nombre_encabezado= (str(user.nombre) + ' ' + str(user.fecha_llegada.strftime('%Y-%m-%d')))
    if request.method == 'POST':
        alertasrtas=[]; alertas=[]

        if request.FILES.getlist('files'):
            files=request.FILES.getlist('files')
            for file in files:
                file_busqueda = str(file).replace(" ", "_") 
                documento_existente = Documents.objects.filter(
                    archivo=f'documents/{nombre_busqueda}/{file_busqueda}', peticionario=user.id).exists()
                if not documento_existente:
                    new_file = Documents(
                        archivo=file, 
                        peticionario=user)
                    new_file.save()
                    alertas.append(f'- El documento {file} cargo con exito')
                else:
                    alertas.append(f'- El documento {file} ya existe')

            documentos = Documents.objects.filter(peticionario=user.id)
            file_list = [documento.archivo.url for documento in documentos]
            name_list = [nombre.archivo.name for nombre in documentos]
            name_list = [item.replace(f'documents/{nombre_busqueda}/', '') for item in name_list]

            rta_data = RtasFinales.objects.filter(peticionario=user.id)
            file_list2 = [rta.rta.url for rta in rta_data]
            name_list2 = [nombre.rta.name for nombre in rta_data]
            name_list2 = [item.replace(f'rtas/', '') for item in name_list2]
            
            return render(request, 'archivos.html', {
                    'urls_and_names': zip(file_list, name_list),
                    'urls_and_names_rta': zip(file_list2, name_list2),
                    'peticionario_id': user.id,
                    'alertasrtas': alertasrtas,
                    'alertas': alertas,
                    'nombre_encabezado': nombre_encabezado,
                    'form':form
                })
        
        if request.FILES['rta']:
            rta=request.FILES['rta']
            data['fecha_salida'] = request.POST.get('fecha_salida')
            data['radicado_salida'] = request.POST.get('radicado_salida')
            data['enviada'] = request.POST.get('enviada')
            form = PeticionarioForm(data, instance=user)
            if form.is_valid():
                rta_busqueda = str(rta).replace(" ", "_")
                rta_existente = RtasFinales.objects.filter(
                    rta=f'rtas/{rta_busqueda}').exists()
                if not rta_existente:
                    new_rta = RtasFinales(
                        rta=rta, 
                        peticionario=user)
                    new_rta.save()
                    alertasrtas.append(f'- El documento {rta} cargo con exito')
                    form.save()
                    alertasrtas.append(f'- Registro de {user.nombre} actualizado')
                else:
                    alertasrtas.append(f'- El documento {rta} ya existe')
            else:
                alertasrtas.append(f'el formulario no es valido: {form.errors}')
                print(form.errors)
            
            
            documentos = Documents.objects.filter(peticionario=user.id)
            file_list = [documento.archivo.url for documento in documentos]
            name_list = [nombre.archivo.name for nombre in documentos]
            name_list = [item.replace(f'documents/{nombre_busqueda}/', '') for item in name_list]

            rta_data = RtasFinales.objects.filter(peticionario=user.id)
            file_list2 = [rta.rta.url for rta in rta_data]
            name_list2 = [nombre.rta.name for nombre in rta_data]
            name_list2 = [item.replace(f'rtas/', '') for item in name_list2]
            
            return render(request, 'archivos.html', {
                    'urls_and_names': zip(file_list, name_list),
                    'urls_and_names_rta': zip(file_list2, name_list2),
                    'peticionario_id': user.id,
                    'alertasrtas': alertasrtas,
                    'alertas': alertas,
                    'nombre_encabezado': nombre_encabezado,
                    'form':form
                })

    else:
        documentos = Documents.objects.filter(peticionario=user.id)
        file_list = [documento.archivo.url for documento in documentos]
        name_list = [nombre.archivo.name for nombre in documentos]
        name_list = [item.replace(f'documents/{nombre_busqueda}/', '') for item in name_list]

        rta_data = RtasFinales.objects.filter(peticionario=user.id)
        file_list2 = [rta.rta.url for rta in rta_data]
        name_list2 = [nombre.rta.name for nombre in rta_data]
        name_list2 = [item.replace(f'rtas/', '') for item in name_list2]
        return render(request, 'archivos.html',{
            'urls_and_names': zip(file_list, name_list),
            'urls_and_names_rta': zip(file_list2, name_list2),
            'peticionario_id': user.id,
            'nombre_encabezado': nombre_encabezado,
            'form': form
        })

@login_required
def delete_document(request, peticionario_id, name):
    user = get_object_or_404(Peticionarios, pk=peticionario_id)
    nombre_busqueda= (str(user.nombre).replace(" ", "_") + ' ' + str(user.fecha_llegada.strftime('%Y-%m-%d')))
    registro_borrar = Documents.objects.filter(peticionario=peticionario_id, archivo=f'documents/{nombre_busqueda}/{name}')
    direc_borrar = os.path.join(settings.MEDIA_ROOT, f'documents/{nombre_busqueda}/{name}')
    print(direc_borrar)
    if os.path.exists(direc_borrar):
        # Eliminar el archivo del sistema de archivos
        os.remove(direc_borrar)
    registro_borrar.delete()
    return redirect('archivos2', programmer_id=peticionario_id)

@login_required
def delete_rta(request, peticionario_id, name):
    user = get_object_or_404(Peticionarios, pk=peticionario_id)
    nombre_busqueda= (str(user.nombre).replace(" ", "_") + ' ' + str(user.fecha_llegada.strftime('%Y-%m-%d')))
    registro_borrar = RtasFinales.objects.filter(peticionario=peticionario_id, rta=f'rtas/{name}')
    direc_borrar = os.path.join(settings.MEDIA_ROOT, f'rtas/{name}')
    if os.path.exists(direc_borrar):
        # Eliminar el archivo del sistema de archivos
        os.remove(direc_borrar)
    registro_borrar.delete()
    return redirect('archivos2', programmer_id=peticionario_id)

@login_required
def upload_dps(request):
    if request.method == 'POST':
        file=request.FILES['file']
        
        # except Exception as e:
        df = pd.read_excel(file) 
        df.fillna('', inplace=True) 
        df['fecha_llegada'] = pd.to_datetime(df['fecha_llegada'], format='%d-%m-%Y', errors='coerce').dt.strftime('%Y-%m-%d')
        df['fecha_entrega'] = pd.to_datetime(df['fecha_entrega'], format='%d-%m-%Y', errors='coerce').dt.strftime('%Y-%m-%d')
        df['fecha_radicado'] = pd.to_datetime(df['fecha_radicado'], format='%d-%m-%Y', errors='coerce').dt.strftime('%Y-%m-%d')
        # df['fecha_salida'] = pd.to_datetime(df['fecha_salida'], errors='coerce').dt.strftime('%Y-%m-%d')

        for index, row in df.iterrows():
            peticionario = Peticionarios(
                fecha_llegada=row['fecha_llegada'],
                fecha_entrega=row['fecha_entrega'],
                fecha_radicado=row['fecha_radicado'],
                nombre=row['nombre'],
                radicado=row['radicado'],
                correo=row['correo'],
                direccion=row['direccion'],
                latitud=row['latitud'],
                longitud=row['longitud'],
                ciudad=row['ciudad'],
                localidad=row['localidad'],
                barrio=row['barrio'],
                tipo_dp=row['tipo_dp'],
                tema_dp=row['tema_dp'],
                asunto=row['asunto'],
                peticion=row['peticion'],
                enviada=row['enviada'],
                # radicado_salida=row['radicado_salida'],
                # fecha_salida=row['fecha_salida'],
            )
            try:
                peticionario.save()
                print(f'Se subio el registro {peticionario}!!!!!!')
                print(f'{peticionario.fecha_llegada}')
            except Exception as e:
                print(f'no se pudo subir el registro {peticionario} por error:{e}')
                print(f'{peticionario.fecha_llegada}')
         
        return render(request, 'index.html')
                

    else:
        return render(request, 'subir_grupo.html')

@login_required
def proyecciones(request, programmer_id):
    user = get_object_or_404(Peticionarios, pk=programmer_id) 
    data = {
        'fecha_llegada': user.fecha_llegada,
        'fecha_radicado':user.fecha_radicado,
        'fecha_entrega':user.fecha_entrega,
        'nombre': user.nombre,
        'radicado':user.radicado,
        'correo': user.correo,
        'direccion':user.direccion,
        'latitud':user.latitud,
        'longitud':user.longitud,
        'ciudad':user.ciudad,
        'localidad':user.localidad,
        'barrio':user.barrio,
        'tipo_dp':user.tipo_dp,
        'tema_dp':user.tema_dp,
        'asunto':user.asunto,
        'peticion':user.peticion,
        'enviada':user.enviada,
        'enviada_aerocivil':user.enviada_aerocivil,
        'radicado_salida':user.radicado_salida,
        'fecha_salida': user.fecha_salida
        # y así sucesivamente, incluye todos los campos que no deseas modificar
    }

    meses_espanol = {1: 'ENERO',2: 'FEBRERO',3: 'MARZO',4: 'ABRIL',5: 'MAYO',
                6: 'JUNIO',7: 'JULIO',8: 'AGOSTO',9: 'SEPTIEMBRE',10: 'OCTUBRE',
                11: 'NOVIEMBRE',12: 'DICIEMBRE'}

    form = PeticionarioForm(instance=user)

    if request.method == 'GET':
        return render(request, 'proyecciones.html',{
            'form': form
        })

    elif request.method == 'POST':
        alertas=[]
        fecha_entrega = request.POST.get('fecha_entrega')
        fecha_radicado = request.POST.get('fecha_radicado')
        saludo = request.POST.get('saludo')
        nombre = request.POST.get('nombre')
        radicado = request.POST.get('radicado')
        correo = request.POST.get('correo')
        direccion = request.POST.get('direccion')
        barrio = request.POST.get('barrio')
        localidad = request.POST.get('localidad')
        asunto = request.POST.get('asunto')
        peticion = request.POST.get('peticion')
        asunto1 = request.POST.get('asunto1')
        asunto2 = request.POST.get('asunto2')
        asunto3 = request.POST.get('asunto3')

        fecha_radicado = dt.strptime(fecha_radicado, '%Y-%m-%d')
        dia = fecha_radicado.day
        mes = fecha_radicado.month
        anio = fecha_radicado.year
        mes_espanol = meses_espanol.get(mes).upper()
        fecha_radicado = f'{dia} DE {mes_espanol} DEL {anio}'

        fecha_entrega = dt.strptime(fecha_entrega, '%Y-%m-%d')
        dia = fecha_entrega.day
        mes = fecha_entrega.month
        anio = fecha_entrega.year
        mes_espanol = meses_espanol.get(mes).lower()
        fecha_entrega = f'{dia} de {mes_espanol} del {anio}'
        
        datos_usuario = {
            'genero_titulo': saludo,
            'genero': saludo.lower(),
            'nombre': nombre,
            'nombre_titulo': nombre.upper(),
            'fecha_oficio': fecha_entrega,
            'radicado': radicado,
            'correo': correo,
            'fecha_radicado': fecha_radicado,
            'direccion': direccion,
            'barrio': barrio,
            'localidad': localidad,
            'asunto': asunto,
            'peticion': peticion,
            'peticion_puntual1': asunto1,
            'peticion_puntual2': asunto2,
            'peticion_puntual3': asunto3,
        }
        plantilla_path = os.path.join(settings.MEDIA_ROOT, 'plantillas\\PlantillaPQRS.docx')
        doc = DocxTemplate(plantilla_path)
        nombre_busqueda = f"{str(user.nombre).replace(' ', '_')} {user.fecha_llegada.strftime('%Y-%m-%d')}"

        doc.render(datos_usuario)
        output = BytesIO()
        nombre_archivo = f'RTA_{nombre_busqueda}.docx' 
        doc.save(output)
        output.seek(0)

        
        carpeta_peticionario = os.path.join(settings.MEDIA_ROOT, 'documents', nombre_busqueda)

        if not os.path.exists(carpeta_peticionario):
            os.makedirs(carpeta_peticionario)

        ruta_archivo = os.path.join(carpeta_peticionario, nombre_archivo)
        # archivo_existente = Documents.objects.filter(archivo=f'documents/{nombre_busqueda}/{nombre_archivo}', peticionario=user.id).exists()

        try:
            with transaction.atomic():
                # Verificar si el registro ya existe en la base de datos
                documento_existente = Documents.objects.filter(
                    archivo=f'documents/{nombre_busqueda}/{nombre_archivo}', 
                    peticionario=user.id
                ).first()

                if documento_existente:
                    # Actualizar registro existente
                    documento_existente.archivo = f'documents/{nombre_busqueda}/{nombre_archivo}'
                    documento_existente.save()
                    alertas.append(f'- El archivo {nombre_archivo} ya existía y se actualizó en la base de datos.')
                else:
                    # Crear nuevo registro
                    nuevo_documento = Documents(
                        archivo=f'documents/{nombre_busqueda}/{nombre_archivo}',
                        peticionario=user
                    )
                    nuevo_documento.save()
                    alertas.append(f'- El archivo {nombre_archivo} se ha registrado correctamente en la base de datos.')

                # Guardar el archivo en el sistema de archivos
                with open(ruta_archivo, 'wb') as f:
                    f.write(output.read())
                    alertas.append(f'- El archivo {nombre_archivo} se ha guardado exitosamente en {carpeta_peticionario}.')

        except Exception as e:
            alertas.append(f'- Ocurrió un error al guardar el archivo: {str(e)}')
    
        data['asunto'] = asunto
        data['peticion'] = peticion
        form = PeticionarioForm(data, instance=user)
        if form.is_valid():
            form.save()
            alertas.append(f'- Se actualizaron los capos de Asunto y Petición para este registro...')
        else:
            alertas.append(f'- El formulario no es valido')
        
        url_archivo = os.path.join(settings.MEDIA_URL, f'documents/{nombre_busqueda}/', nombre_archivo)
        return render(request, 'proyecciones.html',{
            'form': form,
            'url': url_archivo,
            'doc_name': nombre_archivo,
            'alertas': alertas
        })

def read_coordinates_from_txt(txt_path):
    with open(txt_path, 'r') as file:
        # Leer el contenido del archivo
        content = file.read().strip()
    
    # Dividir el contenido en coordenadas individuales
    coord_strings = content.split(' ')
    
    # Convertir las coordenadas a formato numérico y guardarlas en una lista
    coordinates = []
    for coord in coord_strings:
        lon, lat, _ = coord.split(',')
        coordinates.append([float(lat), float(lon)])
    
    return coordinates

@login_required
def mapa(request):
    
    peticionarios = Peticionarios.objects.exclude(longitud='', latitud='')

    initialMap = folium.Map(location=[4.669399, -74.089791], zoom_start=12)
    
    marker_cluster = MarkerCluster().add_to(initialMap)

    for peticionario in peticionarios:
        if peticionario.latitud and peticionario.longitud:
            # Crear el contenido del popup
            popup_content = f"""
                <strong>Nombre:</strong> {peticionario.nombre}<br>
                <strong>Fecha de Llegada:</strong> {peticionario.fecha_llegada}<br>
                <strong>Petición:</strong> {peticionario.peticion}
            """
            
            folium.Marker(
                location=[float(peticionario.latitud), float(peticionario.longitud)],
                popup=folium.Popup(popup_content, max_width=250)
            ).add_to(marker_cluster)

    AI_txt_path = os.path.join(settings.BASE_DIR, 'app', 'coordenadas.txt')
    coordinates = read_coordinates_from_txt(AI_txt_path)
    
    folium.Polygon(
        locations=coordinates,
        color='blue',
        weight=2,
        fill=True,
        fill_color='blue',
        fill_opacity=0.1
    ).add_to(initialMap)
    
    context={'map':initialMap._repr_html_()}
    return render(request, 'map.html', context)

@login_required
def export_dps(request):
    queryset = Peticionarios.objects.all()

    # Crear un DataFrame de Pandas con los datos
    data = {
        'Nombre': [p.nombre for p in queryset],
        'Fecha Llegada': [p.fecha_llegada for p in queryset],
        'Fecha Entrega': [p.fecha_entrega for p in queryset],
        'Fecha Radicado': [p.fecha_radicado for p in queryset],
        'Radicado': [p.radicado for p in queryset],
        'Correo': [p.correo for p in queryset],
        'Dirección': [p.direccion for p in queryset],
        'Longitud': [p.longitud for p in queryset],
        'Latitud': [p.latitud for p in queryset],
        'Ciudad': [p.ciudad for p in queryset],
        'Localidad': [p.localidad for p in queryset],
        'Barrio': [p.barrio for p in queryset],
        'Tipo DP': [p.tipo_dp for p in queryset],
        'Tema DP': [p.tema_dp for p in queryset],
        'Asunto': [p.asunto for p in queryset],
        'Petición': [p.peticion for p in queryset],
        'Radicado Salida': [p.radicado_salida for p in queryset],
        'Fecha Salida': [p.fecha_salida for p in queryset],
        'Ruta Respuesta Final': [RtasFinales.objects.filter(peticionario=p).first().rta.path if RtasFinales.objects.filter(peticionario=p).exists() else '' for p in queryset],
        'Nombre Respuesta Final': [RtasFinales.objects.filter(peticionario=p).first().rta.name if RtasFinales.objects.filter(peticionario=p).exists() else '' for p in queryset],
        'Carpeta Documentos': [os.path.dirname(Documents.objects.filter(peticionario=p).first().archivo.path) if Documents.objects.filter(peticionario=p).exists() else '' for p in queryset],
    }
    df = pd.DataFrame(data)

    # Especificar el orden de las columnas
    column_order = ['Nombre', 'Fecha Llegada', 'Fecha Entrega', 'Fecha Radicado', 'Radicado', 'Correo', 'Dirección', 'Longitud','Latitud','Ciudad', 'Localidad', 'Barrio', 'Tipo DP', 'Tema DP', 'Asunto', 'Petición', 'Radicado Salida', 'Fecha Salida', 'Ruta Respuesta Final', 'Nombre Respuesta Final', 'Carpeta Documentos']
    df = df[column_order]

    excel_file_path = "peticionarios.xlsx"
    df.to_excel(excel_file_path, index=False)

    kml = simplekml.Kml()

    # Añadir puntos para cada peticionario en el KML
    for peticionario in queryset:
        if peticionario.latitud and peticionario.longitud:
            kml.newpoint(name=peticionario.nombre, coords=[(peticionario.longitud, peticionario.latitud)])

    # Guardar el archivo KML
    kml_file_path = "peticionarios.kml"
    kml.save(kml_file_path)

    # Comprimir el archivo KML para generar un KMZ
    kmz_file_path = "peticionarios.kmz"
    with zipfile.ZipFile(kmz_file_path, 'w', zipfile.ZIP_DEFLATED) as kmz:
        kmz.write(kml_file_path)

    # Crear un archivo ZIP que contenga tanto el Excel como el KMZ
    zip_file_path = "peticionarios.zip"
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(excel_file_path)
        zipf.write(kmz_file_path)

    # Crear la respuesta HTTP para descargar el ZIP
    with open(zip_file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=peticionarios.zip'

    # Limpiar archivos temporales
    os.remove(excel_file_path)
    os.remove(kml_file_path)
    os.remove(kmz_file_path)
    os.remove(zip_file_path)
    
    return response

@login_required
def graficos(request):
    if request.method == 'POST':
        start_date = request.POST.get('start-date', '2024-01')
        end_date = request.POST.get('end-date', datetime.today().strftime('%Y-%m'))
        
    else:
        start_date = '2024-01'
        end_date = datetime.today().strftime('%Y-%m')
        

    queryset = Peticionarios.objects.all()
    data = {
        'Nombre': [p.nombre for p in queryset],
        'Fecha Llegada': [p.fecha_llegada for p in queryset],
        'Localidad': [p.localidad for p in queryset],
        'Barrio': [p.barrio for p in queryset],
        'Tipo DP': [p.tipo_dp for p in queryset],
        'Tema DP': [p.tema_dp for p in queryset],
    }
    df_peticiones  = pd.DataFrame(data)

    df_peticiones['Localidad'] = df_peticiones['Localidad'].replace('','Sin ubicación')
    df_peticiones['Barrio'] = df_peticiones['Barrio'].replace('','Sin ubicación')
    df_peticiones['Fecha Llegada'] = pd.to_datetime(df_peticiones['Fecha Llegada'])

    
    date_range = pd.date_range(start_date, end_date, freq='D')

    peticiones_por_dia = df_peticiones['Fecha Llegada'].value_counts().sort_index()
    df_counts1 = peticiones_por_dia.reindex(date_range, fill_value=0).reset_index()
    df_counts1.columns = ['fecha', 'cantidad']
    data_json1 = df_counts1.to_json(orient='records', date_format='iso')

    # Segundo gráfico: Cantidad de peticiones por mes
    df_peticiones['Mes'] = df_peticiones['Fecha Llegada'].dt.to_period('M')
    df_peticiones = df_peticiones[(df_peticiones['Mes'] >= start_date) & (df_peticiones['Mes'] <= end_date)]
    peticiones_por_mes = df_peticiones['Mes'].value_counts().sort_index()
    df_counts2 = peticiones_por_mes.reset_index()
    df_counts2.columns = ['mes', 'cantidad']
    df_counts2['mes'] = df_counts2['mes'].dt.strftime('%Y-%m')
    data_json2 = df_counts2.to_json(orient='records')

   # Grafico de Torta para Localidades
    localidad_counts = df_peticiones['Localidad'].value_counts().reset_index()
    localidad_counts.columns = ['localidad', 'cantidad']
    data_json3 = localidad_counts.to_json(orient='records')

    # Grafico de Torta para Tipos de DP
    tipo_dp_counts = df_peticiones['Tipo DP'].value_counts().reset_index()
    tipo_dp_counts.columns = ['tipo_dp', 'cantidad']
    data_json4 = tipo_dp_counts.to_json(orient='records')

    # Grafico de Torta para Temas de DP
    tema_dp_counts = df_peticiones['Tema DP'].value_counts().reset_index()
    tema_dp_counts.columns = ['tema_dp', 'cantidad']
    data_json5 = tema_dp_counts.to_json(orient='records')

    # Grafico de Torta para Barrios
    barrio_counts = df_peticiones['Barrio'].value_counts().reset_index()
    barrio_counts.columns = ['barrio', 'cantidad']
    data_json6 = barrio_counts.to_json(orient='records')

    return render(request, 'graficos.html', {
        'data_json1': data_json1, 
        'data_json2': data_json2, 
        'data_json3': data_json3, 
        'data_json4': data_json4, 
        'data_json5': data_json5, 
        'data_json6': data_json6,
        'start_date': start_date,
        'end_date': end_date,
        })