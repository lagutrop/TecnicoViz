/*global d3, dispatcher, disableEvents, adjustViews, enableEvents, mouseOver, getFilteredAcronym, mouseOut, Table, drawPill, removeDuplicate, touchDevice, getSelected, selectMouseOut, clicked, highlight, linePill, $*/

var LineChart = (function () {
    "use strict";
    
    var coloredDegrees = {},
        pills = [],
        availableAttributes = ["teacherScore", "studentsNumber"],
        attributeType = "teacherScore",
        request = {"teacherScore": "teachers", "studentsNumber": "courses"},
        operation = {"teacherScore": "mean", "studentsNumber": "sum"},
        display = {"teacherScore": "Teacher Quc", "studentsNumber": "Enrollments"};
    
    function deltaE(color1, color2) {
        var i,
            sum = 0;
        for (i = 0; i < color1.length; i += 1) {
            sum += Math.pow((color1[i] - color2[i]), 2);
        }
        return Math.sqrt(sum);
    }
    
    function deltaE94(color1, color2) {
        var i,
            deltaEFinal,
            deltaL = color1[0] - color2[0],
            deltaA = color1[1] - color2[1],
            deltaB = color1[2] - color2[2],
            c1 = Math.sqrt(Math.pow(color1[1], 2) + Math.pow(color1[2], 2)),
            c2 = Math.sqrt(Math.pow(color2[1], 2) + Math.pow(color2[2], 2)),
            deltaC = c1 - c2,
            deltaH = Math.sqrt(Math.pow(deltaA, 2) + Math.pow(deltaB, 2) - Math.pow(deltaC, 2)),
            kl = 1,
            kh = 1,
            kc = 1,
            sl = 1,
            sc = 1 + 0.045 * c1,
            sh = 1 + 0.015 * c1;
        deltaEFinal = Math.pow(deltaL / (kl * sl), 2) + Math.pow(deltaC / (kc * sc), 2) + Math.pow(deltaH / (kh * sh), 2);
        return Math.sqrt(deltaEFinal);
    }
    
    function comparePlot() {
        var x = parseInt(d3.select("table").style("width").split("px")[0], 10),
            y = parseInt(d3.select(".container").style("height"), 10) + parseInt(d3.select(".plotContainer").style("height"), 10),
            svgHeight = 220,
            svgWidth = 350;
        if (d3.select(".lineContainerCompare").empty()) {
            d3.select("body")
                .append("svg")
                .attr("class", "lineContainerCompare")
                .attr("width", svgWidth)
                .attr("height", svgHeight)
                .style("position", "fixed")
                .style("left", x + 15 + "px")
                .style("top", y + 10 + "px")
                .style("opacity", 0)
                .append("g")
                .attr("transform", "translate(" + 31 + "," + 5 + ")")
                .attr("class", "lineChartCompare")
                .style("opacity", 1);
            d3.select("body")
                .append("div")
                .attr("class", "linePillContainer")
                .style("position", "fixed")
                .style("top", y + "px")
                .style("left", x + 25 + "px");
        }
    }
    
    function rgbGen(id) {
        var r = Math.floor((Math.random() * 255) / 2),
            g = Math.floor((Math.random() * 255) / 2),
            b = Math.floor((Math.random() * 255) / 2),
            lab = d3.lab('rgb(' + r + ',' + g + ',' + b + ')'),
            colorString,
            i,
            color = [r, g, b],
            colorLab = [lab.l, lab.a, lab.y];
        if (coloredDegrees[id] === undefined) {
            for (i = 0; i < Object.keys(coloredDegrees).length; i += 1) {
                if (deltaE94(colorLab, d3.lab('rgb(' + i[0] + ',' + i[1] + ',' + i[2] + ')')) < 30) {
                    r = Math.floor((Math.random() * 255) / 2);
                    g = Math.floor((Math.random() * 255) / 2);
                    b = Math.floor((Math.random() * 255) / 2);
                    lab = d3.lab('rgb(' + r + ',' + g + ',' + b + ')');
                    colorLab = [lab.l, lab.a, lab.y];
                    i = 0;
                }
            }
            coloredDegrees[id] = color;
        }
        colorString = 'rgb(' + coloredDegrees[id][0] + ',' + coloredDegrees[id][1] + ',' + coloredDegrees[id][2] + ')';
        return colorString;
    }
    
    function pill(id) {
        d3.select(".linePillContainer")
            .append("div")
            .attr("class", "linePill " + Table.getAggregation())
            .attr("id", id)
            .text(id)
            .style("background-color", rgbGen(id))
            .style("color", "white")
            .style("cursor", "default")
            .append("span")
            .attr("class", "closebtn")
            .style("color", "white")
            .text("x")
            .on("click", function (d) {
                var line = this.parentNode.id,
                    args;
                d3.selectAll(".line#" + line).remove();
                pills.splice(pills.indexOf(id), 1);
                d3.select(this.parentNode).remove();
                if (d3.select(".svgLineCompare").empty()) {
                    d3.select(".lineChartCompare")
                        .style("opacity", 0);
                } else {
                    args = linePill();
                    dispatcher(LineChart.updateCompare, args[0], args[1]);
                }
            });
        pills.push(id);
    }
    
    function labelToggle(graphLabel) {
        var label = d3.select(graphLabel),
            toggle,
            tran = d3.transition()
                .duration(200)
                .ease(d3.easeLinear);
        if (!label.classed("open")) {
            label.classed("open", true);
            toggle = d3.select("body")
                .append("rect")
                .attr("class", "infoAttribute")
                .style('opacity', 0.0)
                .style("left", d3.event.pageX - 100 + "px")
                .style("top", d3.event.clientY + "px");
            toggle.transition(tran)
                .style('opacity', 1.0);
            toggle.append("p").text("Attributes");
            toggle.selectAll(".infoOption")
                .data(availableAttributes)
                .enter()
                .append("div")
                .attr("class", function (d) {
                    if (attributeType === d) {
                        return "infoOption checked";
                    } else {
                        return "infoOption";
                    }
                })
                .on("mouseover", function () {
                    d3.select(this).style("outline", "2px solid skyblue");
                })
                .on("mouseout", function () {
                    d3.select(this).style("outline", "none");
                })
                .on("click", function (d) {
                    attributeType = d;
                    var acronym,
                        lineRequest,
                        lineRequestCompare = {"degreeAcronym" : "degreeAcronym=", "courseAcronym" : "courseAcronym="},
                        tableSearch = LineChart.getRequest(),
                        args,
                        argsDegree = {},
                        argsCourse = {},
                        argsUpdate = [],
                        acronymList = {"courseAcronym": [], "degreeAcronym": []},
                        concatenatedAcronym;
                    d3.selectAll(".expanded").each(function (d) {
                        acronym = Table.getAggregation() + "Acronym";
                        lineRequest = Table.getAggregation() === "degree" ? [acronym + "=" + d.key] : [acronym + "=" + d.key, getFilteredAcronym()[1] === "" ? "" : "degreeAcronym=" + getFilteredAcronym()[1]];
                        args = {};
                        args[tableSearch] = lineRequest;
                        args.terms = "";
                        dispatcher(LineChart.draw, [args], [d3.select("#" + d.key + ".mainrow").node()]);
                    });
                    d3.selectAll(".linePill").each(function (d, i, k) {
                        acronym = d3.select(this).attr("class").split(" ")[1] + "Acronym";
                        if (k.length === i + 1) {
                            lineRequestCompare[acronym] += this.id;
                        } else {
                            lineRequestCompare[acronym] += this.id + ',';
                        }
                        acronymList[acronym][0] = d3.select(this).attr("class").split(" ")[1] + "Acronym";
                    });
                    if (!d3.selectAll(".linePill").empty()) {
                        argsDegree[tableSearch] = [lineRequestCompare.degreeAcronym];
                        argsCourse[tableSearch] = [lineRequestCompare.courseAcronym];
                        if (acronymList.degreeAcronym.length > 0) {
                            argsUpdate.push(argsDegree);
                        }
                        if (acronymList.courseAcronym.length > 0 && getFilteredAcronym()[1] !== "") {
                            argsCourse[tableSearch].push("degreeAcronym=" + getFilteredAcronym()[1]);
                        }
                        argsUpdate.push(argsCourse);
                        concatenatedAcronym = acronymList.degreeAcronym.concat(acronymList.courseAcronym);
                        dispatcher(LineChart.updateCompare, argsUpdate, concatenatedAcronym);
                    }
                })
                .text(function (d, i) {return Object.values(display)[i]; });
            toggle.append("rect")
                .attr("class", "infoClosebtn")
                .text("X")
                .on("mouseover", function () { d3.select(this).style("color", "blanchedalmond"); })
                .on("mouseout", function () { d3.select(this).style("color", "white"); })
                .on("click", function () {
                    label.classed("open", false);
                    d3.selectAll(".infoAttribute")
                        .transition(tran)
                        .style('opacity', 0)
                        .remove();
                });
        } else {
            label.classed("open", false);
            d3.selectAll(".infoAttribute")
                .transition(tran)
                .style('opacity', 0)
                .remove();
        }
    }
    
    function buildAxis(chart, xAxisOrientation, yAxisOrientation, height) {
        if (d3.select(".yLineAxisCompare").empty()) {
            chart
                .append('g')
                .attr('transform', 'translate(0,' + 180 + ')')
                .attr('class', 'xLineAxisCompare')
                .call(xAxisOrientation);
            chart.append("text")
                .attr("class", "xLineLabelCompare")
                .attr("x", 310)
                .attr("y", 210)
                .style("text-anchor", "end")
                .text("Years");
            chart.append('g')
                .attr('transform', 'translate(0,0)')
                .attr('class', 'yLineAxisCompare')
                .call(yAxisOrientation);
            chart
                .append("svg")
                .attr("class", "yLabelLineContainer")
                .append("rect");
            d3.select(".yLabelLineContainer")
                .append("text")
                .attr("class", "yLineLabelCompare")
                .attr("x", 10)
                .attr("y", 11)
                .style("cursor", "pointer")
                .on("click", function () {
                    labelToggle(".yLineLabelCompare");
                })
                .text(display[attributeType])
                .on("mouseover", function () {
                    d3.select(".yLabelLineContainer > rect")
                        .style("fill", "rgba(135, 185, 201, 0.2)");
                })
                .on("mouseout", function () {
                    d3.select(".yLabelLineContainer > rect")
                        .style("fill", "none");
                });
            d3.select(".yLabelLineContainer > rect")
                .attr("x", d3.select(".yLineLabelCompare").node().getBBox().x - 5)
                .attr("y", 1)
                .attr("height", 15)
                .attr("width", d3.select(".yLineLabelCompare").node().getBBox().width + 5 * 2)
                .style("stroke", "grey")
                .style("fill", "none")
                .style("stroke-width", 1)
                .on("mouseover", function () {
                    d3.select(".yLabelLineContainer > rect")
                        .style("fill", "rgba(135, 185, 201, 0.2)");
                })
                .on("mouseout", function () {
                    d3.select(".yLabelLineContainer > rect")
                        .style("fill", "none");
                });
        } else {
            chart.selectAll(".xLineAxisCompare")
                .call(xAxisOrientation);
            chart.selectAll(".yLineAxisCompare")
                .call(yAxisOrientation);
        }
    }
    
    function filterData(dataRequested, aggregation) {
        var filteredData = [];
        d3.nest()
            .key(function (d) {
                return d[aggregation] + ',' + d.year + ',' + d.term;
            })
            .rollup(function (v) {
                var format = d3.format(".2f"),
                    e = v[0];
                e[attributeType] = parseFloat(format(d3[operation[attributeType]](v, function (f) {
                    return f[attributeType];
                })));
                e.approval = parseFloat(format(d3[operation[attributeType]](v, function (f) {
                    return f.approval;
                })));
                if (!isNaN(e[attributeType]) && e.year < 2016) {
                    filteredData.push(e);
                }
                return v;
            })
            .entries(dataRequested);
        return filteredData.sort(function (x, y) {
            return d3.ascending(x.year + ',' + x.term, y.year + ',' + y.term);
        });
    }
    
    // Public Methods
    return {
        
        circleMouseOver: function (d, element) {
            d3.selectAll(element).transition()
                .duration(100)
                .ease(d3.easeCircleIn)
                .attr("r", 4)
                .attr("stroke-width", "2")
                .attr("stroke", "coral");
        },
    
        circleMouseOut: function (d, element) {
            d3.selectAll(element)
                .transition()
                .duration(400)
                .ease(d3.easeElasticOut)
                .attr("r", 3)
                .attr("stroke-width", "1")
                .attr("stroke", rgbGen(element[0].parentNode.id));
        },
        
        tooltip: function (d, element) {
            var posX = d3.event.pageX + 80 >= $(window).innerWidth() ? d3.event.pageX - 90 : d3.event.pageX + 10,
                el = d3.select("#" + element.id.split(',')[0] + ".linePill"),
                acronym = el.empty() ? Table.getAggregation() + "Acronym" : el.attr("class").split(" ")[1] + "Acronym";
            d3.select(".tooltip")
                .style("left", posX + "px")
                .style("top", $(window).scrollTop() + d3.event.clientY + 10 + "px")
                .style("visibility", "visible")
                .html(d[acronym] + "<br>" + "Year: " + d.year + "<br>" + "Term: " + d.term + "<br>" + display[attributeType] + ": " + d[attributeType]);
        },
        
        draw: function (dataRequested, args) {
            var lineLength,
                height = parseInt(d3.select(".container").style("height"), 10),
                currentRow = args[0],
                tr,
                width,
                scores = filterData(dataRequested[0], Table.getAggregation()),
                xAxis,
                transitionNumber = 0,
                yAxis,
                xAxisOrientation,
                yAxisOrientation,
                chart,
                clone,
                dragged,
                dragIcon,
                finalPosition,
                i,
                j,
                line,
                currentLine;
            d3.selectAll(".infoLabel, .yLineLabelCompare").classed("open", false);
            d3.selectAll(".infoAttribute")
                .transition()
                .duration(200)
                .ease(d3.easeLinear)
                .style('opacity', 0)
                .remove();
            if (currentRow === null) {
                return;
            }
            d3.select("#" + currentRow.id + ".infoChart").remove();
            if (scores.length === 0) {
                return;
            }
            comparePlot();
            tr = d3.select(currentRow.parentNode.insertBefore(document.createElement("tr"), currentRow.nextSibling));
            tr.append("td").style("min-width", "75px");
            dataRequested[1].unshift({year: 2002, term: 1});
            chart = tr
                .attr("id", currentRow.id)
                .classed("infoChart", true)
                .append("td")
                .attr("colspan", "29")
                .append("svg")
                .attr("id", currentRow.id)
                .attr("class", "lineContainer")
                .attr("width", d3.select(".table").node().getBoundingClientRect().width - 78 + "px")
                .attr("height", 50)
                .style("cursor", "default")
                .style("margin-top", "5px")
                .style("margin-bottom", "2px")
                .append("g")
                .attr("class", "lineChart")
                .attr("id", currentRow.id)
                .attr("transform", "translate(" + 80 + "," + 5 + ")");
            
            d3.select("#" + currentRow.id + ".lineContainer")
                .append("svg")
                .attr("class", "labelLineContainer")
                .append("rect");
            d3.select("#" + currentRow.id + ".lineContainer " + "> .labelLineContainer")
                .append("text")
                .attr("class", "infoLabel")
                .attr("x", 8)
                .attr("y", 35)
                .style("text-anchor", "start")
                .style("font-size", "9px")
                .style("cursor", "pointer")
                .on("click", function () {
                    labelToggle(".infoLabel");
                })
                .text(display[attributeType])
                .on("mouseover", function () {
                    d3.select(".labelLineContainer > rect")
                        .style("fill", "rgba(135, 185, 201, 0.2)");
                })
                .on("mouseout", function () {
                    d3.select(".labelLineContainer > rect")
                        .style("fill", "none");
                });
            d3.select("#" + currentRow.id + ".lineContainer " + "> .labelLineContainer > rect")
                .attr("x", d3.select(".infoLabel").node().getBBox().x - 5)
                .attr("y", 25)
                .attr("height", 15)
                .attr("width", d3.select(".infoLabel").node().getBBox().width + 5 * 2)
                .style("stroke", "grey")
                .style("fill", "none")
                .style("stroke-width", 1)
                .on("mouseover", function () {
                    d3.select(".labelLineContainer > rect")
                        .style("fill", "rgba(135, 185, 201, 0.2)");
                })
                .on("mouseout", function () {
                    d3.select(".labelLineContainer > rect")
                        .style("fill", "none");
                });
            dragIcon = d3.select("#" + currentRow.id + ".lineContainer").append("image")
                .attr("width", 10)
                .attr("height", 10).attr("xlink:href", "/static/assets/drag.png")
                .attr("class", "logo")
                .attr("id", currentRow.id)
                .attr("x", 5)
                .attr("y", 5)
                .attr("opacity", 0.8)
                .style("cursor", "move")
                .style("cursor", "grab")
                .style("cursor", "-moz-grab")
                .style("cursor", "-webkit-grab")
                .call(d3.drag()
                    .on("start", function (d) {
                        var data = d3.selectAll(".lineCircle[id^='" + this.id + "'], .selectLineCircle[id^='" + this.id + "']").data(),
                            lineLength = d3.select(".svgLine#" + this.id).node().getTotalLength(),
                            xAxis = d3.scaleBand()
                                .range([0, lineLength])
                                .round(false)
                                .paddingInner(1)
                                .paddingOuter(0)
                                .domain(data.filter(function (k) {
                                    return k.year < 2016;
                                }).map(function (d) {
                                    return d.year + ',' + d.term;
                                })),
                            yAxis = d3.scaleLinear()
                                .domain([0, d3.max(data, function (d) { return d[attributeType]; }) + 1])
                                .range([40, 0]).nice(),
                            xAxisOrientation = d3.axisBottom(xAxis)
                                .tickSize([4])
                                .tickFormat(function (d) {
				                    return d.split(',')[1];
                                }),
                            yAxisOrientation = d3.axisLeft(yAxis),
                            line = d3.line()
                                .x(function (d) {
                                    return xAxis(d.year + ',' + d.term);
                                })
                                .y(function (d) {
                                    return yAxis(d[attributeType]);
                                });
                        d3.event.sourceEvent.stopPropagation();
                        d3.select("body").append("svg")
                            .attr("id", this.id)
                            .attr("class", "clonedChart")
                            .style("position", "fixed")
                            .style("left", "445px")
                            .style("top", "101px")
                            .style("opacity", 0)
                            .style("width", lineLength + "px")
                            .append("g")
                            .attr("class", "lineClone");
                        d3.select(".lineClone").append("path")
                            .attr("id", currentRow.id)
                            .attr("class", "svgLine")
                            .attr("stroke", rgbGen(currentRow.id))
                            .attr("d", line(scores));
                    })
                    .on("drag", function () {
                        var mouseX = d3.event.sourceEvent.pageX,
                            mouseY = d3.event.sourceEvent.clientY,
                            chartPos = d3.select(".lineContainerCompare").node().getBoundingClientRect();
                        finalPosition = [mouseX, mouseY];
                        disableEvents();
                        dragged = true;
                        if (touchDevice()) {
                            mouseX = event.touches[0].pageX;
                            mouseY = event.touches[0].pageY;
                        }
                        d3.select(".clonedChart#" + this.id)
                            .style("opacity", 1)
                            .style("left", mouseX - 20)
                            .style("top", mouseY - 10);
                        d3.select(".lineContainerCompare")
                            .style("outline", "2px dashed black")
                            .style("opacity", 1);
                        if (finalPosition[0] >= chartPos.left && finalPosition[0] <= chartPos.right && finalPosition[1] >= chartPos.top && finalPosition[1] <= chartPos.bottom) {
                            d3.select(".lineContainerCompare")
                                .style("background-color", "rgba(135, 185, 201, 0.2)");
                        } else {
                            d3.select(".lineContainerCompare")
                                .style("background-color", "transparent");
                        }
                    })
                    .on("end", function () {
                        var acronym,
                            lineRequestCompare = {"degreeAcronym" : "degreeAcronym=", "courseAcronym" : "courseAcronym="},
                            acronymList = {"courseAcronym": [], "degreeAcronym": []},
                            argsDegree = {},
                            argsCourse = {},
                            tableSearch = LineChart.getRequest(),
                            concatenatedAcronym,
                            argsUpdate = [];
                        if (dragged) {
                            enableEvents();
                            dragged = false;
                            d3.event.sourceEvent.stopPropagation();
                            if (d3.select(".lineContainerCompare").style("background-color") === "rgba(135, 185, 201, 0.2)" && d3.selectAll(".linePill#" + this.id).empty()) {
                                if (pills.length === 5) {
                                    d3.selectAll(".svgLineCompare#" + pills[0]).remove();
                                    d3.selectAll(".lineCompareCircle[id^=" + pills[0] + "]").remove();
                                    d3.select(".linePill#" + pills[0]).remove();
                                    pills.shift();
                                }
                                pill(this.id);
                                d3.selectAll(".linePill").each(function (d, i, k) {
                                    acronym = d3.select(this)
                                        .attr("class")
                                        .split(" ")[1] + "Acronym";
                                    if (k.length === i + 1) {
                                        lineRequestCompare[acronym] += this.id;
                                    } else {
                                        lineRequestCompare[acronym] += this.id + ',';
                                    }
                                    acronymList[acronym][0] = d3.select(this).attr("class").split(" ")[1] + "Acronym";
                                });
                                if (!d3.selectAll(".linePill").empty()) {
                                    argsDegree[tableSearch] = [lineRequestCompare.degreeAcronym];
                                    if (lineRequestCompare.courseAcronym.split("=")[1] !== "") {
                                        argsCourse[tableSearch] = [lineRequestCompare.courseAcronym];
                                    }
                                    if (acronymList.degreeAcronym.length > 0) {
                                        argsUpdate.push(argsDegree);
                                    }
                                    if (acronymList.courseAcronym.length > 0) {
                                        argsUpdate.push(argsCourse);
                                    }
                                    if (acronymList.courseAcronym.length > 0 && getFilteredAcronym()[1] !== "") {
                                        argsCourse[tableSearch].push("degreeAcronym=" + getFilteredAcronym()[1]);
                                    }
                                    concatenatedAcronym = acronymList.degreeAcronym.concat(acronymList.courseAcronym);
                                    dispatcher(LineChart.updateCompare, argsUpdate, concatenatedAcronym);
                                }
                            }
                            d3.select(".lineContainerCompare")
                                .style("background-color", "transparent")
                                .style("outline", "none");
                            d3.select(".clonedChart").remove();
                        }
                    }));
            width = parseInt(d3.select(".lineContainer").style("width"), 10) - 80;
            xAxis = d3.scaleBand()
                .range([0, width - 5])
                .round(false)
                .paddingInner(1)
                .paddingOuter(0)
                .domain(dataRequested[1].filter(function (k) {
                    return k.year < 2016;
                }).map(function (d) {
                    return d.year + ',' + d.term;
                }));
            yAxis = d3.scaleLinear()
                .domain([0, d3.max(scores, function (d) { return d[attributeType]; }) + 1])
                .range([40, 0]).nice();
            xAxisOrientation = d3.axisBottom(xAxis)
                .tickSize([4])
                .tickFormat(function (d) {
				    return d.split(',')[1];
                });
            yAxisOrientation = d3.axisLeft(yAxis);
            line = d3.line()
                .x(function (d) {
                    return xAxis(d.year + ',' + d.term);
                })
                .y(function (d) {
                    return yAxis(d[attributeType]);
                });
            currentLine = chart
                .append("path")
                .attr("id", currentRow.id)
                .attr("class", "svgLine")
                .attr("stroke", rgbGen(currentRow.id))
                .attr("d", line(scores));
            lineLength = currentLine.node().getTotalLength();
            currentLine
                .attr("stroke-dasharray", lineLength + " " + lineLength)
                .attr("stroke-dashoffset", lineLength)
                .transition()
                .duration(800)
                .attr("stroke-dashoffset", 0);
           /* chart
                .append('g')
                .attr('transform', 'translate(0,' + 90 + ')')
                .attr('class', 'xLineAxis')
                .call(xAxisOrientation);
            chart.append("text")
                .attr("class", "xLineLabel")
                .attr("x", width)
                .attr("y", 115)
                .style("text-anchor", "end")
                .style("font-size", "9px")
                .text("Terms");
            chart.append('g')
                .attr('transform', 'translate(0,0)')
                .attr('class', 'yLineAxis')
                .call(yAxisOrientation);*/
            chart.selectAll(".lineCircle")
                .data(scores)
                .enter()
                .append("circle")
                .on("click", function (d) {
                    var circle = d3.select(this),
                        id,
                        type = Table.getAggregation() === "degree" ? "main" : "sub";
                    highlight(circle, "lineCircle", this.id, type, d);
                })
                .on("mouseover", function (d) {
                    mouseOver(d, this);
                    LineChart.tooltip(d, this);
                })
                .on("mouseout", function (d) {
                    if (d && d3.select(this).classed("lineCircle")) {
                        mouseOut(d, this);
                    } else {
                        selectMouseOut(this);
                    }
                    d3.select(".tooltip")
                        .style("visibility", "hidden");
                })
                .attr("cx", function (d) {
                    return xAxis(d.year + ',' + d.term);
                })
                .attr("cy", function (d) {
                    return yAxis(d[attributeType]);
                })
                .attr("id", function (d) {
                    return currentRow.id + ',' + d.year + ',' + d.term;
                })
                .attr("class", "lineCircle")
                .transition()
                .duration(800)
                .attr("fill", "white")
                .attr("stroke", rgbGen(currentRow.id))
                .attr("r", 3)
                .on("start", function () {
                    transitionNumber += 1;
                })
                .on("end", function () {
                    transitionNumber -= 1;
                    if (transitionNumber === 0) {
                        enableEvents();
                        d3.selectAll(".lineCircle")
                            .attr("class", function (d, i) {
                                var selected = getSelected();
                                if (selected.indexOf(this.id) > -1) {
                                    clicked(d, this);
                                    return "selectLineCircle";
                                }
                                return "lineCircle";
                            });
                    }
                });
        },
        
        updateCompare: function (dataRequested, group) {
            var scores = [],
                lineType = {},
                xAxis,
                yAxis,
                xAxisOrientation,
                yAxisOrientation,
                newData = [],
                transitionNumber = 0,
                line = d3.line()
                    .x(function (d) {
                        return xAxis(d.year + ',' + d.term);
                    })
                    .y(function (d) {
                        return yAxis(d[attributeType]);
                    });
            dataRequested.forEach(function (k, i) {
                var filteredData = filterData(k, group[i]),
                    tempData = newData,
                    tempScores = scores,
                    data = d3.nest().key(function (d) {
                        lineType[d[group[i]]] = group[i];
                        return d[group[i]];
                    })
                        .entries(filteredData);
                scores = tempScores.concat(filteredData);
                newData = tempData.concat(data);
            });
            d3.selectAll(".infoLabel, .yLineLabelCompare").classed("open", false);
            d3.selectAll(".infoAttribute")
                .transition()
                .duration(200)
                .ease(d3.easeLinear)
                .style('opacity', 0)
                .remove();
            d3.select(".lineChartCompare").style("opacity", 1)
                .selectAll(".line")
                .data(newData, function (k) {return (k && k.key) || d3.select(this).attr("id"); })
                .enter()
                .append("g")
                .attr("id", function (d) {return d.key; })
                .attr("class", "line");
            xAxis = d3.scaleBand()
                .range([0, 300])
                .round(false)
                .paddingInner(1)
                .paddingOuter(0)
                .domain(scores.filter(function (k) {
                    return k[attributeType] || k[attributeType] === 0;
                }).map(function (d) {
                    return d.year + ',' + d.term;
                }));
            yAxis = d3.scaleLinear()
                    .domain([Math.floor(d3.min(scores, function (d) { return d[attributeType]; })), d3.max(scores, function (d) { return d[attributeType]; })])
                    .range([180, 0]).nice();
            xAxisOrientation = d3.axisBottom(xAxis)
                .tickSize([4])
                .tickValues([d3.min(scores, function (d) { return d.year + ',' + d.term; }), d3.max(scores, function (d) { return d.year + ',' + d.term; })])
                .tickFormat(function (d) {
                    return d.split(',')[0];
                });
            yAxisOrientation = d3.axisLeft(yAxis);
            var currentLine = d3.selectAll("g.line").data(newData, function (k) {return (k && k.key) || d3.select(this).attr("id"); }).selectAll("path")
                .data(function (k) {return [k]; });
            currentLine.exit()
                .remove();
            currentLine.enter()
                .append("path")
                .attr("class", "svgLineCompare")
                .attr("id", function (d) {
                    return d.key;
                })
                .attr("stroke", function (d) {return rgbGen(d.key); })
                .attr("d", function (d) {
                    return line(d.values);
                })
                .attr("stroke-dasharray", function () {
                    return this.getTotalLength();
                })
                .attr("stroke-dashoffset", function () {
                    return this.getTotalLength();
                })
                .transition()
                .duration(800)
                .attr("stroke-dashoffset", 0);
            currentLine
                .attr("d", function (d) {
                    return line(d.values);
                })
                .attr("stroke-dasharray", function () {
                    return this.getTotalLength();
                })
                .attr("stroke-dashoffset", function () {
                    return this.getTotalLength();
                })
                .transition()
                .duration(800)
                .attr("stroke-dashoffset", 0);
            buildAxis(d3.select(".lineChartCompare"), xAxisOrientation, yAxisOrientation, 30);
            var chart = d3.selectAll("g.line").data(newData, function (k) {return (k && k.key) || d3.select(this).attr("id"); }).selectAll("circle")
                .data(function (k) {return k.values; });
            chart.exit()
                .remove();
            chart.enter()
                .append("circle")
                .style("cursor", "default")
                .on("mouseover", function (d) {
                    mouseOver(d, this);
                    LineChart.tooltip(d, this);
                })
                .on("mouseout", function (d) {
                    if (d3.select(this).classed("lineCompareCircle")) {
                        mouseOut(d, this);
                    } else {
                        selectMouseOut(this);
                    }
                    d3.select(".tooltip")
                        .style("visibility", "hidden");
                })
                .on("click", function (d) {
                    var circle = d3.select(this),
                        id,
                        type = d3.select(".linePill#" + this.id.split(",")[0]).attr("class").split(" ")[1] === "degree" ? "main" : "sub";
                    highlight(circle, "lineCompareCircle", this.id, type, d);
                })
                .attr("id", function (d) {
                    return d[lineType[this.parentNode.id]] + ',' + d.year + ',' + d.term;
                })
                .attr("class", "lineCompareCircle")
                .transition()
                .duration(800)
                .attr("fill", "white")
                .attr("stroke", function (d) {
                    return rgbGen(d[lineType[this.parentNode.id]]);
                })
                .attr("r", 3)
                .attr("cx", function (d) {
                    return xAxis(d.year + ',' + d.term);
                })
                .attr("cy", function (d) {
                    return yAxis(d[attributeType]);
                })
                .on("start", function () {
                    transitionNumber += 1;
                    disableEvents();
                })
                .on("end", function () {
                    transitionNumber -= 1;
                    if (transitionNumber === 0) {
                        enableEvents();
                        d3.selectAll(".lineCompareCircle")
                            .attr("class", function (d, i) {
                                var selected = getSelected();
                                if (selected.indexOf(this.id) > -1) {
                                    clicked(d, this);
                                    return "selectLineCompareCircle";
                                }
                                return "lineCompareCircle";
                            });
                    }
                });
            chart
                .attr("id", function (d) {
                    return d[lineType[this.parentNode.id]] + ',' + d.year + ',' + d.term;
                })
                .attr("cx", function (d) {
                    return xAxis(d.year + ',' + d.term);
                })
                .attr("cy", function (d) {
                    return yAxis(d[attributeType]);
                });
            d3.select(".xLineAxisCompare").transition()
                .duration(1000).call(xAxisOrientation);
            d3.select(".yLineAxisCompare").transition()
                .duration(1000).call(yAxisOrientation);
            d3.select(".yLineLabelCompare")
                .text(display[attributeType]);
            d3.select(".yLabelLineContainer > rect")
                .attr("x", d3.select(".yLineLabelCompare").node().getBBox().x - 5)
                .attr("width", d3.select(".yLineLabelCompare").node().getBBox().width + 5 * 2);
        },
        
        getRequest: function () {
            return request[attributeType];
        },
        
        compareChart: function (dataRequested, id) {
            var lineLength,
                height = parseInt(d3.select(".container").style("height"), 10),
                width,
                xAxis,
                yAxis,
                axisData = [].concat
                    .apply([], d3.selectAll(".svgLineCompare")
                           .data()
                           .map(function (d) {return d.values; }))
                    .concat(dataRequested[0]),
                xAxisOrientation,
                yAxisOrientation,
                chart,
                data = {"key": id, "values": dataRequested[0]},
                clone,
                dragged,
                dragIcon,
                finalPosition,
                i,
                j,
                line,
                currentLine;
            chart = d3.select(".lineChartCompare")
                .style("opacity", 1)
                .append("g")
                .attr("id", id)
                .attr("class", "line");
            width = parseInt(d3.select(".lineContainerCompare").style("width"), 10);
            xAxis = d3.scaleBand()
                .range([0, 300])
                .round(false)
                .paddingInner(1)
                .paddingOuter(0)
                .domain(dataRequested[0].filter(function (k) {
                    return k[attributeType] || k[attributeType] === 0;
                }).map(function (d) {
                    return d.year + ',' + d.term;
                }));
            yAxis = d3.scaleLinear()
                    .domain([0, d3.max(axisData, function (d) { return d[attributeType]; })])
                    .range([180, 0]).nice();
            xAxisOrientation = d3.axisBottom(xAxis)
                .tickSize([4])
                .tickValues([d3.min(dataRequested[0], function (d) { return d.year + ',' + d.term; }), d3.max(dataRequested[0], function (d) { return d.year + ',' + d.term; })])
                .tickFormat(function (d) {
                    return d.split(',')[0];
                });
            yAxisOrientation = d3.axisLeft(yAxis);
            line = d3.line()
                .x(function (d) {
                    return xAxis(d.year + ',' + d.term);
                })
                .y(function (d) {
                    return yAxis(d[attributeType]);
                });
            currentLine = chart
                .append("path")
                .data([data])
                .attr("id", id)
                .attr("class", "svgLineCompare")
                .attr("stroke", rgbGen(id))
                .attr("d", line(data.values));
            lineLength = currentLine.node().getTotalLength();
            currentLine
                .attr("stroke-dasharray", lineLength + " " + lineLength)
                .attr("stroke-dashoffset", lineLength)
                .transition()
                .duration(800)
                .attr("stroke-dashoffset", 0);
            buildAxis(d3.select(".lineChartCompare"), xAxisOrientation, yAxisOrientation, 30);
            chart.selectAll(".lineCircle")
                .data(dataRequested[0])
                .enter()
                .append("circle")
                .style("cursor", "default")
                .on("mouseover", function (d) {
                    mouseOver(d, this);
                    LineChart.tooltip(d, this);
                })
                .on("mouseout", function (d) {
                    if (d && d3.select(this).classed("lineCircle")) {
                        mouseOut(d, this);
                    } else {
                        selectMouseOut(this);
                    }
                    d3.select(".tooltip")
                        .style("visibility", "hidden");
                })
                .attr("cx", function (d) {
                    return xAxis(d.year + ',' + d.term);
                })
                .attr("cy", function (d) {
                    return yAxis(d[attributeType]);
                })
                .attr("id", function (d) {
                    return id + ',' + d.year + ',' + d.term;
                })
                .attr("class", "lineCompareCircle")
                .transition()
                .duration(1400)
                .delay(100)
                .attr("fill", "white")
                .attr("stroke", rgbGen(id))
                .attr("r", 3);
        }
    };
}());