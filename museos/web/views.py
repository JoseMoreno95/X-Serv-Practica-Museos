from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Museo, Distrito, Comentario, Favorito, Like, Titulo, Letra, Color
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from web.parser import parseXML
import operator
from django.template.loader import get_template
from django.template import Context
import datetime

def getMuseums():
    museos = Museo.objects.all()
    allMuseums = {}
    for museo in museos:
        allMuseums[museo.ID_ENTIDAD] = museo.comentario_set.count()
    return allMuseums

def getAccessibleMuseums():
    museos = Museo.objects.all()
    allMuseums = {}
    for museo in museos:
        if museo.ACCESIBILIDAD == '1':
            allMuseums[museo.ID_ENTIDAD] = museo.comentario_set.count()
    return allMuseums

def getRanking():
    allMuseums = getMuseums()
    ranking = sorted(allMuseums.items(), key = operator.itemgetter(1))
    ranking.reverse()
    return ranking

def getAccessibleRanking():
    allMuseums = getAccessibleMuseums()
    ranking = sorted(allMuseums.items(), key = operator.itemgetter(1))
    ranking.reverse()
    return ranking

@csrf_exempt
def mainPage(request):
    template = get_template('index.html')
    topFive = range(5)
    list = '<br>'
    markers = ''
    if request.method == 'GET' or (request.method == 'POST' and request.POST['accion'] == 'mostrar'):
        ranking = getRanking()
        list = (list + "<center><form action='/' method='post'><input type='hidden' name='accion' value='ocultar'>" +
            "<input class='desplegable' type='submit' value='Mostrar museos accesibles'></form></center><div id='scroll'>")
        for item in topFive:
            if ranking[item][1] != 0:
                museum = Museo.objects.get(ID_ENTIDAD = ranking[item][0])
                list = list + "<center><a class='titulos' href=" + museum.CONTENT_URL + '>' + museum.NOMBRE + '</a><br><b>' + str(museum.comentario_set.count()) + ' Comentarios - ' + str(museum.like_set.count()) + ' Likes</b></br></br>'
                list = list + "<a class='direccion'>" + museum.CLASE_VIAL + ' ' + museum.NOMBRE_VIA + ', Nº ' + museum.NUM + ', ' + museum.LOCALIDAD + '</a></br></br>'
                list = list + "<a class='info' href=" + "/museos/" + museum.ID_ENTIDAD + '/>Más información</a></center></br></br>'
                if museum.LATITUD != 'No disponible' and museum.LONGITUD != 'No disponible':
                    markers = (markers +
                    "var " + "X"  + museum.ID_ENTIDAD + "info = new google.maps.InfoWindow({" +
                        "content:'<h1>" + museum.NOMBRE + "</h1>'});" +
                    "var " + "X" + museum.ID_ENTIDAD + "marker = new google.maps.Marker({" +
                        "position: {lat: " + museum.LATITUD + ", lng: " + museum.LONGITUD + " },map: map});" +
                    "X" + museum.ID_ENTIDAD + "marker.addListener('click', function() {" +
                    "X" + museum.ID_ENTIDAD + "info.open(map," + "X" + museum.ID_ENTIDAD + "marker);" +
                    "});")
        list = list + '</div>'
        if list == '':
            list = "<a class='titulos'>" + 'No hay museos con comentarios, ¡sé el primero en comentar!' + '</a></br></br>'
    elif request.method == 'POST' and request.POST['accion'] == 'ocultar':
        ranking = getAccessibleRanking()
        list = (list + "<center><form action='/' method='post'><input type='hidden' name='accion' value='mostrar'>" +
            "<input class='desplegable' type='submit' value='Mostrar todos los museos'></form></center><div id='scroll'>")
        for item in topFive:
            if ranking[item][1] != 0:
                museum = Museo.objects.get(ID_ENTIDAD = ranking[item][0])
                list = list + "<center><a class='titulos' href=" + museum.CONTENT_URL + '>' + museum.NOMBRE + '</a><br><b>' + str(museum.comentario_set.count()) + ' Comentarios - ' + str(museum.like_set.count()) + ' Likes</b></br></br>'
                list = list + "<a class='direccion'>" + museum.CLASE_VIAL + ' ' + museum.NOMBRE_VIA + ', Nº ' + museum.NUM + ', ' + museum.LOCALIDAD + '</a></br></br>'
                list = list + "<a class='info' href=" + "/museos/" + museum.ID_ENTIDAD + '/>Más información</a></center></br></br>'
                if museum.LATITUD != 'No disponbile' and museum.LONGITUD != 'No disponible':
                    markers = (markers +
                    "var " + "X"  + museum.ID_ENTIDAD + "info = new google.maps.InfoWindow({" +
                        "content:'<h1>" + museum.NOMBRE + "</h1>'});" +
                    "var " + "X" + museum.ID_ENTIDAD + "marker = new google.maps.Marker({" +
                        "position: {lat: " + museum.LATITUD + ", lng: " + museum.LONGITUD + " },map: map});" +
                    "X" + museum.ID_ENTIDAD + "marker.addListener('click', function() {" +
                    "X" + museum.ID_ENTIDAD + "info.open(map," + "X" + museum.ID_ENTIDAD + "marker);" +
                    "});")
        list = list + '</div>'
        if list == '' or list == '</div>':
            list = "<a class='titulos'>" + 'No hay museos accesibles con comentarios, ¡sé el primero en comentar!' + '</a></br></br>'
    style = ''
    if request.user.is_authenticated():
        login = 1
        try:
            color = Color.objects.get(usuario = request.user)
            color = color.color
        except Color.DoesNotExist:
            color = 'EEF4F8'
        try:
            letra = Letra.objects.get(usuario = request.user)
            letra = letra.letra
        except Letra.DoesNotExist:
            letra = '9'
        style = ("body{font-family: 'Helvetica', sans-serif;"
            "color: #444444;"
            "font-size: " + letra + "pt;"
            "background-color: #" + color + ";}")
    else:
        login = 0
    users = User.objects.all()
    userList = ''
    for user in users:
        try:
            title = Titulo.objects.get(usuario = user.username)
            userList = userList + "<li><a href='/" + user.username + "'>" + title.titulo + ' - ' + user.username + "</a></li></br>"
        except Titulo.DoesNotExist:
            userList = userList + "<li><a href='/" + user.username + "'>Página de " + user.username + "</a></li></br>"
    return HttpResponse(template.render(Context({'body': list, 'login': login, 'user': request.user, 'userList': userList, 'formato': style, 'markers': markers})))

