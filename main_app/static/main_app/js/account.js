$(function () {
// 1. Load HTML
// 2. Get Data
// ........

var container = $('#main-container')
loadHTML()
getData()

$('.tab').click(_.debounce(function () {
    container.empty()
    $('<div class="h-100 lds-dual-ring-md"></div>').appendTo(container)
    loadHTML()
    getData()
}, 250));


function loadHTML() {
    container.empty()
    container.addClass('d-none')
    dep = $('.tab.active').attr('id')
    if (dep == 'account-info') {
        $(html_templates['account-info']).appendTo(container)
    } else if (dep == 'watchlists') {
        $(html_templates['watchlists']).appendTo(container)
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
            if (dep == 'account-info') {
                displayAccountInfo(data)
            }
            container.removeClass('d-none')
        }
    })
}

function displayAccountInfo(data) {
    $('input#email').val(data['email'])
    $('input#username').val(data['username'])
}


});

var html_templates = {
    'account-info': `
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
                <tbody>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="account-card watchlist">
              <h3>Watchlist Name</h3>
              <table class="table table-hover">
                <tbody>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
    
        <div class="row" id="watchlist-row">
          <div class="col-lg-6">
            <div class="account-card watchlist">
              <h3>Watchlist Name</h3>
              <table class="table table-hover">
                <tbody>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
                  </tr>
                  <tr>
                    <td><img class="country-flag-md" src="/static/main_app/svg/flags/us.svg"></td>
                    <td>AAPL</td>
                    <td>Apple Computers Inc.</td>
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
    `
}