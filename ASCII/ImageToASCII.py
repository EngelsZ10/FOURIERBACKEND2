from django.http import FileResponse
import numpy as np
import base64
import cv2

def scaling(img, inter, maximo):
    #Obtener dimenciones nuevas
    if img.shape[1]>img.shape[0]: # width>height
        width = maximo
        height = round((maximo)*(img.shape[0]/img.shape[1]))
        print((maximo)*(img.shape[0]/img.shape[1]))
    else: # width<height
        height =maximo 
        width = round((maximo)*(img.shape[1]/img.shape[0]))
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = inter)
    return resized

def filter(img, maximo, i):
    #imagen pasa de ser  3D (rgb) a 2D (escala de grises)
    img_grey = cv2.cvtColor(img, code=cv2.COLOR_BGR2GRAY)
    #Aplica gausian blurr para mejorar la calidad de los objetos centrales (enfoqua mejor)
    img_blur = cv2.GaussianBlur(img_grey, (3,3), 0)
    #Cambia el rango de valores de los pixeles a entre 0 y 12 la matriz img_blur tine nxm valores de entre 0 y 12
    img_norm = cv2.normalize(img_blur, None, alpha=0, beta=12, norm_type=cv2.NORM_MINMAX)
    #Lista de metodos de interpolación para escalar imagen
    scaleFun = [cv2.INTER_LINEAR,  cv2.INTER_CUBIC, cv2.INTER_LANCZOS4]
    # Regresa la imagen escalada con la función de interpolación escogida y el lado más grande vale maximo matiene propociones
    # Regresa la matriz img_norm escalada a nxm donde el mayor de n y m vale maximo
    return scaling(img_norm, scaleFun[i], maximo)

#mapea un numero a un character de más claro a más oscuro
switch = np.vectorize(lambda i:{
    0:"..", 1:",,", 2:";;", 
    3:"==", 4:"!!", 5:"**", 
    6:"##", 7:"$$", 8:"@@", 
    9: "\u2591\u2591",10: "\u2592\u2592", 
    11:"\u2593\u2593", 12:'\u25A0\u25A0'}[i])

#mapea un numero a un character de más oscuro a más claro
switchinv = np.vectorize(lambda i :{
    12:"..", 11:",,", 10:";;", 
    9:"==",  8:"!!", 7:"**", 
    6:"##", 5:"$$", 4:"@@", 
    3:"\u2591\u2591", 2:"\u2592\u2592", 
    1:"\u2593\u2593", 0:'\u25A0\u25A0'}[i])

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

    
def getAscii(uri, inverso, max, filtro):
    image = data_uri_to_cv2_img(uri)
    imageFiltered = filter(image, max, filtro)
    matrizStr = switchinv(imageFiltered) if inverso else switch(imageFiltered)
    lines = []
    for line in matrizStr:
        lines.append("".join(line))
    return "<br>".join(lines)