@csrf_exempt
def museumsPage(request):
    template = get_template('museos.html')
    if request.method == 'GET':
        museos = Museo.objects.all()
    elif request.method == 'POST':
        distrito = Distrito.objects.get(nombre = request.POST['distrito'])
        museos = distrito.museo_set.all()
    list = ''
    markers = ''
    i = 1
    for museo in museos:
        list = list + "<center><a class='titulos'>" + museo.NOMBRE + '</a></br>'
        list = list + "<a class='info' href=" + "/museos/" + museo.ID_ENTIDAD + '/>Más información</a></center></br></br>'
        if museo.LATITUD != 'No disponible' and museo.LONGITUD != 'No disponible':
            markers = (markers +
            "var " + "X"  + museo.ID_ENTIDAD + "info = new google.maps.InfoWindow({" +
                "content:'<h1>" + museo.NOMBRE + "</h1>'});" +
            "var " + "X" + museo.ID_ENTIDAD + "marker = new google.maps.Marker({" +
                "position: {lat: " + museo.LATITUD + ", lng: " + museo.LONGITUD + " },map: map});" +
            "X" + museo.ID_ENTIDAD + "marker.addListener('click', function() {" +
            "X" + museo.ID_ENTIDAD + "info.open(map," + "X" + museo.ID_ENTIDAD + "marker);" +
            "});")
    style = ''
    if request.user.is_authenticated():
        login = 1
        try:
            color = Color.objects.get(usuario = request.user)
            color = color.color
        except Color.DoesNotExist:
            color = 'EEF4F8'
        try:
            letra = Letra.objects.get(usuario = request.user)
            letra = letra.letra
        except Letra.DoesNotExist:
            letra = '9'
        style = ("body{font-family: 'Helvetica', sans-serif;"
            "color: #444444;"
            "font-size: " + letra + "pt;"
            "background-color: #" + color + ";}")
    else:
        login = 0
    distritos = Distrito.objects.all()
    districtList = ''
    for distrito in distritos:
        districtList = districtList + "<option value='" + distrito.nombre + "'>" + distrito.nombre + "</option>"
    return HttpResponse(template.render(Context({'body': list, 'login': login, 'user': request.user, 'districtList': districtList, 'formato': style, 'markers': markers})))

