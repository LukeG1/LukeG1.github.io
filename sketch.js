var note = "N/A";
var notePlay = "N/A";
var noteOff = 6;
var notes = ['C','D','E','F','G','A','B'];
var treb = ['C4','D4','E4','F4','G4','A4','B4','C5','D5','E5','F5','G5','A5','B5','C6'];
//var notes = ['D','E','F','G','A','B','C','D','E','F','G'];
var textOff = 50;
let slider;
let inputSoftware;
function setup() { 
  createCanvas(400, 400);
	WebMidi.enable(function (err) { //check if WebMidi.js is enabled
    if (err) {
      console.log("WebMidi could not be enabled.", err);
    } else {
      console.log("WebMidi enabled!");
    }
    console.log("---");
    inputSoftware = WebMidi.inputs[0];
    inputSoftware.addListener('noteon', "all",function (e) {
      note = (e.note.name + e.note.octave);
      // if(e.note.name=="D"){
      //   console.log("A D note has been received, any octave");
      // }
      // if((e.note.name + e.note.octave)=="C4"){
      //   console.log("A C4 note has been received, specifically");
      // }
    });
  });
  resetNote()
  slider = createSlider(0, WebMidi.inputs.length, 1);
  slider.input(updateMIDI);
}


var time = 0;
var timeOffset = 0;
var bestTime = 0;
function draw() { 
  //console.log(WebMidi.inputs.length);
  //let val = slider.value();
  background(51);
  fill(250);
  textAlign(CENTER);
  textSize(20);
  push();
    stroke(250);
    strokeWeight(3);
    line(textOff,height/2-lineSpacing*2,width-textOff,height/2-lineSpacing*2);
    line(textOff,height/2-lineSpacing,width-textOff,height/2-lineSpacing);
    line(textOff,height/2,width-textOff,height/2);
    line(textOff,height/2+lineSpacing,width-textOff,height/2+lineSpacing);
    line(textOff,height/2+lineSpacing*2,width-textOff,height/2+lineSpacing*2);
  pop()


  if(note == notePlay){
    resetNote()
    timeOffset += time
    if(time < bestTime || bestTime == 0){
      bestTime = time
    }
  }

  displayNote(notePlay, int(treb.length/2)-1, 250);
  displayNote(note, int(treb.length/2)-1, [0,0,250]);


  text("Play "+notePlay, width/2, textOff);
  text("Current Time: "+time.toFixed(2)+"s | Best Time: "+bestTime.toFixed(2)+"s", width/2, textOff+25);

  if(WebMidi.inputs.length > 0){
    text("You played "+note, width/2, height-textOff);
  }else{
    text("Connect a keyboard and refresh", width/2, height-textOff);
  }

  //console.log(millis()/1000)
  time = millis()/1000 - timeOffset
  console.log(timeOffset);
}

function updateMIDI(){
  console.log(slider.value())
  inputSoftware = WebMidi.inputs[slider.value()];
    inputSoftware.addListener('noteon', "all",function (e) {
      note = (e.note.name + e.note.octave);
      // if(e.note.name=="D"){
      //   console.log("A D note has been received, any octave");
      // }
      // if((e.note.name + e.note.octave)=="C4"){
      //   console.log("A C4 note has been received, specifically");
      // }
    });
    console.log("HAHAHAHHA");

}


function resetNote(){
  notePlay = treb[int(random(0,treb.length))];
  //notePlay = 'B4'

}




var lineSpacing = 25;
var noteWid = 25;
var noteHeiMult = .6;
function displayNote(n, nOff, c){
  var notePos = -treb.indexOf(n)+nOff;

  push();
    fill(c);
    // if(abs(notePos)>5){
    //   line(width/2-20,height/2+notePos*(lineSpacing/2),width/2+20,height/2+notePos*(lineSpacing/2))
    // }
    ellipse(width/2,height/2+notePos*(lineSpacing/2),noteWid,noteWid*noteHeiMult);

  pop();
}