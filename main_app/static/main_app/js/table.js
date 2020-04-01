$(function(){
    var container = $('.market-table')
    $('<div class="h-100 lds-dual-ring-md"></div>').appendTo(container)
    sendAjax()

    $('#expand').click(_.debounce(function(){
        if ($('#expand').text() == 'Expand') {
            $('#expand').text('Collapse')
            sendAjax()
        } else {
            $('#expand').text('Expand')
            sendAjax()
        };
    },150));

    function sendAjax() {
        if ($('#expand').text() == 'Expand') {
            var expanded = false
        } else {
            var expanded = true
        };
        
        $(container).empty()
        $('<div class="h-100 lds-dual-ring-md"></div>').appendTo(container)
        $.ajax({
            url: '/dev/ajax/all/',
            data: {
            'link': window.location.href,
            'expanded': expanded,
            },
            // error: function(xhr, status, error) {
            // 	console.log(xhr.responseText);
            //   },
            success: function(data){
                container.empty()
                
                if (data['data_list'].length != 0){
                    container.append('<thead><tr></tr></thead>')
                    data['fields'].forEach(e => {
                        $('.market-table tr').append('<th>'+e+'</th>')
                    });
                    container.append('<tbody></tbody>')
                    data['data_list'].forEach(e => {
                        s = ''
                        var hrf = '/dev/asset/' + e['static']['country'].toLowerCase() + '/' + e['static']['Type'] + '/' + e['static']['id'] + '/'
                        s += '<td><a href="' + hrf + '">'+ Object.values(e['live'])[0] + '</a></td>'
                        Object.values(e['live']).slice(1).forEach(v => {
                            if (v.includes('+')) {
                                if (v.includes('%')) {
                                    s += '<td><span class="ml-0 d-initial change up">'+ v + '</span></td>'
                                } else {
                                    s += '<td><span class="ml-0 d-initial text-success">'+ v + '</span></td>'
                                }
                            } else if (v.includes('-')) {
                                if (v.includes('%')) {
                                    s += '<td><span class="ml-0 d-initial change down">'+ v + '</span></td>'
                                } else {
                                    s += '<td><span class="ml-0 d-initial text-danger">'+ v + '</span></td>'
                                }
                            } else {
                                s += '<td>'+ v + '</td>'
                            };
                        });
                        $('.market-table tbody').append('<tr>' + s + '</tr>')
                    
                    });
                } else {
                    $('<h5 class="text-white text-center py-3 mb-0">No data found</h5>').appendTo(container);
                };
            }
        });
    };
});
