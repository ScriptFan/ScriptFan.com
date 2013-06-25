/**
* 用户登陆，注册，资料修改等功能
*/

(function($) {
    // 更新用户的角色类型
    function updateUserRole() {
        $.ajax({
            url: document.location.href,
            data: { privilege: $(this).data('privilege') },
            type: 'POST',
            complete: function(message) {
                document.location.reload(true);
            },
            error: function() {
                document.location.reload(true);
            }
        });
    }

    function initialize() {
        $(document).on('click', '#role-menus li a', updateUserRole);  
    }

    $(document).ready(initialize);
})(jQuery);
