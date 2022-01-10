$(document).ready(function(){
    var csrf_token = $('meta[name="csrf-token"]').attr('content');
    var token = 'token 90a03496eddfb421b5b795292eced8b64777f2d8'

    $.ajaxSetup({
      beforeSend:function(jqXHR,settings){
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            jqXHR.setRequestHeader("X-CSRFToken", csrf_token);
            jqXHR.setRequestHeader("Content-Type", 'application/json');
            jqXHR.setRequestHeader("Authorization", token);
        }
      }
    })
    //    var jwtToken = localStorage.getItem("jwtToken");
    //    var headerObj = {"Authorization": "Bearer " + jwtToken};
    //    http POST http://localhost:9020/api-token-auth/ username='admin' password="admin"
    function getTocken(){
        var request_user = $('meta[name="request-user"]').attr('content');
        var token_url = `${window.location.origin}/api-token-auth/`;
        console.log(request_user)
        console.log(token_url)

        $.ajax({
            type:"POST",
            url: token_url,
            data:{
                username: request_user,
                password:'admin'
            },
            success: function(data){
                console.log(data)
            }
        })
    }

    var downloadFile = function (blob, filename) {
        const data = window.URL.createObjectURL(blob);
        var link = document.createElement('a');
        link.href = data;
        link.download = filename;
        link.click();
        setTimeout(function () {
            window.URL.revokeObjectURL(data);
        }, 100)
    }

    var showFile = function (blob, filename) {
        const data = window.URL.createObjectURL(blob);
        var iframe = document.createElement('iframe');
        iframe.src = data;

        $("#myFrame").attr("src", data);

        /*
        setTimeout(function () {
            window.URL.revokeObjectURL(data);
        }, 100)
        */
    }

    $("#download-btn").click(function(){
//        var objId = $(this).attr('objId');
//        var url = '/download_file/'+objId+'/'
//        var btnUrl = this.getAttribute('url');
//        'Authorization'] = 'Token
        var btnUrl = $(this).attr('url');
        var fileAccess = $(this).attr('file-access');
        var filename = $(this).attr('file-name');
        var url = `${window.location.origin}${btnUrl}?type=${fileAccess}`;
        // var xhr = new XMLHttpRequest();
        $.ajax({
            xhrFields: {
               responseType: 'blob'
            },
            /*
            headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json',
                'Authorization': token
            },
            */
            type:'POST',
            url:url,
            // data: $(this).attr('download'),
        }).done(function(blob){
            downloadFile(blob, filename);
        });
    });

    $("#display-btn").click(function(){
        var objId = $(this).attr('objId');
        var url = '/download_file/'+objId+'/'
        var filename = $(this).attr('file-name');
        $.ajax({
            xhrFields: {
               responseType: 'blob'
            },
            headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json'
            },
            type:'POST',
            url:url
        }).done(function(blob){
            // showFile(blob, filename);
            //  pdfIframe.src = `pdfjs/web/viewer.html?file=${fil_url}`;
            var file_url = window.URL.createObjectURL(blob);
            $("#myFrame").attr("src", file_url);
        });
    });

    $("#pdf-btn").click(function(){
//        var objId = $(this).attr('objId');
//        var url = window.location.origin+$(this).attr('url')

        var btnUrl = $(this).attr('url');
        var fileAccess = $(this).attr('file-access');
        var filename = $(this).attr('file-name');
        var url = `${window.location.origin}${btnUrl}?type=${fileAccess}`;
        // Loaded via <script> tag, create shortcut to access PDF.js exports.
        var pdfjsLib = window['pdfjs-dist/build/pdf'];

        // The workerSrc property shall be specified.
        pdfjsLib.GlobalWorkerOptions.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.js';

        // Asynchronous download of PDF
        var loadingTask = pdfjsLib.getDocument(url);
        loadingTask.promise.then(function(pdf) {
          console.log('PDF loaded');

          // Fetch the first page
          var pageNumber = 1;
          pdf.getPage(pageNumber).then(function(page) {
            console.log('Page loaded');

            var scale = 1.0;
            var viewport = page.getViewport({scale: scale});

            // Prepare canvas using PDF page dimensions
            var canvas = document.getElementById('the-canvas');
            var context = canvas.getContext('2d');
            // canvas.height = viewport.height;
            // canvas.width = viewport.width;
            canvas.height = 600;
            canvas.width = 610;

            // Render PDF page into canvas context
            var renderContext = {
              canvasContext: context,
              viewport: viewport
            };
            var renderTask = page.render(renderContext);
            renderTask.promise.then(function () {
              console.log('Page rendered');
            });

            canvas.classList.add("the-canvas");
          });
        }, function (reason) {
          // PDF loading error
          console.error(reason);
        });
    })

});