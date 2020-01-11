function SortBydate(dates){
    let summ = [];
for (var n=0; dates.length; n++){
    let m = dates[n];
    var p = m.split("/");
    summ.push(p[0]+p[1]+p[2]);
}
console.log(summ);
// sorting by Merge method
if (summ.length <= 1){
    return summ;
}
const middle = Math.floor(summ.length / 2);
var left = summ.slice(0,middle);
var right = summ.slice(middle);

let SortedDates = [];
leftindex = 0;
rightindex = 0;

while (leftindex<left.length && rightindex < right.length){
    if (left[leftindex] < right[rightindex]){
        SortedDates.push(left[leftindex]);
        leftindex++;
    }
    else{
        SortedDates.push(righ[rightindex]);
        rightindex++;
    }
}
return SortedDates.concat(left.slice(leftindex)).concat(right.slice(rightindex));
}