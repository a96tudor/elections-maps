function toggleDropdown(id) {
   let content = document.getElementById(id);
   if (content.style.display === "block") {
      content.style.display = "none";
   } else {
      content.style.display = "block";
   }
}


function increment(type, id) {
    let numberInput = document.getElementById(id);
    numberInput.value = parseInt(numberInput.value) + 1;
}


function decrement(type, id) {
    let numberInput = document.getElementById(id);
    let newValue = parseInt(numberInput.value) - 1;
    numberInput.value = newValue > 0 ? newValue : 0;
}
