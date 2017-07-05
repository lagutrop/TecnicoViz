/*global d3, dispatcher, disableEvents, adjustViews, clicked, enableEvents, highlight, mouseOver, mouseOut, Table, drawPill, removeDuplicate, $*/

var ScatterPlot = (function (data) {
    "use strict";
    var dataRequested = data,
        circleType = "degree",
        scale,
        tooltipText,
        attributeType = {x: "quc", y: "approval"},
        attributeX = attributeType.x + "Average",
        attributeY = attributeType.y + "Average",
        circleColor = "rgb(31, 119, 208)",
        attributes = ["grades", "quc", "approval", "studentsNumber"],
        availableAttributes = {x: ["grades", attributeType.x], y: ["grades", attributeType.y]},
        axisOffset = {"approval": 9, "grades": 1, "quc": 0.5, "studentsNumber": 10, "credits": 1},
        currentData,
        label =  {x: "", y: "%"},
        display = {"approval": "Approval", "grades": "Grades", "quc": "Course Quc", "studentsNumber": "Enrollments", "credits": "Credits"},
        zoomCircle,
        click = 0,
        delay;
    
    function zoomCircles(xAxisOrientation, yAxisOrientation, xAxis, yAxis) {
        scale = d3.event.transform.k;
        d3.select(".xAxis").call(xAxisOrientation.scale(d3.event.transform.rescaleX(xAxis)));
        d3.select(".yAxis").call(yAxisOrientation.scale(d3.event.transform.rescaleY(yAxis)));
        d3.selectAll(".circle, .selectCircle")
            .attr("transform", d3.event.transform)
            .attr("r", function () {
                if (d3.select(this).style("fill") === "rgb(255, 127, 80)") {
                    return 5 / scale;
                } else {
                    return 2.5 / scale;
                }
            });
    }
    
    function updateAttributes(type) {
        var aggregation = Table.getAggregation() === "degree" ? "course" : "degree",
            attributeLabel;
        circleType = type;
        tooltipText = circleType === "degree" ? "" : aggregation + "Acronym";
        attributeX = circleType === "degree" ? attributeType.x + "Average" : attributeType.x;
        attributeY = circleType === "degree" ? attributeType.y + "Average" : attributeType.y;
        circleColor = circleType === "degree" ? "rgb(31, 119, 208)" : "rgb(31, 166, 208)";
        attributes = circleType === "degree" ? ["grades", "quc", "approval", "studentsNumber"] : ["credits", "grades", "quc", "studentsNumber", "approval"];
        availableAttributes.x = attributes.slice();
        attributeLabel = availableAttributes.x;
        attributeLabel.splice(attributeLabel.indexOf(attributeType.y), 1);
        availableAttributes.y = attributes.slice();
        attributeLabel = availableAttributes.y;
        attributeLabel.splice(attributeLabel.indexOf(attributeType.x), 1);
        label.x = attributeType.x === "approval" ? "%" : "";
        label.y = attributeType.y === "approval" ? "%" : "";
        if (circleType === "degree" && attributeType.x === "credits") {
            attributeType.x = availableAttributes.x[0];
            attributeX = attributeType.x + "Average";
        }
        if (circleType === "degree" && attributeType.y === "credits") {
            attributeType.y = availableAttributes.y[0];
            attributeY = attributeType.y + "Average";
        }
    }
    
    function noDataText() {
        d3.select(".canvas > g").append("text")
            .style("font-size", "15px")
            .attr("id", "nodata")
            .attr("opacity", 0)
            .attr("text-anchor", "end")
            .attr("alignment-baseline", "ideographic")
            .attr("transform", "translate(" + parseInt(d3.select(".plotContainer")
                .style("width")
                .split("px")[0], 10) / 2 + "," + (parseInt(d3.select(".plotContainer")
                .style("height")
                .split("px")[0], 10) / 2 - 20) + ")")
            .text("No Data");
    }
    
    function labelToggle(type) {
        var label = d3.select("." + type + "Label"),
            toggle,
            tran = d3.transition()
                .duration(200)
                .ease(d3.easeLinear);
        if (!label.classed("open")) {
            label.classed("open", true);
            toggle = d3.select("body")
                .append("rect")
                .attr("class", type + "Attribute")
                .style('opacity', 0.0)
                .style("left", d3.event.pageX - 100 + "px")
                .style("top", d3.event.clientY + "px");
            toggle.transition(tran)
                .style('opacity', 1.0);
            toggle.append("p").text("Attributes");
            toggle.selectAll("." + type + "Option")
                .data(availableAttributes[type])
                .enter()
                .append("div")
                .attr("class", function (d) {
                    if (attributeType[type] === d) {
                        return type + "Option checked";
                    } else {
                        return type + "Option";
                    }
                })
                .on("mouseover", function () {
                    d3.select(this).style("outline", "2px solid skyblue");
                })
                .on("mouseout", function () {
                    d3.select(this).style("outline", "none");
                })
                .on("mousedown", function (d) {
                    var axisLabel = type === "x" ? "y" : "x",
                        attributeLabel;
                    attributeType[type] = d;
                    updateAttributes(circleType);
                    availableAttributes[axisLabel] = attributes.slice();
                    attributeLabel = availableAttributes[axisLabel];
                    attributeLabel.splice(attributeLabel.indexOf(d), 1);
                    ScatterPlot.update(currentData);
                })
                .text(function (d) {return display[d]; });
            toggle.append("rect")
                .attr("class", type + "closebtn")
                .text("X")
                .on("mouseover", function () { d3.select(this).style("color", "blanchedalmond"); })
                .on("mouseout", function () { d3.select(this).style("color", "white"); })
                .on("mousedown", function () {
                    label.classed("open", false);
                    d3.selectAll("." + type + "Attribute")
                        .transition(tran)
                        .style('opacity', 0)
                        .remove();
                });
        } else {
            label.classed("open", false);
            d3.selectAll("." + type + "Attribute")
                .transition(tran)
                .style('opacity', 0)
                .remove();
        }
    }
    
    // Public Methods
    return {
        
        tooltip: function (d) {
            var posX = d3.event.pageX + 80 >= $(window).innerWidth() ? d3.event.pageX - 90 : d3.event.pageX + 10,
                format = d3.format(".2f"),
                text = d[tooltipText] || "";
            d3.select(".tooltip")
                .style("left", posX + "px")
                .style("top", $(window).scrollTop() + d3.event.clientY + "px")
                .style("visibility", "visible")
                .html(d[Table.getAggregation() + "Acronym"] + " " + text + "<br>" + "Year: " + d.year + "<br>" + "Term: " + d.term + "<br>" + display[attributeType.y] + ": " + format(d[attributeY]) + label.y + "<br>" + display[attributeType.x] + ": " + format(d[attributeX]) + label.x);
        },
        
        circleMouseOver: function (d, element) {
            element.parentNode.appendChild(element);
            d3.select(element).transition()
                .duration(100)
                .ease(d3.easeCircleIn)
                .attr("r", 5 / scale)
                .style("fill", "coral")
                .style("opacity", 1);
        },
    
        circleMouseOut: function (d, element) {
            d3.select(element)
                .transition()
                .duration(400)
                .ease(d3.easeElasticOut)
                .attr("r", 2.5 / scale)
                .style("opacity", 0.3)
                .style("fill", circleColor);
        },
        
        update: function (dataRequested) {
            currentData = dataRequested;
            /*d3.selectAll(".yAxis > .tick").style("visibility", "visible");
            d3.selectAll(".xAxis > .tick").style("visibility", "visible");*/
            d3.selectAll(".xLabel, .yLabel").classed("open", false);
            d3.selectAll(".xAttribute, .yAttribute")
                .transition()
                .duration(200)
                .ease(d3.easeLinear)
                .style('opacity', 0)
                .remove();
            if (!d3.selectAll(".pillContainer").empty()) {
                if (!d3.selectAll(".secondLabel").empty()) {
                    dataRequested[0] = dataRequested[0].filter(function (d) {
                        var data = "",
                            name = d.degreeAcronym;
                        d3.selectAll(".secondLabel").each(function (f) {
                            if (!name || name.toUpperCase().indexOf(f[0]) > -1) {
                                data = d;
                            }
                        });
                        return data !== "";
                    });
                }
                dataRequested[0] = removeDuplicate(dataRequested[0].map(function (element) {
                    var data = {},
                        i,
                        type = circleType === "degree" ? "Average" : "",
                        aggregation = Table.getAggregation() === "degree" ? "course" : "degree";
                    if (circleType === 'course') {
                        data[aggregation + "Acronym"] = element[aggregation + "Acronym"];
                    }
                    data[Table.getAggregation() + "Acronym"] = element[Table.getAggregation() + "Acronym"];
                    data.year = element.year;
                    data.term = element.term;
                    for (i = 0; i < attributes.length; i += 1) {
                        data[attributes[i] + type] = element[attributes[i] + type];
                    }
                    return data;
                }));
            }
            var xAxis = d3.scaleLinear()
                    .domain([d3.min(dataRequested[0].filter(function (d) {
                        return d[attributeX] !== null && !isNaN(d[attributeX]) && d[attributeY] !== null && !isNaN(d[attributeY]);
                    }), function (d) {
                        return d[attributeX];
                    }) - axisOffset[attributeType.x], d3.max(dataRequested[0], function (d) {
                        return d[attributeX];
                    }) + axisOffset[attributeType.x]])
                    .range([0, 300]),
                yAxis = d3.scaleLinear()
                    .domain([d3.min(dataRequested[0].filter(function (d) {
                        return d[attributeX] !== null && !isNaN(d[attributeX]) && d[attributeY] !== null && !isNaN(d[attributeY]);
                    }), function (d) {
                        return d[attributeY];
                    }) - axisOffset[attributeType.y], d3.max(dataRequested[0], function (d) { return d[attributeY]; }) + axisOffset[attributeType.y]])
                    .range([180, 0]),
                xAxisOrientation = d3.axisBottom(xAxis),
                yAxisOrientation = d3.axisLeft(yAxis),
                transitionNumber = 0,
                chart = d3.select(".canvas > g")
                    .selectAll(".circle,.selectCircle")
                    .attr("class", function (d) {
                        mouseOut(d, this);
                        return "circle";
                    })
                    .data(dataRequested[0].filter(function (d) {
                        return d[attributeX] !== null && !isNaN(d[attributeX]) && d[attributeY] !== null && !isNaN(d[attributeY]);
                    }));
            d3.select(".plotContainer")
                .call(zoomCircle.transform, d3.zoomIdentity.translate(0, 0).scale(1))
                .on("wheel", function () {
                    d3.event.preventDefault();
                });
            zoomCircle = d3.zoom()
                .scaleExtent([1, 10])
                /*.on("start", function () {
                    disableEvents();
                })*/
                .on("zoom", function () { zoomCircles(xAxisOrientation, yAxisOrientation, xAxis, yAxis); });
                /*.on("end", function () {
                    enableEvents();
                })*/
            scale = d3.zoomTransform(d3.select(".plotContainer").node()).k;
            chart.exit()
                .remove();
            chart.enter()
                .append("circle")
                .attr("class", "circle")
                .style("cursor", "pointer")
                .merge(chart)
                .on("mouseover", function (d) {
                    var id = circleType === "degree" ? this.id.split(",")[0] : this.id.split(",")[0] + '\\,' + this.id.split(",")[1];
                    ScatterPlot.scrollIntoView(id);
                    mouseOver(d, this);
                    ScatterPlot.tooltip(d);
                })
                .on("mouseout", function (d) {
                    if (d3.select(this).classed("circle")) {
                        mouseOut(d, this);
                    } else {
                        selectMouseOut(this);
                    }
                    d3.select(".tooltip")
                        .style("visibility", "hidden");
                })
                .on("mousedown", function (d) {
                    if (d3.event.defaultPrevented) { return; }
                    var ev = event,
                        selection = d3.select(this),
                        circle = this,
                        id,
                        type = circleType === "degree" ? "main" : "sub";
                    if (click === 1) {
                        click = 0;
                        clearTimeout(delay);
                    } else {
                        delay = setTimeout(function () {
                            click = 0;
                            /*if (circleType === "degree") {
                                updateAttributes("course");
                                d3.select(".tooltip")
                                    .style("visibility", "hidden");
                                d3.select(".pillContainer").remove();
                                drawPill([[d[Table.getAggregation() + "Acronym"], "firstLabel"]]);
                                dispatcher(ScatterPlot.update, [{"courses": [Table.getAggregation() + "Acronym=" + d[Table.getAggregation() + "Acronym"]]}]);
                            }*/
                            highlight(selection, "circle", selection.node().id, type, d, ev);
                        }, 150);
                        click = 1;
                    }
                })
                .transition()
                .duration(1000)
                .attr("id", function (d) {
                    var aggregation = Table.getAggregation() === "degree" ? "course" : "degree",
                        id = circleType === "degree" ? d[Table.getAggregation() + "Acronym"] + ',' + d.year + ',' + d.term : d[Table.getAggregation() + "Acronym"] + ',' + d[aggregation + "Acronym"] + ',' + d.year + ',' + d.term;
                    return id;
                })
                .attr("cx", function (d) {
                    return xAxis(d[attributeX]);
                })
                .attr("cy", function (d) {
                    return yAxis(d[attributeY]);
                })
                /*.attr("class", function (d) {
                    var id = this.id.replace(new RegExp(",", 'g'), "\\,"),
                        selection;
                    if (id !== "") {
                        selection = d3.selectAll("#" + id).filter("[class^=select]");
                        if (selection.empty()) {
                            return "circle";
                        } else {
                            return "selectCircle";
                        }
                    }
                })*/
                .attr("opacity", 0.3)
                .attr("r", 2.5 / scale)
                .style("fill", circleColor)
                .on("start", function () {
                    d3.select(".plotContainer").call(d3.zoom().on("zoom", null));
                    transitionNumber += 1;
                })
                .on("end", function () {
                    transitionNumber -= 1;
                    if (transitionNumber === 0) {
                        enableEvents();
                        d3.selectAll(".circle,selectCircle")
                            .attr("class", function (d, i) {
                                var selected = getSelected(),
                                    ev = event;
                                if (selected.indexOf(this.id) > -1) {
                                    clicked(d, this);
                                    return "selectCircle";
                                }
                                return "circle";
                            });
                    }
                });
            d3.select(".xAxis").transition()
                .duration(1000).call(xAxisOrientation);
            d3.select(".yAxis").transition()
                .duration(1000).call(yAxisOrientation);
            d3.select(".xLabel")
                .text(display[attributeType.x]);
            d3.select(".labelXContainer > rect")
                .attr("x", d3.select(".xLabel").node().getBBox().x - 5)
                .attr("width", d3.select(".xLabel").node().getBBox().width + 5 * 2);
            d3.select(".yLabel")
                .text(display[attributeType.y]);
            d3.select(".labelYContainer > rect")
                .attr("x", d3.select(".yLabel").node().getBBox().x - 5)
                .attr("width", d3.select(".yLabel").node().getBBox().width + 5 * 2);
            if (d3.selectAll(".circle").empty()) {
                d3.select("#nodata").attr("opacity", 0.3);
            } else {
                d3.select("#nodata").attr("opacity", 0);
            }
            adjustViews();
            /*d3.selectAll(".xAxis > .tick")
                .filter(function (d, i, j) {
                    if (i + 1 === j.length) {
                        return this;
                    }
                })
                .style("visibility", "hidden");
            d3.selectAll(".yAxis > .tick")
                .filter(function (d, i, j) {
                    if (i + 1 === j.length) {
                        return this;
                    }
                })
                .style("visibility", "hidden");*/
        },
        
        draw: function (dataRequested) {
            var width = $(window).outerWidth() - 20,
                svgWidth = 350,
                svgHeight = 220,
                posX = parseInt(d3.select("table")
                    .style("width")
                    .split("px")[0], 10),
                height = parseInt(d3.select(".container")
                    .style("height")
                    .split("px")[0], 10),
                xAxis = d3.scaleLinear()
                    .domain([d3.min(dataRequested[0].filter(function (d) {
                        return d[attributeX] !== null && !isNaN(d[attributeX]) && d[attributeY] !== null && !isNaN(d[attributeY]);
                    }), function (d) {
                        return d[attributeX];
                    }) - axisOffset[attributeType.x], d3.max(dataRequested[0], function (d) {
                        return d[attributeX];
                    }) + axisOffset[attributeType.x]])
                    .range([0, 300]),
                yAxis = d3.scaleLinear()
                    .domain([d3.min(dataRequested[0].filter(function (d) {
                        return d[attributeX] !== null && !isNaN(d[attributeX]) && d[attributeY] !== null && !isNaN(d[attributeY]);
                    }), function (d) {
                        return d[attributeY];
                    }) - axisOffset[attributeType.y], d3.max(dataRequested[0], function (d) { return d[attributeY]; }) + axisOffset[attributeType.y]])
                    .range([180, 0]),
                xAxisOrientation = d3.axisBottom(xAxis),
                yAxisOrientation = d3.axisLeft(yAxis),
                chart,
                canvas;
            currentData = dataRequested;
            zoomCircle = d3.zoom()
                .scaleExtent([1, 10])
                /*.on("start", function () {
                    disableEvents();
                })*/
                .on("zoom", function () { zoomCircles(xAxisOrientation, yAxisOrientation, xAxis, yAxis); });
                /*.on("end", function () {
                    enableEvents();
                })*/
            chart = d3.select("body")
                .append("svg")
                .attr("width", svgWidth)
                .attr("height", svgHeight)
                .attr("class", "plotContainer")
                .style("position", "fixed")
                .style("cursor", "default")
                .style("left", posX + 15 + "px")
                .style("top", height + 10)
                .call(zoomCircle)
                .on("wheel", function () {
                    d3.event.preventDefault();
                })
                .append("g")
                .attr("class", "scatterPlot")
                .attr("transform", "translate(" + 31 + "," + 5 + ")");
            scale = d3.zoomTransform(d3.select(".plotContainer").node()).k;
            chart
                .append('g')
                .attr('transform', 'translate(0,' + (svgHeight - 40) + ')')
                .attr('class', 'xAxis')
                .call(xAxisOrientation);
            chart
                .append("svg")
                .attr("class", "labelXContainer")
                .append("rect");
            d3.select(".labelXContainer")
                .append("text")
                .attr("class", "xLabel")
                .attr("x", svgWidth - 40)
                .attr("y", svgHeight - 10)
                .style("text-anchor", "end")
                .style("cursor", "pointer")
                .text(display[attributeType.x])
                .on("mousedown", function () {
                    labelToggle("x");
                })
                .on("mouseover", function () {
                    d3.select(".labelXContainer > rect")
                        .style("fill", "rgba(135, 185, 201, 0.2)");
                })
                .on("mouseout", function () {
                    d3.select(".labelXContainer > rect")
                        .style("fill", "none");
                });
            d3.select(".labelXContainer > rect")
                .attr("x", d3.select(".xLabel").node().getBBox().x - 5)
                .attr("y", svgHeight - 21)
                .attr("height", 15)
                .attr("width", d3.select(".xLabel").node().getBBox().width + 5 * 2)
                .style("stroke", "grey")
                .style("fill", "none")
                .style("stroke-width", 1)
                .on("mouseover", function () {
                    d3.select(".labelXContainer > rect")
                        .style("fill", "rgba(135, 185, 201, 0.2)");
                })
                .on("mouseout", function () {
                    d3.select(".labelXContainer > rect")
                        .style("fill", "none");
                });
            chart.append('g')
                .attr('transform', 'translate(0,0)')
                .attr('class', 'yAxis')
                .call(yAxisOrientation);
            chart
                .append("svg")
                .attr("class", "labelYContainer")
                .append("rect");
            d3.select(".labelYContainer")
                .append("text")
                .attr("class", "yLabel")
                .attr("x", 10)
                .attr("y", 11)
                .style("cursor", "pointer")
                .on("mousedown", function () {
                    labelToggle("y");
                })
                .on("mouseover", function () {
                    d3.select(".labelYContainer > rect")
                        .style("fill", "rgba(135, 185, 201, 0.2)");
                })
                .on("mouseout", function () {
                    d3.select(".labelYContainer > rect")
                        .style("fill", "none");
                })
                .text(display[attributeType.y]);
            d3.select(".labelYContainer > rect")
                .attr("x", d3.select(".yLabel").node().getBBox().x - 5)
                .attr("y", 1)
                .attr("height", 15)
                .attr("width", d3.select(".yLabel").node().getBBox().width + 5 * 2)
                .style("stroke", "grey")
                .style("fill", "none")
                .style("stroke-width", 1)
                .on("mouseover", function () {
                    d3.select(".labelYContainer > rect")
                        .style("fill", "rgba(135, 185, 201, 0.2)");
                })
                .on("mouseout", function () {
                    d3.select(".labelYContainer > rect")
                        .style("fill", "none");
                });
            canvas = chart.append('svg')
                .attr("class", "canvas")
                .attr("width", 330)
                .attr("height", svgHeight - 40)
                .append("g")
                .attr("width", 330)
                .attr("height", svgHeight - 40);
            noDataText();
            canvas.selectAll(".circle")
                .data(dataRequested[0].filter(function (d) {
                    return d[attributeX] !== null && d[attributeY] !== null;
                }))
                .enter().append("circle")
                .attr("class", "circle")
                .attr("id", function (d) {
                    return d.degreeAcronym + ',' + d.year + ',' + d.term;
                })
                .attr("r", 2.5 / scale)
                .on("mouseover", function (d) {
                    var id = circleType === "degree" ? this.id.split(",")[0] : this.id.split(",")[0] + '\\,' + this.id.split(",")[1];
                    ScatterPlot.scrollIntoView(id);
                    mouseOver(d, this);
                    ScatterPlot.tooltip(d);
                })
                .on("mouseout", function (d) {
                    if (d3.select(this).classed("circle")) {
                        mouseOut(d, this);
                    } else {
                        selectMouseOut(this);
                    }
                    d3.select(".tooltip")
                        .style("visibility", "hidden");
                })
                .on("mousedown", function (d) {
                    if (d3.event.defaultPrevented) { return; }
                    var ev = event,
                        selection = d3.select(this),
                        circle = this,
                        id,
                        type = circleType === "degree" ? "main" : "sub";
                    if (click === 1) {
                        click = 0;
                        clearTimeout(delay);
                    } else {
                        delay = setTimeout(function () {
                            click = 0;
                            /*if (circleType === "degree") {
                                updateAttributes("course");
                                d3.select(".tooltip")
                                    .style("visibility", "hidden");
                                d3.select(".pillContainer").remove();
                                drawPill([[d[Table.getAggregation() + "Acronym"], "firstLabel"]]);
                                dispatcher(ScatterPlot.update, [{"courses": [Table.getAggregation() + "Acronym=" + d[Table.getAggregation() + "Acronym"]]}]);
                            }*/
                            highlight(selection, "circle", selection.node().id, type, d, ev);
                        }, 150);
                        click = 1;
                    }
                })
                .attr("cx", function (d) {
                    return xAxis(d[attributeX]);
                })
                .attr("cy", function (d) {
                    return yAxis(d[attributeY]);
                })
                .style("opacity", 0.3)
                .style("cursor", "pointer")
                .style("fill", circleColor);
            /*d3.selectAll(".xAxis > .tick")
                .filter(function (d, i, j) {
                    if (i + 1 === j.length) {
                        return this;
                    }
                })
                .style("visibility", "hidden");
            d3.selectAll(".yAxis > .tick")
                .filter(function (d, i, j) {
                    if (i + 1 === j.length) {
                        return this;
                    }
                })
                .style("visibility", "hidden");*/
        },
        
        scrollIntoView: function (id) {
            var element = d3.selectAll("#" + id).filter("tr").node(),
                scrollPos;
            if (element) {
                scrollPos = element.getBoundingClientRect().top + window.pageYOffset - (window.innerHeight / 2);
                window.scrollTo(0, scrollPos);
            }
        },
        
        getZoom: function () {
            return zoomCircle;
        },
        
        getScale: function () {
            return scale;
        },
        
        getCircleType: function () {
            return circleType;
        },
        
        setCircleType: function (type) {
            updateAttributes(type);
        }
    };
}());