@csrf_exempt
def museumPage(request, museumID):
    template = get_template('museo.html')
    museum = Museo.objects.get(ID_ENTIDAD = museumID)
    if request.method == 'POST' and 'comentario' in request.POST:
        comment = Comentario(texto = request.POST['comentario'], museo = museum, usuario = request.user.username)
        comment.save()
    elif request.method == 'POST' and 'añadir' in request.POST:
        fav = Favorito(museo = museum, usuario = request.user)
        fav.save()
    elif request.method == 'POST' and 'quitar' in request.POST:
        Favorito.objects.filter(museo = museum, usuario = request.user).delete()
    elif request.method == 'POST' and 'mas' in request.POST:
        like = Like(museo = museum, usuario = request.user)
        like.save()
    elif request.method == 'POST' and 'menos' in request.POST:
        Like.objects.filter(museo = museum, usuario = request.user).delete()
    comments = museum.comentario_set.all()
    message = ("<center><b><a class='titulos_museo'>" + museum.NOMBRE + "</a></b></center><div id='scroll'></br>"
    "<center><b><a class='titulos_museo'>Descripción</a></b></center></br>"
    "<center><a class='texto_museo'>" + museum.DESCRIPCION_ENTIDAD + '</a></center></br>'
    "<center><b><a class='titulos_museo'>Horario</a></b></center></br>"
    "<center><a class='texto_museo'>" + museum.HORARIO + '</a></center></br>'
    "<center><b><a class='titulos_museo'>Accesibilidad</a></b></center></br>"
    "<center><a class='texto_museo'>" + museum.ACCESIBILIDAD + '</a></center></br>'
    "<center><b><a class='titulos_museo'>Dirección</a></b></center></br>"
    "<center><a class='texto_museo'>" + museum.CLASE_VIAL + ' ' + museum.NOMBRE_VIA + ', Nº ' + museum.NUM + ', ' + museum.LOCALIDAD + '</a><center></br>'
    "<center><a class='texto_museo'>Barrio: " + museum.BARRIO + '</a></center></br>'
    "<center><a class='texto_museo'>Distrito: " + str(museum.DISTRITO) + '</a></center></br>'
    "<center><b><a class='titulos_museo'>Datos de contacto</a></b></center></br>"
    "<center><a class='texto_museo'>Teléfono: " + museum.TELEFONO + '</a></center></br>'
    "<center><a class='texto_museo'>Email: " + museum.EMAIL + '</a></center></br>'
    "<center><b><a class='titulos_museo'>Comentarios</a></b></center></br>")
    allComments = ''
    for comment in comments:
        allComments = allComments + "<center><a class='texto_museo'><b>" + 'Anónimo</b>: ' + comment.texto + ', ' + (datetime.timedelta(hours=2) + comment.fecha).strftime("%H:%M:%S %d-%m-%Y") + '</a></center></br>'
    message = message + allComments
    style = ''
    if request.user.is_authenticated():
        login = 1
        try:
            favorito = Favorito.objects.get(museo = museum, usuario = request.user)
            favoriteButton = ("<center><form action='/museos/" + museumID + "/' method='post'><input type='hidden' name='quitar' value='fav'>" +
                "<input class='desplegable' type='submit' value='Quitar de favoritos'></form></center>")
        except Favorito.DoesNotExist:
            favoriteButton = ("<center><form action='/museos/" + museumID + "/' method='post'><input type='hidden' name='añadir' value='fav'>" +
                "<input class='desplegable' type='submit' value='Añadir a favoritos'></form></center>")
        try:
            like = Like.objects.get(museo = museum, usuario = request.user)
            likeButton = ("<center><form action='/museos/" + museumID + "/' method='post'><input type='hidden' name='menos' value='like'>" +
                "<input class='desplegable' type='submit' value='Dislike'></form></center>")
        except Like.DoesNotExist:
            likeButton = ("<center><form action='/museos/" + museumID + "/' method='post'><input type='hidden' name='mas' value='like'>" +
                "<input class='desplegable' type='submit' value='Like'></form></center>")
        try:
            color = Color.objects.get(usuario = request.user)
            color = color.color
        except Color.DoesNotExist:
            color = 'EEF4F8'
        try:
            letra = Letra.objects.get(usuario = request.user)
            letra = letra.letra
        except Letra.DoesNotExist:
            letra = '9'
        style = ("body{font-family: 'Helvetica', sans-serif;"
            "color: #444444;"
            "font-size: " + letra + "pt;"
            "background-color: #" + color + ";}")
    else:
        login = 0
        favoriteButton = ''
        likeButton = ''
    if museum.LATITUD != 'No disponbile' and museum.LONGITUD != 'No disponible':
        marker = ("var " + "X"  + museum.ID_ENTIDAD + "info = new google.maps.InfoWindow({" +
            "content:'<h1>" + museum.NOMBRE + "</h1>'});" +
        "var " + "X" + museum.ID_ENTIDAD + "marker = new google.maps.Marker({" +
            "position: {lat: " + museum.LATITUD + ", lng: " + museum.LONGITUD + " },map: map});" +
        "X" + museum.ID_ENTIDAD + "marker.addListener('click', function() {" +
        "X" + museum.ID_ENTIDAD + "info.open(map," + "X" + museum.ID_ENTIDAD + "marker);" +
        "});")
    return HttpResponse(template.render(Context({'body': message, 'login': login, 'user': request.user, 'id': museumID, 'fav': favoriteButton, 'like': likeButton, 'formato': style, 'marker': marker})))

