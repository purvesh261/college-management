function changeActive(id){
    var body = document.body.id;
    var itemId = "item-" + body;
    var element = document.getElementById(itemId);
    // window.alert(element.textContent);
    element.classList.add("active");
    
}


function searchrecords(){
var input,tr,td,filter,table,j,txtdata;
input=document.getElementById("searchtxt");
filter=input.value.toUpperCase();
table=document.getElementById("student_list1");
tr=table.getElementsByTagName("tr");
for(j=0;j<tr.length;j++)
{
td=tr[j].getElementsByTagName("td")[1];

if(td)
{
txtdata=td.innerText;
if(txtdata.toUpperCase().indexOf(filter)>-1){
    tr[j].style.display="";
}
else{
    tr[j].style.display="none";
}
}
}
}

function searchbranch(){
    var input,tr,td,filter,table,j,txtdata;
    input=document.getElementById("stdbranch");
    filter=input.value.toUpperCase();
    table=document.getElementById("student_list1");
    tr=table.getElementsByTagName("tr");
    
    for(j=0;j<tr.length;j++)
    {
    td=tr[j].getElementsByTagName("td")[6];
    
    if(td)
    {
    txtdata=td.innerText;
    if(txtdata.toUpperCase().indexOf(filter)>-1){
        tr[j].style.display="";
    }
    else{
        tr[j].style.display="none";
    }
    }
    }
    }

    function searchsem(){
        var input,tr,td,filter,table,j,txtdata;
        input=document.getElementById("stdsem");
        filter=input.value.toUpperCase();
        table=document.getElementById("student_list1");
        tr=table.getElementsByTagName("tr");
        
        for(j=0;j<tr.length;j++)
        {
        td=tr[j].getElementsByTagName("td")[7];
        
        if(td)
        {
        txtdata=td.innerText;
        if(txtdata.toUpperCase().indexOf(filter)>-1){
            tr[j].style.display="";
        }
        else{
            tr[j].style.display="none";
        }
        }
        }
        }
    
        function searchstaffrecords(){
            var input,tr,td,filter,table,j,txtdata;
            input=document.getElementById("staffsearch");
            filter=input.value.toUpperCase();
            table=document.getElementById("staff_list1");
            tr=table.getElementsByTagName("tr");
            
            for(j=0;j<tr.length;j++)
            {
            td=tr[j].getElementsByTagName("td")[8];
            
            if(td)
            {
            txtdata=td.innerText;
            if(txtdata.toUpperCase().indexOf(filter)>-1){
                tr[j].style.display="";
            }
            else{
                tr[j].style.display="none";
            }
            }
            }
            }
        