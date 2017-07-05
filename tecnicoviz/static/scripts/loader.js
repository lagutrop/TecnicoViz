/*global d3, dispatcher, ScatterPlot, Table, LineChart, BarChart, $*/

var selected = [];

function init() {
    "use strict";
    Table.approval();
    Table.degree();
    dispatcher(Table.draw, [{"degrees": ""}, {"terms": ""}]);
}

function setSelected(id) {
    "use strict";
    selected.push(id);
}

function getSelected() {
    "use strict";
    return selected;
}

function removeSelected(id) {
    "use strict";
    selected.splice(selected.indexOf(id), 1);
}

function adjustViews() {
    "use strict";
    var tableY = parseInt(d3.select(".container").style("height"), 10) + 20,
        headY = parseInt(d3.select(".container").style("height"), 10) + 10,
        height;
    d3.select("thead")
        .attr("style", "top:" + headY + "px");
    d3.select("table")
        .transition()
        .duration(200)
        .attr("style", "top:" + tableY + "px");
    d3.select(".plotContainer")
        .transition()
        .duration(200)
        .style("top", headY + "px");
    if (!d3.select(".lineContainerCompare").empty()) {
        height = parseInt(d3.select(".plotContainer").style("height"), 10) + headY;
        d3.select(".lineContainerCompare")
            .transition()
            .duration(200)
            .style("top", height + "px");
        d3.select(".linePillContainer")
            .transition()
            .duration(200)
            .style("top", parseInt(d3.select(".lineContainerCompare").style("height"), 10) + height + "px");
    }
}

function requestOperators(name) {
    'use strict';
    var filtered = d3.selectAll(".pill.filter").nodes(),
        element = d3.select("#" + name + ".pill.filter").node();
    if (filtered.indexOf(element) > -1) {
        return "~ct~";
    }
    return "";
}

function getFilteredAcronym() {
    "use strict";
    var acronym = [],
        courses = '',
        degrees = '',
        filteredDegrees = d3.selectAll(".pill.firstLabel").nodes(),
        filteredCourses = d3.selectAll(".pill.secondLabel").nodes();
    if (filteredCourses.length !== 0) {
        filteredCourses.forEach(function (d, i) {
            if (i + 1 < filteredCourses.length) {
                courses += requestOperators(d.childNodes[0].data) + d.childNodes[0].data + ',';
            } else {
                courses += requestOperators(d.childNodes[0].data) + d.childNodes[0].data;
            }
        });
    }
    if (filteredDegrees.length !== 0) {
        filteredDegrees.forEach(function (d, i) {
            if (i + 1 < filteredDegrees.length) {
                degrees += requestOperators(d.childNodes[0].data) + d.childNodes[0].data + ',';
            } else {
                degrees += requestOperators(d.childNodes[0].data) + d.childNodes[0].data;
            }
        });
    }
    acronym.push(degrees, courses);
    return acronym;
}

function mouseOver(d, element, ev) {
    "use strict";
    var id = element.id.replace(new RegExp(",", 'g'), "\\,"),
        e = ev || event,
        tableElement = d3.selectAll("#" + id + ".cell, #" + id + ".selectCell")
            .filter(function () {
                return !d3.select(this).classed("summarization");
            }),
        posX = e.changedTouches === undefined ? e.pageX : e.changedTouches[0].pageX,
        posY = ((e.changedTouches === undefined) ? e.pageY : e.changedTouches[0].pageY) - $(window).scrollTop();
    if (!tableElement.empty()) {
        Table.cellMouseOver(d, tableElement.node(), Table.getAttribute());
        Table.mouseOverColumn($(tableElement.node()).parents().eq(1)[0]);
        Table.lineMouseOver($(tableElement.node()).parents().eq(2)[0]);
    }
    if (!d3.selectAll("#" + id + ".circle, #" + id + ".selectCircle").empty()) {
        ScatterPlot.circleMouseOver(d, d3.selectAll("#" + id + ".circle, #" + id + ".selectCircle").node());
    }
    if (!d3.selectAll("#" + id + ".lineCircle, #" + id + ".selectLineCircle").empty()) {
        LineChart.circleMouseOver(d, d3.selectAll("#" + id + ".lineCircle, #" + id + ".selectLineCircle").nodes());
    }
    if (!d3.selectAll("#" + id + ".lineCompareCircle, #" + id + ".selectLineCompareCircle").empty()) {
        LineChart.circleMouseOver(d, d3.selectAll("#" + id + ".lineCompareCircle, #" + id + ".selectLineCompareCircle").nodes());
    }
    if (!d3.selectAll("#" + id + ".bar, #" + id + ".selectBar").empty()) {
        BarChart.mouseOver(d, d3.selectAll("#" + id + ".bar, #" + id + ".selectBar").nodes());
    }
}

