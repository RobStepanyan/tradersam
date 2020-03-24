if (window.location.pathname == '/dev/' ){
$(function(){
    var country = $('#pr-1 .btn-primary.active input').attr('id')
    var type_ = $('#pl-1 .btn-primary.active input').attr('id')
    var container = $('#main-table')
    sendAjax()
    $('#pr-1 .btn-primary').click(_.debounce(function(){
        country = $('#pr-1 .btn-primary.active input').attr('id')
        sendAjax()
    },150));
    $('#pl-1 .btn-primary').click(_.debounce(function(){
        type_ = $('#pl-1 .btn-primary.active input').attr('id')
        sendAjax()
    },150));

    function sendAjax(){
        container.empty()
        $('<div class="h-100 lds-dual-ring-md"></div>').appendTo(container)

        $.ajax({
            url: '/dev/ajax/home',
            data: {
                'country': country,
                'type_': type_
            },
            // error: function(xhr, status, error) {
            // 	console.log(xhr.responseText);
            //   },
            success: function(data){
                container.empty()
                
                container.append('<thead><tr></tr></thead>')
                data['fields'].forEach(e => {
                    $('#main-table tr').append('<th>'+e+'</th>')
                });
                container.append('<tbody></tbody>')
                data['data_list'].forEach(e => {
                    s = ''
                    var hrf = '/dev/asset/' + e['static']['country'].toLowerCase() + '/' + e['static']['Type'] + '/' + e['static']['id'] + '/'
                    s += '<td><a href="' + hrf + '">'+ Object.values(e['live'])[0] + '</a></td>'
                    Object.values(e['live']).slice(1).forEach(v => {
                        if (v) {
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
                        } else {
                            s += '<td>N/A</td>'
                        };
                    });
                    $('#main-table tbody').append('<tr>' + s + '</tr>')
                
                });
            }
        })
    };
});
};