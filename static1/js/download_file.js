$("#myBtn").on("click", function() {
    // Data to post
    data = {
        ids: [1, 2, 3, 4, 5]
    };
    var objId = $(this).attr('objId');
//    var url = 'http://localhost:9004/file_download/'+objId+'/'
    var url = '/download_file/'+objId+'/'
    // Use XMLHttpRequest instead of Jquery $ajax
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        var a;
        if (xhttp.readyState === 4 && xhttp.status === 200) {
            // Trick for making downloadable link
            a = document.createElement('a');
            a.href = window.URL.createObjectURL(xhttp.response);
            // Give filename you wish to download
            a.download = "test-file.pdf";
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
        }
    };
    // Post data to URL which handles post request
    var csrf_token = $('#csrf-token').val()
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json");
//    xhttp.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
    // You should set responseType as blob for binary responses
    xhttp.responseType = 'blob';
    xhttp.send(JSON.stringify(data));
});