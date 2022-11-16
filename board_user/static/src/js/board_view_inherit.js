odoo.define('web.BoardBoardUser', function (require) {
"use strict";

    var BoardView = require('board.BoardView');
    var core = require('web.core');
    var QWeb = core.qweb;
    var Domain = require('web.Domain');
    BoardView.prototype.config.Renderer.include({
        _renderTagBoard: function (node) {
            var self = this;
            // we add the o_dashboard class to the renderer's $el. This means that
            // this function has a side effect.  This is ok because we assume that
            // once we have a '<board>' tag, we are in a special dashboard mode.
            this.$el.addClass('o_dashboard');
            this.trigger_up('enable_dashboard');

            var hasAction = _.detect(node.children, function (column) {
                return _.detect(column.children,function (element){
                    return element.tag === "action"? element: false;
                });
            });
            if (!hasAction) {
                return $(QWeb.render('DashBoard.NoContent'));
            }

            // We should start with three columns available
            node = $.extend(true, {}, node);

            // no idea why master works without this, but whatever
            if (!('layout' in node.attrs)) {
                node.attrs.layout = node.attrs.style;
            }
            for (var i = node.children.length; i < 3; i++) {
                node.children.push({
                    tag: 'column',
                    attrs: {},
                    children: []
                });
            }

            // register actions, alongside a generated unique ID
            _.each(node.children, function (column, column_index) {
                _.each(column.children, function (action, action_index) {
                    action.attrs.id = 'action_' + column_index + '_' + action_index;
                    self.actionsDescr[action.attrs.id] = action.attrs;
                });
            });
            var state_context = self.state.context;
            if (state_context.hasOwnProperty('user_dashboard')){
                node.perm_close = self.state.context.uid === self.state.context.user_dashboard;
            }
            else{
                node.perm_close = true;
            }
            var $html = $('<div>').append($(QWeb.render('DashBoard', {node: node})));

            // render each view
            _.each(this.actionsDescr, function (action) {
                self.defs.push(self._createController({
                    $node: $html.find('.oe_action[data-id=' + action.id + '] .oe_content'),
                    actionID: _.str.toNumber(action.name),
                    context: action.context,
                    domain: Domain.prototype.stringToArray(action.domain, {}),
                    viewType: action.view_mode,
                }));
            });
            $html.find('.oe_dashboard_column').sortable({
                connectWith: '.oe_dashboard_column',
                handle: '.oe_header',
                scroll: false
            }).bind('sortstop', function () {
                self.trigger_up('save_dashboard');
            });
            return $html;
        },
    });

});