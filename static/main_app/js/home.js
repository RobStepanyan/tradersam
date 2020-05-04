$(function () {
  var country = $('#pr-1 .btn-primary.active input').attr('id')
  var type_ = $('#pl-1 .btn-primary.active input').attr('id')
  var container = $('#main-table')
  var container2 = $('#market-carousel')
  var countries = {
    'G': 'All Countries', 'US': 'United States', 'JP': 'Japan', 'UK': 'United Kingdom',
    'HK': 'Hong Kong', 'CH': 'China', 'CA': 'Canada', 'GE': 'Germany', 'AU': 'Australia'
  }
  $('#carousel-header').text(countries[country])
  $('#main-table-header').append('<img class="country-flag-lg" src="/static/main_app/svg/flags/' + country.toLowerCase() + '.svg">')
  $('#main-table-header').append(' ' + type_)

  $('#main-table-more').attr('href', '/dev/all/' + country.toLowerCase() + '/' + type_.toLowerCase() + '/')
  sendAjax()
  sendAjaxCarousel()
  sendAjaxUserTable()
  $('#pr-1 .btn-primary').click(_.debounce(function () {
    country = $('#pr-1 .btn-primary.active input').attr('id')
    if (type_ == 'Commodities' || type_ == 'Currencies' || type_ == 'Cryptocurrencies') {
      country = 'G'
    } else {
      country = $('#pr-1 .btn-primary.active input').attr('id')
    };
    $('#main-table-header').empty()
    $('#main-table-header').append('<img class="country-flag-lg" src="/static/main_app/svg/flags/' + country.toLowerCase() + '.svg">')
    $('#main-table-header').append(' ' + type_)
    if (country == 'G') {
      $(container2).empty()
    }
    $('#carousel-header').text(countries[country])
    $('#main-table-more').attr('href', '/dev/all/' + country.toLowerCase() + '/' + type_.toLowerCase() + '/')
    sendAjax()
    sendAjaxCarousel()
  }, 150));
  $('#pl-1 .btn-primary').click(_.debounce(function () {
    type_ = $('#pl-1 .btn-primary.active input').attr('id')
    if (type_ == 'Commodities' || type_ == 'Currencies' || type_ == 'Cryptocurrencies') {
      country = 'G'
    } else {
      country = $('#pr-1 .btn-primary.active input').attr('id')
    };
    if (country == 'G') {
      $(container2).empty()
    }
    $('#carousel-header').text(countries[country])
    $('#main-table-header').empty()
    $('#main-table-header').append('<img class="country-flag-lg" src="/static/main_app/svg/flags/' + country.toLowerCase() + '.svg">')
    $('#main-table-header').append(' ' + type_)
    $('#main-table-more').attr('href', '/dev/all/' + country.toLowerCase() + '/' + type_.toLowerCase() + '/')
    sendAjax()
  }, 150));

  function sendAjax() {
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
      success: function (data) {
        container.empty()
        if (data['data_list'].length != 0) {
          container.append('<thead><tr></tr></thead>')
          data['fields'].forEach(e => {
            $('#main-table tr').append('<th>' + e + '</th>')
          });
          container.append('<tbody></tbody>')
          data['data_list'].forEach(e => {
            s = ''
            var hrf = '/dev/asset/' + e['static']['country'].toLowerCase() + '/' + e['static']['Type'] + '/' + e['static']['id'] + '/'
            s += '<td><a href="' + hrf + '">' + Object.values(e['live'])[0] + '</a></td>'
            Object.values(e['live']).slice(1).forEach(v => {
              if (v) {
                if (v.includes('+')) {
                  if (v.includes('%')) {
                    s += '<td><span class="ml-0 d-initial change up">' + v + '</span></td>'
                  } else {
                    s += '<td><span class="ml-0 d-initial text-success">' + v + '</span></td>'
                  }
                } else if (v.includes('-')) {
                  if (v.includes('%')) {
                    s += '<td><span class="ml-0 d-initial change down">' + v + '</span></td>'
                  } else {
                    s += '<td><span class="ml-0 d-initial text-danger">' + v + '</span></td>'
                  }
                } else {
                  s += '<td>' + v + '</td>'
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
      success: function (data) {
        container2.empty()
        if (data['data_list'].length != 0) {
          data['data_list'].forEach(dct => {
            s = '<a href="/dev/asset/' + dct['static']['country'].toLowerCase() + '/index/' + dct['static']['id'] + '/">' +
              `<div class="card asset-card card mr-3">
                        <div class="row mb-1">
                        <span class="long-name">` + dct['static']['long_name'] + `</span>
                        </div>
                        <div class="row justify-content-between">
                        <span class="short-name">` + dct['static']['short_name'] + '</span>'

            if (dct['live'] == '+0.00%') {
              s += '<span class="change text-white">' + dct['live'] + '</span></div>'
            } else if (dct['live'].includes('-')) {
              s += '<span class="change down">' + dct['live'] + '</span></div>'
            } else if (dct['live'].includes('+')) {
              s += '<span class="change up">' + dct['live'] + '</span></div>'
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

  function sendAjaxUserTable() {
    $.ajax({
      url: '/ajax/account/',
      data: {
        'dep': 'watchlists'
      },
      success: function (data) {
        if (data['watchlists'].length == 0) {
          content = 
          `
          <h3 class="text-white text-center ml-0 mb-3"><i class="fas fa-user"></i> Your Watchlists</h3>
          <div class="position-absolute card justify-content-center">
            <a href="/account/">
              <h1 class="display-3 text-center"><i class="fas fa-plus"></i></h1>
              <h4 class="text-center">Create a Watchlist</h4>
            </a>
          </div>
          <table class="market-table mb-3 table-striped filter-blur shadow">
            <thead>
              <tr>
                <th></th>
                <th>Ticker</th>
                <th>Last Price</th>
                <th>Change</th>
                <th>Change %</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><i class="fa fa-globe text-dark country-flag-md mb-0"></i></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <td><i class="fa fa-globe text-dark country-flag-md mb-0"></i></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <td><i class="fa fa-globe text-dark country-flag-md mb-0"></i></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <td><i class="fa fa-globe text-dark country-flag-md mb-0"></i></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <td><i class="fa fa-globe text-dark country-flag-md mb-0"></i></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <td><i class="fa fa-globe text-dark country-flag-md mb-0"></i></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <td><i class="fa fa-globe text-dark country-flag-md mb-0"></i></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <td><i class="fa fa-globe text-dark country-flag-md mb-0"></i></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <td><i class="fa fa-globe text-dark country-flag-md mb-0"></i></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
              <tr>
                <td><i class="fa fa-globe text-dark country-flag-md mb-0"></i></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
            </tbody>
          </table>
          `
          var parent = $('#user-table-header').parent().parent()
          parent.empty()
          $(content).appendTo(parent)
          return
        }

        // Table header
        var user_table_dropdown =
          `
        <div class="dropdown" id="user-table-dropdown">
          <a class="btn btn-primary-dark dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            ${data['watchlists'][0]['name']}
          </a>
          <div class="dropdown-menu" data-toggle="buttons">
        `
        data['watchlists'].forEach(watch => {
          user_table_dropdown +=
            `<label class="btn dropdown-item">
            <input type="radio" id="${watch['name']}" autocomplete="off" checked="">${watch['name']}
          </label>`
        })

        user_table_dropdown += `
          </div>
        </div>
        `
        $('#user-table-header').after($(user_table_dropdown))
        $('#user-table-header').parent().find('.dropdown-menu label').first().addClass('active')
        
        displayWatch(data['watchlists'][0])
        
        $('#user-table-dropdown .dropdown-item').click(function(){
          $.ajax({
            url: '/ajax/account/',
            data: {
              'dep': 'watchlists'
            },
            success: function (data) {
              // Table header
              $('#user-table-dropdown a.dropdown-toggle').text($('#user-table-dropdown .dropdown-item.active').text())
              
              data['watchlists'].forEach(watch => {
                console.log()
                console.log(watch['name'] == $('#user-table-dropdown .dropdown-item.active').text())
                if (watch['name'] == $('#user-table-dropdown .dropdown-item.active').text().trim()) {
                  displayWatch(watch)
                }
              });
            }
          })
        })
      }
    })
  }
  function displayWatch(watch) {
    $('#user-table').empty()
    // Table
    var user_table =
      `
      <thead>
        <tr>
          <th></th>
          <th>Symbol</th>
          <th>Last</th>
          <th>Change</th>
          <th>Volume</th>
        </tr>
      </thead>
      <tbody>
      `
    watch['asset_links'].forEach(row => {
      var type = row['type']
      var country = row['country']
      if (type == 'Currency') {
        c = 'crncy'
      } else if (type == 'Cryptocurrency') {
        c = 'crptcrncy'
      } else {
        c = country.toLowerCase()
      };
      user_table +=
        `
        <tr>
          <td><img class="country-flag-md" src="/static/main_app/svg/flags/${c}.svg" alt=""></td>
          <td><a href="${row['href']}">${row['short_name']}</a></td>
          <td>${row['last']}</td>
        `

      if (row['change_perc'].includes('-')) {
        user_table += `<td><span class="ml-0 d-initial change down">${row['change_perc']}</span></td>`
      } else if (row['change_perc'].includes('+')) {
        user_table += `<td><span class="ml-0 d-initial change up">${row['change_perc']}</span></td>`
      } else {
        user_table += `<td><span class="ml-0 d-initial change">${row['change_perc']}</span></td>`
      }
      user_table +=
        `
          <td>${row['volume']}</td>
        </tr>
        `
    });
    user_table += '</tbody>'
    $(user_table).appendTo($('#user-table'))
  }
});