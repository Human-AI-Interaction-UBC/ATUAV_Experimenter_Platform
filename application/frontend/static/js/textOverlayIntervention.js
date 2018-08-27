/**
 * Created by enamul on 6/4/2017.
 */

var vis = d3.select("#overlayText"),//.append("svg")
/*        .attr("width", 500)
        .attr("height", 667)
        .style("position", "absolute"),*/

    scaleX = d3.scale.linear()
        .domain([0,450])
        .range([0,450]),

    scaleY = d3.scale.linear()
        .domain([0,500])
        .range([500,0]);

/*
    poly = [{"x":0.0, "y":25.0},
      {"x":8.5,"y":23.4},
      {"x":13.0,"y":21.0},
      {"x":19.0,"y":15.5}];
*/

/*drawOverlay(poly);*/
function drawOverlay(poly) {
    console.log(JSON.stringify(poly));
  vis.selectAll("polygon").remove();

  vis.selectAll("polygon")
      .data([poly])
      .enter().append("polygon")
      .attr("points",function(d) {
        //offset from the initial screen coordinats: 450, 190
        return d.map(function(d) { return [d.x-130,d.y-80].join(","); }).join(" ");})
      .attr("fill","yellow")
      .attr("stroke","black")
      .attr("stroke-width",.5)
      .style("opacity",.5);
}
