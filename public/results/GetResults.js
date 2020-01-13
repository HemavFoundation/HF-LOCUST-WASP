GetResults();

function GetResults(){
    clearTimeout;
    const xhttp = new XMLHttpRequest();
    xhttp.open('GET','results.json',true);
    xhttp.send();
    xhttp.responseType = "text";

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            let data = JSON.parse(this.responseText);
            console.log(data);
            var i = 0;

            let Results = document.querySelector("#History");
            for (let item of data.flights){
                "<tr>"
                Results.innerHTML+="<td>"+item.id+"</td>"+"<td><button id="+i+" onclick='OpenFR(this.id)' button>GO</td>";
                "</tr>"
                i++;
            }  
        }
    }
}
function OpenFR(i){
    //console.log(i);
    window.open("FlightResults.html","_self");
    ThisResult(i);
}