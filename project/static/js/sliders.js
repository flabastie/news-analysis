// sliders.js


// slider_twords

var slider_twords = document.getElementById("range_twords");
var output_twords = document.getElementById("value_twords");

if (slider_twords) {
  output_twords.innerHTML = slider_twords.value;
}

if(output_twords) {
  slider_twords.oninput = function() {
    output_twords.innerHTML = this.value;
  }
}

// slider_topics

var slider_topics = document.getElementById("range_topics");
var output_topics = document.getElementById("value_topics");

if (slider_topics) {
  output_topics.innerHTML = slider_topics.value;
}

if (output_topics) {
  slider_topics.oninput = function() {
    output_topics.innerHTML = this.value;
  }
}

// slider_docs

var slider_docs = document.getElementById("range_docs");
var output_docs = document.getElementById("value_docs");

if (slider_docs) {
  output_docs.innerHTML = slider_docs.value;
}

if (output_docs) {
  slider_docs.oninput = function() {
    output_docs.innerHTML = this.value;
  }
}


