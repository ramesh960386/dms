$(document).ready(function(){
  $("#download-btn").click(function(){
    var objId = $(this).attr('objId');
    var url = '/file_download/'+objId+'/'
    var csrf_token = $('meta[name="csrf-token"]').attr('content')

    //setup ajax
    $.ajaxSetup({
      beforeSend:function(jqXHR,settings){
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            jqXHR.setRequestHeader("X-CSRFToken", csrf_token);
            jqXHR.setRequestHeader("Content-Type", 'application/json');
        }
        if (settings.datatype === 'binary'){
            settings.xhr().responseType='arraybuffer';
            settings.processData=false;
        }
      }
    })

    //use ajax now

    $.ajax({
      url:url,
      type:"POST",
      datatype:"binary",
      success:function(data){
        var blob = new Blob([data], {type : 'application/pdf'});
        a = document.createElement('a');
        a.href = window.URL.createObjectURL(blob);
        a.download = "myFile.pdf";
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
      },
      error: function (jqXHR, textStatus, errorThrown){
        console.log('success')
      }
    })

    /*
    $.ajax({
        url: url,
        type: 'POST',
       //  data: yourData,
       //  datatype: 'json',
        datatype:'blob',
        headers: {
            'X-CSRFToken': $('meta[name="csrf-token"]').attr('content'),
            'Content-Type': 'application/json'
        },
        success: function (data){
            console.log('download clicked')
            //Convert the Byte Data to BLOB object. //application/octetstream
            var blob = new Blob([data], { type: "application/pdf" });

            //Check the Browser type and download the File.
            var isIE = false || !!document.documentMode;
            if (isIE) {
                window.navigator.msSaveBlob(blob, fileName);
            } else {
                var url = window.URL || window.webkitURL;
                a = document.createElement('a');
                a.href = url.createObjectURL(blob);
                a.download = 'test.pdf';
                a.style.display = 'none';
                document.body.appendChild(a);
                a.click();
            }
        },
        error: function (jqXHR, textStatus, errorThrown){
            console.log('success')
        }
    });
    */

//    http://keyangxiang.com/2017/09/01/HTML5-XHR-download-binary-content-as-Blob/
//    https://developer.mozilla.org/en-US/docs/Web/API/Blob
//    https://newbedev.com/how-to-set-multiple-headers-data-with-xmlhttprequest-in-async-mode
//http://www.henryalgus.com/reading-binary-files-using-jquery-ajax/
  });
});