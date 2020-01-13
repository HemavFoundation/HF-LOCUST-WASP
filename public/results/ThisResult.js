function ThisResult(i,data){
    console.log(i,data);
    //const xhttp = new XMLHttpRequest();
    //xhttp.open('GET','results.json',true);
    //xhttp.send();
    //xhttp.responseType = "text";
    console.log(xhttp);
    xhttp.onreadystatechange = function(){
        console.log(this);
        if (this.readyState == 4 && this.status == 200){
            console.log('Yes');
            let data = JSON.parse(this.responseText);
            console.log(data);
            let Result = document.querySelector("#FlightResults");         
            
            for (let item of data.flights[i].results){
                "<tr>"
                Result.innerHTML+="<td>"+item.id+"</td>"+"<td>"+item.NDVI+"</td>"+"<td>"+item.Latitude+"</td>"+"<td>"+item.Longitude+"</td>"+"<td>"+item.photo+"</td>";
                "</tr>"
            }
        }
        else
            console.log("else");
    }
}