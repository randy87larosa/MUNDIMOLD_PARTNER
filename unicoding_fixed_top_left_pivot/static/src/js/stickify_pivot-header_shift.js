odoo.define('unicoding_fixed_top_left_pivot.PivotRenderer.HeaderShift', function (require) {
"use strict";
 
var PivotRenderer = require('web.PivotRenderer');


PivotRenderer.include({
    
  
    init: function (parent, state, params) {
        this._super.apply(this, arguments);
        
        this.style_stack = $('head #stickify_pivot-stack');
        if(this.style_stack.length < 1) {
            this.style_stack = $('<style id="stickify_pivot-stack" type="text/css"/>').appendTo( $('head') );
        }
    },
    
    // set where to sticky.left?
    // Wrap!, all left are by <th> <span/>.
    
    _renderHeaders: function ($thead, headers, nbrCols) {
        var self = this
        this._super($thead, headers, nbrCols);
        $thead.find('th').map(function() {
          $( this ).wrapInner('<span class="stick-left"/>');
        })
        
        // var sampleCell = self.$el.find('thead ');         
        function updateLefts(){
            var elem = $(this);
            var leftStatic = elem.outerWidth();
            if(leftStatic != self._lastCellWidth) {             
                self._lastCellWidth = leftStatic;
            
                  var sampleCell = elem.next();

                
                var leftPadding = sampleCell.css('padding-left')
                var leftOke = leftStatic + parseFloat(leftPadding) + 1;  //+1 = border
                leftOke = Math.ceil(leftOke);
                var style = $(`<style id="stickify_pivot-stack" type='text/css'> .o_pivot table thead span.stick-left{ left:${leftOke}px;}</style>`)//.appendTo(self.$el);
                             
                self.style_stack.replaceWith(style)
            }
        }
        var throttled = _.throttle(updateLefts, 100);
        $thead.find('tr:nth-child(1) th:nth-child(1)')
          .resize(
            throttled
          );
    },
    
});



});
