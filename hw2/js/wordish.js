var times = 0;
var targetText = 'ELOPE';

function startGame(){
    targetText = document.getElementById("target_text").value.toUpperCase();
    if (targetText.length != 5){
        document.getElementById('status').innerHTML = "invalid input";
        return;
    }

    for(let i = 0; i < 5; i++){
        let x = targetText.substring(i, i + 1)
        if (!((x >= 'a' && x <= 'z') || (x >= 'A' && x <= 'Z'))){
            document.getElementById('status').innerHTML = "invalid input";
            return;
        }
    }

    times = 0;
    document.getElementById('status').innerHTML = "Welcome to Wordish! Start!";
    for(i = 0; i < 6; i++){
        for(let j = 0; j < 5; j++){
            let cell = document.getElementById('cell_' + i + '_' + j);
            cell.innerHTML = null;
            cell.style.backgroundColor = 'lightgrey';
        }
    }
}

function guess(){
    let guessText = document.getElementById("guess_text").value.toUpperCase();

    if (guessText.length != 5){
        document.getElementById('status').innerHTML = "invalid input";
        return;
    }

    for(let i = 0; i < 5; i++){
        let x = guessText.substring(i, i + 1)
        if (!((x >= 'a' && x <= 'z') || (x >= 'A' && x <= 'Z'))){
            document.getElementById('status').innerHTML = "invalid input";
            return;
        }
    }

    document.getElementById('status').innerHTML = "successful input";

    let count = {};

    for(let i = 0; i < 5; i++){
        if(targetText[i] in count){
            count[targetText[i]] += 1;
        }else{
            count[targetText[i]] = 1;
        }
    }

    let correctLetter = 0;

    for(let i = 0; i < 5; i++){
        let x = guessText.substring(i,i + 1);
        let cell = document.getElementById('cell_' + times + '_' + i);
        cell.innerHTML = x;
        cell.style.backgroundColor = "grey";

        
    }

    for(let i = 0; i < 5; i++){
        let cell = document.getElementById('cell_' + times + '_' + i);
        if(guessText[i] == targetText[i] && count[guessText[i]] > 0){
            correctLetter++;
            count[guessText[i]]--;
            cell.style.backgroundColor = 'green';
            continue;
        }
    }

    for(let i = 0; i < 5; i++){
        let cell = document.getElementById('cell_' + times + '_' + i);
        for(let j = 0; j < 5; j++){
            if(guessText[i] == targetText[j] && j != i && count[guessText[i]] > 0){
                count[guessText[i]]--;
                cell.style.backgroundColor = 'yellow';
                break;
            }
        }  
    }

    if(correctLetter == 5){
        document.getElementById('status').innerHTML = "win~";
        return;
    }

    if(times < 5){
        times++;
    }else{
        document.getElementById('status').innerHTML = "You lose.";
        return;
    }
}
