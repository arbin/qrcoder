/* Twitter Plugin
================================================== */

$(function($){
    $(".tweet").tweet({
        username: "pysoldev",
        join_text: "auto",
        count: 1,
        loading_text: "loading tweets...",
        template: "{text}{time}"
    });
});



/* Header Image Slider
/* http://www.buildinternet.com/project/supersized
================================================== */

if ($('#progress-back').length) {

    // progress bar
    $(function() {
        $('#progressbar').each(function(){
            var t = $(this),
                dataperc = t.attr('data-perc'),
                barperc = Math.round(dataperc);
            t.find('.bar').animate({width:barperc+'%'}, dataperc*50);
            t.find('.label').append('<div class="perc"></div>');

            var current = 0;
            var rate = 1;

            var counter = setInterval(function(){
                if(current >= dataperc) clearInterval(counter);

                $(".perc").text(current +'%');

                current = parseInt(current) + parseInt(rate);

            }, dataperc*25 / (dataperc / rate));

            function perc() {
                var length   = t.find('.bar').css('width'),
                    labelpos = (parseInt(length));
                t.find('.label').css('left', labelpos);
            }
            perc();
            setInterval(perc, 0);
        });

        // background image changer
        $.supersized({

            // Functionality
            slideshow               :   1,          // Slideshow on/off
            autoplay                :   1,          // Slideshow starts playing automatically
            start_slide             :   1,          // Start slide (0 is random)
            stop_loop               :   0,          // Pauses slideshow on last slide
            random                  :   0,          // Randomize slide order (Ignores start slide)
            slide_interval          :   3000,       // Length between transitions
            transition              :   1,          // 0-None, 1-Fade, 2-Slide Top, 3-Slide Right, 4-Slide Bottom, 5-Slide Left, 6-Carousel Right, 7-Carousel Left
            transition_speed        :   1000,       // Speed of transition
            new_window              :   1,          // Image links open in new window/tab
            pause_hover             :   0,          // Pause slideshow on hover
            keyboard_nav            :   1,          // Keyboard navigation on/off
            performance             :   1,          // 0-Normal, 1-Hybrid speed/quality, 2-Optimizes image quality, 3-Optimizes transition speed // (Only works for Firefox/IE, not Webkit)
            image_protect           :   1,          // Disables image dragging and right click with Javascript

            // Size & Position
            min_width               :   0,          // Min width allowed (in pixels)
            min_height              :   0,          // Min height allowed (in pixels)
            vertical_center         :   1,          // Vertically center background
            horizontal_center       :   1,          // Horizontally center background
            fit_always              :   0,          // Image will never exceed browser width or height (Ignores min. dimensions)
            fit_portrait            :   1,          // Portrait images will not exceed browser height
            fit_landscape           :   0,          // Landscape images will not exceed browser width

            // Components
            slide_links             :   'blank',    // Individual links for each slide (Options: false, 'number', 'name', 'blank')
            thumb_links             :   1,          // Individual thumb links for each slide
            thumbnail_navigation    :   0,          // Thumbnail navigation
            slides                  :   [           // Slideshow Images
                                        {image : 'assets/img/slider/2.jpg'},
                                        {image : 'assets/img/slider/3.jpg'},
                                        {image : 'assets/img/slider/6.jpg'},
                                        {image : 'assets/img/slider/5.jpg'},
                                        {image : 'assets/img/slider/4.jpg'},
                                        {image : 'assets/img/slider/1.jpg'}
                                        ],

            // Theme Options
            progress_bar            :   1,          // Timer for each slide
            mouse_scrub             :   0

        });

    });

};



/* Countdown Widget
/* http://keith-wood.name/countdown.html
================================================== */

if ($('#countdown').is(":visible")) {

    $(function() {
        launchTime = new Date([2020], [6], [21], [12]); // Set launch: [year], [month], [day], [hour]...
            launchTime.setDate(launchTime.getDate()); // Add 13 days
        $("#countdown").countdown({until: launchTime, compact: true, format: "YOWDHMS"});
    });

}



/* Text Fader
================================================== */

if ($('#words').length) {

    jQuery(function($){

        var data = {

            words: [
                {
                    review: "Facebook Page"
                },
                {
                    review: "Contact Info"
                },
                {
                    review: "Mobile Website"
                },
                {
                    review: "Email Address"
                },
				{
                    review: "Location Map"
                }
            ]

        };

        $.each(data.words,function(i,itemData){
            var p = $('<strong>').text(itemData.review);
            if (i == 0) p.addClass('active');
            else p.css({opacity: 0.0});
            $('#words').append(p);
        });

        function nextWord() {
            var $active = $('#words strong.active');
            if ( $active.length == 0 ) $active = $('#words strong:last');
            var $next =  $active.next().length ? $active.next() : $('#words strong:first');

            $active.removeClass('active').animate({opacity: 0.0}, 1000, function(){
                $active.hide();
                $next.show().addClass('active').animate({opacity: 1.0}, 1000);
            });
        }

        setInterval(nextWord, 5000 );

    });

};



