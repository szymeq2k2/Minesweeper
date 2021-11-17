var time;
var flag;
var flags = [];
var bombs = [20];
var revealed = [100];
var points;
var end;
var victory;
var fieldImages = ["Field_Empty.png", "Field_1.png", "Field_2.png", "Field_3.png", "Field_4.png", "Field_5.png",
                 "Field_6.png", "Field_7.png", "Field_8.png"];
var boom = new Audio("../Game/Audio/mixkit-8-bit-bomb-explosion-2811.wav");
var victory = new Audio("../Game/Audio/mixkit-winning-notification-2018.wav");
var field = new Audio("../Game/Audio/mixkit-arcade-game-jump-coin-216.wav");
Build();
setInterval(Timer, 1000);
document.oncontextmenu = StopContextMenu;

function Build() 
{
    flag = 0;
    end = false;
    time = 0;
    points = 0;
    for(var i = 0; i < 20; i++)
    {
        flags[i] = null;
    }
    for(var i = 0; i < 20; i++)
    {
        bombs[i] = null;
    }
    for(var i = 0; i < 100; i++)
    {
        revealed[i] = false;
    }
    var i = 0;
    while(i < 20)
    {
        var bomb = Math.floor(Math.random() * 100);
        if(bombs.includes(bomb))
        {
            i--;
        }
        else
        {
            bombs[i] = bomb;
            i++;
        }
    }
}

function StopContextMenu(event)
{
    event = event || window.event;

    if(event.preventDefault)
    {
        event.preventDefault();
    }
    else
    {
        event.returnValue = false;
    }
}

function Timer()
{
    if(!end)
    {
        time++;
        document.getElementById("TimerBar").textContent = time;
    }
}

function Face(number, event)
{
    event = event || window.event;
    if(event.which == 1 && !flags.includes(number))
    {
        document.getElementById("FaceImage").src = "../Game/Images/FaceWorried.png";
    }
    else if (event.which == 3)
    {
        Flag(number);
    }
}

function Flag(number)
{
    if(flags.includes(number))
    {
        flag--;
        SortFlags(number);
        document.getElementById("FlagsBar").textContent = flag + "/20";
        document.getElementById("i" + number).style.visibility = "hidden";

    }
    else if(flag != 20)
    {
        flags[flag] = number;
        flag++;
        document.getElementById("FlagsBar").textContent = flag + "/20";
        document.getElementById("i" + number).src = "../Game/Images/Flag.png";
        document.getElementById("i" + number).style.visibility = "visible";
    }
}

function SortFlags(number)
{
    var index = flags.indexOf(number);
    for(var i = index; i < 20; i++)
    {
        flags[i] = flags[i + 1];
    }
}
function Reveal(number)
{
    if(!flags.includes(number))
    {
        if(bombs.includes(number))
        {
            boom.play();
            end = true;
            Revealbombs();
        }
        else if (!revealed[number])
        {
            field.play();
            points++;
            revealed[number] = true;
            var bombCount = 0;
            var i = 0;
            var t = 0;
            var d = 0;
            var l = 0;
            var r = 0;
            console.log(Math.floor((number / 10)));
            if (Math.floor((number / 10)) > 0)
            {
                if(bombCounter(number - 10))
                {
                    bombCount++;
                }
                t = 1;
            }

            if (Math.floor((number / 10)) < 9)
            {
                if(bombCounter(number + 10))
                {
                    bombCount++;
                }
                d = 1;
            }

            if (Math.floor((number % 10)) > 0)
            {
                if(bombCounter(number - 1))
                {
                    bombCount++;
                }
                l = 1;
            }

            if (Math.floor((number % 10)) < 9)
            {
                if(bombCounter(number + 1))
                {
                    bombCount++;
                }
                r = 1;
            }

            if (l == 1 && t == 1)
            {
                if(bombCounter(number - 11))
                {
                    bombCount++;
                }
            }
            if (r == 1 && t == 1)
            {
                if(bombCounter(number - 9))
                {
                    bombCount++;
                }
            }
            if (l == 1 && d == 1)
            {
                if(bombCounter(number + 9))
                {
                    bombCount++;
                }
            }
            if (r == 1 && d == 1)
            {
                if(bombCounter(number + 11))
                {
                    bombCount++;
                }
            }

            if (bombCount == 0)
            {
                document.getElementById("i" + number).style.visibility = "visible";
                document.getElementById("i" + number).src = "../Game/Images/" + fieldImages[bombCount];
                document.getElementById(number).disabled = true;
                document.getElementById(number).style.backgroundColor = "rgb(66, 66, 66)";
                document.getElementById("FaceImage").src = "../Game/Images/FaceHappy.png";
                RevealAround(number, t, d, l, r);
            }
            else 
            {
                document.getElementById("i" + number).style.visibility = "visible";
                document.getElementById("i" + number).src = "../Game/Images/" + fieldImages[bombCount];
                document.getElementById(number).disabled = true;
                document.getElementById(number).style.backgroundColor = "rgb(66, 66, 66)";
                document.getElementById("FaceImage").src = "../Game/Images/FaceHappy.png";
            }
            if(points == 100 - bombs.length)
            {
                victory.play();
                for(var i = 0; i < 20; i++)
                {
                    end = true;
                    document.getElementById("i" + bombs[i]).style.visibility = "visible";
                    document.getElementById("i" + bombs[i]).src = "../Game/Images/Mine.png";
                    document.getElementById(bombs[i]).style.backgroundColor = "rgb(31, 95, 29)";
                    document.getElementById(bombs[i]).disabled = true;
                }
            }
        }
    }
}

function bombCounter(number)
{
    if (bombs.includes(number))
    {
        return true;
    }
    return false;
}

function RevealAround(number, t, d, l, r)
{
    if (t == 1)
    {
        Reveal(number - 10);
    }
    if (d == 1)
    {
        Reveal(number + 10);
    }
    if (l == 1)
    {
        Reveal(number - 1);
    }
    if (r == 1)
    {
        Reveal(number + 1);
    }
    if (l == 1 && t == 1)
    {
        Reveal(number - 11);
    }
    if (r == 1 && t == 1)
    {
        Reveal(number - 9);
    }
    if (l == 1 && d == 1)
    {
        Reveal(number + 9);
    }
    if (r == 1 && d == 1)
    {
        Reveal(number + 11);
    }
}

function Revealbombs()
{
    document.getElementById("FaceImage").src = "../Game/Images/FaceDead.png";
    var i = 0;
    while(i < 20)
    {
        document.getElementById("i" + bombs[i]).style.visibility = "visible";
        document.getElementById("i" + bombs[i]).src = "../Game/Images/Mine.png";
        document.getElementById(bombs[i]).style.backgroundColor = "rgb(128, 33, 33)";
        bombs[i] = 0;
        i++;
    }
    i = 0;
    while(i < 100)
    {
        document.getElementById(i).disabled = true;
        i++;
    }
}

function Restart()
{
    document.getElementById("FaceImage").src = "../Game/Images/FaceHappy.png";
    document.getElementById("TimerBar").textContent = 0;
    document.getElementById("FlagsBar").textContent = "0/20";
    var i = 0;
    while(i < 100)
    {
        document.getElementById(i).disabled = false;
        document.getElementById("i" + i).style.visibility = "hidden";
        document.getElementById(i).style.backgroundColor = "rgb(218, 218, 218)";
        i++;
    }
    Build();
}