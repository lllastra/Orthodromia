// Загрузка данных из data.geojson
window.onload =init()
let geodataurl ="./map_project/data.geojson"
console.log(geodataurl) 

function init()
// Создание Карты
{
    let map = new ol.Map({
        view :new ol.View({
            center:[0.0,0.0],
            zoom :2,maxZoom:10,minZoom:2,
         
        }),

        target : "jsmap"
})

// Подключение шаблонов оформления карты

    const openStreetMapStandard=new ol.layer.Tile({ 
        source: new ol.source.OSM(),
        visible:false,
        title:"OSM_Standard"
    })


    const openStreetMapHumanitarian=new ol.layer.Tile({ 
        source:new ol.source.OSM({url: "https://{a-c}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"}),
        visible:true,
        title:"OSM_Humanitarian"
    })

    const StamenTerrain=new ol.layer.Tile({ 
        source:new ol.source.XYZ({url:"http://tile.stamen.com/terrain/{z}/{x}/{y}.jpg"}),
        visible:true,
        title:"Stamen_Terrain"
    })
    

   
    const baseLayerGroup =new ol.layer.Group({
        layers:[openStreetMapHumanitarian,openStreetMapStandard,StamenTerrain]
    })
    map.addLayer(baseLayerGroup)

//switcher для изменения шаблона оформления
    let baseLayer=document.querySelectorAll(".sidebar >input[type=radio]")
    
    for(let base of baseLayer)
    {
        console.log(base);
        base.addEventListener("change",() => {let select=(base.value);
            baseLayerGroup.getLayers().forEach(function(element,index,array){
                let bltitle=(element.get("title"))
                element.setVisible(bltitle===select);
            })
        })
    }
    const FillStyle = new ol.style.Fill({color :[84,118,255,1 ]})
    const StrokeStyle= new ol.style.Stroke({
        color:[46,45,45,1],
        width:2
    })
    const CircleStyle =new ol.style.Circle({
        fill : new ol.style.Fill({color:[249,49,5,1]}),
        radius :7,
        stroke :StrokeStyle
    })
    

    // Добавления векторного слоя с MultiLineString
    
    
    const RouteGeoJson = new ol.layer.VectorImage({
        source : new ol.source.Vector({
            //ввод данных их data.geojson
            url:
            "./static/data.geojson", 
            format : new ol.format.GeoJSON()
        }), 
        visible:true,
        title:"route",
        style: new ol.style.Style({
            fill:FillStyle,       
            stroke:StrokeStyle,   
            image :CircleStyle,   
            

        })
              

    })
    map.addLayer(RouteGeoJson)
    map.on("click",function(e){
        console.log(e.coordinate)
    })
}

