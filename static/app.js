function toggleDropdown(id) {
   let content = document.getElementById(id);
   if (content.style.display === "block") {
      content.style.display = "none";
   } else {
      content.style.display = "block";
   }
}


function increment(type, id) {
    let elementId = [type, id].join(".");
//    if (elementId.includes('invalid_votes')) elementId = id;
    console.log(elementId);
    let numberInput = document.getElementById(elementId);
    numberInput.value = parseInt(numberInput.value) + 1;

    submitIncrementAction(type, id)
}


function decrement(type, id) {
    let elementId = [type, id].join(".");
//    if (elementId.includes('invalid_votes')) elementId = id;
    console.log(elementId);
    let numberInput = document.getElementById(elementId);
    let newValue = parseInt(numberInput.value) - 1;
    numberInput.value = newValue > 0 ? newValue : 0;
    if (newValue >= 0) submitDecrementAction(type, id)
}


function submitIncrementAction(type, id) {
    action = {
        sessionType: type,
        actionType: "INCREMENT",
        entityId: id
    }

    submitAction(action)
}



function submitDecrementAction(type, id) {
    action = {
        sessionType: type,
        actionType: "DECREMENT",
        entityId: id
    }

    submitAction(action)
}


function submitAction(action) {
    const urlElements = [API_URL, 'numarare', 'action', OBSERVER_ID]
    const full_url = urlElements.join("/")

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(action)
    }

    fetch(full_url, options)
        .then(response => {
            if (!response.ok) {
               console.error("Unsuccessful submit of action")
            }
            else {
                console.log("Successful submit of action")
            }
        })
        .catch(error => {
            console.error("Failed to submit action", error)
        })
}


function openWhatsAppGroup() {
    var whatsappGroupLink = WHATSAPP_LINK;
    window.open(WHATSAPP_LINK, "_blank");
}
