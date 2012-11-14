!function($) {
    $.fn.openid = function(options) {
        return this.each(function() {
            var $this = $(this);
            var options = $.extend({}, $.fn.openid.defaults, $this.data(), options);
            var provider = $this.data('provider');
            $this.click(function() {
                // 从mapping 中查找openid配置并提交表单
                if (options.provider in options.mappings) {
                    $(options.provider_selector).val(options.provider);
                    $(options.identifier_selector).val(options.mappings[options.provider]);
                    $this.parents('form').submit();
                }
            });    
        });
    };

    $.fn.openid.defaults = {
        identifier_selector: '#openid_identifier',
        provider_selector: '#openid_provider',
        mappings: {
            'google': 'https://www.google.com/accounts/o8/id'
        }
    }

    $(function() {
        $('[rel=openid]').openid();
    });
}(window.jQuery);
