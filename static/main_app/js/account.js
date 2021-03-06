$(function () {
  /*
  Overview
  
  1. Load HTML ( loadHTML() )
  loads html_template, contains main js scripts 
  (e.g. change password button .click() function)
  2. getData() -> displayData()
  gets init data with ajax (getData)
  generates html to display that data (displayData)
  */
  var container = $('#main-container')
  var getLoadDebounce = _.debounce(function () { loadHTML(); getData(); }, 250);
  loadHTML()
  getData()

  $('.tab').click(function () {
    container.empty()
    container.addClass('d-flex')
    $('<div class="h-100 lds-dual-ring-md m-auto"></div>').appendTo(container)
    getLoadDebounce()
  })

  // CSRF Protection
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  // End of CSRF Protection

  function loadHTML() {
    container.addClass('d-none')
    container.removeClass('d-flex')
    container.empty()
    dep = $('.tab.active').attr('id')
    if (dep == 'security') {
      $(html_templates['security']).appendTo(container)
      $('#personal-button').click(function () {
        email = $('input#email').val()
        username = $('input#username').val()

        if (username != init_username) {
          $.ajax({
            url: '/ajax/account/change-username/',
            data: {
              'username': username
            },
            success: function (data) {
              if (data['valid']) {
                message =
                  `
								<ul class="px-2 m-0" id="message-username">
								<li class="text-success font-weight-bold list-unstyled">${data['message']}</li>
								</ul>
								`
              } else {
                message =
                  `
								<ul class="px-2 m-0" id="message-username">
								<li class="text-danger font-weight-bold list-unstyled">${data['message']}</li>
								</ul>
								`
              }
              $('#message-username').remove()
              $('#username').after($(message))
            }
          })
        };
        if (email != init_email) {
          $.ajax({
            url: '/ajax/account/change-email/',
            data: {
              'email': email
            },
            success: function (data) {
              if (data['valid']) {
                message =
                  `
								<ul class="px-2 m-0" id="message-email">
								<li class="text-warning font-weight-bold list-unstyled">${data['message']}</li>
								</ul>
								`
              } else {
                message =
                  `
								<ul class="px-2 m-0" id="message-email">
								<li class="text-danger font-weight-bold list-unstyled">${data['message']}</li>
								</ul>
								`
              }
              $('#message-email').remove()
              $('#email').after($(message))
            }
          })
        }
      })
      $('#change-password').click(function () {
        old_pass = $('#old-password').val()
        new_pass1 = $('#new-password1').val()
        new_pass2 = $('#new-password2').val()
        $('#message-password').remove()

        if (old_pass.length == 0 || new_pass1.length == 0 || new_pass2.length == 0) {
          message =
            `
					<ul class="px-2 m-0" id="message-password">
					<li class="text-danger font-weight-bold list-unstyled">Please fill up all the three fields.</li>
					</ul>
					`
          $('#new-password2').after($(message))
        } else {
          if (new_pass1 != new_pass2) {
            message =
              `
						<ul class="px-2 m-0" id="message-password">
						<li class="text-danger font-weight-bold list-unstyled">The two password fields didn’t match.</li>
						</ul>
						`
            $('#new-password2').after($(message))
          } else if (old_pass == new_pass1 || old_pass == new_pass2) {
            message =
              `
						<ul class="px-2 m-0" id="message-password">
						<li class="text-danger font-weight-bold list-unstyled">The new password doesn\'t differ from the old one.</li>
						</ul>
						`
            $('#new-password2').after($(message))
          } else {
            $.ajax({
              type: 'POST',
              url: '/ajax/account/change-password/',
              data: {
                'old_pass': old_pass,
                'new_pass1': new_pass1,
                'new_pass2': new_pass2
              },
              success: function (data) {
                if (data['valid']) {
                  message =
                    `
								<ul class="px-2 m-0" id="message-password">
								<li class="text-success font-weight-bold list-unstyled">${data['message']}</li>
								</ul>
								`
                } else {
                  if (data['iterable']) {
                    message = '<ul class="px-2 m-0" id="message-password">'
                    data['message'].forEach(msg => {
                      message += `<li class="text-danger font-weight-bold list-unstyled">${msg}</li>`
                    });
                    message += '</ul>'
                  } else {
                    message =
                      `
									<ul class="px-2 m-0" id="message-password">
									<li class="text-danger font-weight-bold list-unstyled">${data['message']}</li>
									</ul>
									`
                  }
                }
                $('#new-password2').after($(message))
              }
            })
          }
        }
      })
    } else if (dep == 'watchlists') {
      $(html_templates['watchlists']).appendTo(container)
      getData()

      // } else if (dep == 'alerts') {
      //   $(html_templates['alerts']).appendTo(container)
      // } else if (dep == 'portfolio') {
      //   $(html_templates['portfolio']).appendTo(container)
    } else {
      $('<h2 class="text-white text-center w-100">Under Construction</h2>').appendTo(container)
      container.removeClass('d-none')
    }
  }

  function getData() {
    dep = $('.tab.active').attr('id')
    $.ajax({
      url: '/ajax/account/',
      data: {
        'dep': dep
      },
      success: function (data) {
        displayData(dep, data)
        container.removeClass('d-none')
      }
    })
  }

  var init_email, init_username
  function displayData(dep, data) {
    if (dep == 'security') {
      init_email = data['email']
      init_username = data['username']
      $('input#email').val(init_email)
      $('input#username').val(init_username)
    } else if (dep == 'watchlists') {
      $('#watchlist-row').empty()
      var content = ''

      data['watchlists'].forEach(wlist => {
        content +=
          `
          <div class="col-lg-6">
          <div class="row">
          <h3 class="watch_h3 text-white text-center ml-auto">${wlist['name']}</h3>
          <i type="button" id="${wlist['name']}" class="fas fa-trash ml-auto" data-toggle="modal" data-target="#watchlist-modal"></i>
          <i type="button" id="${wlist['name']}" class="fas fa-pen" data-toggle="modal" data-target="#watchlist-edit-modal"></i>
          </div>
          <div class="account-card watchlist">
            <div class="table-wrapper">
            <table class="table table-hover">
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
        wlist['asset_links'].forEach(row => {
          var type = row['type']
          var country = row['country']
          if (type == 'crncy' || type == 'crptcrncy') {
            country = type
          }
          content +=
            `
            <tr>
              <td><img class="country-flag-md" src="/static/main_app/svg/flags/${country.toLowerCase()}.svg" alt=""></td>
              <td><a href="${row['href']}">${row['short_name']}</a></td>
              <td>${row['last']}</td>
            `

          if (row['change_perc'].includes('-')) {
            content += `<td><span class="ml-0 d-initial change down">${row['change_perc']}</span></td>`
          } else if (row['change_perc'].includes('+')) {
            content += `<td><span class="ml-0 d-initial change up">${row['change_perc']}</span></td>`
          } else {
            content += `<td><span class="ml-0 d-initial change">${row['change_perc']}</span></td>`
          }
          content +=
            `
              <td>${row['volume']}</td>
            </tr>
            `
        });
        content +=
          `
            </tbody>
          </table>
          </div>
          `
        if (wlist['asset_links'].length > 10) {
          content +=
            `
          <a id="see_all" class="btn btn-secondary w-100 mt-3 mb-2" data-toggle="modal" data-target="#watchlist-view-modal">See All</a>
          `
        }
        content +=
          `  
          </div>
        </div>
        `
      });

      content +=
        `
        <div class="col-lg-6">
          <div class="account-card watchlist empty">
            <div class="text-container">
              <h1 class="display-3"><i class="fas fa-plus"></i></h1>
              <h4>Create a Watchlist</h4>
            </div>
          </div>
        </div>
        `

      $(content).appendTo($('#watchlist-row'))
      watch_name_click()
      watch_name_edit_click()
      watch_create_click()
      watch_trash_click()
      watch_see_all_click()
      watch_pen_click()
      var empty_watch
      $('.watchlist.empty').click(function () {
        // Checking quanity of watchlists
        if ($('#watchlist-row>.col-lg-6').length < 100) {
          empty_watch = $('#watchlist-row>.col-lg-6').last()
          content =
            `
          <div class="col-lg-6">
          <div class="row">
          <div class="watch-name-input mx-auto">
            <input maxlength="255" id="new_watch_name"><i id="create-watch" class="fas fa-check"></i>
          </div>
          </div>
          <div class="account-card watchlist">
            <div class="table-wrapper">
            <table class="table table-hover">
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
                <tr>
                  
                </tr>
              </tbody>
            </table>
            </div>
          </div>
          </div>
          `
          $(content).appendTo($('#watchlist-row'))
          $(empty_watch).appendTo($('#watchlist-row'))

          watch_name_click()
          watch_name_edit_click()
          watch_create_click()
          watch_trash_click()
          watch_see_all_click()
          watch_pen_click()
        }
      })
    }
  }
  function watch_name_edit_click(init_watch_name) {
    // When clicked on a save button of a watchlist name
    $('.watch-name-input #edit-watch').click(function () {
      var valid = true
      var new_watch_name = $(this).prev().val()
      if (new_watch_name.trim().length == 0) {
        valid = false
      }
      // iterate throug watchlists and checks for duplicates and empty values
      $('#watchlist-row>.col-lg-6 h3').toArray().forEach(h => {
        if ($(h).text() == new_watch_name) {
          valid = false
        }
      });
      if (valid) {
        $('#watch_name_dup_error').remove()
        // Send name change request to server
        $.ajax({
          url: '/ajax/account/watchlist/',
          data: {
            'action': 'change_name',
            'old_name': init_watch_name,
            'new_name': new_watch_name
          },
          success: function (data) {
            if (data['error']) {
              var error_msg =
                `
                <ul class="m-0 p-0 mt-n3 mb-3" id="watch_name_dup_error">
                  <li class="text-white font-weight-bold list-unstyled">Error has been occured.</li>
                </ul>
                `
              $('#watch_name_dup_error').remove()
              $(this).parent().after($(error_msg))
              return false
            }
          },
        })
        $(this).parent().addClass('d-none')
        $(this).parent().before(`<h3 class="watch_h3 text-white text-center ml-auto">${new_watch_name}</h3><i type="button" id="${new_watch_name}" class="fas fa-trash ml-auto" data-toggle="modal" data-target="#watchlist-modal"></i><i type="button" id="${new_watch_name}" class="fas fa-pen" data-toggle="modal" data-target="#watchlist-edit-modal"></i>`)
        $(this).parent().remove()
      } else {
        $(this).parent().addClass('d-none')
        $(this).parent().before(`<h3 class="watch_h3 text-white text-center ml-auto">${init_watch_name}</h3><i type="button" id="${init_watch_name}" class="fas fa-trash ml-auto" data-toggle="modal" data-target="#watchlist-modal"></i><i type="button" id="${init_watch_name}" class="fas fa-pen" data-toggle="modal" data-target="#watchlist-edit-modal"></i>`)
        $(this).parent().remove()
      }
      watch_name_click()
      watch_name_edit_click()
      watch_create_click()
      watch_trash_click()
    })
  }
  function watch_name_click() {
    // When clicked on a watchlist header
    $('.watch_h3').click(function () {
      var init_watch_name = $(this).text()
      $(this).addClass('d-none')
      var new_watch_name_input =
        `
      <div class="watch-name-input mx-auto">
        <input maxlength="255" id="new_watch_name"><i id="edit-watch" class="fas fa-check"></i>
      </div>
      `
      $(this).before(new_watch_name_input)
      $(this).prev().children().val(init_watch_name)
      var parent = $(this).parent()
      parent.find('.fa-trash').remove()
      parent.find('.fa-pen').remove()
      $(this).remove()
      watch_name_edit_click(init_watch_name)
    })
  }
  function watch_trash_click() {
    // When clicke on a trash icon near watchlist title to delete it
    $('#watchlist-row .fa-trash').click(function () {
      var trash_el_name = $(this).attr('id')
      var col = $(this).parent().parent() // row > col-lg-6
      $('#watchlist-modal-delete').click(function () {
        $.ajax({
          url: '/ajax/account/watchlist/',
          data: {
            'action': 'delete',
            'name': trash_el_name,
          },
          success: function (data) {
            if (data['error']) {
              var error_msg =
                `
                <ul class="m-0 p-0 mt-n3 mb-3" id="watch_name_del_error">
                  <li class="text-white font-weight-bold list-unstyled">Error has been occured.</li>
                </ul>
                `
              $('#watch_name_del_error').remove()
              $(this).parent().after($(error_msg))
            } else {
              // if removed from database
              $(col).remove()
            }
          },
        })
      })
    })
  }
  function watch_create_click() {
    $('.watch-name-input #create-watch').click(function () {
      // check for duplicates, empty values
      var valid = true
      var new_watch_name = $(this).prev().val()
      // iterate throug watchlists and cheecek for valids
      $('.watch_h3').toArray().forEach(h => {
        if ($(h).text() == new_watch_name) {
          valid = false
        }
      });
      if (new_watch_name.trim().length == 0) {
        valid = false
      }
      if (valid) {
        $.ajax({
          url: '/ajax/account/watchlist/',
          data: {
            'action': 'create',
            'name': new_watch_name,
          },
          success: function (data) {
            if (data['error']) {
              var error_msg =
                `
                <ul class="m-0 p-0 mt-n3 mb-3" id="watch_name_del_error">
                  <li class="text-white font-weight-bold list-unstyled">Error has been occured.</li>
                </ul>
                `
              $('#watch_name_del_error').remove()
              $(this).parent().after($(error_msg))
              return false
            }
          },
        })
        $(this).parent().addClass('d-none')
        $(this).parent().before(`<h3 class="watch_h3 text-white text-center ml-auto">${new_watch_name}</h3><i type="button" id="${new_watch_name}" class="fas fa-trash ml-auto" data-toggle="modal" data-target="#watchlist-modal"></i><i type="button" id="${new_watch_name}" class="fas fa-pen" data-toggle="modal" data-target="#watchlist-edit-modal"></i>`)
        $(this).parent().remove()
        watch_see_all_click()
        watch_name_click()
        watch_pen_click()
        watch_trash_click()
        watch_name_edit_click()
      }
    })
  }
  function watch_see_all_click() {
    $('#see_all').click(function () {
      var table = $(this).prev().find('table')
      var table_name = $(this).parent().prev().find('h3').removeClass('text-white')
      $(this).parent().next().addClass('d-none')
      var this_ = $(this)
      $(table).appendTo($('#watchlist-view-modal .modal-body'))
      $(table_name).prependTo($('#watchlist-view-modal .modal-header'))
      $('#watchlist-view-modal .close').click(function () {
        $(table).appendTo(this_.prev())
        table_name.addClass('text-white')
        this_.parent().next().removeClass('d-none')
        $(table_name).prependTo(this_.parent().prev())
      })
    })
  }
  function watch_pen_click() {
    $('#watchlist-row .fa-pen').click(function () {
      var table = $(this).parent().next().find('table')
      if ($(table).find('tbody tr td').length > 0) {
        $(table).find('thead tr').prepend($('<th></th>'))
        $(table).find('tbody tr').each(function () {
          $(this).prepend($('<td><i class="delete_row"></i></td>'))
        });
      }
      var table_name = $(this).parent().find('.watch_h3').removeClass('text-white')
      var this_ = $(this)
      $('#watchlist-edit-modal .modal-body').empty()
      $(table).appendTo($('#watchlist-edit-modal .modal-body'))
      // Search
      $(`
        <h4 class="w-100 text-center">Add to watchlist</h4>
        <div class="search-block-watch w-100 pb-2">
        <div class="search-watch">
          <input type="text" class="searchTerm-watch" placeholder="Search">
          <div class="searchButton-watch">
            <i class="fa fa-search"></i>
          </div>
        </div>
        <div class="collapse search-results-watch" id="search-collapse-watch">
        </div>
      </div>`).appendTo($('#watchlist-edit-modal .modal-body'))
      $('.searchTerm-watch').keyup(_.debounce(searchWatch, 250));
      $('.searchButton-watch').click(function () {
        searchWatch();
        $('#search-collapse-watch').collapse('show');
        $('.searchTerm-watch').focus();
      });
      $('.searchTerm-watch').click(function () {
        $('#search-collapse-watch').collapse('toggle')
      });
      $(document).click(function () {
        $('#search-collapse-watch').collapse('hide')
      });
      // End of search
      $(table_name).prependTo($('#watchlist-edit-modal .modal-header'))
      $(this).parent().next().addClass('d-none')
      watch_name_click()

      $('.delete_row').click(function () {
        $.ajax({
          url: '/ajax/account/watchlist/',
          data: {
            'action': 'edit',
            'sub_action': 'delete',
            'name': table_name.text(),
            'href': $(this).parent().parent().find('a').attr('href')
          }
        })
        $(this).parent().parent().remove()
      })

      $('#watchlist-edit-modal .close').click(function () {
        // remove searchbar
        $(this).parent().parent().find('.search-block-watch').remove()
        if ($(table).find('tbody').find('tr').length > 0) {
          // remove trash icons column from table
          $(table).find('thead').find('tr').children().first().remove()
          $(table).find('tbody').find('tr').each(function () {
            $(this).children().first().remove()
          });
        }
        $(table).prependTo(this_.parent().next().find('.table-wrapper'))
        table_name.addClass('text-white')
        $(table_name).prependTo(this_.parent())
        this_.parent().next().removeClass('d-none')
        $('[data-target="#watchlist-view-modal"').remove()
        if ($(table).find('tbody').find('tr').length < 10) {
          $('[data-target="#watchlist-view-modal"').remove()
        } else {
          this_.parent().next().append('<a id="see_all" class="btn btn-secondary w-100 mt-3 mb-2" data-toggle="modal" data-target="#watchlist-view-modal">See All</a>')
        }
        $('#watchlist-edit-modal h4').remove()
      })
    })
    function search_item_click() {
      $('.search-results-watch a.text-inherit').click(function(){
        var href = $(this).attr('id')
        var table_name = $(this).parent().parent().parent().prev().find('.watch_h3')
        var table = $(this).parent().parent().parent().find('table')
        $.ajax({
          url: '/ajax/account/watchlist/',
          data: {
            'action': 'edit',
            'sub_action': 'add',
            'name': table_name.text(),
            'href': href
          },
          success: function(result) {
            var row = result['asset_dct']
            var type = row['type']
            var country = row['country']
            if (type == 'crncy' || type == 'crptcrncy') {
              country = type
            }
            var content =
            `
            <tr>
              <td><i class="delete_row"></i></td>
              <td><img class="country-flag-md" src="/static/main_app/svg/flags/${c}.svg" alt=""></td>
              <td><a href="${row['href']}">${row['short_name']}</a></td>
              <td>${row['last']}</td>
            `

            if (row['change_perc'].includes('-')) {
              content += `<td><span class="ml-0 d-initial change down">${row['change_perc']}</span></td>`
            } else if (row['change_perc'].includes('+')) {
              content += `<td><span class="ml-0 d-initial change up">${row['change_perc']}</span></td>`
            } else {
              content += `<td><span class="ml-0 d-initial change">${row['change_perc']}</span></td>`
            }
            content +=
            `
              <td>${row['volume']}</td>
            </tr>
            `
            if (table.find('tbody tr td').length == 0) {
              $(table).find('thead tr').prepend($('<th></th>'))
            }
            $(content).appendTo(table.find('tbody'))
          }
        })
      })
    }
    function searchWatch() {
      if ($('.searchTerm-watch').val().length != 0) {
        var container = $('.search-results-watch');
        container.empty()
        $('<div class="lds-dual-ring-sm"></div>').appendTo(container);
        $.ajax({
          url: '/ajax/search/',
          data: {
            'search': $('.searchTerm-watch').val()
          },
          success: function (data) {
            $('#search-collapse-watch').empty();
            $('#search-collapse-watch').collapse('show');
            if (_.isEmpty(data)) {
              $('<div class="text-center py-1">'
                + 'No Results' + '</div>').appendTo(container);
            } else {
              for (var i in data.results) {
                var long_name = data.results[i]['long_name'];
                if (long_name.length > 23) {
                  long_name = long_name.slice(0, 21) + '..'
                };
                var type = data.results[i]['type']
                var country = data.results[i]['country']
                if (type == 'Currency') {
                  c = 'crncy'
                } else if (type == 'Cryptocurrency') {
                  c = 'crptcrncy'
                } else {
                  c = country
                };

                $(
                  '<a class="text-inherit" id="/asset/' + country + '/' + type.toLowerCase() + '/' + data.results[i]['pk'] + '">'
                  + '<div class="search-item">'
                  + '<div class="d-flex">'
                  + data.results[i]['short_name'] + ' | '
                  + '<div class="search-long">' + long_name + '</div>'
                  + '</div>'
                  + '<div class="search-type">'
                  + '<img class="country-flag-sm" src="/static/main_app/svg/flags/' + c + '.svg">'
                  + ' ' + type + '</div>'
                  + '</div></a>'
                ).appendTo(container);
              };
            }
            search_item_click()
          },
        });
      } else {
        $('#search-collapse-watch').empty();
      };
    }

  }


});
// End of jQuery

var html_templates = {
  'security': `
    <div class="row">
    <div class="col-lg-10 mx-auto">
    <div class="account-card mb-3" id="personal-card">
    <h2 class="m-0 pl-2">Personal Info</h2>
    <div class="row">
        <div class="col-lg-6">
        <label class="account-label" for="email">E-mail</label>
        <input class="account-input" type="email" id="email">
        </div>
        <div class="col-lg-6">
        <label class="account-label" for="username">Username</label>
        <input class="account-input" type="username" id="username">
        </div>
    </div>
    <button class="btn btn-primary ml-2 mt-2" id="personal-button">Save Changes</button>
    </div>
    <div class="account-card">
    <h2 class="m-0 pl-2">Password</h2>
    <div class="col-lg-6">
        <label class="account-label" for="old-password">Current Password</label>
        <input class="account-input" type="password" id="old-password">
    </div>
    <div class="col-lg-6">
        <label class="account-label" for="new-password1">New Password</label>
        <input class="account-input" type="password" id="new-password1">
    </div>
    <div class="col-lg-6">
        <label class="account-label" for="new-password2">Confirm Password</label>
        <input class="account-input" type="password" id="new-password2">
    </div>
    <button class="btn btn-primary ml-2 mt-2" id="change-password">Save Changes</button>
    <hr>
    <a href="password-reset/" class="btn btn-secondary ml-2">Reset via E-mail</a>
    </div>
    </div>`,

  'watchlists':
    `
    <div class="row">
      <div class="mx-auto w-100">
        <div class="row" id="watchlist-row">
        </div>
      </div>
    </div>
    
    <!-- Modal -->
    <div class="modal fade" id="watchlist-modal" tabindex="-1" role="dialog" aria-labelledby="watchlist-modal-title" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p class="mb-0">Are you sure you want to delete the Watchlist?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" data-dismiss="modal" id="watchlist-modal-delete">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <div data-keyboard="false" data-backdrop="static" class="modal fade" id="watchlist-view-modal" tabindex="-1" role="dialog" aria-labelledby="watchlist-view-modal-title" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body overflow-auto">
            
          </div>
        </div>
      </div>
    </div>

    <div data-keyboard="false" data-backdrop="static" class="modal fade" id="watchlist-edit-modal" tabindex="-1" role="dialog" aria-labelledby="watchlist-edit-modal-title" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <i class="fas fa-check text-success font-size-2"></i>
            </button>
          </div>
          <div class="modal-body">
            
          </div>
        </div>
      </div>
    </div>
    `
}
