ENV = {
    ROOT: '{{ request.url_root }}',
    STATIC: '{{ url_for('static', filename='') }}',
    VERSION: '1.0'
};

