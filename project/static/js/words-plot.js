var data = data_words;
var margin, width, height;
var x, y, svg;

function drawPlot() {

// get the current width of the div where the chart appear, and attribute it to Svg
currentWidth = parseInt(d3.select('.container-fluid').style('width'), 10);
console.log(currentWidth);

// set the dimensions and margins of the graph
margin = {top: 20, right: 20, bottom: 30, left: 100};
width = currentWidth - margin.left - margin.right;
height = 500 - margin.top - margin.bottom;

// set the ranges
y = d3.scaleBand()
          .range([height, 0])
          .padding(0.1);

x = d3.scaleLinear()
          .range([0, width]);
          
// append the svg object to the body of the page
// append a 'group' element to 'svg'
// moves the 'group' element to the top left margin
svg = d3.select("#words-barplot").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");

  // format the data
  data.forEach(function(d) {
    d.score = +d.score;
  });

  // Scale the range of the data in the domains
  x.domain([0, d3.max(data, function(d){ return d.score; })])
  y.domain(data.map(function(d) { return d.token; }));
  //y.domain([0, d3.max(data, function(d) { return d.score; })]);

  // append the rectangles for the bar chart
  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      //.attr("x", function(d) { return x(d.score); })
      .attr("width", function(d) {return x(d.score); } )
      .attr("y", function(d) { return y(d.token); })
      .attr("height", y.bandwidth());

  // add the x Axis
  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  // add the y Axis
  svg.append("g")
      .call(d3.axisLeft(y));

}

drawPlot()
    
// Add an event listener that run the function when dimension change
window.addEventListener('resize', drawPlot )