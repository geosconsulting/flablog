// d3.json("/analytics_dir/get_flood_data", function(error,data){
d3.json("/api/floods_sparc", function(error,data){

        function print_filter(filter) {
            var f=eval(filter);
            if (typeof(f.length) != "undefined") {}else{}
            if (typeof(f.top) != "undefined") {f=f.top(Infinity);}else{}
            if (typeof(f.dimension) != "undefined") {f=f.dimension(function(d) { return "";}).top(Infinity);}else{}
            console.log(filter+"("+f.length+") = "+JSON.stringify(f).replace("[","[\n\t").replace(/}\,/g,"},\n\t").replace("]","\n]"));
        }

        data.forEach(function(d){
            d.adm0_code = +d.adm0_code;
            d.rp25 = +d.rp25;
            d.rp50 = +d.rp50;
            d.rp100 = +d.rp100;
            d.rp200 = +d.rp200;
            d.rp500 = +d.rp500;
            d.rp1000 = +d.rp1000;
        });

        console.log(data);

        var facts = crossfilter(data);

        //Dimension
        var countryDimension = facts.dimension(function(d){return d.adm0_name;});
        //countryDimension.filterFunction(function(d){ return d.rp25 > 250000; });

        //Count number adm2 in each country
        var countryGroup = countryDimension.group().reduceCount();

        //Sum pop at risk in each country for RP25
        var peopleTotalRP25 = countryDimension.group().reduceSum(function (d){ return d.rp25;});

        //Sum pop at risk in each country for RP50
        var peopleTotalRP50 = countryDimension.group().reduceSum(function (d){ return d.rp50;});

        countries = [];
        Object.values(peopleTotalRP25.top(Infinity)).forEach(item => {
                countries.push(item.key);
            });

        barChartPeople = dc.barChart("#barchart")
                    .width(1100)
                    .height(500)
                    .margins({top:50,bottom:175,right:10,left:80})
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

        numRecords25 = dc.numberDisplay("#rp25")
                            .valueAccessor(function(d){ return d;})
                            .group(peopleRP25Group);

        // var peopleRP50Group = all.reduceSum(function(d){ return d.rp50; });
        peopleRP50Group = facts.groupAll().reduceSum(function(d){ return d.rp50;});
        numRecords50 = dc.numberDisplay("#rp50")
                              .valueAccessor(function(d){return d;})
                              .group(peopleRP50Group);

        peopleRP100Group = facts.groupAll().reduceSum(function(d){ return d.rp100; });
        numRecords100 = dc.numberDisplay("#rp100")
                             .valueAccessor(function(d){return d;})
                             .group(peopleRP100Group);

        peopleRP200Group = facts.groupAll().reduceSum(function(d){ return d.rp200; });
        numRecords200 = dc.numberDisplay("#rp200")
                            .valueAccessor(function(d){return d;})
                            .group(peopleRP200Group);

        peopleRP500Group = facts.groupAll().reduceSum(function(d){ return d.rp500; });
        numRecords500 = dc.numberDisplay("#rp500")
                            .valueAccessor(function(d){return d;})
                            .group(peopleRP500Group);

        peopleRP1000Group = facts.groupAll().reduceSum(function(d){ return d.rp1000; });
        numRecords1000 = dc.numberDisplay("#rp1000")
                            .valueAccessor(function(d){return d;})
                            .group(peopleRP1000Group);

        var countryDimensionTest = facts.dimension(function(d){return d.iso3;});
        //var filtered = countryDimensionTest.filter("DJI");

        // console.log(countryDimensionTest.groupAll().value());
        // console.log(facts.groupAll().value());

        var provinceOneCountryAllRPSum = facts.groupAll().reduce(
            function(i,d){ i.push(d.rp25 + d.rp50 + d.rp100 + d.rp200 + d.rp500 + d.rp1000); return i; },
            function(i){ return i;},
            function(){ return [];}
            ).value();
        print_filter('provinceOneCountryAllRPSum');

        var provinceAllCountriesAllRP = countryDimensionTest.group().reduce(
            function(i,d){ i.push(d.rp25 + d.rp50 + d.rp100 + d.rp200 + d.rp500 + d.rp1000); return i; },
            function(i){ return i;},
            function(){ return [];}
            );
        //print_filter('provinceAllCountriesAllRP');

        var countryGroupAllRP = facts.groupAll().reduce(
            function(i,d){ return  d.iso3 = { 'rp_pop': [pop25 += d.rp25, pop50 += d.rp50,
                                       pop100 += d.rp100,pop200 += d.rp200,
                                       pop500 += d.rp500,pop1000 += d.rp1000]}},
            function(i){ return i;},
            function(){ return iso3 = {'rp_pop': [pop25=0, pop50=0, pop100=0, pop200=0, pop500=0, pop1000=0]}}
            ).value();
        print_filter(countryGroupAllRP);

        // var countryGroupAllRP11 = countryDimensionTest.group().reduce(
        //     function(i,d){ return [pop25 += d.rp25,
        //                                pop50 += d.rp50,
        //                                pop100 += d.rp100,
        //                                pop200 += d.rp200,
        //                                pop500 += d.rp500,
        //                                pop1000 += d.rp1000]},
        //     function(i){ return i;},
        //     function(){ return {iso3:[pop25=0,
        //                              pop50=0,
        //                              pop100=0,
        //                              pop200=0,
        //                              pop500=0,
        //                              pop1000=0]}}
        //     );
        // print_filter(countryGroupAllRP11);

        dc.renderAll();
    });