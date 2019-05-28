
function showFile(content)
{
	$('#main-content').append(f)
	a=$("<pre class='snippet-wrap snippet-formatted sh_sourceCode'></pre>");
	l=$("<ol class='snippet-num'></ol>");
	lines=content.split("\n")
	for(var nr in lines){
		b=$('<li></li>');
		b.append($("<span></span>").text(lines[nr]));
		l.append(b);
	}
	a.append(l);
	$('#main-content').append($("<div class='sh_peachpuff snippet-wrap'></div>").append(a));
}

function openFile(path)
{
	$.get("/api/store/"+path,"",showFile,"text");
	$('#main-content').html("");
	f=$("<h1></h1>");
	f.text(path);
};

onPageLoad = function(args)
{
	openFile(args)
}