@csrf_exempt
def loginPage(request):
    if request.method == 'POST':
        if not request.user.is_authenticated() and 'login' in request.POST:
            username = request.POST['Usuario']
            password = request.POST['Contraseña']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
        elif not request.user.is_authenticated() and 'registro' in request.POST:
            username = request.POST['Usuario']
            password = request.POST['Contraseña']
            try:
                user = User.objects.get(username = username)
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user)
            except User.DoesNotExist:
                user = User.objects.create_user(username = username, password = password)
                user.save()
    request.method = 'GET'
    return mainPage(request)

def logoutPage(request):
    logout(request)
    return mainPage(request)

def userPage(request, user, number):
    if number == None:
        number = 1
    template = get_template('personal.html')
    listTotal = ''
    favoritos = Favorito.objects.filter(usuario = user)
    group = range(5)
    count = 0;
    markers = ''
    for favorito in favoritos:
        count = count + 1;
        museum = Museo.objects.get(NOMBRE = favorito.museo)
        listTotal = listTotal + "<a class='titulos' href=" + museum.CONTENT_URL + '>' + museum.NOMBRE + '</a><br><b>' + str(museum.comentario_set.count()) + ' Comentarios - ' + str(museum.like_set.count()) + ' Likes</b></br></br>'
        listTotal = listTotal + "<a class='direccion'>" + museum.CLASE_VIAL + ' ' + museum.NOMBRE_VIA + ', Nº ' + museum.NUM + ', ' + museum.LOCALIDAD + '</a></br></br>'
        listTotal = listTotal + "<a class='info' href=" + "/museos/" + museum.ID_ENTIDAD + '/>Más información</a> <b>Fecha de guardado:' + (datetime.timedelta(hours=2) + favorito.fecha).strftime("%H:%M:%S %d-%m-%Y") + '</b></br></br></br>'
        if museum.LATITUD != 'No disponible' and museum.LONGITUD != 'No disponible':
            markers = (markers +
            "var " + "X"  + museum.ID_ENTIDAD + "info = new google.maps.InfoWindow({" +
                "content:'<h1>" + museum.NOMBRE + "</h1>'});" +
            "var " + "X" + museum.ID_ENTIDAD + "marker = new google.maps.Marker({" +
                "position: {lat: " + museum.LATITUD + ", lng: " + museum.LONGITUD + " },map: map});" +
            "X" + museum.ID_ENTIDAD + "marker.addListener('click', function() {" +
            "X" + museum.ID_ENTIDAD + "info.open(map," + "X" + museum.ID_ENTIDAD + "marker);" +
            "});")
        if (count % 5) == 0:
            listTotal = listTotal + ';'
    group = listTotal.split(';')[int(number) - 1]
    list = ''
    if (favoritos.count() % 5) == 0:
        pages = int(favoritos.count() / 5)
    else:
        pages = int(favoritos.count() / 5) + 1
    pagesRange = range(pages)
    if pages > 1:
        list = '<br>'
        if int(number) > 1:
            list = list + "<center><div class='pagination'><a href='/" + user + "/" + str(int(number) - 1) + "'>&laquo;</a>"
        else:
            list = list + "<center><div class='pagination'><a href='/" + user + "/" + str(number) + "'>&laquo;</a>"
        for page in pagesRange:
            if page == (int(number) - 1):
                list = list + "<a class='active' href='/" + user + "/" + str(page + 1) + "'>" + str(page + 1) + "</a>"
            else:
                list = list + "<a href='/" + user + "/" + str(page + 1) + "'>" +  str(page + 1) + "</a>"
        if int(number) == pages:
            list = list + "<a href='/" + user + "/" + str(number) + "'>&raquo;</a></div></center></br>"
        else:
            list = list + "<a href='/" + user + "/" + str(int(number) + 1) + "'>&raquo;</a></div></center></br>"
    list = list + "<div id='scroll'><center>"
    for item in group:
        list = list + item
    if (list == '' or list == "<div id='scroll'><center>") and user != 'AnonymousUser':
        list = "<center><a class='titulos'>" + 'Para que aparezcan museos en esta página, ' + user + ' tiene que añadirlos.' + '</a></center></br></br>'
    elif (list == '' or list == "<div id='scroll'><center>") and user == 'AnonymousUser':
        list = "<center><a class='titulos'>" + 'Para ver tu página personal, primero tienes que loguearte.' + '</a></center></br></br>'
    else:
        list = list + "<center><a class='info' href='/" + user + "/xml'>XML del usuario</a></center>"
    list = list + '</center></div>'
    users = User.objects.all()
    userList = ''
    for user in users:
        try:
            title = Titulo.objects.get(usuario = user.username)
            userList = userList + "<li><a href='/" + user.username + "'>" + title.titulo + ' - ' + user.username + "</a></li></br>"
        except Titulo.DoesNotExist:
            userList = userList + "<li><a href='/" + user.username + "'>Página de " + user.username + "</a></li></br>"
    style = ''
    if request.user.is_authenticated():
        login = 1
        try:
            color = Color.objects.get(usuario = request.user)
            color = color.color
        except Color.DoesNotExist:
            color = 'EEF4F8'
        try:
            letra = Letra.objects.get(usuario = request.user)
            letra = letra.letra
        except Letra.DoesNotExist:
            letra = '9'
        style = ("body{font-family: 'Helvetica', sans-serif;"
            "color: #444444;"
            "font-size: " + letra + "pt;"
            "background-color: #" + color + ";}")
    else:
        login = 0
    return HttpResponse(template.render(Context({'body': list, 'login': login, 'user': request.user, 'userList': userList, 'formato': style, 'markers': markers})))

