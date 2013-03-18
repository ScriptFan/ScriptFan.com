$(function() {
    var editor = new EpicEditor({
        basePath: ENV.STATIC + 'lib/epiceditor',
        theme: {
            base:'/themes/base/epiceditor.css',
            preview:'/themes/preview/preview-dark.css',
            editor:'/themes/editor/epic-light.css'
        }
    }).load();
    editor.importFile('post', $('#content').val());

    $('#form-article-create').submit(function() {
        var content = editor.exportFile();
        $('#content').val(content);
        console.log(content);
    });
});
