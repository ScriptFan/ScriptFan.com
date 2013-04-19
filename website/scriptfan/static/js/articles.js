$(function() {
    // 初始化Markdown编辑器
    var editor = new EpicEditor({
        basePath: ENV.STATIC + 'lib/epiceditor',
        theme: {
            base:'/themes/base/epiceditor.css',
            preview:'/themes/preview/preview-dark.css',
            editor:'/themes/editor/epic-light.css'
        }
    }).load();
    editor.importFile('post', $('#content').val());

    // 文章标签编辑器
    $('.tags-manager').tagsManager({ hiddenTagListName: 'tags_text' });
    $('.tags-manager-wrapper').on('click', function() {
        $('.tags-manager').focus();
    });

    $('#form-article-create').submit(function() {
        var content = editor.exportFile();
        $('#content').val(content);
        console.log(content);
    });
});
