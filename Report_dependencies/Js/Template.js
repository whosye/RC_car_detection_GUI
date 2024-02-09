
var ShowPicture = true; 
document.addEventListener("DOMContentLoaded", function() {

    var index = 1;
    var scoreId;
    var scoreElement = document.getElementById(scoreId);
    var rowCount;
    var scoreData = []
    while (true){

        scoreId = "score" + index;
        scoreElement = document.getElementById(scoreId);
        
        if (scoreElement == null){
            break;
        }
        else{

            rowCount = scoreElement.getElementsByTagName("div").length;
            scoreData.push([index,rowCount ]);
            index++;
        }   
    }

    var newScore = [];

    for (var i = 0; i < scoreData.length; i++) { 
        for (var row = 1; row < scoreData[i][1]+1; row++) {
            var rowString = `col${ scoreData[i][0]}row${row}`;
            newScore.push(rowString);
        }
    }
    
    let raceID  = document.getElementById('raceID').getAttribute("data-info");
    var modal = document.getElementById("modal");
    modal.addEventListener("click", closeModal);

    newScore.forEach(function(element){
        var currentElement = document.getElementById(`${element}`);
        currentElement.addEventListener("click", function() {
            let items  = document.getElementById(`${element}`).getAttribute("data-info").split(",");
            let nick = items[0];
            let color = items[1];
            let round = items[2];
            showModal(`Race_Photos/${raceID}_${nick}_${round}.jpg`);

        });
    });

    function showModal(imageSrc) {
        var modal = document.getElementById("modal");
        var modalImage = document.getElementById("modal-image");
      
        modalImage.src = imageSrc;
        modal.style.display = "block";
    }

    function closeModal() {
        var modal = document.getElementById("modal");
        modal.style.display = "none";
    }
});