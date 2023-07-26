// <script>
var modal = document.getElementById("hidden_box");
// Get the button that opens the modal
var btn = document.getElementsByClassName("hidden_box_btn");

for(let i = 0;i < btn.length; i++)
{
 let v = btn[i]
 v.onclick = function() {
   
    modal.style.display = "block";
  }
}

