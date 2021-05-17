function changeActive(id){
  var body = document.body.id;
  var itemId = "item-" + body;
  var element = document.getElementById(itemId);
  element.classList.add("active");
  
}

var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementsByClassName("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function modaldis() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
} 

function Hide(HideID) 
{
  HideID.style.display = "none"; 
}

function Show(ShowID) 
{
  ShowID.style.display = "block"; 
}