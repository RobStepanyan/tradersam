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
    container.empty()
    container.removeClass('d-flex')
    container.addClass('d-none')
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
      

    } else if (dep == 'alerts') {
      $(html_templates['alerts']).appendTo(container)
    } else if (dep == 'portfolio') {
      $(html_templates['portfolio']).appendTo(container)
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
          <div class="row justify-content-center">
          <h3 class="text-white text-center">${wlist['name']}</h3>
          </div>
          <div class="account-card watchlist">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th></th>
                  <th>Symbol</th>
                  <th>Change %</th>
                  <th>Volume</th>
                </tr>
              </thead>
              <tbody>
          `
        wlist['asset_links'].forEach(row => {
          content +=
          `
          <tr>
            <td>f</td>
            <td>f</td>
            <td>f</td>
            <td>f</td>
          </tr>
          `
          //   `
          // <tr>
          //   <td><img class="country-flag-md" src="/static/main_app/svg/flags/${row[0]['country']}.svg" alt=""></td>
          //   <td><a href="${row[1]['href']}">${row[1]['short_name']}</a></td>
          //   <td><span class="ml-0 d-initial change down">${row[2]['change_perc']}</span></td>
          //   <td>${row[3]['volume']}</td>
          // </tr>
          // `
        });
        content +=
          `
            </tbody>
          </table>
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
      new_watch_name_click()
      var empty_watch
      $('.watchlist.empty').click(function(){
        if ($('#watchlist-row>.col-lg-6').length < 100) {
          empty_watch = $('#watchlist-row>.col-lg-6').last()
          content =
          `
          <div class="col-lg-6">
          <div class="row justify-content-center">
          <h3 class="text-white text-center">Watchlist Name</h3>
          </div>
          <div class="account-card watchlist">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th></th>
                  <th>Symbol</th>
                  <th>Change %</th>
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
          `
          $(content).appendTo($('#watchlist-row'))
          $(empty_watch).appendTo($('#watchlist-row'))
          
          new_watch_name_click()
        }
      })
    }
  }
  function new_watch_check_click(init_watch_name){
    // Check mark
    // Click event for newly appeared button
    $('.watch-name-input i').click(function(){
      var duplicate = false
      var new_watch_name = $(this).prev().val()
      $('#watchlist-row>.col-lg-6 h3').toArray().forEach(h => {
        if ($(h).text() == new_watch_name) {
          duplicate = true
        }
      });
      if (!duplicate) {
        // replace check mark icon with loading icon
        $('#watch_name_dup_error').remove()
        // Send name change request to server
        $.ajax({
          url: '/ajax/account/change-watch-name/',
          data: {
            'old_name': init_watch_name,
            'new_name': new_watch_name
          },
          success: function(){
            
          },
          error: function(){
            var error_msg = 
            `
            <ul class="m-0 p-0 mt-n3 mb-3" id="watch_name_dup_error">
              <li class="text-white font-weight-bold list-unstyled">Error has been occured.</li>
            </ul>
            `
            $('#watch_name_dup_error').remove()
            $(this).parent().after($(error_msg))
          }
        })
        $(this).parent().addClass('d-none')
        $(this).parent().before(`<h3 class="text-white text-center">${new_watch_name}</h3>`)
        $(this).parent().remove()
        new_watch_name_click()
      } else {
        var error_msg = 
        `
        <ul class="m-0 p-0 mt-n3 mb-3" id="watch_name_dup_error">
          <li class="text-white font-weight-bold list-unstyled">Watchlist with a same name already exists.</li>
        </ul>
        `
        $('#watch_name_dup_error').remove()
        $(this).parent().after($(error_msg))
      }
    })
  }
  function new_watch_name_click(){
    $('#watchlist-row>.col-lg-6 h3').click(function(){
      var init_watch_name = $(this).text()
      $(this).addClass('d-none')
      var new_watch_name_input = 
      `
      <div class="watch-name-input">
        <input maxlength="255" id="new_watch_name"><i class="fas fa-check"></i>
      <div>
      `
      $(this).before(new_watch_name_input)
      $('#new_watch_name').val(init_watch_name)
      $(this).remove()
      new_watch_check_click(init_watch_name)
    })
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
      <div class="col-lg-12 mx-auto">
        <div class="row" id="watchlist-row">
        </div>
      </div>
    </div>
    `,

  'alerts':
    `
    <div class="row">
      <div class="m-auto w-100">
        <div class="account-card p-1 overflow-auto">  
          <table class="table table-nowrap">
            <thead>
              <tr>
                <th></th>
                <th>Name</th>
                <th>Alert Type</th>
                <th>Condition</th>
                <th>Frequency</th>
                <th>Delivery Method</th>
                <th>On/Off</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><img src="/static/main_app/svg/flags/au.svg" class="country-flag-md"></td>
                <td>SPDR S&P 500 ETF Trust</td>
                <td>Price</td>
                <td>Moves Above 500.00</td>
                <td>Once</td>
                <td><h5><i class="fas fa-envelope hover" data-toggle="tooltip" title="E-mail message"></i> 
                  <i class="fas fa-laptop hover" data-toggle="tooltip"title="Notification"></i></h5></td>
                <td>
                  <div class="switch switch-xs switch-label-onoff pl-0 mr-2 d-flex fl justify-content-center">
                    <input class="switch-input" id="switch1" type="checkbox" :checked>
                    <label class="switch-btn" for="switch1"></label>
                  </div>
                </td>
                <td><h5><i class="fas fa-pen hover" data-toggle="tooltip" title="Edit"></i> 
                  <i class="fas fa-trash hover" data-toggle="tooltip" title="Remove"></i></h5></td>
              </tr>
              <tr>
                <td><img src="/static/main_app/svg/flags/au.svg" class="country-flag-md"></td>
                <td>SPDR S&P 500 ETF Trust</td>
                <td>Price</td>
                <td>Moves Above 500.00</td>
                <td>Once</td>
                <td><h5><i class="fas fa-envelope hover" data-toggle="tooltip" title="E-mail message"></i> 
                  <i class="fas fa-laptop hover" data-toggle="tooltip"title="Notification"></i></h5></td>
                <td>
                  <div class="switch switch-xs switch-label-onoff pl-0 mr-2 d-flex fl justify-content-center">
                    <input class="switch-input" id="switch2" type="checkbox" :checked>
                    <label class="switch-btn" for="switch2"></label>
                  </div>
                </td>
                <td><h5><i class="fas fa-pen hover" data-toggle="tooltip" title="Edit"></i> 
                  <i class="fas fa-trash hover" data-toggle="tooltip" title="Remove"></i></h5></td>
              </tr>
              <tr>
                <td><img src="/static/main_app/svg/flags/au.svg" class="country-flag-md"></td>
                <td>SPDR S&P 500 ETF Trust</td>
                <td>Price</td>
                <td>Moves Above 500.00</td>
                <td>Once</td>
                <td><h5><i class="fas fa-envelope hover" data-toggle="tooltip" title="E-mail message"></i> 
                  <i class="fas fa-laptop hover" data-toggle="tooltip"title="Notification"></i></h5></td>
                <td>
                  <div class="switch switch-xs switch-label-onoff pl-0 mr-2 d-flex fl justify-content-center">
                    <input class="switch-input" id="switch3" type="checkbox" :checked>
                    <label class="switch-btn" for="switch3"></label>
                  </div>
                </td>
                <td><h5><i class="fas fa-pen hover" data-toggle="tooltip" title="Edit"></i> 
                  <i class="fas fa-trash hover" data-toggle="tooltip" title="Remove"></i></h5></td>
              </tr>
              <tr>
                <td><img src="/static/main_app/svg/flags/au.svg" class="country-flag-md"></td>
                <td>SPDR S&P 500 ETF Trust</td>
                <td>Price</td>
                <td>Moves Above 500.00</td>
                <td>Once</td>
                <td><h5><i class="fas fa-envelope hover" data-toggle="tooltip" title="E-mail message"></i> 
                  <i class="fas fa-laptop hover" data-toggle="tooltip"title="Notification"></i></h5></td>
                <td>
                  <div class="switch switch-xs switch-label-onoff pl-0 mr-2 d-flex fl justify-content-center">
                    <input class="switch-input" id="switch4" type="checkbox" :checked>
                    <label class="switch-btn" for="switch4"></label>
                  </div>
                </td>
                <td><h5><i class="fas fa-pen hover" data-toggle="tooltip" title="Edit"></i> 
                  <i class="fas fa-trash hover" data-toggle="tooltip" title="Remove"></i></h5></td>
              </tr>
              <tr>
                <td><img src="/static/main_app/svg/flags/au.svg" class="country-flag-md"></td>
                <td>SPDR S&P 500 ETF Trust</td>
                <td>Price</td>
                <td>Moves Above 500.00</td>
                <td>Once</td>
                <td><h5><i class="fas fa-envelope hover" data-toggle="tooltip" title="E-mail message"></i> 
                  <i class="fas fa-laptop hover" data-toggle="tooltip"title="Notification"></i></h5></td>
                <td>
                  <div class="switch switch-xs switch-label-onoff pl-0 mr-2 d-flex fl justify-content-center">
                    <input class="switch-input" id="switch5" type="checkbox" :checked>
                    <label class="switch-btn" for="switch5"></label>
                  </div>
                </td>
                <td><h5><i class="fas fa-pen hover" data-toggle="tooltip" title="Edit"></i> 
                  <i class="fas fa-trash hover" data-toggle="tooltip" title="Remove"></i></h5></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    `,

  'portfolio':
    `
    <div class="account-card p-3">
      <div class="row align-items-center justify-content-between">
        <div class="dropdown show mr-3 my-2">
          <a class="btn btn-primary dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Medium Risk
          </a>
        
          <div class="dropdown-menu" data-toggle="buttons">
            <h6 class="dropdown-header">Your Portfolios</h6>
            <label class="btn dropdown-item active">
              <input type="radio" id="low-risk" autocomplete="off" checked>  
              Low Risk
            </label>
            <label class="btn dropdown-item">
              <input type="radio" id="medium-risk" autocomplete="off">  
              Medium Risk
            </label>
            <label class="btn dropdown-item">
              <input type="radio" id="trading" autocomplete="off">  
              Trading
            </label>
            <div class="dropdown-divider"></div>
            <label class="btn dropdown-item">
              <input type="radio" id="create_" autocomplete="off">  
              <i class="fas fa-plus"></i> Create
            </label>
          </div>
        
        </div>
        <div class="row my-2">
          <div class="px-2 border-right-bold">
            Holdings:
            <h4 class="text-success">$1K / 3456.45%</h4>
          </div>
          <div class="px-2 border-right-bold">
            Open P/L:
            <h4 class="text-success">$1K / 3456.45%</h4>
          </div>
          <div class="px-2">
            Daily P/L:
            <h4 class="text-success">$1K / 3456.45%</h4>
          </div>  
        </div>
      </div>
      <div class="w-100 overflow-auto">
        <table class="table table-nowrap">
        <thead>
          <tr>
            <th></th>
            <th>Name</th>
            <th>Symbol</th>
            <th>Open Date</th>
            <th>Type</th>
            <th>Amount</th>
            <th>Avg Price</th>
            <th>Current Price</th>
            <th>Daily P/L</th>
            <th>Open P/L</th>
            <th>Open P/L (%)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
            <td>SPDR S&P 500 ETF Trust</td>
            <td>SPY</td>
            <td>08/07/1998</td>
            <td>BUY</td>
            <td>12</td>
            <td>245.36</td>
            <td>2437.21</td>
            <td><span class="text-success">+2341.21</span></td>
            <td><span class="text-success">+6534.24</span></td>
            <td><span class="text-success">+2021.32%</span></td>
          </tr>
          <tr>
            <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
            <td>SPDR S&P 500 ETF Trust</td>
            <td>SPY</td>
            <td>08/07/1998</td>
            <td>BUY</td>
            <td>12</td>
            <td>245.36</td>
            <td>2437.21</td>
            <td><span class="text-success">+2341.21</span></td>
            <td><span class="text-success">+6534.24</span></td>
            <td><span class="text-success">+2021.32%</span></td>
          </tr>
          <tr>
            <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
            <td>SPDR S&P 500 ETF Trust</td>
            <td>SPY</td>
            <td>08/07/1998</td>
            <td>BUY</td>
            <td>12</td>
            <td>245.36</td>
            <td>2437.21</td>
            <td><span class="text-success">+2341.21</span></td>
            <td><span class="text-success">+6534.24</span></td>
            <td><span class="text-success">+2021.32%</span></td>
          </tr>
          <tr>
            <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
            <td>SPDR S&P 500 ETF Trust</td>
            <td>SPY</td>
            <td>08/07/1998</td>
            <td>BUY</td>
            <td>12</td>
            <td>245.36</td>
            <td>2437.21</td>
            <td><span class="text-success">+2341.21</span></td>
            <td><span class="text-success">+6534.24</span></td>
            <td><span class="text-success">+2021.32%</span></td>
          </tr>
        </tbody>
      </table>
      </div>
      
    </div>
    `
}