function selectMouseOut(element) {
    "use strict";
    var id = element.id.replace(new RegExp(",", 'g'), "\\,"),
        tableElement = d3.selectAll("#" + id + ".cell, #" + id + ".selectCell")
            .filter(function () {
                return !d3.select(this).classed("summarization");
            });
    if (!tableElement.empty()) {
        Table.mouseOutColumn($(tableElement.node()).parents().eq(1)[0]);
        Table.lineMouseOut($(tableElement.node()).parents().eq(2)[0]);
    }
}

function clicked(d, element, ev) {
    "use strict";
    var id = element.id.replace(new RegExp(",", 'g'), "\\,"),
        e = ev || event,
        tableElement = d3.selectAll("#" + id + ".cell, #" + id + ".selectCell")
            .filter(function () {
                return !d3.select(this).classed("summarization");
            });
    if (!d3.selectAll("#" + id + ".circle, #" + id + ".selectCircle").empty()) {
        ScatterPlot.circleMouseOver(d, d3.selectAll("#" + id + ".circle, #" + id + ".selectCircle").node());
    }
    if (!d3.selectAll("#" + id + ".lineCircle, #" + id + ".selectLineCircle").empty()) {
        LineChart.circleMouseOver(d, d3.selectAll("#" + id + ".lineCircle, #" + id + ".selectLineCircle").nodes());
    }
    if (!d3.selectAll("#" + id + ".lineCompareCircle, #" + id + ".selectLineCompareCircle").empty()) {
        LineChart.circleMouseOver(d, d3.selectAll("#" + id + ".lineCompareCircle, #" + id + ".selectLineCompareCircle").nodes());
    }
    if (!d3.selectAll("#" + id + ".bar, #" + id + ".selectBar").empty()) {
        BarChart.mouseOver(d, d3.selectAll("#" + id + ".bar, #" + id + ".selectBar").nodes());
    }
    if (!tableElement.empty()) {
        Table.cellMouseOver(d, tableElement.node(), Table.getAttribute());
        Table.mouseOutColumn($(tableElement.node()).parents().eq(1)[0]);
        Table.lineMouseOut($(tableElement.node()).parents().eq(2)[0]);
    }
}

function touchDevice() {
    "use strict";
    return !!window.navigator.maxTouchPoints;
}

function mouseOut(d, element) {
    "use strict";
    var id = element.id.replace(new RegExp(",", 'g'), "\\,"),
        tableElement = d3.selectAll("#" + id + ".cell")
            .filter(function () {
                return !d3.select(this).classed("summarization");
            });
    if (!tableElement.empty()) {
        Table.cellMouseOut(d, tableElement.node(), Table.getAttribute());
        Table.mouseOutColumn($(tableElement.node()).parents().eq(1)[0]);
        Table.lineMouseOut($(tableElement.node()).parents().eq(2)[0]);
    }
    if (!d3.selectAll("#" + id + ".circle").empty()) {
        ScatterPlot.circleMouseOut(d, d3.selectAll("#" + id + ".circle").node());
    }
    if (!d3.selectAll("#" + id + ".lineCircle").empty()) {
        LineChart.circleMouseOut(d, d3.selectAll(".lineCircle#" + id).nodes());
    }
    if (!d3.selectAll("#" + id + ".lineCompareCircle").empty()) {
        LineChart.circleMouseOut(d, d3.selectAll(".lineCompareCircle#" + id).nodes());
    }
    if (!d3.selectAll("#" + id + ".bar").empty()) {
        BarChart.mouseOut(d, d3.selectAll(".bar#" + id).nodes());
    }
}

