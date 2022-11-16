odoo.define('unicoding_fixed_top_left_pivot.PivotRenderer', function (require) {
"use strict";
 
var core = require('web.core');
var config = require('web.config');
var PivotRenderer = require('web.PivotRenderer');


PivotRenderer.include({
    

    init: function (parent, state, params) {
        this._super.apply(this, arguments);
        this.paddingLeftHeaderTabWidth = config.device.isMobile ? 5 : 18;

        this.style_tops = $('head #stickify_pivot-tops');
        if(this.style_tops.length < 1) {
            this.style_tops = $('<style id="stickify_pivot-tops" type="text/css"/>').appendTo( $('head') );
        }
    },
    
    // triggered by second column of first tr>th
    _renderHeaders: function ($thead, headers, nbrCols) {
        var self = this
        this._super($thead, headers, nbrCols);

        // var sampleCell = self.$el.find('thead ');
        function updateTops(){
            var sampleCell = $(this);
            var cellHeight = sampleCell.css('height');

            if(cellHeight != self._lastCellHeight) {
              self._lastCellHeight = cellHeight;

              var nextTr  = '+tr';
              var trtr = "";
              for (var i = 0; i < 15; i++) {
                trtr += '.o_pivot thead tr '+nextTr.repeat(i)+' th{ top: calc('+i+' * '+cellHeight+');}';
              }
              //console.log(trtr);
              // console.log('pivot.render l',leftStatic,'p:',leftPadding,'both:',leftOke);
              var style = $(`<style id="stickify_pivot-tops" type='text/css'>${trtr}</style>`)//.appendTo(self.$el);
              self.style_tops.replaceWith(style)
            }
        }
        var throttled = _.throttle(updateTops, 100);
        $thead.find('tr:nth-child(1) th:nth-child(2)')
          .resize(
            throttled
          );
      // return $row;
    },

    _renderHeaders0: function ($thead, headers, nbrCols)  {
        var self = this
        this._super($thead, headers, nbrCols);
        $thead.find('th').map(function() {
          $( this ).wrapInner('<span class="stick-left"/>');
        })
        $thead.find('tr:nth-child(1) th:nth-child(1)')
          .html('')
          .resize(function(){
              var elem = $(this);

              console.log('1th-resizing!', elem.outerWidth())
              var sampleCell = self.$el.find('thead tr:nth-child(1) th:nth-child(2)');
              var cellHeight = sampleCell.css('height')
              var trtr = "";
              var i;
              var nextTr  = '+tr';
              for (i = 0; i < 15; i++) {
                trtr += '.o_pivot thead tr '+nextTr.repeat(i)+' th{ top: calc('+i+' * '+cellHeight+');}';
              }

              var leftPadding = sampleCell.css('padding')
              var leftStatic = elem.outerWidth()
              var leftOke = leftStatic + parseFloat(leftPadding) + 1;  //+1 = border
              leftOke = Math.ceil(leftOke);
              // console.log('pivot.render l',leftStatic,'p:',leftPadding,'both:',leftOke);
              var style = $(`<style id="stickify_pivot" type='text/css'> .o_pivot table thead span.stick-left{ left:${leftOke}px;} ${trtr}</style>`)//.appendTo(self.$el);
              var old = $('head #stickify_pivot');
              if(old.length)
                 old.replaceWith(style)
              else
                $('head').append(style)
          });
      // return $row;
    }

});


var PivotController = require('web.PivotController');

PivotController.include({

    /**
     * When we click on a closed header cell, we either want to open the
     * dropdown menu to select a new groupby level, or we want to open the
     * clicked header, if a corresponging groupby has already been selected.
     *
     * @private
     * @param {MouseEvent} event
     */
    _onClosedHeaderClick: function (event) {
        this._lastClosedHeader$Target = $(event.target);
        this._super(event);        
    },

});


});
