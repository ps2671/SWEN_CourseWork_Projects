function changeLoc(){
    var r = confirm("Are you sure you want to log out?");
		 
	if (r==true){ 
		window.location.href = "/logout/" 
	} 
}

function borrowToolsDetail(){
    var name = document.getElementById("name_OfTheTool").value;
    var address = document.getElementById("address_OfTheTool").value;
    var status= document.getElementById("status_OfTheTool").value;
    var category = document.getElementById("category_OfTheTool").value;
    window.alert("Category of the tool: " + category + "\n"
    + "Name of the tool: " + name + "\n"
    + "Status of the tool: " + status + "\n"
    + "Pick up address: " + address + "\n");
}

function requestedToolsDetail(){
    var name = document.getElementById("name_OfTheTool").value;
    var address = document.getElementById("address_OfTheTool").value;
    var category = document.getElementById("category_OfTheTool").value;
    window.alert("Category of the tool: " + category + "\n"
    + "Name of the tool: " + name + "\n"
    + "Pick up address: " + address + "\n");
}

function acceptedToolsDetail(){
    var address = document.getElementById("address_OfTheTool").value;
    window.alert("Pick up address is: " + address + "\n");
}

function rejectedToolsDetail(){
    var name = document.getElementById("name_OfTheTool1").value;
    var address = document.getElementById("address_OfTheTool1").value;
    var category = document.getElementById("category_OfTheTool1").value;
    window.alert("Category of the tool: " + category + "\n"
    + "Name of the tool: " + name + "\n"
    + "Pick up address: " + address + "\n"
    + "Special Instructions: " + "No any instructions(Need to create field for special instructions)" + "\n");
}


function notificationOFFAlert(){
    window.alert("You have no new notifications!")
}

function notificationONAlert(){
    window.alert("You have new notifications! Go inside the Tools section to view it!")
}

function fetchFromDjango(){
    window.alert("This is working! ")
}