function highlight(element, elementClass, id, type, d, ev) {
    "use strict";
    if (element.classed(elementClass)) {
        d3.selectAll(".cell#" + id.replace(new RegExp(",", 'g'), "\\,")).attr("class", "selectCell");
        d3.selectAll(".circle#" + id.replace(new RegExp(",", 'g'), "\\,")).attr("class", "selectCircle");
        d3.selectAll(".lineCircle#" + id.replace(new RegExp(",", 'g'), "\\,")).attr("class", "selectLineCircle");
        d3.selectAll(".lineCompareCircle#" + id.replace(new RegExp(",", 'g'), "\\,")).attr("class", "selectLineCompareCircle");
        d3.selectAll(".bar#" + id.replace(new RegExp(",", 'g'), "\\,")).attr("class", "selectBar");
        clicked(d, element.node(), ev);
        setSelected(element.node().id);
    } else {
        d3.selectAll(".selectCircle#" + id.replace(new RegExp(",", 'g'), "\\,")).attr("class", "circle");
        d3.selectAll(".selectLineCircle#" + id.replace(new RegExp(",", 'g'), "\\,")).attr("class", "lineCircle");
        d3.selectAll(".selectLineCompareCircle#" + id.replace(new RegExp(",", 'g'), "\\,")).attr("class", "lineCompareCircle");
        d3.selectAll(".selectCell#" + id.replace(new RegExp(",", 'g'), "\\,")).attr("class", "cell " + type);
        d3.selectAll(".selectBar#" + id.replace(new RegExp(",", 'g'), "\\,")).attr("class", "bar");
        mouseOut(d, element.node());
        removeSelected(element.node().id);
    }
}

function linePill() {
    "use strict";
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
        return [argsUpdate, concatenatedAcronym];
    } else {
        return [[{"teachers": ["degreeAcronym="]}]];
    }
}

function parseAcronym() {
    "use strict";
    var firstIndex = Table.getAggregation() === "course" ? 0 : 1,
        secondIndex = Table.getAggregation() === "course" ? 1 : 0,
        acronym = getFilteredAcronym(),
        requestCourse = acronym[firstIndex] === '' ? '' : ["courseAcronym=" + acronym[firstIndex]],
        requestDegree = acronym[secondIndex] === '' ? '' : ["degreeAcronym=" + acronym[secondIndex]],
        request = requestCourse === '' ? [{"degrees": requestDegree}, {"terms": ""}] : [{"degrees": requestDegree}, {"terms": ""}, {"courses": requestCourse.concat(requestDegree)}];
    return request;
}

function pillGrouping(courseLabel) {
    "use strict";
    var firstLabels = d3.selectAll(".pill.firstLabel"),
        secondLabels = d3.selectAll(".pill.secondLabel");
    firstLabels.classed("firstLabel", false).classed("secondLabel", true);
    secondLabels.classed("secondLabel", false).classed("firstLabel", true);
}


function courseAggregationSwitch() {
    "use strict";
    var courseLabel = Table.getAggregation() === "degree" ? "secondLabel" : "firstLabel",
        acronym = '',
        request;
    if (!d3.select(".pillContainer").selectAll(".pill." + courseLabel).empty()) {
        d3.selectAll(".pill." + courseLabel)
            .nodes()
            .forEach(function (d, i) {
                if (i + 1 === d3.selectAll(".pill." + courseLabel).nodes().length) {
                    acronym += d3.select(d.childNodes[0]).text();
                } else {
                    acronym += d3.select(d.childNodes[0]).text() + ',';
                }
            });
        request = parseAcronym();
        if (Table.getAggregation() === "degree") {
            pillGrouping();
        }
        Table.course();
    } else {
        request = parseAcronym();
        if (Table.getAggregation() === "course") {
            pillGrouping();
        }
        Table.degree();
    }
}

function updatePill() {
    "use strict";
    var container = d3.select(".container");
    return container;
}

function createPill(label) {
    "use strict";
    //draw filtering pill
    var container = d3.select(".container");
    container.data([label]).enter();
    container
        .append("div")
        .attr("class", "pillContainer")
        .append("div")
        .attr("class", "clearpill")
        .text("Clear all")
        .on("click", function () {
            label = "";
            d3.select(".container").data([label]).enter();
            Table.degree();
            d3.selectAll(".pillContainer").remove();
            courseAggregationSwitch();
            adjustViews();
            dispatcher(Table.draw, [{"degrees": ""}, {"terms": ""}]);
        })
        .style("opacity", 0.0).transition().duration(600).style("opacity", 1.0);
    return container;
}

