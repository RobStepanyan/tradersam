import * as LightweightCharts from '/static/main_app/js/lightweight-charts.esm.development.js';

$(function(){
var container = $('#chart');
container.css('position','relative');

var width = $('#chart').width();
if (width < 576) {
	var height = width * 1.2
} else {
	var height = $(window).height() - $('#asset-header').height() - 48
};

$('<div class="h-100 lds-dual-ring-md"></div>').appendTo(container);
var link = window.location.href
var timeFrame = '1M'
var chartType = 'line'
var priceData, volumeData

function dataAjax(timeFrame, chartType) {
	$.ajax({
		url: '/dev/ajax/hist/',
		data: {
		'link': link,
		'time_frame': timeFrame,
		'chart_type': chartType
		},
		success: function(data){
			var currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;
			container.empty()
			if (currentTheme) {
				createChart(currentTheme, data['hist_data'], data['vol_data'], chartType);
			} else {
				createChart('light', data['hist_data'], data['vol_data'], chartType);
			};
			if (currentTheme == 'dark') {
				$('#switch').prop("checked", true);
			};
		}
	});
};
dataAjax(timeFrame, chartType);
$(window).on('resize', function() {
	width = $('#chart').width();
	if (width < 576) {
		height = width * 1.2
	} else {
		height = $(window).height() - $('#asset-header').height() - 48
	};

	$('#chart').empty(); // remove old chart
	if ($('#switch').is(':checked')) {
		createChart();
	} else {
		createChart('light');
	};
});
$('.switcher-item').click(_.debounce(function(){
	timeFrame = $('.switcher-active-item').val();
	chartType = $('.btn.dropdown-item.active').attr('id');
	dataAjax(timeFrame, chartType);
},250));
$('.btn.dropdown-item').click(_.debounce(function(){
	timeFrame = $('.switcher-active-item').val();
	chartType = $('.btn.dropdown-item.active').attr('id');
	dataAjax(timeFrame, chartType);
},250));


function createChart(color='dark', priceData, volumeData, chartType) {
	// chart - line chart, volume bars, go to live btn, time frames switcher
	var lineWidth = 2
	if (color == 'dark') {
		var backgroundColor = '#131722';
		var textColor = '#d1d4dc';
		var vertColor = 'rgba(42, 46, 57, 0.2)';
		var horzColor = 'rgba(42, 46, 57, 0.6)';
		var topColor = 'rgba(38,198,218, 0.56)';
		var bottomColor = 'rgba(38,198,218, 0.04)';
		var lineColor = 'rgba(38,198,218, 1)';
	} else {
		var vertColor = 'rgba(255, 255, 255, 0.2)';
		var horzColor = 'rgba(215, 215, 215, 0.6)';
		var topColor ='rgba(33, 150, 243, 0.56)';
		var bottomColor ='rgba(33, 150, 243, 0.04)';
		var lineColor ='rgba(33, 150, 243, 1)';
	};
		
	
	// time frames switcher
	function createSimpleSwitcher(items, activeItem, activeItemChangedCallback) {
		var switcherElement = document.createElement('div');
		switcherElement.classList.add('switcher');

		var intervalElements = items.map(function(item) {
			var itemEl = document.createElement('button');
			itemEl.innerText = item;
			itemEl.classList.add('switcher-item');
			itemEl.classList.toggle('switcher-active-item', item === activeItem);
			itemEl.addEventListener('click', function() {
				onItemClicked(item);
			});
			switcherElement.appendChild(itemEl);
			return itemEl;
		});

		function onItemClicked(item) {
			if (item === activeItem) {
				return;
			}

			intervalElements.forEach(function(element, index) {
				element.classList.toggle('switcher-active-item', items[index] === item);
			});

			activeItem = item;

			activeItemChangedCallback(item);
		}

		return switcherElement;
	}

	var intervals = ['1D', '5D', '1M', '3M', '6M', '1Y', '5Y', 'Max'];
	var dayData = priceData;
	var weekData = priceData;
	var monthData = priceData;
	var months3Data = priceData;
	var months6Data = priceData;
	var yearData = priceData;
	var years5Data = priceData;
	var maxData = priceData;
	var seriesesData = new Map([
		['1D', dayData ],
		['5D', weekData ],
		['1M', monthData ],
		['3M', months3Data ],
		['6M', months6Data ],
		['1Y', yearData ],
		['5Y', years5Data ],
		['Max', maxData ],
	]);

	var switcherElement = createSimpleSwitcher(intervals, intervals[0], syncToInterval);
	// end of time frame switcher
	
	var chartElement = document.createElement('div');
	if (color == 'dark') {
		var chart = LightweightCharts.createChart(chartElement, {
			width: width,
			height:  height,
			priceScale: {
				scaleMargins: {
					top: 0.3,
					bottom: 0.25,
				},
				borderVisible: false,
			},
			layout: {
				backgroundColor: backgroundColor,
				textColor: textColor,
			},
			grid: {
				vertLines: {
					color: vertColor,
				},
				horzLines: {
					color: horzColor,
				},
			},
		});
	} else {
		var chart = LightweightCharts.createChart(chartElement, {
			width: width,
			height: height,
			priceScale: {
				scaleMargins: {
					top: 0.3,
					bottom: 0.25,
				},
				borderVisible: false,
			},
			layout: {
				backgroundColor: backgroundColor,
				textColor: textColor,
			},
			grid: {
				vertLines: {
					color: vertColor,
				},
				horzLines: {
					color: horzColor,
				},
			},
		});	
	};
	container.append(chartElement);

	if (chartType=='line') { 
		// chart - line
		var areaSeries = chart.addAreaSeries({
			topColor: topColor,
			bottomColor: bottomColor,
			lineColor: lineColor,
			lineWidth: lineWidth,
		});
		areaSeries.setData(priceData);
		// end of chart - line
	} else if (chartType='ohlc') {
		// chart ohlc (bar chart)
		var barSeries = chart.addBarSeries({
			thinBars: false,
			downColor: 'rgba(255,82,82, 0.8)',
			upColor: 'rgba(0, 150, 136, 0.8)',
		});
		barSeries.setData(priceData);
		// end of ohlc (bar chart)
	} else if (chartType='candle') {
		// chart candlesticks
		var candleSeries = chart.addCandlestickSeries({
		  });
		candleSeries.setData(priceData);
		// end of candlesticks
	};
	// chart volume
	var volumeSeries = chart.addHistogramSeries({
		color: '#26a69a',
		lineWidth: 2,
		priceFormat: {
			type: 'volume',
		},
		overlay: true,
		scaleMargins: {
			top: 0.8,
			bottom: 0,
		},
	});
	volumeSeries.setData(volumeData);
	// end of chart - volume
	// end of chart

	// time frames switcher
	container.append(switcherElement)

	function syncToInterval(interval) {
		if (areaSeries) {
			chart.removeSeries(areaSeries);
			areaSeries = null;
		}
		areaSeries = chart.addAreaSeries({
		topColor: topColor,
		bottomColor: bottomColor,
		lineColor: lineColor,
		lineWidth: lineWidth,
		});
		areaSeries.setData(seriesesData.get(interval));
	}

	syncToInterval(intervals[0]);
	// end of time frames switcher

	// Go to real-time button
	var btn_width = 27;
	var btn_height = 27;

	var button = document.createElement('div');
	button.className = 'go-to-realtime-button';
	button.style.left = (width - btn_width - 60) + 'px';
	button.style.top = (height - btn_height - 30) + 'px';
	button.style.color = '#4c525e';
	button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 14 14" width="14" height="14"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="2" d="M6.5 1.5l5 5.5-5 5.5M3 4l2.5 3L3 10"></path></svg>';
	chartElement.append(button);

	var timeScale = chart.timeScale();
	chart.subscribeVisibleTimeRangeChange(function() {
		var buttonVisible = timeScale.scrollPosition() < 0;
		button.style.display = buttonVisible ? 'block' : 'none';
	});

	button.addEventListener('click', function() {
		timeScale.scrollToRealTime();
	});

	button.addEventListener('mouseover', function() {
		button.style.background = 'rgba(250, 250, 250, 1)';
		button.style.color = '#000';
	});

	button.addEventListener('mouseout', function() {
		button.style.background = 'rgba(250, 250, 250, 0.6)';
		button.style.color = '#4c525e';
	});
	// End of go to real time button
}; // End of create chart

function switchTheme() {
	if ($('#switch').is(':checked')) {
		$('#chart').empty();
		createChart();
		localStorage.setItem('theme', 'dark');
	}
    else {
		$('#chart').empty();
		createChart('light');
		localStorage.setItem('theme', 'light');
    }    
}
$('#switch').on('click', switchTheme);
}); // jQuery

