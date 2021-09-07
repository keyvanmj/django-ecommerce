function myFunction() {
    var x = document.getElementById('myInput');
    if (x.type === 'password') {
        x.type = 'text';
    } else {
        x.type = 'password';
    }
}

var on_count = '{% autoescape off %} {{on_count}} {% endautoescape %}';
var product_count = '{% autoescape off %} {{ product_count }} {% endautoescape %}';
(function ($) {
    $.fn.countTo = function (options) {
        options = options || {};

        return $(this).each(function () {
            // set options for current element
            var settings = $.extend({}, $.fn.countTo.defaults, {
                from: $(this).data('from'),
                to: $(this).data('to'),
                speed: $(this).data('speed'),
                refreshInterval: $(this).data('refresh-interval'),
                decimals: $(this).data('decimals')
            }, options);

            // how many times to update the value, and how much to increment the value on each update
            var loops = Math.ceil(settings.speed / settings.refreshInterval),
                increment = (settings.to - settings.from) / loops;

            // references & variables that will change with each update
            var self = this,
                $self = $(this),
                loopCount = 0,
                value = settings.from,
                data = $self.data('countTo') || {};

            $self.data('countTo', data);

            // if an existing interval can be found, clear it first
            if (data.interval) {
                clearInterval(data.interval);
            }
            data.interval = setInterval(updateTimer, settings.refreshInterval);

            // initialize the element with the starting value
            render(value);

            function updateTimer() {
                value += increment;
                loopCount++;

                render(value);

                if (typeof (settings.onUpdate) == 'function') {
                    settings.onUpdate.call(self, value);
                }

                if (loopCount >= loops) {
                    // remove the interval
                    $self.removeData('countTo');
                    clearInterval(data.interval);
                    value = settings.to;

                    if (typeof (settings.onComplete) == 'function') {
                        settings.onComplete.call(self, value);
                    }
                }
            }

            function render(value) {
                var formattedValue = settings.formatter.call(self, value, settings);
                $self.html(formattedValue);
            }
        });
    };

    $.fn.countTo.defaults = {
        from: 0,               // the number the element should start at
        to: 0,                 // the number the element should end at
        speed: 1000,           // how long it should take to count between the target numbers
        refreshInterval: 100,  // how often the element should be updated
        decimals: 0,           // the number of decimal places to show
        formatter: formatter,  // handler for formatting the value before rendering
        onUpdate: null,        // callback method for every time the element is updated
        onComplete: null       // callback method for when the element finishes updating
    };

    function formatter(value, settings) {
        return value.toFixed(settings.decimals);
    }
}(jQuery));

jQuery(function ($) {
    // custom formatting example
    $('.count-number').data('countToOptions', {
        formatter: function (value, options) {
            return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
        }
    });
    // start all the timers
    $('.timer').each(count);

    function count(options) {
        var $this = $(this);
        options = $.extend({}, options || {}, $this.data('countToOptions') || {});
        $this.countTo(options);
    }
});

// checkebox filter
$(document).ready(function () {
    if (sessionStorage.getItem('checked-checkboxes') && $.parseJSON(sessionStorage.getItem('checked-checkboxes')).length !== 0) {
        var arrCheckedCheckboxes = $.parseJSON(sessionStorage.getItem('checked-checkboxes'));
        //Convert checked checkboxes array to comma seprated id
        $(arrCheckedCheckboxes.toString()).prop('checked', true);
    }
    $("input:checkbox").change(function () {
        var arrCheckedCheckboxes = [];
        // Get all checked checkboxes
        $.each($("input:checkbox:checked"), function () {
            arrCheckedCheckboxes.push("#" + $(this).attr('id'));
        });
        // Convert checked checkboxes array to JSON ans store it in session storage
        sessionStorage.setItem('checked-checkboxes', JSON.stringify(arrCheckedCheckboxes));
    });
});
var urlParams = new URLSearchParams(window.location.search);
const params = Object.fromEntries(urlParams.entries())
para = Object.keys(params)
var arrCheckbox = $.parseJSON((sessionStorage.getItem('checked-checkboxes')));
if (window.location.search === '' || window.location.pathname === '/products/filter' || window.location.pathname === '/search/results') {
    $(document).ready(function () {
        $('input:checkbox#id_all').prop('checked', true) && $('input:checkbox:checked.updating').prop('checked', false);
    });
}
else if (window.location.pathname === '/products/filter-by-categories/') {
    $(document).ready(function () {
        if ('all' == para) {
            $('input:checkbox#id_all').prop('checked', true) && $('input:checkbox:checked.updating').prop('checked', false);
        } else {
            $('input:checkbox#id_all').prop('checked', false) && $(arrCheckbox.toString()).prop('checked', true);
        }
    })
}

var all = document.getElementById('id_all');
all.addEventListener('click', function () {
    if (this.checked) {
        $('input:checkbox.updating').prop('checked', false);
    } else {
        $('input:checkbox#id_all').prop('checked', true);
    }
});
$(function () {
    $('.updating').click(function () {
        var check_id = $(this).attr('id')
        if (this.checked) {
            $('input:checkbox#id_all').prop('checked', false);
        } else if ($('input:checkbox:checked').length < 1) {
            $('input:checkbox#id_all').prop('checked', true);
        } else {
            $('input:checkbox#id_all').prop('checked', false);
        }
    });
})
// checkbox filter


// live search

var urls = window.location.href
var searchForm = document.getElementById('_search')
var resultBox = document.getElementById('search-box')
document.querySelectorAll('[id=search-box]').forEach(search_box=>{


document.querySelectorAll('[id=id_q]').forEach(element=>{

const sendSearchData = (product) =>{
    $.ajax({
        type:'GET',
        url:'/search/result',
        data:{
            'q':product
        },
        success : (res) =>{
            const data = res.data
            if (Array.isArray(data)){
                search_box.innerHTML = ''
                data.forEach(product =>{
                    search_box.innerHTML += `
                    <a href="${product.get_absolute_url}" class="item">
                        <div class="row mt-2 mb-2">
                            <div class="col-4">
                                <img src="${product.list_image}" class="search-product-img">
                            </div>
                            <div class="col-8">
                                <h5 class="text-dark">${product.name}</h5>
                                <p class="text-dark">قیمت : <p class="text-muted">${product.price}</p></p>
                                <br>
                                <p class="text-dark mt-2"><i class="fa fa-eye text-secondary"></i> بازدید : ${product.hits}</p>

                            </div>

                        </div>
                    </a>
                        <hr>
                    `
                })
            }
            else{
                if (element.value.length > 0){
                    search_box.innerHTML = `<b>${data}</b>`
                }else{
                    search_box.classList.add('not-visible')
                }
            }
        },
        error : (err) =>{
            console.log(err)
        }
    })
}



element.addEventListener('keyup', e => {
    if (search_box.classList.contains('not-visible')){
        search_box.classList.remove('not-visible')
    }
    sendSearchData(e.target.value)
})
    })
})

// live search

