var records = [];
var listCountries = [];
var listCrops = [];

var scouting;
var all;

var uniqueCountries;
var uniqueCrops;

var cropDimension;
var groupScoutingByCrops;
var groupInfestationByCrops;

var dateDimension;
let minDate;
let maxDate;
var groupCountScouting;

var stageDimension;
var groupStageInfestation;

var checkedInfestedDimension;
var checkedInfestedGroup;

var barChart;
var lineChart;
var pieChart;
var dataTable;
var africaChart;
var scatter;
var dataCount;

// const queryString = window.location.search;
function get(name){
   if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
      return decodeURIComponent(name[1]);
}
var cntry = get('country');

function onlyUnique(value, index, self) {
        return self.indexOf(value) === index;
    };

d3.json('/analytics/get_famews_data/'+cntry).then(function(data){

    function print_filter(filter) {
    var f=eval(filter);
    if (typeof(f.length) != "undefined") {}else{}
    if (typeof(f.top) != "undefined") {f=f.top(Infinity);}else{}
    if (typeof(f.dimension) != "undefined") {f=f.dimension(function(d) { return "";}).top(Infinity);}else{}
    console.log(filter+"("+f.length+") = "+JSON.stringify(f).replace("[","[\n\t").replace(/}\,/g,"},\n\t").replace("]","\n]"));
  }

    data.forEach(function (row) {
        // console.log(row);
        // let ld = row['data'];
        // listCountries.push(ld.country);
        if(isNaN(row.scoutingPercentageFAW)){
            return false;
        }else{
            listCrops.push(row.main_crop);
            records.push({
                id: row.id, date: row.date_of_survey, country: row.country,region: row.region, 'Crop': row.main_crop,
                'Stage': row.crop_stage, 'System': row.farming_system, 'Irrigation': row.irrigation,
                'Fertilizer': row.fertilizer, latitude: row.lat, longitude: row.long, 'Region': row.region,
                'Checked': row.scoutingPlantsChecked, 'FAW': row.scoutingPlantsFAW,'Prevalence': row.scoutingPercentageFAW,
                'd_source' : row.origin  })
            }});

    records.forEach(function (d) {
        let tempDate = new Date(d.date);
        d.date = tempDate;
        d.scoutingPlantsChecked = +d.scoutingPlantsChecked;
        d.scoutingPlantsFAW = +d.scoutingPlantsFAW;
        d.scoutingPercentageFAW = +d.scoutingPercentageFAW;
    });

    scouting = crossfilter(records);
    all = scouting.groupAll();

    //CROP related
    cropDimension = scouting.dimension(function (d) { return d.Crop; })
    groupScoutingByCrops = cropDimension.group().reduceCount(function (d) {
        return d.scoutingPlantsChecked;
    });

    groupInfestationByCrops = cropDimension.group().reduceSum(function (d) {
        return d.scoutingPlantsFAW/d.scoutingPlantsChecked;
    });

    //STAGE related
    stageDimension = scouting.dimension(function (d) {return d.Stage;});
    groupStageInfestation = stageDimension.group().reduceSum(function (d) {return d.Prevalence});

    uniqueCrops = listCrops.filter(onlyUnique);

    barChart = dc.barChart("#barchart")
        .width(1100)
        .height(250)
        .margins({top: 10, bottom: 30, right: 20, left: 40})
        .dimension(cropDimension)
        .group(groupScoutingByCrops)
        .x(d3.scaleBand().domain(uniqueCrops))
        .xUnits(dc.units.ordinal)
        .xAxisLabel("Crops")
        .yAxisLabel("Number of Scouting");

    dateDimension = scouting.dimension(function (d) {
        return new Date(
            d.date.getFullYear(),
            d.date.getMonth(),
            d.date.getDay())
    });

    // minDate = dateDimension.bottom(1)[0].date;
    minDate = new Date("January 1, 2019 00:00:00");
    maxDate = dateDimension.top(1)[0].date;

    groupCountScouting = dateDimension.group().reduceCount(function (d) {
        return d.scoutingPlantsChecked;
    });

    groupCountInfested = dateDimension.group().reduceCount(function (d) {
        return d.scoutingPlantsFAW;
    });

    lineChart = dc.lineChart("#linechart")
        .width(1100)
        .height(250)
        .dimension(dateDimension)
        .group(groupCountInfested,"Plants Infested")
        .stack(groupCountScouting, "Plants Checked")
        .yAxisLabel("Scouting")
        .renderHorizontalGridLines(true)
        .elasticY(true)
        .renderArea(true)
        .legend(dc.legend().x(900).y(15).itemHeight(12).gap(5))
        .x(d3.scaleTime().domain([minDate, maxDate]));

    lineChart.yAxis().ticks(5);
    lineChart.xAxis().ticks(12);

    checkedInfestedDimension = scouting.dimension(function (d) {return [d.Checked, d.FAW]; });
    checkedInfestedGroup = checkedInfestedDimension.group();

    scatter = dc.scatterPlot("#scatterplot")
        .width(450)
        .height(200)
        .margins({top: 10, bottom: 30, right: 20, left: 40})
        .dimension(checkedInfestedDimension)
        .group(checkedInfestedGroup)
        .symbolSize(10)
        .clipPadding(20)
        // .symbol(d3.shape().type(d3.symbolDiamond))
        .colorAccessor(function (d) {return d.key[1];})
        .colors(d3.scaleOrdinal(d3.schemeSet1)) //schemeDark2
        .x(d3.scaleLinear().domain([0, 100]));

    scatter.yAxis().ticks(5);

    pieChart = dc.pieChart("#piechart")
        .width(450)
        .height(200)
        .radius(90)
        .innerRadius(40)
        .drawPaths(true)
        .title(function (d) { return d.key + ': ' + d.value;})
        .colors(d3.scaleOrdinal(d3.schemeSet1))
        .transitionDuration(500)
        .dimension(cropDimension)
        .group(groupScoutingByCrops)
        .legend(dc.legend());

    dataCount = dc.dataCount(".dc-data-count")
        .dimension(scouting)
        .group(all)
        .html({
            some: '<strong>%filter-count</strong> selected out of <strong>%total-count</strong> records | ' +
                '<a href="\javascript:dc.filterAll(); dc.renderAll();\">Reset All</a>',
            all: 'All records selected. Please click on the graph to apply filters.'
        });

    dataTable = dc.dataTable("#table-records")
        .dimension(dateDimension)
        .showSections(true)
        .size(15)
        .section(function (d) { return d.Region;})
        .columns([{
            label: 'Date', format: function (d) {
                return d.date.getFullYear() + '/' +
                    d.date.getMonth() + '/' +
                    d.date.getDay()
            }
        },
            'Crop', 'Fertilizer', 'System', 'Irrigation', 'Stage', 'Checked', 'FAW', 'Prevalence','d_source'])
        .sortBy(function (d) {
            return d.date;
        })
        .order(d3.ascending)
        .on("renderlet", function (table) {
            table.selectAll('.dc-table-group').classed('info', true);
        });

    // var ndGroup = all.reduceSum(function (d) { return d.Checked;});
    var ndGroup = all.reduceCount();
    numberDisplay = dc.numberDisplay("#number-display")
        .group(ndGroup)
        .valueAccessor(function (d) {return d;});

    stageArrayGroup = stageDimension.group().reduce(
                function(i,d){ i.push(d.Prevalence); return i; },
                function(i,d){ i.splice((d.Prevalence),0); return i; },
                function(){ return []; }
            );
            // print_filter('stageArrayGroup');

    boxPlot = dc.boxPlot("#boxplotchart")
                .width(750)
                .height(300)
                .colors("#1f77b4")
                .margins({top:40,bottom:60,right:80,left:60})
                .dimension(stageDimension)
                .group(stageArrayGroup);

    bubble = dc.bubbleChart("#bubbleplotchart")
                .width(450)
                .height(200)
                .margins({top:40,bottom:60,right:80,left:60})
                .dimension(checkedInfestedDimension)
                .group(checkedInfestedGroup)
                .renderHorizontalGridLines(true)
                .renderVerticalGridLines(true)
                .legend(dc.legend().x(1200).y(5).itemHeight(12).gap(5))
                .clipPadding(70)
                .colorAccessor(function(d){ return d.key[0]; })
                .colors(colorbrewer.RdBu[6]).colorDomain([0,150])
                .keyAccessor(function(d){ return d.key[0]; })
                .valueAccessor(function(d){ return d.key[1]; })
                .radiusValueAccessor(function(d){ return d.key[1]; })
                .maxBubbleRelativeSize(0.04)
                .xAxisLabel("Plants Checked")
                .yAxisLabel("Infested")
                .title(function(d){ return 'x: '+d.key[0]+', y: '+d.key[1]+', val: '+d.value; })
                .r(d3.scale.linear().domain([1,75]))
                .y(d3.scale.linear().domain([0,100]))
                .x(d3.scale.linear().domain([0,250]));

    var select1 = new dc.SelectMenu('#select1');
    select1
        .dimension(cropDimension)
        .group(groupScoutingByCrops)
        .controlsUseVisibility(false);

    infestedDimension = scouting.dimension(function (d) {return d.country;});
    infestedGroup = infestedDimension.group();

    // Equivalent to reductio().avg(function(d) { return d.bar; }), which sets the .sum() and .count() values.
    var reducer = reductio()
        .count(true)
        .sum(function(d) { return d.FAW; })
        .avg(true);

    // Now it should track count, sum, and avg.
    reducer(infestedGroup);
    print_filter(infestedGroup.top(Infinity));


    dc.renderAll();
});