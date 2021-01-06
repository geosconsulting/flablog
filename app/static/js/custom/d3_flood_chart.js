d3.json("/analytics/get_flood_data", function(error,data){

        function print_filter(filter) {
            var f=eval(filter);
            if (typeof(f.length) != "undefined") {}else{}
            if (typeof(f.top) != "undefined") {f=f.top(Infinity);}else{}
            if (typeof(f.dimension) != "undefined") {f=f.dimension(function(d) { return "";}).top(Infinity);}else{}
            console.log(filter+"("+f.length+") = "+JSON.stringify(f).replace("[","[\n\t").replace(/}\,/g,"},\n\t").replace("]","\n]"));
        }

        var facts = crossfilter(data);

        var scatterDimension = facts.dimension(function(d){ return [d.rp25,d.rp50]; });
        //print_filter('scatterDimension');
        var scatterGroup = scatterDimension.group();
        //print_filter('scatterGroup');

        //Dimension
        var countryDimension = facts.dimension(function(d){return d.adm0_name;});
        //countryDimension.filterFunction(function(d){ return d.rp25 > 250000; });
        //print_filter('countryDimension');

        //Count number adm2 in each country
        var countryGroup = countryDimension.group().reduceCount();
        //print_filter('countryGroup');

        //Sum pop at risk in each country for RP25
        var peopleTotalRP25 = countryDimension.group().reduceSum(function (d){ return d.rp25;});
        //print_filter('peopleTotalRP25');

        //Sum pop at risk in each country for RP50
        var peopleTotalRP50 = countryDimension.group().reduceSum(function (d){ return d.rp50;});
        //print_filter('peopleTotalRP50');

        countries = [];
        Object.values(peopleTotalRP25.top(Infinity)).forEach(item => {
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
                    .group(peopleTotalRP25)
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

        all = facts.groupAll();

        var peopleRP25Group = facts.groupAll().reduceSum(function(d){ return d.rp25;});
        //var peopleRP25Group = countryDimension.groupAll().reduceSum(function(d){return d.rp25;}); //.value();

        var numRecords25 = dc.numberDisplay("#rp25")
                            .valueAccessor(function(d){ return d;})
                            .group(peopleRP25Group);

        // var peopleRP50Group = all.reduceSum(function(d){ return d.rp50; });
        var peopleRP50Group = facts.groupAll().reduceSum(function(d){ return d.rp50;});
        var numRecords50 = dc.numberDisplay("#rp50")
                              .valueAccessor(function(d){return d;})
                              .group(peopleRP50Group);

        var peopleRP100Group = facts.groupAll().reduceSum(function(d){ return d.rp100; });
        var numRecords100 = dc.numberDisplay("#rp100")
                             .valueAccessor(function(d){return d;})
                             .group(peopleRP100Group);

        var peopleRP200Group = facts.groupAll().reduceSum(function(d){ return d.rp200; });
        var numRecords200 = dc.numberDisplay("#rp200")
                            .valueAccessor(function(d){return d;})
                            .group(peopleRP200Group);

        var peopleRP500Group = facts.groupAll().reduceSum(function(d){ return d.rp500; });
        var numRecords500 = dc.numberDisplay("#rp500")
                            .valueAccessor(function(d){return d;})
                            .group(peopleRP500Group);

        var peopleRP1000Group = facts.groupAll().reduceSum(function(d){ return d.rp1000; });
        var numRecords1000 = dc.numberDisplay("#rp1000")
                            .valueAccessor(function(d){return d;})
                            .group(peopleRP1000Group);


        dc.renderAll();
    });