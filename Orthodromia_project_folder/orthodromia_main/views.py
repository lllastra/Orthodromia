import json
from django.shortcuts import render
from shapely import from_wkt
from .forms import GetDataForm, DropDownList
from pyproj import Geod, Proj, transform
from functools import partial
from shapely import from_wkt, points, get_coordinates, LineString
# Create your views here.

def main(request):
    # Инициализация форм для вызова в index.html
    form = GetDataForm (request.POST or None)
    form1 = DropDownList (request.POST or None)
    
    if request.method == "POST" and form.is_valid() and form1.is_valid() :

        # Сбор данных и их упрощение
        data  = form.cleaned_data
        sk = form1.cleaned_data
    
        Point1 =from_wkt(data["p1"].replace('"', ''))
        Point2 =from_wkt(data["p2"].replace('"', ''))

        # Данные о системах координат для transform 
        P4284 = Proj(init='epsg:4284')
        P4326 = Proj(init='epsg:4326')

        # Перевод данных из СК-42 в WGS84 если ввод был в СК-42
        if sk == {'SK': '1'}:

            x1,y1 = transform(P4284,P4326,  Point1.x, Point1.y)
            x2,y2 = transform(P4284,P4326,  Point2.x, Point2.y)
        else:
            x1,y1= Point1.x, Point1.y
            x2, y2 =Point2.x, Point2.y

        # Инициализация переменных для создание дополнительных точек с помощью geod.npts
        lon1, lat1 = x1,y1
        lon2, lat2 = x2,y2
        n_extra_points = data["NumberOfPoints"]

        # Создание дополнительных точек

        geoid = Geod(ellps="WGS84")
        extra_points = geoid.npts(lon1, lat1, lon2, lat2, n_extra_points)


        # Инициализация переменных и настройка transformer для перевода координат полученных точек 
        # обратно в Ск-42 из WGS84 для отображения в окне результатов

        all_points = points(extra_points)
        proj_4284 = Proj(init="epsg:4284")
        proj_4326 = Proj(init="epsg:4326")
        transformer = partial(transform, proj_4326, proj_4284)



        list_of_final_points = []
        List_of_coordinates_of_final_points=[]


        # Перевод координат полученных точек обратно в Ск-42 из WGS84 если для вводна был выбран СК-43
        # Сбор полученных точек в лист

        if sk == {'SK': '1'}:

            if n_extra_points != 0:
                i = 0
                while i < n_extra_points:
                        list_of_final_points.append(
                                transformer(get_coordinates(all_points)[i][0], get_coordinates(all_points)[i][1]))
                        i += 1
        else:
            if n_extra_points != 0:
                i = 0
                while i < n_extra_points:
                        list_of_final_points.append((get_coordinates(all_points)[i][0], get_coordinates(all_points)[i][1]))
                        i += 1
        

        # Добавление первой и последней точки введенных пользователем

        list_of_final_points.insert(0,(Point1.x,Point1.y))
        list_of_final_points.append((Point2.x,Point2.y))


        # Получение координат для простроения MultiLineString 

        if n_extra_points!= 0:
            i=0
            while i<n_extra_points-1:
                List_of_coordinates_of_final_points.append((get_coordinates(all_points)[i].tolist(), get_coordinates(all_points)[i+1].tolist()))
                i += 1
       

        # Создание Line для вывода в окне резуьтата

        Line = LineString(list_of_final_points)

  
    
        # Построение MultiLineString

        multy_line_string={
              "type":"MultiLineString"
              ,"coordinates":[]
              }
        multy_line_string["coordinates"]= List_of_coordinates_of_final_points


        # Запись данных в data.geojson для отображения MultiLineString в main.js

        geofile='static\data.geojson'
        with open(geofile, 'w') as outfile:
            json.dump(multy_line_string, outfile)
        
        # поиск середины MultiLineString для зума к линии на карте
        # centroid = ((x1+x2) / 2.0, (y1+y2) / 2.0)

    
    return render(request,"index.html",locals())
