$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

const recognition = new webkitSpeechRecognition();
const audio = new Audio('/static/sound/move.mp3');

recognition.lang = 'en-US';
recognition.continuous = true;
recognition.interimResults = false;
recognition.maxAlternatives = 1;

recognition.onresult = (event) => {
    const speechResult = event.results[event.results.length - 1][0].transcript;
    socket.emit('speech', {speech: speechResult, depth:document.getElementById("depth").value});
    $("#speech").text(speechResult)
}

function startSpeech() {
    recognition.start();
}

function stopSpeech() {
    recognition.stop();
}


var socket = io();

function onDrop (source, target, piece, newPos, oldPos, orientation) {
    socket.emit('move', {
        source: source,
        target: target,
        piece: piece,
        newPos: Chessboard.objToFen(newPos),
        oldPos: Chessboard.objToFen(oldPos),
        orientation: orientation,
        depth:document.getElementById("depth").value
        
    });

    audio.play();
    board.draggable = false;
}

var config = {
    draggable: true,
    position: 'start',
    onDrop: onDrop,
    onDragStart: onDragStart,
    pieceTheme: '/static/img/chesspieces/default/{piece}.png',
}
$('#status').hide();
$('#danger').hide();

function reset() {
    socket.emit('reset');
    board.draggable = false;
    board.orientation('white');
}

function invert() {
    board.draggable = false;
    reset();
    board.orientation('flip');
    socket.emit('invert', {orientation: board.orientation(), depth:document.getElementById("depth").value});
}

function depthWarning(){
    
    const value = document.getElementById("depth").value;
    if(value > 3){
        $('#danger').show();
    }else{
        $('#danger').hide();
    }
}

function onDragStart (source, piece, position, orientation) {
    if ((orientation === 'white' && piece.search(/^w/) === -1) ||
        (orientation === 'black' && piece.search(/^b/) === -1)) {
    return false
    }
}

$("#switch-shadow").on("click", function() {
    if($(this).is(":checked")) {
        startSpeech();

        $("#mic-image").attr("src", "/static/img/micdesmut.png")
    } else {
        stopSpeech();
        $("#mic-image").attr("src", "/static/img/mic.png")
    }
});

socket.on('thinking', function(msg) {
    board.draggable = false;
    if(msg == true) {
        $('#status').show();
        
    }
    else {
        $('#status').hide();
    }
});

socket.on('game_state', function(msg) {
    board.position(msg);
    audio.play();
    $("#fen").text(board.fen());
    board.draggable = true;
});

var board = Chessboard('board-layout-chessboard', config)
$(window).resize(board.resize)