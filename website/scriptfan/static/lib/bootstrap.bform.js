/* 
 * bootstrap.bform.js v0.1
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 * 
 * Simple bootstrap form utilities.
 */
!function ($) {
    var BForm = function (element, options) {
        this.init(element, options);
    };

    BForm.prototype = {

        constructor: BForm,

        init: function (element, options) {
            var self = this;
            this.isForm = element.tagName === 'FORM';
            this.$element = $(element);
            this.options = $.extend({}, $.fn.bform.defaults, options);
            this.$alerts = $(this.options.alerts);

            // 如果是表单，绑定提交事件，如果是链接或者按钮，则模拟提交事件
            if (this.isForm) {
                this.$element.on('submit', $.proxy(this.submit, this));
                // 保存field中的原有提示信息
                this.$element.find(this.options.fieldHelp).each(function() {
                    $(this).data('default', $(this).html());
                });
                this.$element.find('[name]').each(function() {
                    var $field = $(this);
                    $field.blur(function() { self.clear($field.attr('name')); });
                    $field.change(function() { self.clear($field.attr('name')); });
                });
            } else {
                this.$element.on('click.bform', $.proxy(this.click, this));
            }
        },

        click: function(event) {
            event.preventDefault();
            this.clear();

            $.ajax({
                url: this.$element.attr('href') || this.$element.data('action'),
                dataType: this.options.dataType,
                type: this.$element.data('method') || this.options.method,
                success: $.proxy(this.success, this),
                error: $.proxy(this.error, this)
            });
        },

        submit: function(event) {
            event.preventDefault();
            this.clear();

            $.ajax({
                url: this.$element.attr('action'),
                data: this.$element.serialize(),
                dataType: this.options.dataType,
                type: this.$element.attr('method') || this.options.method,
                success: $.proxy(this.success, this),
                error: $.proxy(this.error, this)
            });
        },

        success: function(data) {
            this.showMessages(data.messages);
            var redirect = null;

            if (data.success) {
                redirect = data.redirect || this.options.redirect;
            } else {
                this.showErrors(data.errors);
            }

            this.$alerts.find('.alert').delay(this.options.delay).fadeOut(function() {
                if (redirect) window.location = redirect;
                $(this).remove();
            });
        },

        error: function(jqXHR, textStatus, errorThrown) {
            this.showMessages({ error: '服务器错误，请稍候再试'});
        },

        clear: function(field) {
            this.$alerts.empty();

            if (field) {
                var $field = this.$element.find(fmt('[name="%{1}"]', field));
                $field.parents('.control-group').removeClass('error');
                var $help = this.getFieldHelp($field);
                var data = $help.data('default');
                data !== undefined && $help.html(data);
            } else {
                this.$element.find('.control-group').removeClass('error');
                this.$element.find(this.options.fieldHelp).each(function() {
                    var $help = $(this);
                    var data = $help.data('default');
                    data !== undefined && $help.html(data);
                });
            }
        },

        getFieldHelp: function($field) {
            var $help = $field.nextAll(this.options.fieldHelp);
            if ($help.size() === 0) {
                $help = $field.parents('.controls').find(this.options.fieldHelp);
            }
            return $help;
        },

        showErrors: function(errors) {
            var $this = this;
            $.each(errors || {}, function(field, message) {
                var $field = $this.$element.find(fmt('[name="%{1}"]', field));
                $field.parents('.control-group').addClass('error');
                $this.getFieldHelp($field).html($.isArray(message) ? message[0] : message);
            });
        },

        showMessages: function(messages) {
            var $this = this;
            $.each(messages || {}, function(category, message) {
                $this.$alerts.append(fmt($this.options.tpls.alert, category, message));
            });
        }
    };

    /* PRIVATE FUNCTIONS
     *=================*/
    function fmt() {
        var args = arguments;
        return args[0].replace(/%\{(.*?)}/g, function(match, prop) {
            return function(obj, props) {
                var prop = /\d+/.test(props[0]) ? parseInt(props[0]) : props[0];
                if (props.length > 1) {
                    return arguments.callee(obj[prop], props.slice(1));
                } else {
                    return obj[prop] || '';
                }
            }(typeof args[1] === 'object' ? args[1] : args, prop.split(/\.|\[|\]\[|\]\./));
        });
    }

    /* BOOTSTRAP FORM PLUGIN DEFINITION
     * ========================= */

    $.fn.bform = function ( option ) {
        return this.each(function () {
            var $this = $(this);
            var data = $this.data('bform');
            var options = typeof option == 'object' && option;
            if (!data) $this.data('bform', (data = new BForm(this, options)));
            if (typeof option == 'string') data[option]();
        });
    };

    $.fn.bform.Constructor = BForm;

    $.fn.bform.defaults = {
        method: 'GET',
        dataType: 'json',
        alerts: '.alert-messages',
        fieldHelp: '.help-inline, .help-block',
        tpls: {
            alert: '<div class="alert alert-%{1} fade in"><button type="button" class="close" data-dismiss="alert">×</button>%{2}</div>'
        },
        redirect: window.location.toString(),
        delay: 1000
    }
}(window.jQuery);