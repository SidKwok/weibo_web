    $(function () {
        $("#search").bind('click', function () {
            $.ajax({
                type: "GET",
                url: "/search/",
                dataType: "json",
                success: function (data) {
                    $("#name").text(data.name);
                    $("#sex").text(data.sex);
                    $("#area").text(data.area);
                    //                    $("#birthday").text(data.birthday);
                    //                    $("#summary").text(data.summary);
                }
            });
        })

    })

    //    var dataset = {
    //        nodes: [
    //            {
    //                name: "Natalie"
    //            },
    //        ],
    //        edges: []
    //    };
    var dataset = {
        nodes: [],
        edges: []
    };

    $(function () {
        $("#fansearch").bind('click', function () {
            $.ajax({
                type: "GET",
                url: "/fansearch/",
                dataType: "json",
                beforeSend: function (xhr) {
                    $("#loading").show();
                },
                success: function (data) {
                    dataset.nodes.push({
                        name: data[0].name,
                        sex: data[0].sex,
                        area: data[0].area,
                        url: data[0].url,
                        icon: data[0].icon
                    })
                    for (var i = 1; i < data.length; i++) {
                        dataset.nodes.push({
                            //                            name: data[i]
                            name: data[i].name,
                            sex: data[i].sex,
                            area: data[i].area,
                            url: data[i].url,
                            icon: data[i].icon
                        });
                        dataset.edges.push({
                            source: i,
                            target: 0
                        });
                    }
                },
                complete: function () {
                    $("#loading").hide();
                    showData();
                }
            });
        })

    })

    function showData() {

        ele = document.getElementById("container");
        var w = ele.clientWidth;
        var h = ele.clientHeight;
        //Initialize a default force layout, using the nodes and edges in dataset
        var force = d3.layout.force()
            .nodes(dataset.nodes)
            .links(dataset.edges)
            .size([w, h])
            .linkDistance([70])
            .charge([-100])
            .start();

        var colors = d3.scale.category10();

        //Create SVG element
        var svg = d3.select(ele)
            .append("svg")
            .attr("width", w)
            .attr("height", h);

        //Create edges as lines
        var edges = svg.selectAll("line")
            .data(dataset.edges)
            .enter()
            .append("line")
            .style("stroke", "#ccc")
            .style("stroke-width", 1);

        //Create nodes as circles
        var nodes = svg.selectAll("circle")
            .data(dataset.nodes)
            .enter()
            .append("circle")
            .attr("r", 10)
            .style("fill", function (d, i) {
                return colors(i);
            })
            .call(force.drag);

        //鼠标点击事件
        nodes.on("click", function (d) {
            window.open(d.url);
        })

        //        悬停效果
        nodes.on("mouseover", function (d, i) {
            var xPosition = parseFloat(d3.select(this).attr("cx"));
            var yPosition = parseFloat(d3.select(this).attr("cy"));
            var tipColor = colors(i);

            $("#icon").attr("src", d.icon);

            d3.select(this)
                .transition()
                .duration(250)
                .attr("r", 20);

            d3.select("#tooltip")
                .style("left", xPosition + "px")
                .style("top", yPosition + "px")
                .style("background-color", tipColor)
                .select("#name")
                .text(d.name);
            d3.select("#tooltip")
                .select("#sex")
                .text(d.sex);
            d3.select("#tooltip")
                .select("#area")
                .text(d.area);

            d3.select("#tooltip").classed("hidden", false);

        });


        nodes.on("mouseout", function (d, i) {
            d3.select(this)
                .transition()
                .duration(250)
                .attr("r", 10);

            d3.select("#tooltip").classed("hidden", true);
        });

        //Every time the simulation "ticks", this will be called
        force.on("tick", function () {

            edges.attr("x1", function (d) {
                    return d.source.x;
                })
                .attr("y1", function (d) {
                    return d.source.y;
                })
                .attr("x2", function (d) {
                    return d.target.x;
                })
                .attr("y2", function (d) {
                    return d.target.y;
                });

            nodes.attr("cx", function (d) {
                    return d.x;
                })
                .attr("cy", function (d) {
                    return d.y;
                });

        });



    }
