if (window.location.href.includes('all/')) {
    // || window.location.href.endsWith('dev/')
$(function(){
    var container = $('.market-table')
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
                
                container.append('<thead><tr></tr></thead>')
                data['fields'].forEach(e => {
                    $('.market-table tr').append('<th>'+e+'</th>')
                });
                container.append('<tbody></tbody>')
                data['data_list'].forEach(e => {
                    s = ''
                    
                    Object.values(e['live']).forEach(v => {
                        console.log(v)
                        if (v.includes('+')) {
                            if (v.includes('%')) {
                                s += '<td><span class="change up">'+ v + '</span></td>'
                            } else {
                                s += '<td><span class="text-success">'+ v + '</span></td>'
                            }
                        } else if (v.includes('-')) {
                            if (v.includes('%')) {
                                s += '<td><span class="change down">'+ v + '</span></td>'
                            } else {
                                s += '<td><span class="text-danger">'+ v + '</span></td>'
                            }
                        } else {
                            s += '<td>'+ v + '</td>'
                        };
                    });
                    $('.market-table tbody').append('<tr>' + s + '</tr>')
                
                });
            }
        });
    };
});
}
