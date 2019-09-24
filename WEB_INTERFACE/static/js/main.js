var thrustGauge;
var steerGuage;

document.getElementById("log_dir_content").value = "/home/pi/LOG/default"

var log_status = "STANDBY"

function onDocumentReady() {
  thrustGauge = gauge('#thrust-gauge', {
    size: 300,
    clipWidth: 300,
    clipHeight: 300,
    ringWidth: 60,
    minValue: 0,
    maxValue: 180,
    transitionMs: 2000,
  });
  

  steerGuage = gauge('#steer-gauge', {
    size: 300,
    clipWidth: 300,
    clipHeight: 300,
    ringWidth: 60,
    minValue: 0,
    maxValue: 180,
    transitionMs: 2000,
  });

  thrustGauge.render();
  steerGuage.render();

}

window.addEventListener("gamepadconnected", function(e) {
    console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
      e.gamepad.index, e.gamepad.id,
      e.gamepad.buttons.length, e.gamepad.axes.length);
    let status = document.getElementById('status_content')
    status.innerHTML = "Connected"
});


function scangamepad(){
    let gamepads = navigator.getGamepads()
    if(gamepads.length > 0){
      for(let i = 0; i<gamepads.length; i+=1){
        if (gamepads[i] === null){}
        else{return gamepads[i]}
      }
    }
    return null;
}

function clean_up_down(val){
    if (val <= 0.0){
        val = 0.0;
    }
    // scale val from [0.0,1.0] to [00, 15]
    let scaled = val*30.0;
    return 90+scaled;
}

// convert from [-1,+1] to [0,180]
function clean_left_right(val){
    // [-1,+1] to [-0.5,0.5]
    val = val*0.5;
    // [-0.5, +0.5] to [0,1.0]
    val = val+0.5;
    // [0,1.0] to [0,180]
    val = val*180;
    // clip to range [90-30, 90+30]
    if (val <= 60){
        val = 60;
    }
    if (val >= 120){
        val = 120;
    }
    return val;
}


setInterval(()=>{
    let controller = scangamepad();
    if(controller === null){
      return
    }
    up = clean_up_down(controller.axes[1]*-1);
    lr = clean_left_right(controller.axes[2]);
    let start_logging = controller.buttons[5].pressed;
    let stop_logging  = controller.buttons[4].pressed;
    if(start_logging){
        log_status = "LOGGING";
    }
    if(stop_logging){
        log_status = "STANDBY";
    }
    let status = document.getElementById('log_status_content');
    let log_dir = document.getElementById("log_dir_content").value;
    status.innerHTML = log_status;
    // up = 0.0
    thrustGauge.update(up);
    steerGuage.update(lr);
    data={};
    data["thrust"] = up;
    data["steer"] = lr;
    data["log_status"]=log_status;
    data["log_dir"] = log_dir;
    post(data)
}, 50);



if ( !window.isLoaded ) {
  window.addEventListener("load", function() {
    onDocumentReady();
  }, false);
} else {
  onDocumentReady();
}