(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 72)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 72
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 60) {
      $("#mainNav").addClass("navbar-scrolled");
    } else {
      $("#mainNav").removeClass("navbar-scrolled");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);
})(jQuery); // End of use strict

// home.html carousel in market overview section
$(document).ready(function(){
  $('#market-carousel').slick({
    slidesToShow: 5,
    variableWidth: true,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2000,
  });
});

// Nav bar search
function search() {
  if ($('.searchTerm').val().length != 0) {
    var container = $('.search-results');
    container.empty()
    $('<div class="lds-dual-ring-sm"></div>').appendTo(container);
    $.ajax({
      url: '/dev/ajax/search/',
      data: {
        'search': $('.searchTerm').val()
      },
      success: function(data) {
        $('#search-collapse').empty();
        $('#search-collapse').collapse('show');
        if (_.isEmpty(data)){
          $('<div class="text-center py-1">' 
             + 'No Results' + '</div>').appendTo(container);
        }else{
          for (var i in data.results) {
            var long_name = data.results[i]['long_name'];
            if (long_name.length > 23) {
              long_name = long_name.slice(0, 21) + '..'
            };
            var type = data.results[i]['type']
            var country = data.results[i]['country']
            if (type == 'Currency') {
              country = 'crncy'
            }else if (type == 'Cryptocurrency') {
              country = 'crptcrncy'
            };
            
            $(
              '<a class="text-inherit" href="/dev/asset/' + type.toLowerCase() + '/' + data.results[i]['pk'] +'">'
            + '<div class="search-item">' 
            + '<div class="d-flex">'
            + data.results[i]['short_name'] + ' | '
            + '<div class="search-long">' + long_name + '</div>'
            + '</div>'
            + '<div class="search-type">'
            + '<img class="country-flag-sm" src="/static/main_app/svg/flags/' + country + '.svg">'
            + ' ' + type + '</div>'
            + '</div></a>'
            ).appendTo(container);
          };
        }
      },
    });
  }else{
    $('#search-collapse').empty();
  };
}

$('.searchTerm').keyup(_.debounce(search,250));
$('.searchButton').click(function(){
  search();
  $('#search-collapse').collapse('show');
  $('.searchTerm').focus();
});
$('.searchTerm').click(function(){
  $('#search-collapse').collapse('toggle')
});
$(document).click(function(){
  $('#search-collapse').collapse('hide')
});