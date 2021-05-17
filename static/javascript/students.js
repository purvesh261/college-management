function Hide(HideID) 
{
  HideID.style.display = "none"; 
}

function Show(ShowID) 
{
  ShowID.style.display = "block"; 
}

function changeActive(id){
  var body = document.body.id;
  var itemId = "item-" + body;
  var element = document.getElementById(itemId);
  element.classList.add("active");
  
}