/* Header Google Map
================================================== */

// cordinates
var posY = 51.54500;
var posX = -0.02832;

function initialize() {

    // create positions
    secheltLoc = new google.maps.LatLng(posY,posX);

    // offset for infobox
    posY = posY - 0.002500;
    posX = posX - 15;
    offsetLoc = new google.maps.LatLng(posY,posX);

    // map styling
    var styleArray = [
        {
          stylers: [
            { hue: "#000000" },
            { saturation: -100},
            { lightness:-25 }
        ]
        },{
          featureType: "road",
          elementType: "geometry",
          stylers: [
            { visibility: "off" }
          ]
        },{
          featureType: "road",
          featureType: "city",
          elementType: "labels",
          stylers: [
            { visibility: "off" }
          ]
        }
    ];

    var myMapOptions = {
        panControl: false,
        zoomControl: false,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        overviewMapControl: false,
        draggable: true,
        disableDoubleClickZoom: true,
        scrollwheel: false,
        zoom:5,
        styles: styleArray,
        center: offsetLoc,
        mapTypeId: google.maps.MapTypeId.ROADMAP //   ROADMAP; SATELLITE; HYBRID; TERRAIN;
    };

    var theMap = new google.maps.Map(document.getElementById("map_canvas"), myMapOptions);

    var marker = new google.maps.Marker({
        map: theMap,
        draggable: false,
        position: secheltLoc,
        visible: true,
        icon: new google.maps.MarkerImage("assets/img/dot.png"),
    });

};

/* Pretty Photo Image Gallery
/* http://no-margin-for-errors.com/projects/prettyphoto-jquery-lightbox-clone/documentation/
================================================== */

if ($('.gallery').length) {

    $(document).ready(function() {

        $(".gallery:first a[rel^='prettyPhoto']").prettyPhoto({
            overlay_gallery: true,
            show_title:false,
            opacity:0.95,
            allow_resize:true,
            default_width: 500,
            default_height: 344,
            deeplinking:false,
            animation_speed:'normal',
            theme:'facebook',
            slideshow:3000,
            autoplay_slideshow:false,
            social_tools:false
         });
    });

}



/* Subscribe Widget
================================================== */

if ($('#subscribe').is(":visible")) {

    $("#subscribe button").click(function() {

        var email   = $("#email").val();
        var emailReg = /^[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,4}(\.[a-zA-Z]{2,3})?(\.[a-zA-Z]{2,3})?$/;

        // client-side validation
         if(emailReg.test(email) == false)
            return false;

        $.ajax({
            type: "post",
            dataType: "json",
            url: "save-email.php",
            data: $("#subscribe").serialize(),
            success: function(data) {

                $('#subscribe').html('<p class="medium">We will notify you upon release. Thank you.</p>');

            }
        });
        return false;
    });

};



/* Contact Form Widget
================================================== */

if ($('#contact').is(":visible")) {

    $("#contact button").click(function() {

        var name     = $("#contactname").val();
        var message  = $("#contactmessage").val();
        var email    = $("#contactemail").val();
        var emailReg = /^[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,4}(\.[a-zA-Z]{2,3})?(\.[a-zA-Z]{2,3})?$/;

        // client-side validation
        if(emailReg.test(email) == false) {
            var emailValidation = false;
            $('#contactemail').addClass("error");
        }
        else
            $('#contactemail').removeClass("error");

        if(name.length < 1) {
            var nameValidation = false;
            $('#contactname').addClass("error");
        }
        else
            $('#contactname').removeClass("error");

        if(message.length < 1) {
            var messageValidation = false;
            $('#contactmessage').addClass("error");
        }
        else
            $('#contactmessage').removeClass("error");

        if ((nameValidation == false) || (emailValidation == false) || (messageValidation == false))
            return false;

        $.ajax({
            type: "post",
            dataType: "json",
            url: "send-email.php",
            data: $("#contact").serialize(),
            success: function(data) {

                $('.form').html('<p class="success">Email sent. Thank you.</p>');

            }
        });
        return false;
    });

};

$("#qrcode button").click(function() {
	$.ajax({
            type: "post",
            dataType: "json",
            url: "",
            data: $("#qrcode").serialize(),
            success: function(data) {
				alert("hello");
                //$('.form').html('<p class="success">Email sent. Thank you.</p>');

            }
        });
        //return false;
});
