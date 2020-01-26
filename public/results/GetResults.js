GetResults();

function GetResults(){
    clearTimeout;
    const xhttp = new XMLHttpRequest();
    xhttp.open('GET','/results.json',true);
    xhttp.send();
    xhttp.responseType = "text";
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            let data = JSON.parse(this.responseText);
            var i = 0;

            let Results = document.querySelector("#tableID");
            for (let item of data.flights){
                "<tr>"
                Results.innerHTML+="<td>"+item.id+"</td>"+"<td><button class=square_btn_small id="+i+" onclick='OpenFR(this.id) || deleteRows()' button>GO</td>";
                "</tr>"
                i++;
            }  
        }else{
            console.log('error, readyState is:', this.readyState, 'status fetch is:', this.status)
        }
    }
}
function OpenFR(i){
    ThisResult(i);  
}

function deleteRows() {
    let table = document.querySelector("#flight");

}

function ThisResult(i){
    const xhttp = new XMLHttpRequest();
    xhttp.open('GET','/results.json',true);
    xhttp.send();
    xhttp.responseType = "text";

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            let data = JSON.parse(this.responseText);
            let Result = document.querySelector("#flight");         
            
            for (let item of data.flights[i].results){
                "<tr>"
                Result.innerHTML+="<td>"+item.id+"</td>"+"<td>"+item.NDVI+"</td>"+"<td>"+item.Latitude+"</td>"+"<td>"+item.Longitude+"</td>"+"<td>"+"<a href=" + item.photo  + ">Show photo!</a>"+"</td>";
                "</tr>"
            }
        }
    }
}


