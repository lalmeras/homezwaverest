(function($, window, document, undefined) {
    if (window.console === undefined) {
        window.console = function() {};
    }

    var level = 99;

    $(document).ready(function() {
        $.ajax({
            url : '/nodes/',
            type : 'GET',
            complete : function(data, status) {
                var nodes = data.responseJSON;
                console.log(nodes);
                $.each(nodes, function(index, item) {
                    if (item.node_id == 1) return;
                    var $nodeWrapper = $('#zwave-node').clone();
                    $('#zwave-node-title', $nodeWrapper).text(item.name).attr('id', '');
                    $('#zwave-node-location', $nodeWrapper).text(item.location).attr('id', '');
                    var $node = $($nodeWrapper.html());
                    var $level = $('.zwave-node-level', $node).hide();
                    doLoadLevel(item.node_id, $level);
                    $node.on('click', '[data-bind=global-action]', { node_id: item.node_id }, doAction);
                    $node.on('click', '[data-bind=config-action]', { node_id: item.node_id }, doConfig);
                    $('#node-list').append($node);
                });
            },
        });

        var doConfig = function(event) {
            var node_id = event.data.node_id;
            var data = 'Yes';
            var index = 29;
            $.ajax({
                url : '/node/' + node_id + '/command_class/112/value/' + index + '/' + data + '/',
                type : 'PUT',
            })
        };

        var doLoadLevel = function(node_id, $level) {
            $.ajax({
                url : '/node/' + node_id + '/command_class/38/value/0/',
                type : 'GET',
                dataType : 'json'

            }).done(function(data, textStatus, jqXHR) {
                console.log(data, textStatus, jqXHR);
                $level.text('(' + jqXHR.responseJSON.data + '%)').show();
            }).fail(function(jqXHR, textStatus, errorThrown) {
                console.log(jqXHR, textStatus, errorThrown);
            });
        };

        var doAction = function(event) {
            var node_id = event.data.node_id;
            var data = level;
            var index = 0;
            $.ajax({
                url : '/node/' + node_id + '/command_class/38/value/' + index + '/' + data + '/',
                type : 'PUT',
            });
        };

        $('[data-bind=global-action-level]').click(function(event) {
            $(window).trigger('hzrGlobalAction', Number($(this).attr('data-level')));
        });

        $(window).on('hzrGlobalAction', function(event, newLevel) {
            level = Number(newLevel);
            $('[data-bind=global-action-level]').each(function(index, item) {
                var $that = $(this);
                if ($that.attr('data-level') == level) {
                    $that.addClass('active');
                } else {
                    $that.removeClass('active');
                }
            });
        });

        $(window).trigger('hzrGlobalAction', level);
    });

    var action = 'UP';

} (jQuery, window, document));
