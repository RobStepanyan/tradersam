$(function () {
// 1. Load HTML
// 2. Get Data
// ........

var container = $('#main-container')
var getLoadDebounce = _.debounce(function(){loadHTML();getData();}, 250);
loadHTML()
getData()

$('.tab').click(function(){
  container.empty()
  container.addClass('d-flex')
  $('<div class="h-100 lds-dual-ring-md m-auto"></div>').appendTo(container)
  getLoadDebounce()
})


function loadHTML() {
    container.empty()
    container.removeClass('d-flex')
    container.addClass('d-none')
    dep = $('.tab.active').attr('id')
    if (dep == 'security') {
        $(html_templates['security']).appendTo(container)
        $('#personal-button').click(function(){
          email = $('input#email').val()
          username = $('input#username').val()

          if (username != init_username) {
            $.ajax({
              url: '/ajax/account/change-username/',
              data: {
                'username': username
              },
              success: function(data){
                if (data['valid']){
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
              success: function(data){
                if (data['valid']){
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
    } else if (dep == 'watchlists') {
        $(html_templates['watchlists']).appendTo(container)
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
    sendAjax(dep)
}

function sendAjax(dep) {
    $.ajax({
        url: '/ajax/account/',
        data: {
            'dep': dep
        },
        success: function (data) {
            if (dep == 'security') {
                displaySecurity(data)
            }
            container.removeClass('d-none')
        }
    })
}

var init_email, init_username
function displaySecurity(data) {
    init_email = data['email']
    init_username = data['username']
    $('input#email').val(init_email)
    $('input#username').val(init_username)
}



});

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
        <label class="account-label" for="current-password">Current Password</label>
        <input class="account-input" type="password" id="current-password">
    </div>
    <div class="col-lg-6">
        <label class="account-label" for="new-password">New Password</label>
        <input class="account-input" type="password" id="new-password">
    </div>
    <div class="col-lg-6">
        <label class="account-label" for="confirm-password">Confirm Password</label>
        <input class="account-input" type="password" id="confirm-password">
    </div>
    <button class="btn btn-primary ml-2 mt-2">Save Changes</button>
    </div>
    </div>`,

    'watchlists': 
    `
    <div class="row">
      <div class="col-lg-10 mx-auto">
        <div class="row" id="watchlist-row">
          <div class="col-lg-6">
            <div class="account-card watchlist">
              <h3>Watchlist Name</h3>
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
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">AKS</a></td>
                    <td><span class="ml-0 d-initial change up">+1.76%</span></td>
                    <td>12.79M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">CIEN</a></td>
                    <td><span class="ml-0 d-initial change down">-1.33%</span></td>
                    <td>2.63M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">CLF</a></td>
                    <td><span class="ml-0 d-initial change up">+1.40%</span></td>
                    <td>17.39M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">FCX</a></td>
                    <td><span class="ml-0 d-initial change up">+1.63%</span></td>
                    <td>68.00M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">INTC</a></td>
                    <td><span class="ml-0 d-initial change down">-0.56%</span></td>
                    <td>60.73M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">RIG</a></td>
                    <td><span class="ml-0 d-initial change up">+11.30%</span></td>
                    <td>38.90M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">S</a></td>
                    <td><span class="ml-0 d-initial change down">-1.18%</span></td>
                    <td>43.60M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">T</a></td>
                    <td><span class="ml-0 d-initial change down">-1.43%</span></td>
                    <td>121.10M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">TEVA</a></td>
                    <td><span class="ml-0 d-initial change down">-5.57%</span></td>
                    <td>30.15M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">X</a></td>
                    <td><span class="ml-0 d-initial change up">+3.22%</span></td>
                    <td>21.49M</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="account-card watchlist">
              <h3>Watchlist Name</h3>
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
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">AKS</a></td>
                    <td><span class="ml-0 d-initial change up">+1.76%</span></td>
                    <td>12.79M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">CIEN</a></td>
                    <td><span class="ml-0 d-initial change down">-1.33%</span></td>
                    <td>2.63M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">CLF</a></td>
                    <td><span class="ml-0 d-initial change up">+1.40%</span></td>
                    <td>17.39M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">FCX</a></td>
                    <td><span class="ml-0 d-initial change up">+1.63%</span></td>
                    <td>68.00M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">INTC</a></td>
                    <td><span class="ml-0 d-initial change down">-0.56%</span></td>
                    <td>60.73M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">RIG</a></td>
                    <td><span class="ml-0 d-initial change up">+11.30%</span></td>
                    <td>38.90M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">S</a></td>
                    <td><span class="ml-0 d-initial change down">-1.18%</span></td>
                    <td>43.60M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">T</a></td>
                    <td><span class="ml-0 d-initial change down">-1.43%</span></td>
                    <td>121.10M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">TEVA</a></td>
                    <td><span class="ml-0 d-initial change down">-5.57%</span></td>
                    <td>30.15M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">X</a></td>
                    <td><span class="ml-0 d-initial change up">+3.22%</span></td>
                    <td>21.49M</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="account-card watchlist">
              <h3>Watchlist Name</h3>
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
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">AKS</a></td>
                    <td><span class="ml-0 d-initial change up">+1.76%</span></td>
                    <td>12.79M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">CIEN</a></td>
                    <td><span class="ml-0 d-initial change down">-1.33%</span></td>
                    <td>2.63M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">CLF</a></td>
                    <td><span class="ml-0 d-initial change up">+1.40%</span></td>
                    <td>17.39M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">FCX</a></td>
                    <td><span class="ml-0 d-initial change up">+1.63%</span></td>
                    <td>68.00M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">INTC</a></td>
                    <td><span class="ml-0 d-initial change down">-0.56%</span></td>
                    <td>60.73M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">RIG</a></td>
                    <td><span class="ml-0 d-initial change up">+11.30%</span></td>
                    <td>38.90M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">S</a></td>
                    <td><span class="ml-0 d-initial change down">-1.18%</span></td>
                    <td>43.60M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">T</a></td>
                    <td><span class="ml-0 d-initial change down">-1.43%</span></td>
                    <td>121.10M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">TEVA</a></td>
                    <td><span class="ml-0 d-initial change down">-5.57%</span></td>
                    <td>30.15M</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/ch.svg" alt=""></td>
                    <td><a href="">X</a></td>
                    <td><span class="ml-0 d-initial change up">+3.22%</span></td>
                    <td>21.49M</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="col-lg-6">
            <a href="">
              <div class="account-card watchlist empty">
                <div class="text-container">
                  <h1 class="display-3"><i class="fas fa-plus"></i></h1>
                  <h4>Create a Watchlist</h4>
                </div>
              </div>
            </a>
          </div>
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