def userXMLPage(request, user):
    template = get_template("personalXML.xml")
    favoriteList = []
    favoriteMuseums = Favorito.objects.filter(usuario = user)
    for favorite in favoriteMuseums:
        favoriteList = favoriteList + [favorite.museo]
    return HttpResponse(template.render(Context({'favoriteList': favoriteList, 'user': user})), content_type = "text/xml")

@csrf_exempt
def preferencesPage(request, user):
    template = get_template("preferencias.html")
    if request.method == 'POST':
        if 'color' in request.POST:
            try:
                color = Color.objects.get(usuario = user)
                color.color = request.POST['color']
            except Color.DoesNotExist:
                color = Color(usuario = user, color = request.POST['color'])
            color.save()
        elif 'tamaño' in request.POST:
            try:
                size = Letra.objects.get(usuario = user)
                size.letra = request.POST['tamaño']
            except Letra.DoesNotExist:
                size = Letra(usuario = user, letra = request.POST['tamaño'])
            size.save()
        elif 'título' in request.POST:
            try:
                title = Titulo.objects.get(usuario = user)
                title.titulo = request.POST['título']
            except Titulo.DoesNotExist:
                title = Titulo(usuario = user, titulo = request.POST['título'])
            title.save()
    style = ''
    if request.user.is_authenticated():
        login = 1
        try:
            color = Color.objects.get(usuario = request.user)
            color = color.color
        except Color.DoesNotExist:
            color = 'EEF4F8'
        try:
            letra = Letra.objects.get(usuario = request.user)
            letra = letra.letra
        except Letra.DoesNotExist:
            letra = '9'
        style = ("body{font-family: 'Helvetica', sans-serif;"
            "color: #444444;"
            "font-size: " + letra + "pt;"
            "background-color: #" + color + ";}")
    else:
        login = 0
    return HttpResponse(template.render(Context({'login': login, 'user': user, 'formato': style})))

