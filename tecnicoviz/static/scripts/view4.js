/*global d3, dispatcher, disableEvents, enableEvents, mouseOver, selectMouseOut, highlight, getFilteredAcronym, mouseOut, Table, drawPill, removeDuplicate, getSelected, clicked, touchDevice, $*/

var BarChart = (function () {
    "use strict";
    //attributes
    
    // Private Methods
    
    // Public Methods
    return {
        
        tooltip: function (d) {
            var posX = d3.event.pageX + 80 >= $(window).innerWidth() ? d3.event.pageX - 90 : d3.event.pageX + 10,
                acronym = Table.getAggregation() + "Acronym",
                secondColumn = Table.getAggregation() === "degree" ? "courseAcronym" : "degreeAcronym";
            d3.select(".tooltip")
                .style("left", posX + "px")
                .style("top", $(window).scrollTop() + d3.event.clientY + 10 + "px")
                .style("visibility", "visible")
                .html(d[acronym] + " " + d[secondColumn] + "<br>" + "Year: " + d.year + "<br>" + "Term: " + d.term + "<br>" + "Teacher Quc" + ": " + d.teacherScore);
        },
        
        mouseOver: function (d, element) {
            d3.selectAll(element)
                .style("stroke-width", "2px")
                .style("stroke", "black");
        },
    
        mouseOut: function (d, element) {
            d3.selectAll(element)
                .style("stroke-width", "1px")
                .style("stroke", "rgb(200, 200, 200)");
        },
        
        draw: function (dataRequested, args) {
            var svgHeight,
                width,
                xAxis,
                barchart,
                barContainer,
                yAxis,
                transitionNumber,
                colorDomain = [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
                colors = ['#d73027', '#fc8d59', '#fee08b', '#ffffbf', '#d9ef8b', '#91cf60', '#1a9850'],
                colorScale = d3.scaleQuantile()
                                .domain(colorDomain)
                                .range(colors),
                nestData = d3.nest()
                    .key(function (d) {
                        return d.name;
                    }).entries(dataRequested[0].filter(function (d) { if (d.teacherScore || d.teacherScore === 0) { return d; } })),
                xAxisOrientation,
                yAxisOrientation,
                chart,
                i,
                j,
                line,
                tr,
                currentRow = d3.select("#" + args[0] + '\\,' + args[1] + ".row").node(),
                currentLine;
            if (nestData.length === 0) {
                return;
            }
            if (d3.select(currentRow).classed("subExpanded")) {
                d3.select("#" + args[0] + '\\,' + args[1] + ".barRow").transition().duration(600).style("opacity", 0).remove();
                d3.select(currentRow).classed("subExpanded", false);
                return;
            } else {
                d3.select(currentRow).classed("subExpanded", true);
            }
            tr = d3.select(currentRow.parentNode.insertBefore(document.createElement("tr"), currentRow.nextSibling)).data([{key: currentRow.id + ", barRow"}]);
            tr.append("td").style("min-width", "75px");
            tr.append("td").style("min-width", "75px");
            dataRequested[1].unshift({year: 2002, term: 1});
            chart = tr
                .attr("id", currentRow.id)
                .classed("barRow", true)
                .append("td")
                .attr("colspan", "28")
                .append("svg")
                .attr("id", currentRow.id)
                .attr("class", "barContainer")
                .attr("width", d3.select(".table").node().getBoundingClientRect().width - 78 * 2 + "px")
                .style("cursor", "default")
                .style("margin-top", "5px")
                .style("margin-bottom", "2px")
                .selectAll(".barChart")
                .data(nestData);
            barContainer = d3.select("#" + args[0] + '\\,' + args[1] + ".barContainer");
            barchart = chart
                .enter()
                .append("g")
                .attr("class", "barChart")
                .attr("id", function (d) {return d.key; })
                .attr("transform", function (d, i) {
                    return "translate(0," + (20 * i) + ")";
                });
            width = parseInt(d3.select(".barContainer").style("width"), 10) - 15;
            xAxis = d3.scaleBand()
                .range([0, width])
                .round(false)
                .paddingInner(1)
                .paddingOuter(0)
                .domain(dataRequested[1].filter(function (k) {
                    return k.year < 2016;
                }).map(function (d) {
                    return d.year + ',' + d.term;
                }));
            yAxis = d3.scaleLinear()
                .domain([0, 9])
                .range([15, 0]).nice();
            xAxisOrientation = d3.axisBottom(xAxis);
            yAxisOrientation = d3.axisLeft(yAxis);
            currentLine = barchart.selectAll(".bar")
                .data(function (k) {return k.values; })
                .enter()
                .append("rect")
                .attr("class", "bar")
                .attr("id", function (d) {
                    return currentRow.id + ',' + d.year + ',' + d.term;
                })
                .attr("x", function (d) { return xAxis(d.year + ',' + d.term); })
                .style("stroke", "rgb(200, 200, 200)")
                .style("stroke-width", "1px")
                .attr("width", 15)
                .on("mousedown", function (d) {
                    var bar = d3.select(this),
                        id,
                        type = Table.getAggregation() === "degree" ? "main" : "sub";
                    highlight(bar, "bar", this.id, type, d);
                })
                .on("mouseover", function (d) {
                    mouseOver(d, this);
                    BarChart.tooltip(d);
                })
                .on("mouseout", function (d) {
                    if (d3.select(this).classed("bar")) {
                        mouseOut(d, this);
                    } else {
                        selectMouseOut(this);
                    }
                    d3.select(".tooltip")
                        .style("visibility", "hidden");
                })
                .style("fill", function (d) {
                    return colorScale(d.teacherScore);
                })
                .attr("y", function (d) { return 15; })
                .attr("height", 0)
                .transition()
                .duration(800)
                .attr("height", function (d) { return 15 - yAxis(d.teacherScore); })
                .attr("y", function (d) { return 4 + yAxis(d.teacherScore); })
                .on("start", function () {
                    transitionNumber += 1;
                })
                .on("end", function () {
                    transitionNumber -= 1;
                    if (transitionNumber === 0) {
                        enableEvents();
                        d3.selectAll(".bar")
                            .attr("class", function (d, i) {
                                var selected = getSelected();
                                if (selected.indexOf(this.id) > -1) {
                                    clicked(d, this);
                                    return "selectBar";
                                }
                                return "bar";
                            });
                    }
                });
            barchart.append("g")
                .attr("class", "barAxis")
                .attr("transform", "translate(5," + 15 + ")")
                .call(xAxisOrientation);
            barchart.append("text")
                .attr("class", "labelBar")
                .attr("transform", "translate(0, 15)")
                .style("text-anchor", "start")
                .style("font-size", "9px")
                .text(function (d) {
                    var name = d.key.split(" ");
                    return name[0] + " " + name.splice(-1);
                });
            barchart.selectAll(".brline").data(function (k) {return [k]; })
                .enter()
                .append("line")
                .attr("class", "brline")
                .attr("x1", 0)
                .attr("x2", width + 12)
                .attr("y1", 20)
                .attr("y2", 20)
                .style("stroke-width", "1px")
                .attr("stroke", "rgb(200, 200, 200)");
            svgHeight = barContainer.node().getBBox().height;
            barContainer.attr("height", svgHeight + 5);
        }
    };
}());