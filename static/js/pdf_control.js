// If absolute URL from the remote server is provided, configure the CORS
// header on that server.
//var url = 'https://raw.githubusercontent.com/mozilla/pdf.js/ba2edeae/examples/learning/helloworld.pdf';
//var url = 'http://localhost:9002/media/uploads/dummy_pdf.pdf';
var url = document.getElementById("myFile").href;
/////////////////////////////////////////////////

$(document).ready(function(){
  $("#myBtn").click(function(){
    url = $(this).attr('objId');
    $.ajax({
        url: 'http://localhost:9003/file_download/'+url+'/',
        type: 'GET',
//        data: yourData,
        datatype: 'blob',
        success: function (data){
            var fileName = 'test.pdf'
            //Convert the Byte Data to BLOB object. //application/octetstream
            var blob = new Blob([data], { type: "application/pdf" });

            //Check the Browser type and download the File.
            var isIE = false || !!document.documentMode;
            if (isIE) {
                window.navigator.msSaveBlob(blob, fileName);
            } else {
                console.log('else block')
                var url = window.URL || window.webkitURL;
                link = url.createObjectURL(blob);
                var a = $("<a />");
                a.attr("download", fileName);
                a.attr("href", link);
                $("body").append(a);
                a[0].click();
                $("body").remove(a);
            }
        },
        error: function (jqXHR, textStatus, errorThrown){
            console.log('success')
        }
    });
  });
});
/*
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
  });
}, function (reason) {
  // PDF loading error
  console.error(reason);
});

https://pdfjs.express/blog/how-to-build-pdf-viewer-jquery-pdfjs
https://pspdfkit.com/blog/2018/render-pdfs-in-the-browser-with-pdf-js/
https://www.aspsnippets.com/Articles/Download-PDF-File-using-AJAX-in-jQuery.aspx
https://www.py4u.net/discuss/909664

https://jsfiddle.net/pdfjs/9engc9mw/?utm_source=website&utm_medium=embed&utm_campaign=9engc9mw
https://pdf.wondershare.com/buy/pdfelement-windows.html
*/