function drawPill(firstLabel) {
    "use strict";
    var container,
        request,
        containerData,
        label = firstLabel.map(function (d) {return d[0].toUpperCase(); });
    if (d3.select(".pill").empty() && firstLabel.length > 0) {
        container = createPill(label);
    } else {
        container = updatePill();
    }
    containerData = container.data()[0];
    container.select(".pillContainer")
        .selectAll(".pill")
        .data(firstLabel, function (d) { return d[0]; })
        .enter()
        .insert("div", ".clearpill")
        .attr("id", function (d) { return d[0].toUpperCase(); })
        .attr("class", function (d) {
            return "pill " + d[1];
        })
        .text(function (d) { return d[0].toUpperCase(); })
        .append("span")
        .attr("class", "closebtn")
        .text("x")
        .on("click", function () {
            var selector = this.parentElement,
                elementPos = label.indexOf(d3.select(selector.childNodes[0]).text()),
                element;
            selector.remove();
            container.data([label]).enter();
            element = d3.selectAll("div").nodes().filter(function (d) {
                return d.id === label[elementPos] || d.id.indexOf(',' + label[elementPos]) !== -1;
            });
            if (elementPos !== -1) {
                label.splice(elementPos, 1);
                firstLabel.splice(elementPos, 1);
                if (d3.select(".pill").empty()) {
                    d3.selectAll(".pillContainer").remove();
                    Table.degree();
                }
                courseAggregationSwitch();
                request = parseAcronym();
                dispatcher(Table.draw, request);
            }
            adjustViews();
        })
        .style("opacity", 0.0).transition().duration(600).style("opacity", 1.0);
}

function filterType(data, element) {
    "use strict";
    var type,
        request;
    if (Table.getAggregation() === "degree") {
        type = data[0].length === 0 ? "secondLabel" : "firstLabel";
    } else {
        type = data[0].length === 0 ? "firstLabel" : "secondLabel";
    }
    drawPill([[element[0].toUpperCase(), type + " filter"]]);
    adjustViews();
    request = parseAcronym();
    dispatcher(Table.draw, request);
    courseAggregationSwitch();
}

function keyboardFilter(el) {
    "use strict";
    var modifiedSelection = [];
    if (d3.select("#" + el.toUpperCase() + ".pill").empty()) {
        modifiedSelection.push(el);
    }
    if (modifiedSelection.length > 0) {
        dispatcher(filterType, [{"degrees": ["degreeAcronym=~ct~" + el]}], [el]);
        
    }
    /*var filter = element.value.toUpperCase(),
        currentRow;
    d3.selectAll(".mainrow")
        .each(function (d) {
            currentRow = d.key.toUpperCase();
            if (currentRow.indexOf(filter) === -1 && (d.values[0].degreeType + ' em ' + d.values[0][Table.getAggregation() + "Name"]).toUpperCase().indexOf(filter) === -1) {
                d3.selectAll(".mainrow, .row, .circle").filter("[id^='" + d.key + "']")
                    .style("display", "none");
            } else {
                d3.selectAll(".mainrow, .row, .circle").filter("[id^='" + d.key + "']")
                    .style("display", "");
            }
        });*/
}

