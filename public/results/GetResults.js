GetResults();

function GetResults(){
    console.log('Yes1');
    const xhttp = new XMLHttpRequest();
    xhttp.open('GET','pruebas.json',true);
    xhttp.send();
    xhttp.responseType = "text";

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            console.log('Yes2');
            let data = JSON.parse(this.responseText);
            console.log(data);

            let Results = document.querySelector("#History");
            for (let item of data){
                "<tr>"
                Results.innerHTML += "<td>"+item.Hour+"</td>"+"<td>"+item.Date+"</td>"+"<td><button onclick=alert(this.rowIndex) button>GO</td>";
                "</tr>"
            }  
        }
    }
}
function GetRow(x){
		alert("Tu vieja is:"+x.rowIndex);
	}

function ThisResult()
{
    window.location="FlightResults.html";

    console.log('Yes');
    const xhttp2 = new XMLHttpRequest();
    xhttp2.open('GET','pruebas.json',true);
    xhttp2.send();
    xhttp2.responseType = "text";
    xhttp2.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            console.log('Yes1');
            let data = JSON.parse(this.responseText);
            console.log(data);

            let Result = document.querySelector("#FlightResults");
            console.log("data length = "+data.length);
            //console.log(x);          
            for (let item of data[0].Results){
                "<tr>"
                Result.innerHTML += "<td>"+item.NDVI+"</td>"+"<td>"+item.Latitude+"</td>"+"<td>"+item.Longitude+"</td>"+"<td><a href='"+item.Link+"'>IMAGE</a>";
                "</tr>"
            }  
        }
    }
}