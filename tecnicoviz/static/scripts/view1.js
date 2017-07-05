/*jslint devel: true, nomen: true*/
/*global d3, crossfilter, dispatcher, keyboardFilter, enableEvents, disableEvents, adjustViews, drawPill, getFilteredAcronym, parseAcronym, clicked, mouseOver, mouseOut, highlight, courseAggregationSwitch, touchDevice, BarChart, $*/

Array.prototype.containsArray = function (element) {
    "use strict";
    var i;
    if (!element) {
        return false;
    }
    if (this.length === 0) {
        return false;
    }
    for (i = 0; i < this.length; i += 1) {
        if (this[i].toString() === element.toString()) {
            return true;
        }
    }
    return false;
};

Array.prototype.removeDuplicate = function (element, attribute) {
    "use strict";
    var tempArray = [],
        attributes = [],
        i;
    for (i = 0; i < element.length; i += 1) {
        if (attributes.indexOf(element[i][attribute]) === -1) {
            tempArray.push(element[i]);
            attributes.push(element[i][attribute]);
        }
    }
    return tempArray;
};

var Table = (function (data) {
    "use strict";
    var dataRequested = data,
        attribute = '',
        aggregation = '',
        colorDomain = '',
        sorting = 'ascending',
        sortBy = 'Degrees',
        label = '',
        expandedRows = {"degree": [], "course": []},
        filteredData = [];
    
    function ignoreWhiteSpaceSort(a, b) {
        a = a.replace(new RegExp(' ', 'g'), '');
        b = b.replace(new RegExp(' ', 'g'), '');
        if (a < b) {
            return -1;
        }
        if (a > b) {
            return 1;
        }
        if (a === b) {
            return 0;
        }
    }
    
    function changeSorting(currentSort) {
        if (currentSort !== sortBy) {
            sorting = currentSort === "Degrees" ? 'ascending' : 'descending';
            sortBy = currentSort;
        } else {
            sorting = sorting === 'ascending' ? 'descending' : 'ascending';
        }
    }
    
    function inRange(value1, value2, item) {
        var elem = item._groups[0][0].getBoundingClientRect(),
            minX = elem.left,
            maxX = elem.right,
            minY = elem.top + window.scrollY,
            maxY = elem.bottom + window.scrollY;
        if (value1 >= minX && value1 <= maxX && value2 >= minY && value2 <= maxY) {
            return true;
        }
        return false;
    }

    function getElementsByArea(x, y, width, height) {
        var firstLabelNodes = d3.selectAll(".firstTextLabel").nodes(),
            secondLabelNodes = d3.selectAll(".secondTextLabel").nodes(),
            nodes = firstLabelNodes.concat(secondLabelNodes),
            boundaries,
            centerX,
            centerY;
        nodes.forEach(function (node) {
            boundaries = node.getBoundingClientRect();
            centerX = boundaries.left + boundaries.width / 4;
            centerY = boundaries.top + boundaries.width / 4 + window.scrollY;
            if (x <= centerX && centerX <= x + width && (y <= centerY && centerY <= y + height)) {
                d3.select(node).classed("selected", true);
            } else {
                d3.select(node).classed("selected", false);
            }
        });
    }

    function headerMouseOver(d, i, type, offset) {
        d3.select(".tooltip").style("left", d3.event.pageX + 10 + "px")
            .style("top", d3.event.pageY + "px")
            .style("visibility", function () {
                if (i > offset) { return "visible"; } else { return "hidden"; }
            })
            .text(function () {
                if (type === "Year") {
                    return type + " " + d + "/" + (parseInt(d, 10) + 1);
                } else {
                    return type + " " + d;
                }
            });
    }

    function dragRow(element, clone, mouseX, posY, mouseY, rowType) {
        d3.select(element.parentNode.parentNode.parentNode).nodes()[0].insertBefore(clone, d3.select(element.parentNode.parentNode).nodes()[0].nextSibling);
        d3.select(clone).attr("class", "copy");
        d3.select("body")
            .style("cursor", "move")
            .style("cursor", "grabbing")
            .style("cursor", "-moz-grabbing")
            .style("cursor", "-webkit-grabbing");
        d3.selectAll(".draggedRow")
            .style("top", function (d) {return posY + "px"; });
        d3.selectAll("td, th")
            .style("border-bottom", "none")
            .style("margin-bottom", "0px")
            .classed("switch", false);
        d3.select(document.elementFromPoint(mouseX, mouseY)).filter(function () {
            var row = d3.select(this.parentNode),
                mainrow,
                subRow,
                graph;
            if (rowType === 'subrow') {
                if (row.node().tagName.toLowerCase() === "tr") {
                    graph = d3.select("#" + row.attr("id") + ".infoChart").empty() ? mainrow = true : mainrow = !row.classed("mainrow");
                    graph = !row.classed("subExpanded") ? subRow = true : subRow = !row.classed("subExpanded");
                    return d3.select(this)
                        .node()
                        .tagName
                        .toLowerCase() === "td" && row.attr("id").indexOf(d3.select(".draggedRow").attr("id").split(',')[0]) > -1 && mainrow && subRow;
                }
            } else {
                var currentRow = this.parentNode,
                    rowId = this.tagName === "TD" ? currentRow.id.split(',')[0] : "none",
                    nodes = d3.selectAll("#" + rowId + ", [id^='" + rowId + ",']").filter("tr").nodes();
                return d3.select(this).attr("id") === Table.display(aggregation) + "s" || (d3.select(this).nodes()[0].tagName.toLowerCase() === "td" && currentRow === nodes[nodes.length - 1]);
            }
        })
            .style("border-bottom", "2px solid black")
            .style("margin-bottom", "-1px")
            .classed("switch", true);
    }

    function endDragRow(rowType, clone, belowRow) {
        var insertRow = d3.selectAll(".draggedRow"),
            targetRow = d3.select(".switch"),
            insert,
            subRows;
        if (targetRow.empty()) {
            insert = belowRow.nodes()[0];
            if (insert === null) {
                insert = d3.select("tbody").nodes()[0].lastChild;
            }
        } else {
            if (targetRow.attr("id") === Table.display(aggregation) + "s" && insertRow.classed("mainrow")) {
                insert = d3.select(".mainrow").nodes()[0];
            } else {
                insert = targetRow.nodes()[0].parentNode.nextSibling;
            }
        }
        clone.remove();
        insertRow.node().parentNode
            .insertBefore(insertRow.node(), insert);
        insertRow.classed("draggedRow", false);
        if (!d3.selectAll(".barRow").filter("[id^='" + insertRow.attr("id") + "']").empty()) {
            insertRow.node()
                .parentNode
                .insertBefore(d3.selectAll(".barRow").filter("[id^='" + insertRow.attr("id") + "']").node(), insertRow.node().nextSibling);
        }
        if (insertRow.classed("mainrow")) {
            subRows = d3.selectAll(".row").filter("[id^='" + insertRow.attr("id") + "']").each(function (d) {
            /*subRows.transition()
                .duration(400)
                .style('opacity', 0).ease(d3.easeLinear).on("end", function () {*/
                insertRow.node()
                    .parentNode
                    .insertBefore(this, insertRow.node().nextSibling);
                    /*subRows.transition()
                        .duration(400)
                        .style('opacity', 1)
                        .ease(d3.easeLinear);*/
                if (!d3.selectAll("#" + this.id.split(",")[0] + '\\,' + this.id.split(",")[1] + ".barRow").empty()) {
                    insertRow.node()
                        .parentNode
                        .insertBefore(d3.selectAll("#" + this.id.split(",")[0] + '\\,' + this.id.split(",")[1] + ".barRow").node(), this.nextSibling);
                }
                if (!d3.selectAll(".infoChart").filter("[id^='" + insertRow.attr("id") + "']").empty()) {
                    insertRow.node()
                        .parentNode
                        .insertBefore(d3.selectAll(".infoChart").filter("[id^='" + insertRow.attr("id") + "']").node(), insertRow.node().nextSibling);
                }
                //});
            });
            d3.selectAll(".row, .barRow").filter("[id^='" + insertRow.attr("id") + "']").sort(function (x, y) {
                var row1 = x.key.toUpperCase(),
                    row2 = y.key.toUpperCase();
                return d3.ascending(row1, row2);
            });
        }
        d3.select("body").style("cursor", "crosshair");
        targetRow.style("border-bottom", "none")
            .style("margin-bottom", "0px")
            .classed("switch", false);
        enableEvents();
    }
    
    function click(currentRow, name, acronym) {
        var secondColumn = aggregation === "degree" ? "course" : "degree",
            requestCourse = acronym[1] === '' ? [aggregation + "Acronym=" + name] : [aggregation + "Acronym=" + name, secondColumn + "Acronym=" + acronym[1]];
        dispatcher(Table.drawSubLevels, [{"courses": requestCourse}, {"terms": ""}], [currentRow]);
    }
    
    function clickSubRow(d) {
        var secondColumn = Table.getAggregation() === "degree" ? "course" : "degree",
            request = [Table.getAggregation() + "Acronym=" + d.key.split(",")[0], secondColumn + "Acronym=" + d.key.split(",")[1]];
        dispatcher(BarChart.draw, [{"teachers": request}, {"terms": ""}], [d.key.split(",")[0], d.key.split(",")[1]]);
    }
    
    function combineObjects(year, term) {
        var colec = [], i, j;
        for (i = 0; i < year.length; i += 1) {
            for (j = 0; j < term.length; j += 1) {
                var yearTerm = {};
                if (year[i] !== 2016) {
                    yearTerm.year = year[i];
                    yearTerm.term = term[j];
                    colec.push(yearTerm);
                }
            }
        }
        return colec;
    }
    
    function retrieveTerms(data) {
        // year axis
        var x_axis = d3.nest()
                    .key(function (d) { return d.year; })
                    .entries(data)
                    .map(function (d) { return parseInt(d.key, 10); })
                    .sort(),

            // term axis
            terms = d3.nest()
                        .key(function (d) {return d.term; })
                        .entries(data)
                        .map(function (d) {return parseInt(d.key, 10); })
                        .sort(),

            // term-years combination
            termsYears = combineObjects(x_axis, terms),
            labelData = combineObjects(x_axis, terms);
        x_axis.unshift("");
        x_axis = x_axis.filter(function (d) { return d < 2016; });
        return [x_axis, termsYears, labelData];
    }

    function nullSort(a, b, sort, aName, bName) {
        if (a === b) {
            return aName.localeCompare(bName);
        }
        if (a === undefined || a === null) {
            return 1;
        }
        if (b === undefined || b === null) {
            return -1;
        }
        if (sort === "ascending") {
            return a < b ? -1 : 1;
        }
        if (sort === "descending") {
            return a < b ? 1 : -1;
        }
    }
    
    function tableBody(cellData, firstLabel, termsYears, width, cellHeight, labelData) {
        firstLabel.sort(ignoreWhiteSpaceSort);
        // draw degree rows
        var acronym = getFilteredAcronym(),
            lastPos = null,
            dragged = false,
            belowRow,
            clone,
            mainRows = d3.select("table").append("tbody")
                .selectAll(".mainrow")
                .data(cellData)
                .enter()
                .append("tr")
                .attr("id", function (d) { return d.key; })
                .attr("class", "mainrow")
                .on("mouseover", function () {
                    Table.lineMouseOver(this);
                })
                .on("mouseout", function () {
                    Table.lineMouseOut(this);
                }),
            degreelabel = d3.select("table")
                .selectAll(".mainrow"),
            mainColumns,
            colors = ['#d73027', '#fc8d59', '#fee08b', '#ffffbf', '#d9ef8b', '#91cf60', '#1a9850'],
            colorScale = d3.scaleQuantile().domain(colorDomain).range(colors),
            bodyTd = degreelabel.append("td").style("min-width", "75px");

        bodyTd
            .append("div")
            .attr("class", function (d) {
                var pillNodes = [];
                d3.selectAll(".pill")
                    .nodes()
                    .forEach(function (d) {
                        pillNodes.push(d3.select(d.childNodes[0]).text());
                    });
                return "firstTextLabel";
            })
            .attr("id", function (d) { return d.key; })
            .style("cursor", "pointer")
            .style("display", "inline-block")
            .text(function (d) { return d.key; })
            .on("mouseover", function (d) {
                var tooltipText = aggregation === "degree" ?
                                    d.values[0].degreeType + ' em ' + d.values[0][aggregation + "Name"] :
                                    d.values[0][aggregation + "Name"];
                Table.bodyMouseOver(tooltipText);
            })
            .on("mouseout", function () { d3.select(".tooltip").style("visibility", "hidden"); });
        bodyTd
            .append("svg")
            .attr("width", width)
            .attr("height", cellHeight)
            .style("float", "right")
            .on("mouseover", function (d) {
                var format = d3.format(".2f"),
                    studentsFormat = d3.format(","),
                    years = [],
                    average = parseFloat(format(d3.mean(d.values, function (f) {
                        if (years.indexOf(f.year + "," + f.term) === -1) {
                            years.push(f.year + "," + f.term);
                            return f[attribute + "Average"];
                        }
                    }))),
                    students;
                years = [];
                students = parseFloat(format(d3.sum(d.values, function (f) {
                    if (years.indexOf(f.year + "," + f.term) === -1) {
                        years.push(f.year + "," + f.term);
                        return f.studentsNumberAverage;
                    }
                })));
                Table.bodyMouseOver(Table.display(attribute) + ": " + average + label + '<br>' + "Enrollments: " + studentsFormat(students));
                d3.select(this).select("rect").style("stroke", "black").style("stroke-width", "4px");
            })
            .on("mouseout", function () {
                d3.select(".tooltip")
                    .style("visibility", "hidden");
                d3.select(this)
                    .select("rect")
                    .style("stroke", "rgb(200, 200, 200)")
                    .style("stroke-width", "2px");
            })
            .append("rect")
            .attr("id", function (d) {
                return d.key;
            })
            .attr("class", "cell main summarization")
            .attr("width", width)
            .attr("height", cellHeight)
            .attr("cursor", "default")
            .style("fill", function (d) {
                var format = d3.format(".2f"),
                    average = parseFloat(format(d3.mean(d.values, function (f) {
                        return f[attribute + "Average"];
                    })));
                return colorScale(average);
            });
        degreelabel.append("td").attr("style", "min-width:75px");
        // draw degree cells
        d3.select("table")
            .selectAll(".mainrow")
            .data(cellData);
        mainColumns = mainRows.selectAll("td")
            .data(function (rows) {
                return termsYears.map(function (column) {
                    return rows.values.filter(function (d) {
                        if (d.year === column.year && d.term === column.term) {
                            return d;
                        }
                    })[0];
                });
            })
            .enter()
            .append("td")
            .attr("class", function (d, i) {
                if (i > 0) {
                    return "col_" + (i - 1);
                }
            })
            .on("mouseover", function (d, i) {
                if (i > 0) {
                    Table.mouseOverColumn(this);
                }
            })
            .on("mouseout", function (d, i) {
                Table.mouseOutColumn(this);
            })
            .append("svg")
            .attr("width", width)
            .attr("height", cellHeight)
            .append("rect")
            .attr("id", function (d) {
                if (d) {
                    return d[aggregation + "Acronym"] + ',' + d.year + "," + d.term;
                }
            })
            .attr("class", function (d, i) {
                var selected = getSelected();
                if (selected.indexOf(this.id) > -1) {
                    return "selectCell";
                }
                return "cell main";
            })
            .attr("width", width)
            .attr("height", cellHeight)
            .style("fill", function (d) {
                if (d && (d[attribute + "Average"] || d[attribute + "Average"] === 0)) {
                    return colorScale(d[attribute + "Average"]);
                }
            });

        d3.selectAll(".cell.main, .selectCell").filter(function () {
            if (!d3.select(this).classed("summarization")) {
                return this;
            }
        })
            .on("mouseover", function (d, i) {
                if (d) {
                    if (d[attribute + "Average"] || d[attribute + "Average"] === 0) {
                        var format = d3.format(",");
                        mouseOver(d, this);
                        Table.bodyMouseOver(Table.display(attribute) + ": " + d[attribute + "Average"] + label + '<br>' + "Enrollments: " + format(d.studentsNumberAverage));
                    }
                }
            })
            .on("mouseout", function (d) {
                if (d && d3.select(this).classed("cell")) {
                    mouseOut(d, this);
                }
                d3.select(".tooltip")
                    .style("visibility", "hidden");
            })
            .on("click", function (d) {
                if (d) {
                    var cell = d3.select(this),
                        type = Table.getAggregation() === "degree" ? "main" : "sub";
                    highlight(cell, "cell", this.id, type, d);
                }
            });
        // expand degree row
        d3.selectAll(".mainrow")
            .select("td")
            .select("div")
            /*.on("click", function () {
                if (d3.event.defaultPrevented) {
                    return;
                }
                var currentRow = this.parentNode.parentNode,
                    name = this.innerHTML,
                    secondColumn = aggregation === "degree" ? "course" : "degree",
                    requestCourse = acronym[1] === '' ?
                                    [aggregation + "Acronym=" + name] :
                                    [aggregation + "Acronym=" + name, secondColumn + "Acronym=" + acronym[1]];
                dispatcher(Table.drawSubLevels, [{"courses": requestCourse}, {"terms": ""}], [currentRow]);
            })*/
            .call(d3.drag()
                .on("start", function (d) {
                    d3.event.sourceEvent.stopPropagation();
                    clone = d3.select(this.parentNode.parentNode).nodes()[0].cloneNode(true);
                    belowRow = d3.select(this.parentNode.parentNode.nextSibling);
                    lastPos = d3.event.sourceEvent.pageY - $(window).scrollTop();
                })
                .on("drag", function () {
                    var mouseY = d3.event.sourceEvent.pageY - $(window).scrollTop(),
                        posY = d3.event.sourceEvent.pageY - parseInt(d3.select(".container").style("height"), 10) - parseInt(d3.select("thead").style("height"), 10) + 15;
                    if (Math.abs(lastPos - mouseY) > 5) {
                        disableEvents();
                        dragged = true;
                        d3.select(this.parentNode.parentNode).classed("draggedRow", true);
                        if (touchDevice()) {
                            posY = event.touches[0].pageY;
                        }
                        dragRow(this, clone, 10, posY, mouseY, "row");
                    }
                })
                .on("end", function () {
                    if (dragged) {
                        dragged = false;
                        d3.event.sourceEvent.stopPropagation();
                        endDragRow("mainrow", clone, belowRow);
                    } else {
                        var currentRow = this.parentNode.parentNode,
                            name = this.innerHTML;
                        click(currentRow, name, acronym);
                    }
                }));
    }
    
    function menuButton(type, buttonClass, checked) {
        var request,
            button = d3.select(".toggle")
                .append("div")
                .attr("id", type)
                .attr("class", buttonClass)
                .text(type.charAt(0).toUpperCase() + type.slice(1))
                .on("mouseover", function () {
                    d3.select(this).style("outline", "2px solid skyblue");
                })
                .on("mouseout", function () {
                    d3.select(this).style("outline", "none");
                })
                .on("click", function () {
                    Table[type]();
                    request = parseAcronym();
                    dispatcher(Table.draw, request);
                    d3.selectAll(".checked").classed("checked", false);
                    d3.select(this).classed("checked", true);
                });
    }
    
    function menuClick() {
        var tran = d3.transition()
                .duration(200)
                .ease(d3.easeLinear),
            toggle,
            menu = d3.select(".menu");
        menu.on("click", null);
        if (!menu.classed("open")) {
            menu.classed("open", true);
            toggle = d3.select("body")
                .append("rect")
                .style("opacity", "0")
                .attr("class", "toggle");
            toggle.transition(tran)
                .style('opacity', 1.0)
                .on("end", function () {
                    menu.on("click", menuClick);
                });
            toggle.append("p").text("Attributes");
            menuButton("approval", "attributeButton", "");
            menuButton("grades", "attributeButton", "");
            menuButton("quc", "attributeButton", "");
            d3.select("#" + attribute).classed("checked", true);
            toggle.append("rect")
                .attr("class", "menuclosebtn")
                .text("X")
                .on("mouseover", function () { d3.select(this).style("color", "blanchedalmond"); })
                .on("mouseout", function () { d3.select(this).style("color", "white"); })
                .on("click", function () {
                    menu.classed("open", false);
                    d3.selectAll(".toggle")
                        .transition(tran)
                        .style('opacity', 0).on("end", function () { menu.on("click", menuClick); })
                        .remove();
                });
        } else {
            d3.selectAll(".menu").classed("open", false);
            d3.selectAll(".toggle").transition(tran).style('opacity', 0).on("end", function () { menu.on("click", menuClick); }).remove();
        }
    }
    
    function multiSelection() {
        var startingX,
            startingY,
            posX,
            posY,
            allowedWidth = $("tbody").width() + 10,
            allowedHeight,
            drag = false,
            start = touchDevice() ? "touchstart" : "mousedown",
            move = touchDevice() ? "touchmove" : "mousemove",
            end = touchDevice() ? "touchend" : "mouseup";
        d3.select("body")
                .append("div")
                .attr("class", "multiSelection")
                .style("visibility", "hidden");
        document.addEventListener(start, function (event) {
            allowedHeight = $(document).height();
            startingX = event.changedTouches === undefined ? event.x : event.changedTouches[0].pageX;
            startingY = $(window).scrollTop() + ((event.changedTouches === undefined) ? event.y : event.changedTouches[0].pageY);
        });
        document.addEventListener(move, function (event) {
            posX = event.changedTouches === undefined ? event.x : event.changedTouches[0].pageX;
            posY = $(window).scrollTop() + ((event.changedTouches === undefined) ? event.y : event.changedTouches[0].pageY);
            var width,
                height,
                newStartingX,
                newStartingY;
            if (posX !== startingX && posY !== startingY && startingY !== undefined && startingX < allowedWidth) {
                drag = true;
                disableEvents();
                width = Math.abs(posX - startingX);
                height = Math.abs(posY - startingY);
                newStartingX = (posX - startingX < 0) ? posX : startingX;
                newStartingY = (posY - startingY < 0) ? posY : startingY;
                d3.select(".multiSelection")
                    .style("visibility", "visible")
                    .style("width", width + "px")
                    .style("max-width", allowedWidth - newStartingX + "px")
                    .style("max-height", allowedHeight - newStartingY + "px")
                    .style("height", height + "px")
                    .style("left", newStartingX + "px")
                    .style("top", newStartingY + "px");
                getElementsByArea(newStartingX, newStartingY, width, height);
            }
        });
        document.addEventListener(end, function () {
            startingY = undefined;
            startingX = undefined;
            if (drag) {
                drag = false;
                var data = [],
                    type = [],
                    request,
                    id = '',
                    elementClass,
                    container = d3.select(".container").data()[0] || [],
                    pillsNumber = d3.selectAll(".pill")
                                        .nodes()
                                        .length,
                    modifiedSelection;
                d3.selectAll(".selected")
                    .classed("selected", false)
                    .nodes()
                    .forEach(function (d) {
                        type = [];
                        id = d.id.split(',')[1] || d.id;
                        elementClass = d3.select(d).attr("class").indexOf("firstTextLabel") !== -1 ? "firstLabel" : "secondLabel";
                        type.push(id, elementClass);
                        if (!data.containsArray(type)) {
                            data.push(type);
                        }
                    });
                modifiedSelection = data.filter(function (d) {
                    var containerData = d3.select(".container").data()[0] || d3.select(".container").data();
                    if (containerData.indexOf(d[0].toLowerCase()) === -1) {
                        return d[0].toLowerCase();
                    }
                });
                drawPill(data);
                d3.select(".multiSelection")
                    .style("visibility", "hidden")
                    .style("top", "50px");
                enableEvents();
                if (modifiedSelection.length > 0) {
                    courseAggregationSwitch();
                    adjustViews();
                    request = parseAcronym();
                    dispatcher(Table.draw, request);
                }
            }
        });
    }

    function menu() {
        if (d3.selectAll(".container").empty()) {
            multiSelection();
            var width = window.innerWidth || document.body.clientWidth,
                container = d3.select("body")
                    .append("div")
                    .attr("class", "container")
                    .style("width", width - 20 + "px"),
                searchInput,
                menuDiv = d3.select(".container")
                    .append("div").attr("class", "menu")
                    .on("click", function () {
                        menuClick();
                    }),
                i;
            for (i = 0; i < 3; i += 1) {
                menuDiv.append("div").attr("class", "line");
            }
            searchInput = container.append("div")
                .attr("class", "searchBox");
            searchInput.append("div")
                .attr("class", "icon");
            searchInput.append("input")
                .attr("class", "inputField")
                .attr("type", "text")
                .attr("placeholder", "Enter the degree/course name")
                .on("keyup", function (d) {
                    if (d3.event.keyCode === 13) {
                        keyboardFilter(this.value);
                        this.value = "";
                    }
                });
        }
    }

    function yearSorting(rows, year, column) {
        rows.sort(function (x, y) {
            var compareX = x.values.filter(function (d) {
                return d.year === year;
            }),
                compareY = y.values.filter(function (d) {
                    return d.year === year;
                }),
                value1,
                value2;
            compareX = compareX.removeDuplicate(compareX, "term");
            compareY = compareX.removeDuplicate(compareY, "term");
            if (compareX.length > 0) {
                value1 = compareX[0][column];
                value2 = compareX[1] !== undefined ? compareX[1][column] : 0;
                compareX = (value1 + value2) / 2;
            } else {
                compareX = undefined;
            }
            if (compareY.length > 0) {
                value1 = compareY[0][column];
                value2 = compareY[1] !== undefined ? compareY[1][column] : 0;
                compareY = (value1 + value2) / 2;
            } else {
                compareY = undefined;
            }
            return nullSort(compareX, compareY, sorting, x.key.toUpperCase(), y.key.toUpperCase());
        });
    }

    function degreeSorting(rows, sorting) {
        rows.sort(function (x, y) {
            return d3[sorting](x.key.toUpperCase(), y.key.toUpperCase());
        });
    }

    function courseSorting(sorting) {
        d3.selectAll(".expanded")
            .each(function (d) {
                var rows = d3.selectAll(".row,.barRow").filter("[id^='" + d.key + ",']");
                rows.sort(function (x, y) {
                    return d3[sorting](x.key.toUpperCase(), y.key.toUpperCase());
                });
            });
    }

    function termSorting(rows, year, term, column) {
        rows.sort(function (x, y) {
            var compareX = x.values.filter(function (d) {
                return d.year === year && d.term === term;
            })[0],
                compareY = y.values.filter(function (d) {
                    return d.year === year && d.term === term;
                })[0];
            if (compareX) {
                compareX = compareX[column];
            }
            if (compareY) {
                compareY = compareY[column];
            }
            return nullSort(compareX, compareY, sorting, x.key.toUpperCase(), y.key.toUpperCase());
        });
    }

    /* Fixed header creation */
    function tableHead(padding, x_axis, width, cellHeight, termsYears) {
        var tableY,
            headY,
            table,
            topAxisRow,
            topAxisColumns,
            bottomAxisRow,
            bottomAxisColumns;
        // draw table
        table = d3.select("body")
            .append("table")
            .attr("class", "table")
            .attr("style", "top:0px");

        // draw top header row
        topAxisRow = d3.select("table")
            .append("thead")
            .attr("style", "top:0px")
            .append("tr")
            .attr("class", "year");
        // draw top header columns
        topAxisColumns = topAxisRow.selectAll("th")
            .data(x_axis, function (d) {return d; })
            .enter()
            .append("th")
            .attr("id", function (d) {return d; })
            .attr("colspan", 2)
            .attr("class", function (d, i) { if (i > 0) {return "yearcol_" + i; } })
            .attr("style", function (d, i) { if (i > 0) { return "background-color:antiquewhite"; } })
            .text(function (d) { return d; })
            .attr("width", width)
            .attr("height", cellHeight)
            .style("cursor", "pointer")
            .on("click", function (d) {
                var column = this.id,
                    year = d,
                    rows = d3.select("tbody").selectAll(".mainrow"),
                    subRows;
                changeSorting(this.id);
                column = attribute + "Average";
                yearSorting(rows, year, column);
                subRows = d3.select("tbody").selectAll(".row,.infoChart,.barRow");
                subRows.nodes().forEach(function (d) {
                    var mainrow = d3.select(".mainrow#" + d.id.split(',')[0]);
                    mainrow.node().parentNode.insertBefore(d, mainrow.node().nextSibling);
                    if (!d3.selectAll("#" + d.id.split(",")[0] + '\\,' + d.id.split(",")[1] + ".barRow").empty()) {
                        subRows.node()
                            .parentNode
                            .insertBefore(d3.selectAll("#" + d.id.split(",")[0] + '\\,' + d.id.split(",")[1] + ".barRow").node(), mainrow.node().nextSibling);
                    }
                    if (!d3.selectAll(".infoChart").filter("[id^='" + mainrow.attr("id") + "']").empty()) {
                        subRows.node()
                            .parentNode
                            .insertBefore(d3.selectAll(".infoChart").filter("[id^='" + mainrow.attr("id") + "']").node(), mainrow.node().nextSibling);
                    }
                });
                d3.selectAll(".expanded")
                    .each(function (d) {
                        rows = d3.selectAll(".row,.infoChart").filter("[id^='" + d.key + ",']");
                        yearSorting(rows, year, attribute);
                    });
                d3.selectAll(".barRow")
                    .each(function (d) {
                        this
                            .parentNode
                            .insertBefore(this, d3.select("#" + d.key.split(",")[0] + '\\,' + d.key.split(",")[1] + ".row").node().nextSibling);
                    });
            })
            .on("mouseover", function (d, i) { headerMouseOver(d, i, "Year", 0); })
            .on("mouseout", function (d) { d3.select(".tooltip").style("visibility", "hidden"); });

        // draw bottom header row
        bottomAxisRow = d3.select("thead")
            .append("tr")
            .attr("class", "term");

        // draw bottom header columns
        bottomAxisColumns = bottomAxisRow.selectAll("th")
            .data(termsYears)
            .enter()
            .append("th")
            .attr("id", function (d, i) {
                if (i > 1) {
                    return d.year + ',' + d.term;
                } else {
                    return d.term;
                }
            })
            .attr("class", function (d, i) { if (i > 1) { return "termcol_" + (i - 1); } })
            .attr("style", function (d, i) { if (i > 1) { return "background-color:antiquewhite"; } })
            .style("cursor", "pointer")
            .on("click", function (d) {
                var column = this.id,
                    year = d.year,
                    term = d.term,
                    rows = d3.select("tbody").selectAll(".mainrow"),
                    subRows;
                changeSorting(this.id);
                if (column === Table.display(aggregation) + "s") {
                    column = "degreeAcronym";
                    degreeSorting(rows, sorting);
                    subRows = d3.select("tbody").selectAll(".row,.infoChart,.barRow");
                    subRows.nodes()
                        .forEach(function (d) {
                            var mainrow = d3.select(".mainrow#" + d.id.split(',')[0]);
                            mainrow.node()
                                .parentNode
                                .insertBefore(d, mainrow.node().nextSibling);
                            if (!d3.selectAll("#" + d.id.split(",")[0] + '\\,' + d.id.split(",")[1] + ".barRow").empty()) {
                                subRows.node()
                                    .parentNode
                                    .insertBefore(d3.selectAll("#" + d.id.split(",")[0] + '\\,' + d.id.split(",")[1] + ".barRow").node(), mainrow.node().nextSibling);
                            }
                            if (!d3.selectAll(".infoChart").filter("[id^='" + mainrow.attr("id") + "']").empty()) {
                                subRows.node()
                                    .parentNode
                                    .insertBefore(d3.selectAll(".infoChart").filter("[id^='" + mainrow.attr("id") + "']").node(), mainrow.node().nextSibling);
                            }
                        });
                    d3.selectAll(".expanded")
                        .each(function (d) {
                            rows = d3.selectAll(".row,.infoChart,.barRow").filter("[id^='" + d.key + ",']");
                            degreeSorting(rows, "ascending");
                        });
                } else {
                    if (column === "Courses" || column === "Degrees") {
                        courseSorting(sorting);
                        d3.selectAll(".barRow")
                            .each(function (d) {
                                this
                                    .parentNode
                                    .insertBefore(this, d3.select("#" + d.key.split(",")[0] + '\\,' + d.key.split(",")[1] + ".row").node().nextSibling);
                            });
                    } else {
                        column = attribute + "Average";
                        termSorting(rows, year, term, column);
                        subRows = d3.select("tbody").selectAll(".row,.infoChart,.barRow");
                        subRows.nodes()
                            .forEach(function (d) {
                                var mainrow = d3.select(".mainrow#" + d.id.split(',')[0]);
                                mainrow.node()
                                    .parentNode
                                    .insertBefore(d, mainrow.node().nextSibling);
                                if (!d3.selectAll("#" + d.id.split(",")[0] + '\\,' + d.id.split(",")[1] + ".barRow").empty()) {
                                    subRows.node()
                                        .parentNode
                                        .insertBefore(d3.selectAll("#" + d.id.split(",")[0] + '\\,' + d.id.split(",")[1] + ".barRow").node(), mainrow.node().nextSibling);
                                }
                                if (!d3.selectAll(".infoChart").filter("[id^='" + mainrow.attr("id") + "']").empty()) {
                                    subRows.node()
                                        .parentNode
                                        .insertBefore(d3.selectAll(".infoChart").filter("[id^='" + mainrow.attr("id") + "']").node(), mainrow.node().nextSibling);
                                }
                            });
                        d3.selectAll(".expanded")
                            .each(function (d) {
                                rows = d3.selectAll(".row,.infoChart").filter("[id^='" + d.key + ",']");
                                column = attribute;
                                termSorting(rows, year, term, column);
                            });
                        d3.selectAll(".barRow")
                            .each(function (d) {
                                this
                                    .parentNode
                                    .insertBefore(this, d3.select("#" + d.key.split(",")[0] + '\\,' + d.key.split(",")[1] + ".row").node().nextSibling);
                            });
                    }
                }
            })
            .on("mouseover", function (d, i) { headerMouseOver(d.term, i, "Term", 1); })
            .on("mouseout", function (d) { d3.select(".tooltip").style("visibility", "hidden"); })
            .text(function (d) { return d.term; });
    }
    
    // Public Methods
    return {
        
        drawSubLevels: function (dataRequested, args) {
            var currentRow = d3.select(args[0]),
                terms = retrieveTerms(dataRequested[1]),
                termsYears = terms[2],
                aggregationData = aggregation === "degree" ? "courseName" : "degreeName",
                colors,
                colorScale,
                row,
                column,
                currentDegreeId,
                selectedRow,
                clone,
                belowRow,
                lastPos = null,
                dragged = false,
                td,
                rowsId,
                idFirst = aggregation === "degree" ? "degreeAcronym" : "courseAcronym",
                idSecond = aggregation === "degree" ? "courseAcronym" : "degreeAcronym";
            if (currentRow.node() === null) {
                return;
            }
            if (currentRow.attr("class") === "mainrow") {
                colors = ['#d73027', '#fc8d59', '#fee08b', '#ffffbf', '#d9ef8b', '#91cf60', '#1a9850'];
                colorScale = d3.scaleQuantile()
                                .domain(colorDomain)
                                .range(colors);
                currentRow.style("border-bottom", "1px solid rgb(180, 180, 180)").style("margin-bottom", "-1px");
                if (expandedRows[aggregation].indexOf(currentRow.attr("id")) === -1) {
                    expandedRows[aggregation].push(currentRow.attr("id"));
                }
                // draw course rows
                row = currentRow.selectAll(".row")
                    .data(d3.nest()
                            .key(function (d) { return d[idFirst] + ',' + d[idSecond]; })
                            .entries(dataRequested[0].filter(function (d) {return d[attribute] !== null; })))
                    .enter()
                    .select(function () {
                        return this._parent.parentNode.insertBefore(document.createElement("tr"), this._parent.nextSibling);
                    })
                    .attr("id", function (d) { return d.key; })
                    .attr("class", "row")
                    .on("mouseover", function () {
                        var posX = event.changedTouches === undefined ? event.pageX : event.changedTouches[0].pageX,
                            posY = ((event.changedTouches === undefined) ? event.pageY : event.changedTouches[0].pageY) - $(window).scrollTop();
                        Table.lineMouseOver(this);
                    })
                    .on("mouseout", function () {
                        Table.lineMouseOut(this);
                    });
                currentRow.style("cursor", "default");
                currentRow.attr("class", "mainrow expanded");
                row.append("td").style("min-width", "75px").style("min-height", "18px").classed("firstTd", true);
                td = row.append("td").style("min-width", "75px");
                td.append("div")
                    .attr("class", function (d) {
                        var pillNodes = [];
                        d3.selectAll(".pill")
                            .nodes()
                            .forEach(function (d) {
                                pillNodes.push(d3.select(d.childNodes[0]).text());
                            });
                        return "secondTextLabel " + aggregation;
                    })
                    .attr("id", function (d) { return d.key; })
                    .text(function (d) { return d.key.split(",")[1]; })
                    /*.on("click", function (d) {
                        var secondColumn = Table.getAggregation() === "degree" ? "course" : "degree",
                            request = [Table.getAggregation() + "Acronym=" + d.key.split(",")[0], secondColumn + "Acronym=" + d.key.split(",")[1]];
                        dispatcher(BarChart.draw, [{"teachers": request}, {"terms": ""}], [d.key.split(",")[0], d.key.split(",")[1]]);
                    })*/
                    .call(d3.drag()
                        .on("start", function (d) {
                            d3.event.sourceEvent.stopPropagation();
                            clone = d3.select(this.parentNode.parentNode).nodes()[0].cloneNode(true);
                            belowRow = d3.select(this.parentNode.parentNode.nextSibling);
                            lastPos = d3.event.sourceEvent.pageY - $(window).scrollTop();
                        })
                        .on("drag", function () {
                            var mouseY = d3.event.sourceEvent.pageY - $(window).scrollTop(),
                                posY = d3.event.sourceEvent.pageY - parseInt(d3.select(".container").style("height"), 10) - parseInt(d3.select("thead").style("height"), 10) + 15;
                            if (Math.abs(lastPos - mouseY) > 5) {
                                dragged = true;
                                disableEvents();
                                d3.select(this.parentNode.parentNode).classed("draggedRow", true).select("td").style("background-color", "transparent");
                                if (touchDevice()) {
                                    posY = event.touches[0].pageY;
                                }
                                dragRow(this, clone, 120, posY, mouseY, "subrow");
                            }
                        })
                        .on("end", function (d) {
                            if (dragged) {
                                dragged = false;
                                d3.event.sourceEvent.stopPropagation();
                                endDragRow("subrow", clone, belowRow);
                            } else {
                                clickSubRow(d);
                            }
                        }))
                    .on("mouseover", function (d) {
                        var tooltipText = aggregation === "degree" ?
                                            d.values[0][aggregationData] :
                                            d.values[0].degreeType + ' em ' + d.values[0][aggregationData];
                        Table.bodyMouseOver(tooltipText);
                    })
                    .on("mouseout", function () {
                        d3.select(".tooltip")
                            .style("visibility", "hidden");
                    });
                td.append("svg")
                    .attr("width", 15)
                    .attr("height", 15)
                    .style("float", "right")
                    .style("margin-right", "10px")
                    .on("mouseover", function (d) {
                        var format = d3.format(".2f"),
                            studentsFormat = d3.format(","),
                            average = parseFloat(format(d3.mean(d.values, function (f) {
                                return f[attribute];
                            }))),
                            students = parseFloat(format(d3.sum(d.values, function (f) {
                                return f.studentsNumber;
                            })));
                        Table.bodyMouseOver(Table.display(attribute) + ": " + average + label + '<br>' + "Enrollments: " + studentsFormat(students));
                        d3.select(this)
                            .select("rect")
                            .style("stroke", "black")
                            .style("stroke-width", "4px");
                    })
                    .on("mouseout", function () {
                        d3.select(".tooltip").style("visibility", "hidden");
                        d3.select(this)
                            .select("rect")
                            .style("stroke", "rgb(200, 200, 200)")
                            .style("stroke-width", "2px");
                    })
                    .append("rect")
                    .attr("id", function (d) { return d.key; })
                    .attr("class", "cell sub summarization")
                    .attr("width", 15)
                    .attr("height", 15)
                    .attr("cursor", "default")
                    .style("fill", function (d) {
                        var format = d3.format(".2f"),
                            average = parseFloat(format(d3.mean(d.values, function (f) {
                                return f[attribute];
                            })));
                        return colorScale(average);
                    });
                // draw sublevel cells
                column = row.selectAll(".subcells")
                    .data(function (rows) { return termsYears.map(function (column) { return rows.values.filter(function (d) {if (d.year === column.year && d.term === column.term) { return d; } })[0]; }); })
                    .enter()
                    .append("td")
                    .attr("class", function (d, i) { return "col_" + (i + 1); })
                    .on("mouseover", function (d, i) {
                        Table.mouseOverColumn(this);
                    })
                    .on("mouseout", function (d, i) {
                        Table.mouseOutColumn(this);
                    })
                    .append("svg")
                    .attr("width", 15)
                    .attr("height", 15)
                    .attr("class", "subcells")
                    .append("rect")
                    .attr("id", function (d) {
                        if (d) {
                            var subLabel = aggregation === "degree" ? "course" : "degree";
                            return d[aggregation + "Acronym"] + ',' + d[subLabel + "Acronym"] + ',' + d.year + "," + d.term;
                        }
                    })
                    .attr("class", function (d) {
                        var selected = getSelected();
                        if (selected.indexOf(this.id) > -1) {
                            return "selectCell";
                        }
                        return "cell sub";
                    })
                    .attr("width", 15)
                    .attr("height", 15)
                    .style("fill", function (d) {
                        if (d && (d[attribute] || d[attribute] === 0)) {
                            return colorScale(d[attribute]);
                        }
                    });

                d3.selectAll(".cell.sub, .selectCell").filter(function () {
                    if (!d3.select(this).classed("summarization")) {
                        return this;
                    }
                })
                    .on("click", function (d) {
                        if (d) {
                            var cell = d3.select(this),
                                type = Table.getAggregation() === "degree" ? "main" : "sub";
                            highlight(cell, "cell", this.id, type, d);
                        }
                    })
                    .on("mouseover", function (d) {
                        if (d) {
                            if (d[attribute] || d[attribute] === 0) {
                                var format = d3.format(",");
                                mouseOver(d, this);
                                Table.bodyMouseOver(Table.display(attribute) + ": " + d[attribute] + label + '<br>' + "Enrollments: " + format(d.studentsNumber));
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
                row.sort(function (x, y) { return d3.ascending(x.key.toUpperCase(), y.key.toUpperCase()); })
                    .style('opacity', 0.0)
                    .transition()
                    .delay(function (d, i) {return (1200 * i) / row.size(); })
                    .duration(1000).style('opacity', 1.0)
                    .ease(d3.easeLinear);
            } else {
                currentDegreeId = currentRow.attr("id");
                expandedRows[aggregation].splice(expandedRows[aggregation].indexOf(currentDegreeId), 1);
                selectedRow = d3.selectAll(".row");
                rowsId = selectedRow.filter(function (d) {
                    if (d.key.indexOf(currentDegreeId) > -1) {
                        return d;
                    }
                })
                        .transition()
                        .style("pointer-events", "none")
                        .delay(function (d, i) {return (1000 * i) / selectedRow.size(); })
                        .duration(500)
                        .style('opacity', 0.0)
                        .ease(d3.easeLinear)
                        .remove();
                d3.select(".mainrow#" + currentDegreeId)
                    .style("border-bottom", null).style("margin-bottom", null)
                    .attr("class", "mainrow");
                d3.selectAll(".barRow").transition().duration(600).style("opacity", 0).remove();
            }
        },
        
        filterData: function (dataRequested) {
            filteredData = [];
            d3.nest()
                .key(function (d) {
                    return d[aggregation + "Acronym"] + ',' + d.year + ',' + d.term;
                })
                .rollup(function (v) {
                    v.forEach(function (e) {
                        var format = d3.format(".2f");
                        e.approvalAverage = parseFloat(format(d3.mean(v, function (f) {
                            return f.approval;
                        })));
                        e.qucAverage = parseFloat(format(d3.mean(v, function (f) {
                            return f.quc;
                        })));
                        e.gradesAverage = parseFloat(format(d3.mean(v, function (f) {
                            return f.grades;
                        })));
                        e.studentsNumberAverage = parseFloat(format(d3.sum(v, function (f) {
                            return f.studentsNumber;
                        })));
                        filteredData.push(e);
                    });
                    return v;
                })
                .entries(dataRequested[2]);
            dataRequested[0] = filteredData;
        },
        
        draw: function (dataRequested) {
            d3.select("table").remove();
            d3.select(".tooltip").remove();
            var padding = 20,
                cellHeight = 15,
                width = 15,
                label1 = aggregation === "degree" ? "Degrees" : "Courses",
                label2 = aggregation === "degree" ? "Courses" : "Degrees",
                degreesData = crossfilter(dataRequested[0]),
                labelDimension,
                cellData,
                labelGrouping,
                firstLabel,
                tooltip,
                terms = retrieveTerms(dataRequested[1]),
                x_axis = terms[0],
                termsYears = terms[1],
                labelData = terms[2];
            d3.selectAll(".menu").classed("open", false);
            d3.selectAll(".toggle")
                .transition()
                .duration(200)
                .ease(d3.easeLinear)
                .style('opacity', 0)
                .remove();
            filteredData = dataRequested[0];
            if (dataRequested[2]) {
                Table.filterData(dataRequested);
            }
            termsYears.unshift({ year: "", term: label1}, { year: "", term: label2});
            labelDimension = degreesData.dimension(function (d) {
                if (aggregation === "degree") {
                    return d[aggregation + "Acronym"] + ',' + d.degreeType + ',' + d[aggregation + "Name"];
                } else {
                    return d[aggregation + "Acronym"] + ',' + d[aggregation + "Name"];
                }
            });
            cellData = d3.nest()
                .key(function (d) {
                    return d[aggregation + "Acronym"];
                })
                .entries(dataRequested[0].filter(function (d) { if (d[attribute + "Average"] || d[attribute + "Average"] === 0) { return d; } }))
                .sort(function (x, y) {
                    return d3.ascending(x.key.toUpperCase(), y.key.toUpperCase());
                });
            labelGrouping = labelDimension.group().all();
            firstLabel = labelGrouping.map(function (d) {return d.key; });
            tooltip = d3.select("body")
                        .append("div")
                        .attr("class", "tooltip")
                        .style("visibility", "hidden");
            tableHead(padding, x_axis, width, cellHeight, termsYears);
            tableBody(cellData, firstLabel, termsYears, width, cellHeight, labelData);
            menu();
            adjustViews();
            //keyboardFilter(d3.select(".inputField").nodes()[0]);
        },
        
        mouseOverColumn: function (element) {
            var currentColumn = d3.select(element).attr("class").split('_')[1];
            d3.selectAll('.col_' + currentColumn + ',' + '.termcol_' + currentColumn + ',' + '.yearcol_' + Math.round(currentColumn / 2))
                .style('background-color', 'rgb(224, 240, 244)');
        },

        mouseOutColumn: function (element) {
            var currentColumn = d3.select(element).attr("class").split('_')[1];
            d3.selectAll('.col_' + currentColumn)
                .style('background-color', null);
            d3.selectAll('.termcol_' + currentColumn + ',' + '.yearcol_' + Math.round(currentColumn / 2))
                .style('background-color', "antiquewhite");
        },
        
        lineMouseOver: function (element) {
            if (d3.select(element).classed("row")) {
                Table.subRowsMouseOver(element);
            } else {
                d3.select(element).style("background-color", "rgb(224, 240, 244)");
            }
        },
        
        lineMouseOut: function (element) {
            d3.select(element).style("background-color", "rgb(247, 247, 247)");
        },
        
        display: function (token) {
            return token.charAt(0).toUpperCase() + token.slice(1);
        },
        
        getAttribute: function () {
            return attribute;
        },
        
        getLabel: function () {
            return label;
        },
        
        approval: function () {
            attribute = 'approval';
            colorDomain = [0, 100];
            label = '%';
        },
        grades: function () {
            attribute = 'grades';
            colorDomain = [0, 20];
            label = '';
        },
        quc: function () {
            attribute = 'quc';
            colorDomain = [0, 10];
            label = '';
        },
        
        course: function () {
            aggregation = 'course';
        },
        
        degree: function () {
            aggregation = 'degree';
        },
        
        getAggregation: function () {
            return aggregation;
        },
        
        cellMouseOver: function (d, elem) {
            var column = d3.select(elem).classed("main") ? d[attribute] + "Average" : d[attribute];
            d3.select(elem)
                .style("stroke", "black")
                .style("cursor", "default")
                .style("stroke-width", "4px");
        },
        
        cellMouseOut: function (d, elem) {
            d3.select(elem)
                .style("stroke", "rgb(200, 200, 200)")
                .style("stroke-width", "2px");
        },
        
        subRowsMouseOver: function (element) {
            var posX = element.getBoundingClientRect().left,
                posY = element.getBoundingClientRect().top;
            d3.select(element).style("background-color", "rgb(224, 240, 244)");
            d3.select("[id='" + element.id + "'] > .firstTd")
                .style("background-color", "rgb(247, 247, 247)");
        },
        
        bodyMouseOver: function (d) {
            d3.select(".tooltip")
                .style("left", d3.event.pageX + 10 + "px")
                .style("top", d3.event.pageY + "px")
                .style("visibility", "visible")
                .html(d);
        },
        
        getExpandedRows: function (aggregation) {
            return expandedRows[aggregation];
        },
        
        getFilteredData: function () {
            return filteredData;
        }
    };
}());