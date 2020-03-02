$(document).ready(function() {

 // Set the CSRF token so that we are not rejected by server
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    // Configure ajaxSetupso that the CSRF token is added to the header of every request
  $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
              }
        }
      }
);
    // Attach a function to trigger when users click on the voting links - either an up
//vote, or a down vote
    $("a.choose").on("click", function() {
        var clicked_obj = $(this);
        // Which idea was clicked? Fetch the idea ID
        var G_id = $(this).attr('id');
    // Is it an upvote or downvote?
        var choose_type = $(this).children()[0].id;

        var choose_type2 = $(this).children()[1].id;
        // This is the actual call which sends data to the server. It captures the data we
//need in order to update the vote count: the ID of the idea which was clicked, and which
//count to incrememnt.
        $.ajax({
            url: '/collect',
            type: 'POST',
            data: JSON.stringify({ game_id: G_id, choose_type: choose_type,choose_type2:choose_type2}),
      // We are using JSON, not XML
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response){
                console.log(response);
                // Update the html rendered to reflect new count
                // Check which count to update
                if(choose_type == "like") {
                   clicked_obj.children()[1].innerHTML = " " + response.Likes;
                } else {
                    clicked_obj.children()[1].innerHTML = " " + response.Dislikes;
                }
            },
            error: function(error){
                console.log(error);
            }
});
    });
});