//Global variables for the game
var playerRed = 1;
var playerYellow = 2;
var currPlayer = playerRed;
var userStarts = true;
var gameOver = false;
var board;
var rows = 6;
var columns = 7;
var currColumns = []; //keeps track of which row each column is at.
var gameWasRefreshed = false

window.onload = function() {
    setGame();
}

//Creates de board and the necessary things to play
function setGame() {
    //Refresh the board and the game variables
    document.getElementById("board").remove()
    let htmlBoard = document.createElement("div")
    htmlBoard.id = "board"
    document.getElementById("game").append(htmlBoard)

    document.getElementById("secret_play_list").innerHTML = ""
    gameOver = false

    //The event listeners cannot be initialized twice, so we have to check if they already did
    if (!gameWasRefreshed) {
        addJavaScriptEventListeners();
    }

    //Sets the board and its event listeners
    board = [];
    currColumns = [5, 5, 5, 5, 5, 5, 5];
    for (let r = 0; r < rows; r++) {
        let row = [];
        for (let c = 0; c < columns; c++) {
            // JS
            row.push(' ');
            // HTML
            let tile = document.createElement("div");
            tile.id = r.toString() + "-" + c.toString();
            tile.classList.add("tile");
            if (userStarts) { 
              tile.addEventListener("click", setPieceUser);
            }
            document.getElementById("board").append(tile);
        }
        board.push(row);
    }
    //If pc moves first, we have to click the IA's turn button, and then add the event listener to allow the user to play
    if (!userStarts) {
        document.getElementById("ia_turn").click()
        console.log("Se realizó la primera jugada de la IA")
        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < columns; c++) {
                document.getElementById(r.toString() + "-" + c.toString()).addEventListener("click", setPieceUser);
            }
        }
    }
}

//When the user clicks somewhere on the board, this is executed, getting the coordenates and placing the piece
function setPieceUser() {
    if (gameOver) {
        return;
    }
   
    //get coords of that tile clicked
    let coords = this.id.split("-");
    let r = parseInt(coords[0]);
    let c = parseInt(coords[1]);
    // figure out which row the current column should be on
    r = currColumns[c]; 
    if (r < 0) {
        return;
    }
    board[r][c] = currPlayer; //update JS board
    let tile = document.getElementById(r.toString() + "-" + c.toString());
    if (currPlayer == playerRed) {
        tile.classList.add("red-piece");
        currPlayer = playerYellow;
    }
    else {
        tile.classList.add("yellow-piece");
        currPlayer = playerRed;
    }

    r -= 1; //update the row height for that column
    currColumns[c] = r; //update the array

    //Updates the secret list play list
    document.getElementById("secret_play_list").innerHTML = document.getElementById("secret_play_list").innerHTML + c
    //Check if someone already won
    checkWinner();
    //Makes Python/IA to play
    document.getElementById('ia_turn').click()
    
    
}

//When the python IA plays, this is executed, placing the IA's piece
function setPieceIA (column_to_play) {
    if (gameOver) {
        return;
    }
    r = currColumns[column_to_play]; 
    c = column_to_play
    if (r < 0) {
        return;
    }

    board[r][c] = currPlayer; //update JS board
    let tile = document.getElementById(r.toString() + "-" + c.toString());
    if (currPlayer == playerRed) {
        tile.classList.add("red-piece");
        currPlayer = playerYellow;
    }
    else {
        tile.classList.add("yellow-piece");
        currPlayer = playerRed;
    }
    r -= 1; //update the row height for that column
    currColumns[c] = r; //update the array

    checkWinner();
}

//Event listener to the users_turn button, clicked by the IA when it finishes playing
//And event listener for the multiple buttons in HTML
function addJavaScriptEventListeners () {
    //This will get executed when the IA clicks the button of "users_turn", drawing the IAs play
    //and letting the user to play again
    document.getElementById('user_turn').addEventListener('click', () => {
        plays = document.getElementById('secret_play_list').innerHTML
        plays = plays.toString()
        col = plays[plays.length-1]
        setPieceIA(col)
    })
    
    document.getElementById("setGameVariables").addEventListener('click', () => {
        gameWasRefreshed = true

        //Set the player in the HTML that the IA will use to know if its playing first or second
        var element = document.getElementById("first_Player");
        var player = element.options[element.selectedIndex].value;
        
        if (player === 'IA') {
            console.log("El jugador que empezará jugando será la IA")
            userStarts = false;
            document.getElementById("secret_pc_player").innerHTML = "1"
        }
        else {
            console.log("El jugador que empezará jugando será el usuario")
            userStarts = true;
            document.getElementById("secret_pc_player").innerHTML = "2"    
        }
        var element = document.getElementById("difficulty");
        var difficulty = element.options[element.selectedIndex].value;
        //Set the difficulty
        document.getElementById("secret_difficulty").innerHTML = difficulty.toString() 

        console.log("Se cambiaron las variables del juego exitosamente")
        setGame()

        if(document.getElementById("winner").innerText!=null || document.getElementById("winner").innerText!=''){
            document.getElementById("winner").innerText = ''
        }

        document.getElementById("winner").hidden=true

    })
    console.log("Los event listeners para que la IA juegue y para que cambie el jugador fueron seteados correctamente")

}

function checkWinner() {
     // horizontal
     for (let r = 0; r < rows; r++) {
         for (let c = 0; c < columns - 3; c++){
            if (board[r][c] != ' ') {
                if (board[r][c] == board[r][c+1] && board[r][c+1] == board[r][c+2] && board[r][c+2] == board[r][c+3]) {
                    setWinner(r, c);
                    return;
                }
            }
         }
    }

    // vertical
    for (let c = 0; c < columns; c++) {
        for (let r = 0; r < rows - 3; r++) {
            if (board[r][c] != ' ') {
                if (board[r][c] == board[r+1][c] && board[r+1][c] == board[r+2][c] && board[r+2][c] == board[r+3][c]) {
                    setWinner(r, c);
                    return;
                }
            }
        }
    }

    // anti diagonal
    for (let r = 0; r < rows - 3; r++) {
        for (let c = 0; c < columns - 3; c++) {
            if (board[r][c] != ' ') {
                if (board[r][c] == board[r+1][c+1] && board[r+1][c+1] == board[r+2][c+2] && board[r+2][c+2] == board[r+3][c+3]) {
                    setWinner(r, c);
                    return;
                }
            }
        }
    }

    // diagonal
    for (let r = 3; r < rows; r++) {
        for (let c = 0; c < columns - 3; c++) {
            if (board[r][c] != ' ') {
                if (board[r][c] == board[r-1][c+1] && board[r-1][c+1] == board[r-2][c+2] && board[r-2][c+2] == board[r-3][c+3]) {
                    setWinner(r, c);
                    return;
                }
            }
        }
    }
}

function setWinner(r, c) {
    let winner = document.getElementById("winner");
    if (board[r][c] == playerRed) {
        winner.className = "alert alert-danger alert-dismissible fade show"
        winner.innerText = "Red Wins";
        winner.hidden=false             
    } else {
        winner.className = "alert alert-warning alert-dismissible fade show"
        winner.innerText = "Yellow Wins";
        winner.hidden=false
    }
    gameOver = true;
}
