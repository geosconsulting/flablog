d3.json("/analytics/get_flood_data", function(error,data){

        function print_filter(filter) {
            var f=eval(filter);
            if (typeof(f.length) != "undefined") {}else{}
            if (typeof(f.top) != "undefined") {f=f.top(Infinity);}else{}
            if (typeof(f.dimension) != "undefined") {f=f.dimension(function(d) { return "";}).top(Infinity);}else{}
            console.log(filter+"("+f.length+") = "+JSON.stringify(f).replace("[","[\n\t").replace(/}\,/g,"},\n\t").replace("]","\n]"));
        }

        var facts = crossfilter(data);
        //print_filter('facts');

        //Dimension
        var countryDimension = facts.dimension(function(d){return d.adm0_name;});
        //countryDimension.filterFunction(function(d){ return d.rp25 > 250000; });
        print_filter(countryDimension);

        var peopleTotal = countryDimension.group().reduceSum(function (d){ return d.rp25;});
        //print_filter(peopleTotal);

        countries = [];
        Object.values(peopleTotal.top(Infinity)).forEach(item => {
                countries.push(item.key);
            });

        barChartPeople = dc.barChart("#barchart")
                    .width(1100)
                    .height(500)
                    .margins({top:10,bottom:175,right:10,left:80})
                    .centerBar(false)
                    .barPadding(0.1)
                    .outerPadding(0.2)
                    .dimension(countryDimension)
                    .group(peopleTotal)
                    .x(d3.scale.ordinal().domain(countries))
                    .xUnits(dc.units.ordinal)
                    .xAxisLabel("Countries")
                    .yAxisLabel("Number of People")
                    .elasticX(true);

        dataTable = dc.dataTable("#tablechart")
                    .width(1360)
                    .height(300)
                    .dimension(countryDimension)
                    .showGroups(true)
                    .size(10)
                    .group(function (d) {return d.adm0_name;})
                    .columns([
                        'adm1_name','adm2_name',
                        'rp25','rp50','rp100','rp200','rp500','rp1000'])
                    .sortBy(function(d){ return d.type; })
                    .order(d3.ascending);

        dc.renderAll();
    });