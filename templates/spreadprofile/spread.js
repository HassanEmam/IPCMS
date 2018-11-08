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
var period120 = document.getElementById('period20');

period1.addEventListener("blur", validatePercent);

function validatePercent()
{
    for(var i=1; i<21; i++)
    {
        alert('activated');
        var elementid = 'period' + i;
        var elementHandler = document.getElementById(elementid)
        if (elementHandler.value >100) {
            document.getElementById('message').innerHTML ='the sum of values has to be equal 100%'
        }
    }
}