
$(document).ready(function() {
    $(window).scrollTop();
    $(window).scrollLeft();
});

    let view="";
    let zoom = "";
    let searchWidget="";
    let timestamp=new Date().toLocaleString().slice(0,17);;

async function getdatafromoutside(url){
    let response = await fetch(url);
    if (response.ok) {
     let txt = await response.json();
     let arr = [];
     for(let i=1; i< txt.length;i++){
         let temp = [];
         temp.push(txt[i][0].substring(10,txt[i][0].length-7));
         temp.push(parseFloat(txt[i][1]));
         temp.push(parseFloat(txt[i][2]));
         temp.push(parseFloat(txt[i][3]));
         arr.push(temp);
     }
    google.load("visualization", "1", {packages:["corechart"]});
    google.charts.setOnLoadCallback( function() { drawBasic(arr) });
    }else {
      alert("Ошибка HTTP: " + response.status);
    }
}

async function getdatafromoutsideSolar(url){
    let response = await fetch(url);
    if (response.ok) {
     let txt = await response.json();
     let arr = [];
     for(let i=1; i< txt.length;i++){
         let temp = [];
         temp.push(txt[i][0].substring(10,txt[i][0].length-7));
         temp.push(parseFloat(txt[i][1]));
         temp.push(parseFloat(txt[i][2]));
         arr.push(temp);
     }
    google.load("visualization", "1", {packages:["corechart"]});
    google.charts.setOnLoadCallback( function() { drawBasic2(arr) });
    }else {
      alert("Ошибка HTTP: " + response.status);
    }
}

async function getdatafromyd(url){
    //let url = 'http://gimslaw8.bget.ru/getdata.php?type=power&dt=2021-02-10-11:55';
    let response = await fetch(url);
    if (response.ok) {
        let txt = await response.json();
        let arr_ = [];
        if(txt!=='none'){
            for(let i = 0; i < txt.length;i++){
            let tmp = txt[i].split(',');
            tmp = tmp.toString();
            tmp = tmp.replace(/\s+/g, ' ').trim();
            let a = tmp.split(' ');
            let b = [];
            //console.log(a[1].slice(11,16));
            //b.push(a[0]+' '+a[1]);
            b.push(a[1].slice(11,16));
            b.push(parseFloat(a[2]));
             b.push(parseFloat(a[3]));
            arr_.push(b);
        }
        }

        google.load("visualization", "1", {packages:["corechart"]});
        google.charts.setOnLoadCallback( function() { drawBasic3(arr_) });
    }
    else {
      alert("Ошибка HTTP: " + response.status);
    }
}

async function getdata(url){
let response = await fetch(url);
if (response.ok) {
 let txt = await response.json();
 document.getElementById("NorthHPI").innerHTML = txt[0];
 document.getElementById("SouthHPI").innerHTML = txt[1];
 document.getElementById("Bx").innerHTML = txt[2];
 document.getElementById("By").innerHTML = txt[3];
 document.getElementById("Bz").innerHTML = txt[4];
 document.getElementById("Long").innerHTML = txt[5];
 document.getElementById("Lat").innerHTML = txt[6];
 document.getElementById("speed").innerHTML = txt[7];
  document.getElementById("density").innerHTML = txt[8];
} else {
  alert("Ошибка HTTP: " + response.status);
}
}

function drawBasic(arr) {
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'D');
      data.addColumn('number', 'Bx [nT]');
      data.addColumn('number', 'By [nT]');
      data.addColumn('number', 'Bz [nT]');
      data.addRows(arr);
      var options = {lineWidth: 1,
             colors: ['#CC9900','#FF6600','#CC0000'],
             bar: {groupWidth: '95%'},
             legend: {position: 'top',textStyle: {color: '#F5F5F7'}},
            // title: $('<div>&#32;&#32;&#32; REAL TIME CHARTS &#10;</div>').html(),//'&#32; REAL TIME CHARTS \n',
            textStyle:{color: '#FFF'},
            titleTextStyle : {color: 'white', fontSize: 9},
           backgroundColor: '#4a4a4a',
                hAxis: {
         baselineColor: '#ccc',
         gridlineColor: '#ccc',//textPosition: 'none',
                textStyle:{color: '#FFF'}},
                vAxis: {
                     baselineColor: '#ccc',
         gridlineColor: '#ccc',
                    gridlines: { count:5 },
                textStyle:{color: '#FFF'},
                },
                is3D: true,
              titleTextStyle: {
        //color: <string>,    // any HTML string color ('red', '#cc00cc')
       // fontName: <string>, // i.e. 'Times New Roman'
        fontSize: 12, // 12, 18 whatever you want (don't specify px)
        bold: true,
        // true or false
        //italic: <boolean>   // true of false
    },
    titlePosition: 'out'
      };
      var chart = new google.visualization.LineChart(document.getElementById('Bz_chart'));
      chart.draw(data, options);
    }
