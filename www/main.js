$(document).ready(function () {

    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },

    });

    // Siri Wave config
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        style: "ios9",
        amplitude: "2",
        autostart: true,
        width: 800,
        height: 200,
      });

    // Siri Wave animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },

    });

    // Mic Button click
    $("#MicBtn").click(function () {
        eel.postassistantsound()()
        $("#oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommand()()
    });

    function doc_keyUp(e) {
        // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

        if (e.key === 'j' && e.metaKey) {
            eel.postassistantsound()
            $("#oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommand()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // to play assisatnt 
    function PlayAssistant(message) {

        if (message != "") {

            $("#oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommand(message);
            $("#chatbox").val()
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }

    }

    // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // key up event handler on text box
    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    
    });
    
    // send button event handler
    $("#SendBtn").click(function () {
    
        let message = $("#chatbox").val();
        PlayAssistant(message)
    
    });

    // enter press event handler on chat box
    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });
    $("#ExitBtn").click(function () { 
    let cww = confirm("Are sure you want to exit W.I.S.D.O.M.")

    if (cww==true){
        window.close()
        eel.htmlexit()()
    }
    else{
        alert("Request Cancelled!")
    }
        
    });
});