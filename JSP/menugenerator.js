	window.onscroll=function(){StandBy(document.getElementById("navigator"),300);StandBy(document.getElementById("contentbar"),320);};
function getElementLeft(element){
	var actualLeft = element.offsetLeft;
	var current = element.offsetParent;
	while (current !== null){
		actualLeft += current.offsetLeft;
		current = current.offsetParent;
	}
	return actualLeft;
}
function getElementTop(element){
	var actualTop = element.offsetTop;
	var current = element.offsetParent;
	while (current !== null){
		actualTop += current.offsetTop;
		current = current.offsetParent;
	}
	return actualTop;
}
function StandBy(element,i)
{
	//alert(element.getElementTop)
	if(i < document.body.scrollTop)
	{
		//alert("hehe");
		element.className="standby";
		//element.style.margin-left="0";
		//element.style.margin-right="0";
	}else
	{
		element.className="free";
	}
}


