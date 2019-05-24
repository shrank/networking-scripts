
function setCollectionResult(result)
{
	$.each( result, function( i, item ) {
		col=$("#result_"+i);
		col.find(".spinner").remove();
		for(var file in item)
		{
			header=$("<div class='snippet-header'></div>");
			f=$("<a></a>");
			f.attr("href","showFile.html?"+i+"/"+file);
			f.text(file);
			header.append(f);
			changed=new Date(item[file]["changed"])
			header.append($("<span class='sh_comment'></span>").text("(changed:"+changed.toLocaleDateString()+" "+changed.toLocaleTimeString()+")"))
			a=$("<pre class='snippet-wrap snippet-formatted sh_sourceCode'></pre>");
			a.append(header);
			l=$("<ol class='snippet-num'></ol>");
			for(var nr in item[file]["matches"])
			{
				b=$('<li></li>');
				b.attr("value",item[file]["matches"][nr]["lnr"])
				b.append($("<span></span>").text(item[file]["matches"][nr]["line"]));
				l.append(b);
			}
			a.append(l);
			col.append($("<div class='sh_peachpuff snippet-wrap'></div>").append(a));
		}
	});
}	

function searchCollection(collection,filters)
{
	filters["c"]=collection;
	col=$('<div id="result_'+collection+'" class="result"></div>');
	col.append($("<h2></h2>").text(collection));
	col.append($("<div class='spinner'></div>"));
	col.appendTo('#main-content');
	$.getJSON("/api/search/",query,setCollectionResult);
	return false;
}


function startSearch(form)
{
	$('#main-content').html("");
	query={"q":form.q.value};
	$('.filter_collections:checkbox:checked').each(function()
	{
		searchCollection(this.name,query);
	}); 
	return false;
}

function loadCollections()
{
	$.getJSON("/api/store/","",function (result)
	{
		$("#filter_collections").html("");
		$.each( result, function( i, item ) {
			option=$("<div><input type='checkbox' class='filter_collections' name='"+item+"' id='fc_"+i+"' checked/><label for='fc_"+i+"'>"+item+"</label></div>");
			$("#filter_collections").append(option);
		});
	});
}

$(function()
{
	activateNavItem("nav_search");
	loadCollections();
});