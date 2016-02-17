/**
 * jquery.ripple.js
 * 
 * @version 0.0.1
 * @author SUSH <sush@sus-happy.ner>
 * https://github.com/sus-happy/jquery.ripple.js
 */

( function( $, U ) {
    // use border-radius
    $.support.borderRadius = false;
    // use transition
    $.support.transition = false;
    $( function() {
        $.each( [ 'borderRadius', 'BorderRadius', 'MozBorderRadius', 'WebkitBorderRadius', 'OBorderRadius', 'KhtmlBorderRadius' ], function( i, v ) {
            if( document.body.style[v] !== undefined ) $.support.borderRadius = true;
            return (! $.support.borderRadius );
        } );

        var el = $("<div>");
        $.support.transition = typeof el.css("transitionProperty") === "string";
    } );

    $.extend( {
        // jquery.rippleз”ЁгЃ®й–ўж•°
        ripple: {
            // г‚ўгѓ‹гѓЎгѓјг‚·гѓ§гѓігЃ®иЈЏгЃ«йљ г‚ЊгЃЄгЃ„г‚€гЃ†гЃ«гЃ™г‚‹DOM
            $textSpan: $('<span>').css( { position: 'relative', 'z-index': 2 } ),
            // г‚ўгѓ‹гѓЎгѓјг‚·гѓ§гѓіз”ЁгЃ®DOM
            $rippleWrap: $('<span>', { 'class': 'rippleWrap' } ).css( { position: 'absolute', 'z-index': 1, 'left': 0, 'top': 0, 'overflow': 'hidden' } ).append(
                            $('<span>', { 'class': 'rippleAnimate' } ).css( { position: 'absolute', 'left': 0, 'top': 0, 'width': 0, 'height': 0, 'border-radius': '50%' } )
                         ),
            // jquery.rippleгЃЊе€©з”ЁгЃ§гЃЌг‚‹гЃ‹пјџ
            is: function() {
                return $.support.borderRadius && $.support.transition;
            },
            // coreг‚Їгѓ©г‚№
            core: function( target, param ) {
                this.$target   = target;
                this._v_duration = 400;
                this._h_duration = 400;
                this._timer      = null;

                // paramгЃ«еЂ¤гЃЊгЃ‚г‚ЊгЃ°иЁ­е®ље¤‰ж›ґ
                if( param !== U && Object.prototype.hasOwnProperty.call( param, 'v_duration' ) ) {
                    this.set_view_duration( param.v_duration );
                }
                if( param !== U && Object.prototype.hasOwnProperty.call( param, 'h_duration' ) ) {
                    this.set_hide_duration( param.h_duration );
                }

                // г‚¤гѓ™гѓігѓ€е€ќжњџиЁ­е®љ
                this.init();
            }
        }
    } );

    // coreг‚Їгѓ©г‚№г‚’ж‹ЎејµгЃ—гЃ¦гЃЉгЃЏ
    $.ripple.core.prototype = {
        // иЁ­е®ље¤‰ж›ґ
        set_view_duration: function( v_duration ) {
            this._v_duration = v_duration;
        },
        set_hide_duration: function( h_duration ) {
            this._h_duration = h_duration;
        },

        // г‚¤гѓ™гѓігѓ€е€ќжњџиЁ­е®љ
        init: function() {
            var that = this;

            // position staticгЃ гЃЈгЃџг‚‰relativeгЃ«гЃ—гЃ¦гЃЉгЃЏ
            if( this.$target.css( 'position' ) === 'static' ) {
                this.$target.css( 'position', 'relative' );
            }
            // г‚№гѓћгѓ›з«Їжњ«гЃ®гѓЏг‚¤гѓ©г‚¤гѓ€г‚’е€‡г‚‹
            this.$target.css( '-webkit-tap-highlight-color', 'rgba( 0, 0, 0, 0 )' );

            // еї…и¦ЃDOMг‚’иїЅеЉ 
            this.$target.wrapInner( $.ripple.$textSpan );
            this.$target.append( $.ripple.$rippleWrap.clone() );

            // еї…и¦ЃDOMг‚’е¤‰ж•°гЃ«е…Ґг‚ЊгЃ¦гЃЉгЃЏ
            this.$rippleWrap    = this.$target.find( '.rippleWrap' );
            this.$rippleAnimate = this.$target.find( '.rippleAnimate' );

            // гѓћг‚№г‚ЇгЃ«й–ўдї‚гЃ™г‚‹г‚№г‚їг‚¤гѓ«г‚’еЏЌж гЃ™г‚‹
            // border-radius
            this.$rippleWrap.css( 'border-radius', this.$target.css( 'border-radius' ) );

            // и‰Іг‚’жЊ‡е®љ
            this.$target.find( '.rippleAnimate' ).css( 'background-color', this.$target.attr( 'data-color' ) );

            // г‚¤гѓ™гѓігѓ€г‚’з™»йЊІ
            if( ('ontouchstart' in window) ) {
                this.$target.bind( 'touchstart.ripple', function( e ) {
                    that.view( e.originalEvent.touches[0] );
                } );
                this.$target.bind( 'touchend.ripple', function( e ) {
                    that.hidden( e.originalEvent.touches[0] );
                } );
                this.$target.bind( 'mouseleave.ripple', function( e ) {
                    that.hidden( e );
                } );
            } else {
                this.$target.bind( 'mousedown.ripple', function( e ) {
                    that.view( e );
                } );
                this.$target.bind( 'mouseup.ripple mouseleave.ripple', function( e ) {
                    that.hidden( e );
                } );
            }
        },

        // г‚¤гѓ™гѓігѓ€е»ѓж­ў
        remove: function() {
        },

        // г‚ўгѓ‹гѓЎгѓјг‚·гѓ§гѓій–‹е§‹
        view: function( e ) {
            // г‚їг‚¤гѓћгѓјгЃЇе€‡гЃЈгЃ¦гЃЉгЃЏ
            clearTimeout( this._timer );

            // гѓћг‚№г‚Їи¦Ѓзґ гЃ®г‚µг‚¤г‚єг‚’е†ЌеЏ–еѕ—пј€е¤‰г‚Џг‚‹еЏЇиѓЅжЂ§г‚‚иЂѓж…®гЃ—гЃ¦пј‰
            var width  = this.$target.outerWidth();
            var height = this.$target.outerHeight();
            this.$rippleWrap.stop( true, false ).width( width ).height( height ).css( { 'opacity': 1, 'transition': 'none' } );

            // г‚µг‚¤г‚єг‚’жЊ‡е®љпј€зё¦жЁЄгЃ®е¤§гЃЌгЃ„еЂ¤пј‰
            var circleRatio      = 2.8;
            var size = Math.max( width, height );

            // гѓћг‚¦г‚№гѓњг‚їгѓігЃ®дЅЌзЅ®г‚’еЏ–еѕ—
            // offsetX, offsetYгЃЊгЃЉгЃ‹гЃ—гЃ„гЃ®гЃ§pageX, pageYгЃ‹г‚‰иЁ€з®—гЃ™г‚‹
            var offsetX = e.pageX - this.$target.offset().left;
            var offsetY = e.pageY - this.$target.offset().top;
            this.$rippleAnimate.css( { 'width': size, 'height': size, 'transform': 'scale3d( 0, 0, 1 )', 'left': offsetX-size/2, 'top': offsetY-size/2, 'transition': 'none' } );

            var animateTo        = {};
            animateTo.transform  = 'scale3d( ' + circleRatio + ', ' + circleRatio + ', 1 )';
            animateTo.transition = ( this._v_duration/1000 )+'s ease-out';

            // г‚ўгѓ‹гѓЎгѓјг‚·гѓ§гѓій–‹е§‹
            this.$rippleAnimate.show()
                .css( animateTo );
        },

        // г‚ўгѓ‹гѓЎгѓјг‚·гѓ§гѓізµ‚дє†
        hidden: function( e ) {
            var that = this;
            // WrapгЃ®йЂЏжЋеє¦г‚’дё‹гЃ’гЃ¦йљ гЃ—гЃ¦гЃ„гЃЏ
            this.$rippleWrap.stop( true, false ).css( { 'opacity': 0, 'transition': 'opacity '+( this._h_duration/1000 )+'s ease-out' } );

            // г‚ўгѓ‹гѓЎгѓјг‚·гѓ§гѓізµ‚дє†г‚їг‚¤гѓџгѓіг‚°гЃ§г‚µг‚¤г‚єе¤‰ж›ґ
            clearTimeout( this._timer );
            this._timer = setTimeout( function() {
                that.$rippleWrap.css( { 'opacity': 1, 'transition': 'none' } );
                that.$rippleAnimate.css( { 'transform': 'scale3d( 0, 0, 1 )', 'transition': 'none' } );
            }, this._v_duration );
        }
    };

    $.fn.extend( {
        // jquery.ripple
        ripple: function( opt ) {
            // еї…и¦ЃжќЎд»¶гЃ«жєЂгЃџгЃ•гЃЄгЃ‘г‚ЊгЃ°зµ‚дє†
            // border-radiusгЃЁtransitionгЃЊдЅїгЃ€г‚ЊгЃ°гЃџгЃ¶г‚“е‹•гЃЏ
            if(! $.ripple.is() ) {
                return $(this);
            }

            // еЇѕи±ЎDOMгЃ«еЇѕгЃ—гЃ¦г‚¤гѓ™гѓігѓ€г‚’з™»йЊІгЃ™г‚‹
            $(this).each( function() {
                new $.ripple.core( $(this), opt );
            } );

            return $(this);
        }
    } );
} )( jQuery );

( function( $ ) {
    $( function() {

        $( '.ripple' ).ripple();
        $( '.ripple-fast' ).ripple( { 'v_duration': 150, 'h_duration': 150 } );
        $( '.ripple-slow' ).ripple( { 'v_duration': 700, 'h_duration': 700 } );
        $( '.ripple-fast-slow' ).ripple( { 'v_duration': 600, 'h_duration': 150 } );

    } );
} )( jQuery );