def aboutPage(request):
    template = get_template('about.html')
    style = ''
    if request.user.is_authenticated():
        login = 1
        try:
            color = Color.objects.get(usuario = request.user)
            color = color.color
        except Color.DoesNotExist:
            color = 'EEF4F8'
        try:
            letra = Letra.objects.get(usuario = request.user)
            letra = letra.letra
        except Letra.DoesNotExist:
            letra = '9'
        style = ("body{font-family: 'Helvetica', sans-serif;"
            "color: #444444;"
            "font-size: " + letra + "pt;"
            "background-color: #" + color + ";}")
    else:
        login = 0
    # MOSTRAR LA INFORMACIÓN
    return HttpResponse(template.render(Context({'login': login, 'user': request.user, 'formato': style})))

def updateDB(request):
    #Museo.objects.all().delete()
    museos = parseXML('web/museos.xml')
    for museo in museos:
        try:
            distrito = Distrito.objects.get(nombre = museos[museo]['DISTRITO'])
        except Distrito.DoesNotExist:
            distrito = Distrito(nombre = museos[museo]['DISTRITO'])
            distrito.save()
    for museo in museos:
        try:
            A = museos[museo]['ID-ENTIDAD']
        except KeyError:
            A = 'No disponible'
        try:
            B = museos[museo]['NOMBRE']
        except KeyError:
            B = 'No disponible'
        try:
            C = museos[museo]['DESCRIPCION-ENTIDAD']
        except KeyError:
            C = 'No disponible'
        try:
            D = museos[museo]['HORARIO']
        except KeyError:
            D = 'No disponible'
        try:
            E = museos[museo]['TRANSPORTE']
        except KeyError:
            E = 'No disponible'
        try:
            F = museos[museo]['ACCESIBILIDAD']
        except KeyError:
            F = 'No disponible'
        try:
            G = museos[museo]['CONTENT-URL']
        except KeyError:
            G = 'No disponible'
        try:
            H = museos[museo]['NOMBRE-VIA']
        except KeyError:
            H = 'No disponible'
        try:
            I = museos[museo]['CLASE-VIAL']
        except KeyError:
            I = 'No disponible'
        try:
            J = museos[museo]['TIPO-NUM']
        except KeyError:
            J = 'No disponible'
        try:
            K = museos[museo]['NUM']
        except KeyError:
            K = 'No disponible'
        try:
            L = museos[museo]['LOCALIDAD']
        except KeyError:
            L = 'No disponible'
        try:
            M = museos[museo]['PROVINCIA']
        except KeyError:
            M = 'No disponible'
        try:
            N = museos[museo]['CODIGO-POSTAL']
        except KeyError:
            N = 'No disponible'
        try:
            Ñ = museos[museo]['BARRIO']
        except KeyError:
            Ñ = 'No disponible'
        try:
            O = Distrito.objects.get(nombre = museos[museo]['DISTRITO'])
        except KeyError:
            O = 'No disponible'
        try:
            P = museos[museo]['COORDENADA-X']
        except KeyError:
            P = 'No disponible'
        try:
            Q = museos[museo]['COORDENADA-Y']
        except KeyError:
            Q = 'No disponible'
        try:
            R = museos[museo]['LATITUD']
        except KeyError:
            R = 'No disponible'
        try:
            S = museos[museo]['LONGITUD']
        except KeyError:
            S = 'No disponible'
        try:
            T = museos[museo]['TELEFONO']
        except KeyError:
            T = 'No disponible'
        try:
            U = museos[museo]['FAX']
        except KeyError:
            U = 'No disponible'
        try:
            V = museos[museo]['EMAIL']
        except KeyError:
            V = 'No disponible'
        try:
            W = museos[museo]['TIPO']
        except KeyError:
            W = 'No disponible'
        try:
            viejoMuseo = Museo.objects.get(ID_ENTIDAD = A)
        except Museo.DoesNotExist:
            nuevoMuseo = Museo(
            ID_ENTIDAD = A,
            NOMBRE = B,
            DESCRIPCION_ENTIDAD = C,
            HORARIO = D,
            TRANSPORTE = E,
            ACCESIBILIDAD = F,
            CONTENT_URL = G,
            NOMBRE_VIA = H,
            CLASE_VIAL = I,
            TIPO_NUM = J,
            NUM = K,
            LOCALIDAD = L,
            PROVINCIA = M,
            CODIGO_POSTAL = N,
            BARRIO = Ñ,
            DISTRITO = O,
            COORDENADA_X = P,
            COORDENADA_Y = Q,
            LATITUD = R,
            LONGITUD = S,
            TELEFONO = T,
            FAX = U,
            EMAIL = V,
            TIPO = W)
            nuevoMuseo.save()
    return mainPage(request)
