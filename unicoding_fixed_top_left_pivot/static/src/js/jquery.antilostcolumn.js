/*! part of friendly_pivot project
    2019-November-09 
    Fathony L.
	 */

;(function ($, window, undefined) {
	'use strict';
  
  // helper funcs:
  
  function _implicitWidth($obj) {
    // var html = $obj.html();
    // $obj.html('');
    // var width = $obj.width();
    // $obj.html(html);
    var tmp = $obj.clone().html('').appendTo($('body'));
    var width = tmp.width();
    var explicitWidth = (width > 0) ? $obj.css('width') : null;
    
    if(explicitWidth !== null)
      $obj.css('width', '');
    $obj.css('position', 'absolute' );
    var implicitWidth = parseInt($obj.css('width')) ;
    $obj.css('position','');
    if(explicitWidth !== null)
      $obj.css('width', explicitWidth) ;
    return implicitWidth;
  }
  // function _hasSetHeight($obj) {
    // var html = $obj.html();
    // $obj.html('');
    // var width = $obj.width();
    // $obj.html(html);
    // var explicitWidth = (width > 0) ? "yes" : "no";
    // return setHeight;
  // }
  
  function _boundingWidth($cell){
    var boundingClientRect = $cell[0].getBoundingClientRect();
    if (boundingClientRect.width) {
      return boundingClientRect.width; // #39: border-box bug
    } else {
      return boundingClientRect.right - boundingClientRect.left; // ie8 bug: getBoundingClientRect() does not have a width property
    }
  }
  
  function _computedStyleWidth($cell){
      return width = parseFloat(window.getComputedStyle($cell[0], null).width);
  }
  function _ie8Width($cell){
      // ie8 only
        var leftPadding = parseFloat($cell.css('padding-left'));
        var rightPadding = parseFloat($cell.css('padding-right'));
        // Needs more investigation - this is assuming constant border around this cell and it's neighbours.
        var border = parseFloat($cell.css('border-width'));
        return $cell.outerWidth() - leftPadding - rightPadding - border;
  }
  function _cellWidth($cell){
      return $cell.width()
  }
  
  // plugin
	var name = 'antiLostColumn',
		id = 0,
		defaults = {
			// fixedOffset: 0,
			// leftOffset: 0,
			// marginTop: 0,
			objDocument: document,
			// objHead: 'head',
			scrollableArea: window,
			expandMergedCellOnly: true,
			// zIndex: 3
		};

	function Plugin (el, options) {
		// To avoid scope issues, use 'base' instead of 'this'
		// to reference this class from internal events and functions.
		var base = this;

		// Access to jQuery and DOM versions of element
		base.$el = $(el);
		base.el = el;
		base.id = id++;

		// Listen for destroyed, call teardown
		base.$el.bind('destroyed',
			$.proxy(base.teardown, base));


		// Keep track of state
		// base.leftOffset = null;
		// base.topOffset = null;

    
    base.lookupBestWidthFunc = function($ths) {
      var $cell = $ths.eq(0),
            fn;
      // I assumed that all cell has similar style, so I am checking once and apply to all
      if ($cell.css('box-sizing') === 'border-box') {
        fn = _boundingWidth
      } else {
        // var $origTh = $('th:first,td:first', base.$originalHeader);
        if ($cell.css('border-collapse') === 'collapse') {
          if (window.getComputedStyle) {
            // width = parseFloat(window.getComputedStyle($cell[0], null).width);
            fn = _computedStyleWidth
          } else {
            // ie8 only
            fn = _ie8Width ;
          }
        } else {
          // width = $cell.width();
          fn = _cellWidth
        }
      }
      base.globalGetWidth = fn;
    };
    
		base.init = function () {
			base.setOptions(options);

			base.$el.each(function () {
				var $this = $(this);

				// remove padding on <table> to fix issue #7
				// $this.css('padding', 0);

				// base.$originalHeader = $('thead:first', this);
				// base.$clonedHeader = base.$originalHeader.clone();
				// $this.trigger('clonedHeader.' + name, [base.$clonedHeader]);

				// base.$clonedHeader.addClass('tableFloatingHeader');
				// base.$clonedHeader.css({display: 'none', opacity: 0.0});

				// base.$originalHeader.addClass('tableFloatingHeaderOriginal');

				// base.$originalHeader.after(base.$clonedHeader);

				// base.$printStyle = $('<style type="text/css" media="print">' +
					// '.tableFloatingHeader{display:none !important;}' +
					// '.tableFloatingHeaderOriginal{position:static !important;}' +
					// '</style>');
				// base.$head.append(base.$printStyle);
			});
			
			// base.$clonedHeader.find("input, select").attr("disabled", true);
      //merged th
      base.$mergeHeaderCells = base.options.expandMergedCellOnly ?
        base.$el.find("thead th[colspan]").filter("th[colspan!='1']") :
        base.$el.find("thead th");
      base.lookupBestWidthFunc( base.$mergeHeaderCells )
      base.$mergeHeaderCells.each(function(){
          // return;
          var $th = $(this);
          $th.addClass('this-th-parsed')
          // $th.parent().css('height', $th.parent().css('height') );
          // $th.css('height', $th.css('height') );
          
          //calculate max-width
          // $th.data('max-width', $th.css('width') );
          $th.data('max-width', base.globalGetWidth($th) );
          
          
          $th.data('inner-width', $th.width() );
          $th.data('padding-left', parseInt($th.css('padding-left')) );
          $th.data('padding-right', parseInt($th.css('padding-right')) );
          
          //calculate min-width
          // var position = $th.css('position'
          // $th.css('position', 'absolute' );
          // $th.data('min-width', parseInt($th.css('width')) );
          // $th.css({'position':''/*, 'width': $th.data('max-width')*/ });
          $th.data('min-width', _implicitWidth($th) );
          
          // $th.text( $th.width() +'spanleft:'+$th.css('padding-left') +' spanright:'+$th.css('padding-right') )
      })
			// base.updateWidth();
			base.adjustColTextVisibility();
			base.bind();
		};

		base.destroy = function (){
			base.$el.unbind('destroyed', base.teardown);
			base.teardown();
		};

		base.teardown = function(){
			// if (base.isSticky) {
				// base.$originalHeader.css('position', 'static');
			// }
			$.removeData(base.el, 'plugin_' + name);
			base.unbind();

			// base.$clonedHeader.remove();
			// base.$originalHeader.removeClass('tableFloatingHeaderOriginal');
			// base.$originalHeader.css('visibility', 'visible');
			// base.$printStyle.remove();

			base.el = null;
			base.$el = null;
		};

		base.bind = function(){
			// base.$scrollableArea.on('scroll.' + name, base.toggleHeaders);
			base.$scrollableArea.on('scroll.' + name, base.adjustColTextVisibility);
		};

		base.unbind = function(){
			// unbind window events by specifying handle so we don't remove too much
			// base.$scrollableArea.off('.' + name, base.toggleHeaders);
			base.$scrollableArea.off('.' + name, base.adjustColTextVisibility);
		};

		// We debounce the functions bound to the scroll and resize events
		base.debounce = function (fn, delay) {
			var timer = null;
			return function () {
				var context = this, args = arguments;
				clearTimeout(timer);
				timer = setTimeout(function () {
					fn.apply(context, args);
				}, delay);
			};
		};

		base.toggleHeaders = base.debounce(function () {
			if (base.$el) {
				base.$el.each(function () {
					console.log('antilost.toggled!',$(this))
				});
			}
		}, 0);

		// base.adjustColTextVisibility = base.debounce(function () {
    base.adjustColTextVisibility = function() {
      // console.log('antilost.adjustColTextVisibility!',$(this));
      // return;
      var
        viewportLeft =  base.$scrollableArea.offset().left
      //merged th
      base.$mergeHeaderCells.each(function(i){
          var $th = $(this);
          // $th.css('background-color', 'yellow');
          if(!$th.text()) return;
          
          // var width = $th.data('max-width');
          var width = base.globalGetWidth($th)
          
          if(!width)
            return;
          // console.log(i,$th.parent().index(), $th.index(),  $th.text(), left, width  )
          
          var left = $th.offset().left;
          var padl = $th.data('padding-left');
          var newPadL = undefined;
          
          if($th.is('.o_pivot_header_cell_closed') || left >= viewportLeft){
              // $th.css('padding-left', $th.data('padding-left'))
              newPadL = padl;
          } else {
              //sticky merged th. show offscreen text
              // var width = 
              // if(left<0){
                  // var inner = $th.data('inner-width');
                  var inner = $th.data('min-width');
                  // var xleft = -left;
                  var xleft = viewportLeft - left;
                  // padl = parseInt($th.data('padding-left'));
                  var padr = $th.data('padding-right');
                  // width += left; // width = width - -left;
                  var rightAlignedSpanLeft = (width - padr) - inner;
                  // var leftAlignedSpanLeft = (width - xleft) + padl + xleft;
                  var leftAlignedSpanLeft = xleft + padl ;
                  // var space = $th.data('inner-width') 
                  newPadL = (leftAlignedSpanLeft + inner + padr) < width ? leftAlignedSpanLeft : rightAlignedSpanLeft;
              // }              
          }
          if(newPadL != parseInt($th.css('padding-left')))
            $th.css('padding-left', newPadL)
          // console.log('change:',$th.parent().index(), $th.index(),  $th.text(), newPadL )
          // $th.parent().css('height', $th.parent().css('height') );
          // $th.css('height', $th.css('height') );
          
          //calculate max-width
          // $th.data('max-width', $th.css('width') );
          // $th.data('max-width', base.globalGetWidth($th) );
          
          //calculate min-width
          // $th.css('position', 'absolute' );
          // $th.data('min-width', $th.css('width') );
          // $th.css({'position':'initial'/*, 'width': $th.data('max-width')*/ });
          
          // $th.text( $th.width() )
      });


			
		}



		base.setOptions = function (options) {
			base.options = $.extend({}, defaults, options);
			// base.$window = $(base.options.objWindow);
			// base.$head = $(base.options.objHead);
			base.$document = $(base.options.objDocument);
			// base.$scrollableArea = $(base.options.scrollableArea);
      var $table = base.$el.is('table') ? base.$el : base.$el.find('table');
      // console.log('antilost.getscroll.EL=',base.$el.html())
      // console.log('antilost.getscroll.tbl=',base.$el.find('table'))
			// base.$scrollableArea = base.$el.find('table').scrollParent()
			base.$scrollableArea = $table.scrollParent()
      console.log('antilost.EL:',base.$el)
      console.log('antilost.scroll$:',base.$scrollableArea)
		};

		base.updateOptions = function (options) {
			base.setOptions(options);
			// scrollableArea might have changed
			base.unbind();
			base.bind();
			base.toggleHeaders();
		};

		// Run initializer
		base.init();
	}

	// A plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[name] = function ( options ) {
		return this.each(function () {
			var instance = $.data(this, 'plugin_' + name);
			if (instance) {
				if (typeof options === 'string') {
					instance[options].apply(instance);
				} else {
					instance.updateOptions(options);
				}
			} else if(options !== 'destroy') {
				$.data(this, 'plugin_' + name, new Plugin( this, options ));
			}
		});
	};

})(jQuery, window);
