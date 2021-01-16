//   var data = [{"token":"Bob","score":33},{"token":"Robin","score":12},{"token":"Anne","score":41},{"token":"Mark","score":16},{"token":"Joe","score":59},{"token":"Eve","score":38},{"token":"Karen","score":21},{"token":"Kirsty","score":25},{"token":"Chris","score":30},{"token":"Lisa","score":47},{"token":"Tom","score":5},{"token":"Stacy","score":20},{"token":"Charles","score":13},{"token":"Mary","score":29}];
  var data = data_words;


  // set the dimensions and margins of the graph
  var margin = {top: 20, right: 20, bottom: 30, left: 100},
      width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;
  
  // set the ranges
  var y = d3.scaleBand()
            .range([height, 0])
            .padding(0.1);
  
  var x = d3.scaleLinear()
            .range([0, width]);
            
  // append the svg object to the body of the page
  // append a 'group' element to 'svg'
  // moves the 'group' element to the top left margin
  var svg = d3.select("#words-barplot").append("svg")
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
  
  