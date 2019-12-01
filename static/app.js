        
// Access the device camera and stream to cameraView


// Set constraints for the video stream
function printURL(imagePath) {
    alert(imagePath)
    // body...
}

function keyboardBinding() {
    Mousetrap.bind('left', function() { 
        document.getElementById("yes").checked = true;
    });
    Mousetrap.bind('right', function() { 
        document.getElementById("no").checked = true;
    })
    Mousetrap.bind('enter', function() { 
        document.getElementById("submit").click();
    });
    Mousetrap.bind('esc', function() { 
        document.getElementById("cancel").click();
    })

     Mousetrap.bind('space', function() { 
        document.getElementById("camera--trigger").click();
    })
};

$(document).ready(function(){
    
    var browserDetails = navigator.userAgent;
    
    let imageData = ""
    const cameraView = document.querySelector("#camera--view")

    const cameraOutput = document.querySelector("#camera--output");
    const cameraSensor = document.querySelector("#camera--sensor");
            
    const formSubmit = document.querySelector('#form-submit');
    const cameraTrigger = document.querySelector("#camera--trigger");

    function cameraStart() {
        var constraints = { video: { facingMode: "user" }, audio: false };
        var track = null;
        navigator.mediaDevices
            .getUserMedia(constraints)
            .then(function(stream) {
                track = stream.getTracks()[0];
                cameraView.srcObject = stream;
            })
            .catch(function(error) {
                console.error("Oops. Something is broken.", error);
            });
    }

    $('#camera--output').hide()
    $('#output').hide()

    cameraStart();
    keyboardBinding();

// Take a picture when cameraTrigger is tapped
    cameraTrigger.onclick = function() {
        cameraSensor.width = cameraView.videoWidth;
        cameraSensor.height = cameraView.videoHeight;
    
        cameraSensor.getContext("2d").drawImage(cameraView, 0, 0);
        $('#output').show()
        $('#camera--output').show()
    
        imageData = cameraSensor.toDataURL('image/png');
        cameraOutput.src = imageData;
        console.log('output is: ', cameraOutput.src)
        cameraOutput.classList.add("taken");
        //printURL(cameraSensor.toDataURL('image/png'))
     //track.stop();
    };

    $('#submit').on('click', function() {
          if($('input[name=posture]:checked').val() === undefined) {
                  alert('please select yes or no')
          }
          else {
            var json =  {
                "base64": imageData.split(',')[1],
                "label": $('input[name=posture]:checked').val(),
                "extension": "png",
                "details" : navigator.appVersion
            };
          $.ajax('http://localhost:5000/image', {
            type: 'POST',
            data: JSON.stringify(json),
            contentType: 'application/json; charset=utf-8' ,
    success: function (data, status, xhr) {
        console.log('success')
    },
    error: function (jqXhr, textStatus, errorMessage) {
        console.log('error')
    }
    })
    }
      });
    
    $('#cancel').on('click', function() {
    
        $('#camera--output').hide()
        $('#output').hide()
    });

});
    



/*
1. click image
2. show the clicked image on the side
3. give options for a. bad posture b. good posture c. cancel(if eyes are closed or very blurry) - checkboxes and shortcut
4. create API on backend to recieve the file and posture
5. store file as jpeg  - uuid_posture
6. show user option to click another image(with keyboard binding to click image as well)
*/
