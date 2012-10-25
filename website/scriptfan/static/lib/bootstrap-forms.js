/* 
 * bootstrap-form.js v0.1
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 * 
 * Simple bootstrap form utilities.
 */
!function($) {

    /* FORM CLASS DEFINITION
     * ======================*/
    var Form = function(element, options) {
        this.init(element, options); 
    };

    Form.prototype = {
        constructor: Form,

        init: function(element, options) {
            this.$element = $(element);
            this.options = $.extend({}, $.fn.form.defaults, options, 
                                        this.$element.data());
        }
    };

    $.fn.form = function(option) {
        return this.each(function() {
            var $this = $(this);
            var data = $this.data('form');
            var options = typeof option == 'object' && option;
            
            if (!data) $this.data('form', (data = new Form(this, options)));
            if (typeof option == 'string') data['option'](); 
        }); 
    };

    $.fn.form.Constructor = Form;
}(window.jQuery);

