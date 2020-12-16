
//static\js\search.js

$(document).ready(function() {

    var words = [];
    sessionStorage.setItem('words_list', []);
    var topics = JSON.parse(window.localStorage.getItem("topics_received"));
    if(topics && topics.length()>0) {
      alert(topics)
    }

    /* --------------------------------
        btn_topics ("Envoyer")
        url : '/topics'
        sends selected params to flask
        and displays topics received
    ----------------------------------*/

    $('#btn_topics').bind('click', function(event) {

      // var words = [];
      // sessionStorage.setItem('words_list', []);

      // get params from forms
      var twords = $("#range_twords").val();
      var model = $("#sel_model").val();
      var section = $("#sel_section").val();
      var topics = $("#range_topics").val();
      var docs = $("#range_docs").val();
      var select_params = {
        'sel_twords' : twords,
        'sel_model' : model,
        'sel_section' : section,
        'sel_topics' : topics,
        'sel_docs' : docs
      };
      sessionStorage.setItem('select_params', JSON.stringify(select_params));

      // send params to flask
      $.ajax({
        data : {
          sel_twords : twords,
          sel_model : model,
          sel_section : section,
          sel_topics : topics,
          sel_docs : docs,
          },
          type : 'POST',
          url : '/topics'
        })
        .done(function(data) {
          // empty table before all
          $("#words_selection").empty();
          if(data.topics==0){
            // No topics received
            console.log("ERROR");
          }
        else {
          // display topics
          $("#topics_display").show();
          $("#loading-infos").hide();

          // rappel params
          params = $('<div>'+section+' &middot; '+model+' model &middot; '+twords+' top-words &middot; '+topics+' topics &middot; '+docs+' documents</div>');
          $("#rappel_params").html(params);

          // store topics
          sessionStorage.setItem('topics_received', JSON.stringify(data.topics));

          // append table
          jQuery.each(data.topics, function(i,data) {
            // creation element row
            i++;
            row = $('<tr class="twords_row"><td>' + i + '</td></tr>');
            $("#words_selection").append(row);
            // append to row
            data[1].forEach(element => {
              var item = $('<td class="tword">'+element+'</td>');
              row.append(item);
            });
          });

          /* --------------------------------
              Click on twords
          ----------------------------------*/
          $( "#words_selection .tword" ).click(function() {
            $( this ).toggleClass("clicked");
            var word = $( this ).text();
            // check if is present before to add
            const index = words.indexOf(word);
            (index > -1) ? words.splice(index, 1) : words.push(word);
            // update sessionStorage var
            sessionStorage.setItem('words_list', words);
            // display selected words
            $('#words_selected').text(words.join(' · '));
            // if some words are selected
            if (words.length > 0) {
              // remove message "No item selected"
              $('#result_message').empty();
            }
          });
        }

    });
    event.preventDefault();
    });

    /* --------------------------------
        btn_reset_params
    ----------------------------------*/
    
    $( "#btn_reset_params" ).click(function() {
      // remove top words array
      $("#words_selection").empty();
      $("#topics_display").hide();
      $("#loading-infos").hide();
      // remove sessionStorage var
      sessionStorage.clear();
    });

    /* --------------------------------
        btn_search ("Rechercher")
        url : '/search'
        send selected words to flask
        and then redirect to '/exploration'
    ----------------------------------*/

    $('#btn_search').bind('click', function(event) {
        $.ajax({
          data : {w : sessionStorage.getItem('words_list')},
          type : 'POST',
          url : '/search'
        })
        .done(function(data) {
          if(data.result==0) {
            $("#result_message").text("Veuiller sélectionner des top-words ! Merci.");
          }
          else {
            document.location.href='/exploration';
          }
        });
        event.preventDefault();
      });

    /* --------------------------------
        reset_words_select
    ----------------------------------*/

    $("#reset_words_select").click(function() {
        // empty words var
        words = [];
        // console.log(words);
        // update sessionStorage var
        sessionStorage.setItem('words_list', words);
        // sessionStorage.removeItem('words_list');
        // reset message
        $('#words_selected').text("Cliquer sur les top-words à sélectionner.");
        // remove class
        $( "#topics_display .tword" ).removeClass( "clicked" )
        // remove message "No item ..."
        $('#result_message').empty();
    });

    /* --------------------------------
        update total of possible docs
    ----------------------------------*/

    var selected_section = $('#sel_section').find(":selected").text();
    max_docs = selected_section.split(' ')[2];
    document.getElementById("range_docs").max = max_docs;

    $('#sel_section').on('change', function() {
      selected_section = $("#sel_section option:selected").html();
      max_docs = selected_section.split(' ')[2];selected_section.split(' ')[2];
      document.getElementById("range_docs").max = max_docs;
    });

});