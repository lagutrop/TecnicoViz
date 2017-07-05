/*jslint devel: true*/
/*global $, filterType, Table, ScatterPlot, LineChart, BarChart, parseAcronym, getFilteredAcronym, linePill, disableEvents, d3*/

var callbacks = [Table.draw, Table.drawSubLevels, ScatterPlot.draw, LineChart.draw, LineChart.updateCompare, BarChart.draw, filterType],
    ipAddress = "85.244.165.89",
    request = function (url, index, result, callback) {
        'use strict';
        var i;
        $.ajax(url[index])
            .done(function (data) {
                if (url[index] !== undefined) {
                    index += 1;
                    result.push(data);
                    if (url[index] === undefined) {
                        callback(null, result);
                    } else {
                        request(url, index, result, callback);
                    }
                }
            });
    },
    filterData = function (dataRequested) {
        'use strict';
        var filteredData = [];
        d3.nest()
            .key(function (d) {
                return d[Table.getAggregation() + "Acronym"] + ',' + d.year + ',' + d.term;
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
        return filteredData;
    },
    removeDuplicate = function (arr) {
        'use strict';
        var i,
            j,
            result = [],
            compare = [];
        for (i = 0; i < arr.length; i += 1) {
            if (compare.indexOf(JSON.stringify(arr[i])) === -1) {
                result.push(arr[i]);
                compare.push(JSON.stringify(arr[i]));
            }
        }
        return result;
    },
    requestHandler = function (args, callback) {
        'use strict';
        var i, j, id, key, query, url = [], parsedParams;
        for (i = 0; i < args.length; i += 1) {
            for (key in args[i]) {
                if (args[i].hasOwnProperty(key)) {
                    parsedParams = "?";
                    query = args[i];
                    if (Number.isInteger(query[key])) {
                        id = query[key];
                        url.push("http://" + ipAddress + "/" + key + "/" + id);
                    } else {
                        if (query[key] !== "") {
                            for (j = 0; j < query[key].length; j += 1) {
                                parsedParams += query[key][j] + '&';
                            }
                            url.push("http://" + ipAddress + "/" + key + "/" + parsedParams);
                        } else {
                            url.push("http://" + ipAddress + "/" + key);
                        }
                    }
                }
            }
        }
        callback(null, url);
    };

function dispatcher(callback, args, funcparam) {
    'use strict';
    var aggregation = Table.getAggregation(),
        line,
        lineAcronym = aggregation + "Acronym",
        filteredCondition = getFilteredAcronym()[1] === "" ? "" : "degreeAcronym=" + getFilteredAcronym()[1],
        lineArgs,
        tableSearch = LineChart.getRequest(),
        lineRequest,
        plotArgs = [],
        i,
        expanded = Table.getExpandedRows(aggregation),
        q = d3.queue();
    switch (callback) {
    case callbacks[0]:
        lineArgs = linePill();
        line = lineArgs;
        q.defer(requestHandler, args);
        q.defer(requestHandler, lineArgs[0]);
        for (i = 0; i < expanded.length; i += 1) {
            var secondColumn = aggregation === "degree" ? "course" : "degree",
                acronym = getFilteredAcronym(),
                requestCourse = acronym[1] === '' ? [aggregation + "Acronym=" + expanded[i]] : [aggregation + "Acronym=" + expanded[i], secondColumn + "Acronym=" + acronym[1]],
                expandargs = [{"courses": requestCourse}, {"terms": ""}];
            lineRequest = aggregation === "degree" ? [lineAcronym + "=" + expanded[i]] : [lineAcronym + "=" + expanded[i], filteredCondition];
            lineArgs = {};
            lineArgs[tableSearch] = lineRequest;
            lineArgs.terms = "";
            q = q.defer(requestHandler, expandargs);
            q = q.defer(requestHandler, [lineArgs]);
        }
        q.awaitAll(function (error, data) {
            var q2 = d3.queue();
            for (i = 0; i < data.length; i += 1) {
                q2.defer(request, data[i], 0, []);
            }
            q2.awaitAll(function (error, result) {
                callbacks[0](result[0]);
                if (!d3.select(".linePill.course").empty() && !d3.select(".pill.firstLabel").empty()) {
                    callbacks[4](result[1], line[1]);
                }
                for (i = 2; i < expanded.length * 2 + 1; i += 2) {
                    callbacks[1](result[i], [d3.select("#" + expanded[(i - (1 + i / 2))] + ".mainrow").node()]);
                    plotArgs = plotArgs.concat(result[i][0]);
                    callbacks[3](result[i + 1], [d3.select("#" + expanded[(i - (1 + i / 2))] + ".mainrow").node()]);
                }
                if (d3.selectAll(".expanded").empty()) {
                    ScatterPlot.setCircleType("degree");
                    callbacks[2](result[0]);
                } else {
                    ScatterPlot.setCircleType("course");
                    callbacks[2]([plotArgs]);
                }
                callbacks[2] = ScatterPlot.update;
            });
        });
        break;
    case callbacks[1]:
        var expandedRows = d3.selectAll(".expanded");
        plotArgs = [{"courses": [aggregation + "Acronym="]}];
        lineRequest = aggregation === "degree" ? [lineAcronym + "=" + funcparam[0].id] : [lineAcronym + "=" + funcparam[0].id, filteredCondition];
        lineArgs = {};
        lineArgs[tableSearch] = lineRequest;
        lineArgs.terms = "";
        ScatterPlot.setCircleType("course");
        if (d3.select(funcparam[0]).attr("class").indexOf('expanded') === -1) {
            plotArgs[0].courses[0] += funcparam[0].id;
        }
        if (expandedRows.size() === 1 && funcparam[0].id === expandedRows.node().id) {
            plotArgs = [{"degrees": ""}];
            ScatterPlot.setCircleType("degree");
            if (!d3.selectAll(".firstLabel, .secondLabel").empty()) {
                plotArgs = parseAcronym();
            }
        } else {
            expandedRows.each(function (d, i, l) {
                if (this !== funcparam[0]) {
                    var id = ',' + d.key;
                    plotArgs[0].courses[0] += id;
                }
            });
        }
        d3.queue()
            .defer(requestHandler, args)
            .defer(requestHandler, plotArgs)
            .defer(requestHandler, [lineArgs])
            .await(function (error, url1, url2, url3) {
                d3.queue()
                    .defer(request, url1, 0, [])
                    .defer(request, url2, 0, [])
                    .defer(request, url3, 0, [])
                    .await(function (error, result1, result2, result3) {
                        callbacks[1](result1, funcparam);
                        if (d3.select(funcparam[0]).classed("expanded")) {
                            callbacks[3](result3, funcparam);
                        } else {
                            d3.select("#" + funcparam[0].id + ".infoChart")
                                .transition()
                                .duration(400)
                                .remove();
                        }
                        if (expandedRows.size() === 1 && funcparam[0].id === expandedRows.node().id && aggregation === "course") {
                            callbacks[2]([filterData(result2)]);
                        } else {
                            callbacks[2](result2);
                        }
                    });
            });
        break;
    case callbacks[3]:
        d3.queue()
            .defer(requestHandler, args)
            .await(function (error, url1) {
                d3.queue()
                    .defer(request, url1, 0, [])
                    .await(function (error, result1) {
                        callbacks[3](result1, funcparam);
                    });
            });
        break;
    case callbacks[4]:
        d3.queue()
            .defer(requestHandler, args)
            .await(function (error, url1) {
                d3.queue()
                    .defer(request, url1, 0, [])
                    .await(function (error, result1) {
                        callbacks[4](result1, funcparam);
                    });
            });
        break;
    case callbacks[5]:
        d3.queue()
            .defer(requestHandler, args)
            .await(function (error, url1) {
                d3.queue()
                    .defer(request, url1, 0, [])
                    .await(function (error, result1) {
                        callbacks[5](result1, funcparam);
                    });
            });
        break;
    case callbacks[6]:
        d3.queue()
            .defer(requestHandler, args)
            .await(function (error, url1) {
                d3.queue()
                    .defer(request, url1, 0, [])
                    .await(function (error, result1) {
                        callbacks[6](result1, funcparam);
                    });
            });
        break;
    }
}