function enableEvents() {
    "use strict";
    var aggregationData = Table.getAggregation() === "degree" ? "courseName" : "degreeName";
    d3.selectAll(".firstTextLabel")
        .on("mouseover", function (d) {
            var tooltipText = Table.getAggregation() === "degree" ? d.values[0].degreeType + ' em ' + d.values[0][Table.getAggregation() + "Name"] : d.values[0][Table.getAggregation() + "Name"];
            Table.bodyMouseOver(tooltipText);
        })
        .on("mouseout", function () {
            d3.select(".tooltip")
                .style("visibility", "hidden");
        });
    d3.selectAll(".secondTextLabel")
        .on("mouseover", function (d) {
            var tooltipText = Table.getAggregation() === "degree" ? d.values[0][aggregationData] : d.values[0].degreeType + ' em ' + d.values[0][aggregationData];
            Table.bodyMouseOver(tooltipText);
        })
        .on("mouseout", function () {
            d3.select(".tooltip")
                .style("visibility", "hidden");
        });
    d3.selectAll(".cell.sub")
        .on("mouseover", function (d) { if (d) {
            var attribute = Table.getAttribute(),
                format = d3.format(",");
            if (d[attribute] || d[attribute] === 0) {
                mouseOver(d, this);
                Table.bodyMouseOver(Table.display(attribute) + ": " + d[attribute] + Table.getLabel() + '<br>' + "Enrollments: " + format(d.studentsNumber));
            }
        } })
        .on("mouseout", function (d) {
            if (d && d3.select(this).classed("cell")) {
                mouseOut(d, this);
            }
            d3.select(".tooltip")
                .style("visibility", "hidden");
        });
    d3.selectAll(".cell.main")
        .on("mouseover", function (d) {
            var attribute = Table.getAttribute(),
                format = d3.format(",");
            if (d) {
                if (d[attribute + "Average"] || d[attribute + "Average"] === 0) {
                    mouseOver(d, this);
                    Table.bodyMouseOver(Table.display(attribute) + ": " + d[attribute + "Average"] + Table.getLabel() + '<br>' + "Enrollments: " + format(d.studentsNumberAverage));
                }
            }
        })
        .on("mouseout", function (d) {
            if (d && d3.select(this).classed("cell")) {
                mouseOut(d, this);
            }
            d3.select(".tooltip")
                .style("visibility", "hidden");
        });
    d3.selectAll(".cell.sub.summarization")
        .on("mouseover", function (d) {
            var format = d3.format(".2f"),
                attribute = Table.getAttribute(),
                studentsFormat = d3.format(","),
                average = parseFloat(format(d3.mean(d.values, function (f) {
                    return f[attribute];
                }))),
                students = parseFloat(format(d3.sum(d.values, function (f) {
                    return f.studentsNumber;
                })));
            Table.bodyMouseOver(Table.display(attribute) + ": " + average + Table.getLabel() + '<br>' + "Enrollments: " + studentsFormat(students));
            d3.select(this)
                .select("rect")
                .style("stroke", "black")
                .style("stroke-width", "4px");
        });
    d3.selectAll(".cell.main.summarization")
        .on("mouseover", function (d) {
            var format = d3.format(".2f"),
                attribute = Table.getAttribute(),
                years = [],
                studentsFormat = d3.format(","),
                average = parseFloat(format(d3.mean(d.values, function (f) {
                    return f[attribute + "Average"];
                }))),
                students = parseFloat(format(d3.sum(d.values, function (f) {
                    if (years.indexOf(f.year + "," + f.term) === -1) {
                        years.push(f.year + "," + f.term);
                        return f.studentsNumberAverage;
                    }
                })));
            Table.bodyMouseOver(Table.display(attribute) + ": " + average + Table.getLabel() + '<br>' + "Enrollments: " + studentsFormat(students));
            d3.select(this)
                .select("rect")
                .style("stroke", "black")
                .style("stroke-width", "4px");
        });
    d3.select("tbody").selectAll(".mainrow")
        .on("mouseover", function () {
            Table.lineMouseOver(this);
        })
        .on("mouseout", function () {
            Table.lineMouseOut(this);
        });
    d3.select("tbody").selectAll(".row")
        .on("mouseover", function () {
            var posX = event.changedTouches === undefined ? event.pageX : event.changedTouches[0].pageX,
                posY = ((event.changedTouches === undefined) ? event.pageY : event.changedTouches[0].pageY) - $(window).scrollTop();
            Table.lineMouseOver(this);
        })
        .on("mouseout", function () {
            Table.lineMouseOut(this);
        });
    d3.selectAll("tr").selectAll("td").filter("[class^=col_]")
        .on("mouseover", function () {
            Table.mouseOverColumn(this);
        })
        .on("mouseout", function () {
            Table.mouseOutColumn(this);
        });
    d3.select(".inputField").style("outline", null);
    d3.selectAll(".circle")
        .on("mouseover", function (d) {
            var id = ScatterPlot.getCircleType() === "degree" ? this.id.split(",")[0] : this.id.split(",")[0] + '\\,' + this.id.split(",")[1];
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
        });
    d3.selectAll(".lineCircle")
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
        });
    d3.selectAll(".bar")
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
        });
    d3.select(".plotContainer").call(ScatterPlot.getZoom());
}

function disableEvents() {
    "use strict";
    d3.select(".inputField").style("outline", "none");
    d3.selectAll(".firstTextLabel, .secondTextLabel")
        .on("mouseover", null)
        .on("mouseout", null);
    d3.selectAll(".cell.main,.cell.sub,.summarization")
        .on("mouseover", null)
        .on("mouseout", null)
        .style("stroke", "rgb(200, 200, 200)")
        .style("stroke-width", "2px");
    d3.select(".tooltip")
        .style("visibility", "hidden");
    d3.selectAll("[class^='col_']")
        .on("mouseover", null)
        .on("mouseout", null)
        .style("background-color", null);
    d3.selectAll("[class^='yearcol_'],[class^='termcol_']")
        .style("background-color", "antiquewhite");
    d3.select("tbody").selectAll("tr")
        .on("mouseover", null)
        .on("mouseout", null)
        .style("background-color", null);
    d3.selectAll(".circle, .lineCircle")
        .on("mouseover", null)
        .on("mouseout", null);
    d3.selectAll(".bar")
        .on("mouseover", null)
        .on("mouseout", null);
    d3.select(".plotContainer").call(d3.zoom().on("zoom", null));
}