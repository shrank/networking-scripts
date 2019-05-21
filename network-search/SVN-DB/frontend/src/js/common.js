
function addNavItem(id,text,href)
{
	$("#nav ul").append($("<li></li>").append($("<a></a>").text(text).attr("href",href)).attr("id",id))
};

function activateNavItem(id)
{
	$("#nav li").removeClass("active");
	$("#"+id).addClass("active");
};


addNavItem("nav_search","home","search.html")

function onPageLoad(args)
{};

$(function()
{
	addNavItem("nav_search","HOME","search.html")
	
	parts=window.location.href.split("?");
	if(parts.length>1)
	{
		onPageLoad(parts[1]);
	}
});
