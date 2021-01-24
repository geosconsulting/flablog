var Stadia_AlidadeSmooth = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {
	maxZoom: 20,
	attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
});

var myGeoJSONPath = '../../static/data/africa-asia.geo.json';

var myCustomStyle = {
        stroke: false,
        fill: true,
        fillColor: '#00f',
        fillOpacity: 0.2
}

$.getJSON(myGeoJSONPath,function(data){
       var map = L.map('map').setView([5.0, 55.0], 3);
       Stadia_AlidadeSmooth.addTo(map);

       L.geoJson(data, {
            clickable: false,
            style: myCustomStyle
         }).addTo(map);
})
