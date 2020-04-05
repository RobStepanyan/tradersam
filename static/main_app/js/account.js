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
    `
}