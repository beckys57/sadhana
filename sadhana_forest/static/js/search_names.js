$(document).ready(function(){
    $("#search").on('keyup', function(){
        console.log('Search');
        var query = $(this).val();
        var data = {'query':query}
        var url = "{% url 'people:filter_list' %}"
        console.log('Url', url)
    
        
        $.ajax({
              type: 'GET',
              url: url+'?query='+query,
              success: function(returned){
                console.log('success', returned);
                $('#people').html(returned['html'])
              },
              error: function(){
                console.log('failure');
              }
            
        })
    });
});
    