//
function drawBasic2(arr) {
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'D');
      data.addColumn('number', 'density [#/cc]');
      data.addColumn('number', 'speed [km/s]');
      data.addRows(arr);
      var options = {lineWidth: 1,
             colors: ['red','green'],
             bar: {groupWidth: '95%'},
             legend: {position: 'top',textStyle: {color: '#F5F5F7'}},
             //legend: 'none',
           // title: 'Density',
            textStyle:{color: '#FFF'},
            titleTextStyle : {color: 'white', fontSize: 9},
           backgroundColor: '#4a4a4a',
           series: {
          0: {targetAxisIndex: 0, axis: 'density'},
          1: {targetAxisIndex: 1, axis: 'speed'}
        },
        axes: {
          y: {
            density: {label: 'Temps (Ceffflsius)'},
            speed: {label: 'Daylight'}
          }
        },
        hAxis: {
         baselineColor: 'transparent',
         gridlineColor: '#ccc',//textPosition: 'none',
                textStyle:{color: '#FFF'}},
                vAxis: {
                              0: {label: 'Temps (Celsius)'},
          speed: {title: 'Daylight'},
                     baselineColor: '#ccc',
         gridlineColor: '#ccc',
                    gridlines: { count:3 },
                textStyle:{color: '#FFF'},
                },

                is3D: true
      };
      var chart = new google.visualization.LineChart(document.getElementById('Solar_chart'));
      chart.draw(data, options);
}

function drawBasic3(arr) {
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'D');
      data.addColumn('number', 'NorthHPI [GW]');
      data.addColumn('number', 'SouthHPI [GW]');
      data.addRows(arr);
      var options = {lineWidth: 1,
             colors: ['blue','red'],
             bar: {groupWidth: '95%'},
            legend: {position: 'top',textStyle: {color: '#F5F5F7'}},
             //legend: 'none',
            //title: 'HPI',
            textStyle:{color: '#FFF'},
            titleTextStyle : {color: 'white', fontSize: 9},
           backgroundColor: '#4a4a4a',
                hAxis: {
         baselineColor: '#ccc',
         gridlineColor: '#ccc',//textPosition: 'none',
                textStyle:{color: '#FFF'}},
                vAxis: {
                     baselineColor: '#ccc',
         gridlineColor: '#ccc',
                    gridlines: { count:5 },
                textStyle:{color: '#FFF'},
                },
                is3D: true};
      var chart = new google.visualization.LineChart(document.getElementById('HPI_chart'));
      chart.draw(data, options);
}

async function getdatafromsand(url){
    let response = await fetch(url);
    if (response.ok) {
        let txt = await response.json();
        let arr = [];
        var date = new Date();
        var now_utc =  Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(),
         date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds());
        var tutc=moment.utc(date);
        $(function () {
            $('#datetimepicker1').datetimepicker({
                        locale: 'ru',
                        enabledDates: txt,
                        defaultDate: tutc,
                        format: 'YYYY-MM-DD HH:mm',
                        format: 'L',
                        ignoreReadonly: true
                    });
            });

        $(function () {
            $('#datetimepicker2').datetimepicker({
                locale: 'ru',
                defaultDate: tutc,
                format: 'HH:mm',
                format: 'LT',
                ignoreReadonly: true
            });
        });

        $('#datetimepicker1').on('change.datetimepicker', function(e) {

        });
   }
    else {
      alert("Ошибка HTTP: " + response.status);
    }
}

getdatafromsand('/sand');
getdatafromoutside('https://services.swpc.noaa.gov/products/solar-wind/mag-6-hour.json');
getdatafromoutsideSolar('https://services.swpc.noaa.gov/products/solar-wind/plasma-6-hour.json');
var x = foo();
getdatafromyd('/getdata?type=power&dt='+x);

getdata('/data?tmstp='+x);
drawglobe("/test?tmstp="+x,'o');


