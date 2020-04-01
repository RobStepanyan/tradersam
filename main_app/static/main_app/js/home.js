$(function(){
    var country = $('#pr-1 .btn-primary.active input').attr('id')
    var type_ = $('#pl-1 .btn-primary.active input').attr('id')
    var container = $('#main-table')
    var container2 = $('#market-carousel')
    var countries = {
        'G':'All Countries', 'US': 'United States', 'JP': 'Japan', 'UK':'United Kingdom',
        'HK': 'Hong Kong', 'CH':'China', 'CA': 'Canada', 'GE': 'Germany', 'AU': 'Australia'
    } 
    $('#carousel-header').text(countries[country])
    $('#main-table-header').append('<img class="country-flag-lg" src="/static/main_app/svg/flags/'+ country.toLowerCase() + '.svg">')
    $('#main-table-header').append(' '+type_)

    $('#main-table-more').attr('href', '/dev/all/'+country.toLowerCase()+'/'+type_.toLowerCase()+'/')
    sendAjax()
    sendAjaxCarousel()
    $('#pr-1 .btn-primary').click(_.debounce(function(){
        country = $('#pr-1 .btn-primary.active input').attr('id')
        if (type_ == 'Commodities' || type_ == 'Currencies' || type_ == 'Cryptocurrencies') {
            country = 'G'
        } else {
            country = $('#pr-1 .btn-primary.active input').attr('id')
        };
        $('#main-table-header').empty()
        $('#main-table-header').append('<img class="country-flag-lg" src="/static/main_app/svg/flags/'+ country.toLowerCase() + '.svg">')
        $('#main-table-header').append(' '+type_)
        $('#carousel-header').text(countries[country])
        $('#main-table-more').attr('href', '/dev/all/'+country.toLowerCase()+'/'+type_.toLowerCase()+'/')
        sendAjax()
        sendAjaxCarousel()
    },150));
    $('#pl-1 .btn-primary').click(_.debounce(function(){
        type_ = $('#pl-1 .btn-primary.active input').attr('id')
        if (type_ == 'Commodities' || type_ == 'Currencies' || type_ == 'Cryptocurrencies') {
            country = 'G'
        } else {
            country = $('#pr-1 .btn-primary.active input').attr('id')
        };
        $('#main-table-header').empty()
        $('#main-table-header').append('<img class="country-flag-lg" src="/static/main_app/svg/flags/'+ country.toLowerCase() + '.svg">')
        $('#main-table-header').append(' '+type_)
        $('#main-table-more').attr('href', '/dev/all/'+country.toLowerCase()+'/'+type_.toLowerCase()+'/')
        sendAjax()
    },150));

    function sendAjax(){
        container.empty()
        $('<div class="h-100 lds-dual-ring-md"></div>').appendTo(container)

        $.ajax({
            url: '/dev/ajax/home/main-table',
            data: {
                'country': country,
                'type_': type_
            },
            // error: function(xhr, status, error) {
            // 	console.log(xhr.responseText);
            //   },
            success: function(data){
                container.empty()
                if (data['data_list'].length != 0){
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
                } else {
                    $('<h5 class="text-white text-center py-3 mb-0">No data found</h5>').appendTo(container);
                };
            }
        })
    };

    function sendAjaxCarousel() {
        container2.empty()
        $('<div class="h-100 lds-dual-ring-md"></div>').appendTo(container2)

        $.ajax({
            url: '/dev/ajax/home/carousel/',
            data: {
                'country': country,
            },
            // error: function(xhr, status, error) {
            // 	console.log(xhr.responseText);
            //   },
            success: function(data){
                container2.empty()
                if (data['data_list'].length != 0){
                    data['data_list'].forEach(dct => {
                        s = '<a href="/dev/asset/'+ dct['static']['country'].toLowerCase()+'/index/'+ dct['static']['id']+'/">' +
                        `<div class="card asset-card card mr-3">
                        <div class="row mb-1">
                        <span class="long-name">` + dct['static']['long_name'] + `</span>
                        </div>
                        <div class="row justify-content-between">
                        <span class="short-name">` + dct['static']['short_name'] + '</span>'
                        
                        if (dct['live'] == '+0.00%') {
                            s+= '<span class="change text-white">' + dct['live'] + '</span></div>' 
                        } else if (dct['live'].includes('-')) {
                            s +='<span class="change down">' + dct['live'] + '</span></div>'
                        } else if (dct['live'].includes('+')) {
                            s+= '<span class="change up">'+ dct['live'] + '</span></div>'
                        };
                        s += '</div></div></a>'
                        container2.append(s)
                    });
                    container2.attr('class', 'row')
                    container2.slick({
                        slidesToShow: 5,
                        variableWidth: true,
                        slidesToScroll: 1,
                        autoplay: true,
                        autoplaySpeed: 2000,
                    });
                } else {
                    $('<h5 class="text-white text-center py-3 mb-0 w-100">No data found</h5>').appendTo(container2);
                };
            }
        })
    }
});