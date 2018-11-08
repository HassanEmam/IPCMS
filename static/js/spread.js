var period1 = document.getElementById('period1');
var period2 = document.getElementById('period2');
var period3 = document.getElementById('period3');
var period4 = document.getElementById('period4');
var period5 = document.getElementById('period5');
var period6 = document.getElementById('period6');
var period7 = document.getElementById('period7');
var period8 = document.getElementById('period8');
var period9 = document.getElementById('period9');
var period10 = document.getElementById('period10');
var period11 = document.getElementById('period11');
var period12 = document.getElementById('period12');
var period13 = document.getElementById('period13');
var period14 = document.getElementById('period14');
var period15 = document.getElementById('period15');
var period16 = document.getElementById('period16');
var period17 = document.getElementById('period17');
var period18 = document.getElementById('period18');
var period19 = document.getElementById('period19');
var period20 = document.getElementById('period20');
period1.addEventListener("blur", validatePercent);
period2.addEventListener("blur", validatePercent);
period3.addEventListener("blur", validatePercent);
period4.addEventListener("blur", validatePercent);
period5.addEventListener("blur", validatePercent);
period6.addEventListener("blur", validatePercent);
period7.addEventListener("blur", validatePercent);
period8.addEventListener("blur", validatePercent);
period9.addEventListener("blur", validatePercent);
period10.addEventListener("blur", validatePercent);
period11.addEventListener("blur", validatePercent);
period12.addEventListener("blur", validatePercent);
period13.addEventListener("blur", validatePercent);
period14.addEventListener("blur", validatePercent);
period15.addEventListener("blur", validatePercent);
period16.addEventListener("blur", validatePercent);
period17.addEventListener("blur", validatePercent);
period18.addEventListener("blur", validatePercent);
period19.addEventListener("blur", validatePercent);
period20.addEventListener("blur", validatePercent);

var submitButton = document.getElementById('btn');
submitButton.disabled =true;

function validatePercent()
{
    var issues = false;
    var sum =0.0;
    for(var i=1; i<21; i++)
    {
        var elementid = 'period' + i;
        var elementHandler = document.getElementById(elementid)
        sum += parseFloat(elementHandler.value) || 0;
    }
    if (sum != 100){
        issues =true;
    }
    
    if (issues==true){
            
        var msg = document.getElementById('message')
        msg.style.visibility = 'visible'
        msg.innerHTML ="the sum of values has to be equal 100%"
        
        console.log(msg)
    } else{
        submitButton.disabled = false;
        document.getElementById('message').innerHTML= ""
    }
}