function drawglobe(url1,ow){

var activeWidget = null;
const url =  "/static/files/aurora_ext.csv";
require(["esri/Map",
"esri/views/SceneView",
"esri/layers/CSVLayer",
"esri/layers/GeoJSONLayer",
"esri/renderers/UniqueValueRenderer",
"esri/widgets/Legend",
"esri/core/watchUtils",
"esri/TimeExtent",
"esri/widgets/Expand",
"esri/widgets/BasemapGallery",
"esri/widgets/Search",
"esri/widgets/support/DatePicker",
"esri/widgets/Zoom","esri/widgets/AreaMeasurement3D",
"esri/widgets/DirectLineMeasurement3D"],
function(Map, SceneView, CSVLayer, GeoJSONLayer, UniqueValueRenderer,Legend,watchUtils,TimeExtent,Expand,BasemapGallery,Search,DatePicker,Zoom,AreaMeasurement3D, DirectLineMeasurement3D) {
    const template = {
    title: "",
    content: "Intensivity {category} latitude {latitude} longitude {longitude}."
    };

    const map = new Map({
        basemap: "hybrid",
        ground: "world-elevation",
        maxZoom: 5,
        effectiveMaxZoom:5,
        effectiveMinZoom:5,
        minZoom: 5,
        maxScale: 5000000
    });
    var renderer;
    var popupTemplate;
    if(ow=='o'){
    renderer = {
    type: "unique-value",
    defaultSymbol: { type: "line-3d",
    symbolLayers: [{
        type: "line",
        outline: { color: [255, 84, 54, 0.6], size: 10, width: 2},
        join: "round"
    }]},

    visualVariables: [
        {
            type: "size",
            field: "title",
            stops: [
                { value: 4, size: 1},
                { value: 100, size: 1}
            ]
        },
        {
            type: "color",
            field: "title",
            legendOptions: {
            title: "Prob., %"
            },
            //#5813fc,#1cc2fd,#7dfd94,#f5c926,#ff2b18
            stops: [
                {
                    value: 5,
                    color: "#5813fc",
                    label: "0",
                },
                {
                    value: 10,
                    color: "#1cc2fd",
                },
                {
                    value: 20,
                    color: "#7dfd94",
                },
                {
                    value: 40,
                    color: "#f5c926",
                },
                {
                    value: 100,
                    color: "#ff2b18",
                    label: " 100",
                }
            ]

        }
    ]
    };
         popupTemplate = {
        title: "Aurora Probability",
        content: "{title}"
    };
}
else{
    var renderer = {
    type: "unique-value",
    defaultSymbol: { type: "line-3d",
    symbolLayers: [{
        type: "line",
        outline: { color: [255, 84, 54, 0.6], size: 10, width: 2},
        join: "round"
    }]},

    visualVariables: [
        {
            type: "size",
            field: "title",
            stops: [
                { value: 4, size: 1},
                { value: 100, size: 1}
            ]
        },
        {
            type: "color",
            field: "title",
            legendOptions: {
            title: "kV"
            },
            //#5813fc,#1cc2fd,#7dfd94,#f5c926,#ff2b18
            stops: [
                {
                    value: -60,
                    color: "#5813fc",
                    label: "-100",
                },
                {
                    value: -30,
                    color: "#1cc2fd",
                },
                {
                    value: 30,
                    color: "#7dfd94",
                },
                {
                    value: 60,
                    color: "#f5c926",
                },
                {
                    value: 100,
                    color: "#ff2b18",
                    label: " 100",
                }
            ]

        }
    ]
    };
    popupTemplate = {
        title: "EPOT [kV]",
        content: "{title}"
    };
}


    const geoJSONLayer = new GeoJSONLayer({
        url: url1,
        popupEnabled: true,
        outFields: ["title"],
        popupTemplate: popupTemplate,
        renderer: renderer,
        highlightOptions: {
            haloOpacity: 0.9,
            fillOpacity: 0.2
        },
        elevationInfo:{
            mode:'relative-to-scene'
        }
    });
    geoJSONLayer.opacity = 1;

    map.add(geoJSONLayer);

    view = new SceneView({
    container: "viewDiv",
    map: map,
    scale: 60000000,
    minScale:30000000,
    center: [-101.17, 21.78],
    qualityProfile: "high",
    alphaCompositingEnabled: false,
    environment: {
        lighting: {
            cameraTrackingEnabled: false
        },
        waterReflectionEnabled: true,
        starsEnabled: true,
        atmosphereEnabled: true,
        atmosphere: {
            quality: "high"
        },
    }
    });

    var legend = new Legend({
    view: view,
    container: leg,
    title: "Aurora Probability",
    layerInfos: [{
        layer: geoJSONLayer
    }]
    });

    view.ui.components =[""];

    view.ui.add(legend, "top-right");
    view.popup.dockOptions.buttonEnabled = false;
    view.popup.viewModel.actions = [];

     document.getElementById("zoom").innerHTML="";
     document.getElementById("search").innerHTML="";
     document.getElementById("leg").innerHTML="";
     searchWidget= "";
     zoom = new Zoom({   view: view,   layout: "horizontal", container: "zoom"});
     searchWidget = new Search({
          view: view,
          container: search
     });

        document
          .getElementById("areaButton")
          .addEventListener("click", function() {
            setActiveWidget(null);
            if (!this.classList.contains("activee")) {
              setActiveWidget("area");
            } else {
              setActiveButton(null);
            }
          });

                  document
          .getElementById("distanceButton")
          .addEventListener("click", function() {
            setActiveWidget(null);
            if (!this.classList.contains("activee")) {
              setActiveWidget("distance");
            } else {
              setActiveButton(null);
            }
          });

    view.when(function() {
        setTimeout(function(){
        }, 5010);
        const camera = view.camera.clone();
        camera.position.latitude = 90;
        view.goTo(camera, { duration:5000,});
        document.getElementById("loader1").style.visibility= 'hidden';
    });

        function setActiveWidget(type) {
          switch (type) {
            case "distance":
              activeWidget = new DirectLineMeasurement3D({
                view: view
              });

              // skip the initial 'new measurement' button
              activeWidget.viewModel.newMeasurement();

              view.ui.add(activeWidget, "middle");
              setActiveButton(document.getElementById("distanceButton"));
              break;
            case "area":
              activeWidget = new AreaMeasurement3D({
                view: view
              });

              // skip the initial 'new measurement' button
              activeWidget.viewModel.newMeasurement();

              view.ui.add(activeWidget, "middle");
              setActiveButton(document.getElementById("areaButton"));
              break;
            case null:
              if (activeWidget) {
                view.ui.remove(activeWidget);
                activeWidget.destroy();
                activeWidget = null;
              }
              break;
          }
        }

        ///

document
          .getElementById("Home")
          .addEventListener("click", function() {
 //

         const camera = view.camera.clone();
        camera.position.latitude = 90;
        camera.position.lontitude = 0;camera.position.z=17701447.44765657;
        view.goTo(camera, { duration:5000,});
          });

document
          .getElementById("Northern Hemisphere")
          .addEventListener("click", function() {
 //

         const camera = view.camera.clone();
        camera.position.latitude = 90;
        camera.position.lontitude = 0;camera.position.z=17701447.44765657;
        view.goTo(camera, { duration:5000,});
          });

          document
          .getElementById("Southern Hemisphere")
          .addEventListener("click", function() {
 //
         const camera = view.camera.clone();//alert(camera.position.z);
        camera.position.latitude = -90;
        camera.position.lontitude = 0;
        camera.position.z=17701447.44765657;
        view.goTo(camera, { duration:5000,});
          });
        //
        /*
            var coordsWidget = document.createElement("div");
      coordsWidget.id = "coordsWidget";
      coordsWidget.className = "esri-widget esri-component";
      coordsWidget.style.padding = "5px 5px 5px";
      coordsWidget.style.background = "rgba(56,56,56,0.6)";
      coordsWidget.style.color = "rgba(255,255,255, 0.6)";
      view.ui.add(coordsWidget, "top-right");*/
       // view.ui.add("topbar", "top-right");

              function showCoordinates(pt) {
          if(pt!=null) {
        var coords = "GeoLat(N) / GeoLon(E):  " + pt.latitude.toFixed(3) + " / " + pt.longitude.toFixed(3) +
            " | Scale 1:" + Math.round(view.scale * 1) / 1;
        coordsWidget.innerHTML = coords;
          }
      }


      view.watch(["stationary"], function() {
        showCoordinates(view.center);
      });


      view.on(["pointer-down","pointer-move"], function(evt) {
        showCoordinates(view.toMap({ x: evt.x, y: evt.y }));
      });
        //

});
}
function foo(){
    var date_to_parse = $('#datetimepicker1').datetimepicker('viewDate');
    var date = moment(date_to_parse).format('YYYY-MM-DD');
    var time_to_parse = $('#datetimepicker2').datetimepicker('viewDate');
    var time = moment.utc(time_to_parse).format('HH:mm');
    return date+'-'+time;
}

function refresh(){
    document.getElementById("loader1").style.visibility= 'visible';
    var xx = foo();
    var formats = ["YYYY-MM-DD-HH:mm"];
    //var check = moment(xx,formats, true).isValid();
   // alert(check);
    if($('#ow').prop('checked')!=true){
     //   document.getElementById("viewDiv").innerHTML="";
       // document.getElementById("zoom").innerHTML="";
         //document.getElementById("search").innerHTML="";
        drawglobe("/weimer?tmstp="+x,'w');
    }
    else{
    drawglobe("/test?tmstp="+xx,'o');
    }
    getdata('/data?tmstp='+xx);
}
